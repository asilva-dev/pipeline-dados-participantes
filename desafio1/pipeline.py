"""Etapas de tratamento e reconciliação dos dados de participantes.

`executar_pipeline` é a função pública deste módulo: recebe um
DataFrame bruto e devolve o DataFrame tratado + o relatório de
qualidade da execução. Por não fazer I/O, é trivial de testar
passando DataFrames construídos em memória.
"""

from __future__ import annotations

import logging

import pandas as pd

from desafio1.config import COLUNAS_OBRIGATORIAS, VALORES_ID_PENDENTE
from desafio1.normalizadores import (
    parse_data,
    normalizar_data,
    normalizar_email,
    normalizar_status,
    normalizar_texto,
)
from desafio1.qualidade import RelatorioQualidade

logger = logging.getLogger(__name__)


class SchemaInvalidoError(Exception):
    """Levantado quando o arquivo de entrada não tem as colunas esperadas."""


def validar_schema(df: pd.DataFrame) -> None:
    """Falha cedo e de forma explícita se colunas esperadas não existirem."""
    faltantes = set(COLUNAS_OBRIGATORIAS) - set(df.columns)
    if faltantes:
        raise SchemaInvalidoError(
            f"Colunas obrigatórias ausentes no arquivo de entrada: {sorted(faltantes)}"
        )


def isolar_registros_sem_matricula(
    df: pd.DataFrame, relatorio: RelatorioQualidade
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Separa registros sem matrícula, que não devem ser deduplicados
    como se fossem a mesma pessoa (armadilha do NaN == NaN no pandas)."""
    sem_chave = df[df["matricula"].isna() | (df["matricula"].astype(str).str.strip() == "")]
    com_chave = df.drop(sem_chave.index)

    relatorio.registros_sem_matricula = len(sem_chave)
    if len(sem_chave) > 0:
        logger.warning(
            "%d registro(s) sem matrícula foram isolados (não deduplicados).",
            len(sem_chave),
        )

    return com_chave, sem_chave


def remover_duplicidades(
    df: pd.DataFrame, relatorio: RelatorioQualidade
) -> pd.DataFrame:
    """Mantém, por matrícula, o registro com a data de matrícula mais
    recente — em vez de confiar na ordem em que o arquivo chegou."""
    df = df.copy()
    df["_data_matricula_ordenacao"] = df["data_matricula"].apply(parse_data)
    df = df.sort_values("_data_matricula_ordenacao", na_position="first")

    antes = len(df)
    df = df.drop_duplicates(subset=["matricula"], keep="last")
    relatorio.registros_duplicados_removidos = antes - len(df)

    return df.drop(columns="_data_matricula_ordenacao").reset_index(drop=True)


def normalizar_campos(df: pd.DataFrame, relatorio: RelatorioQualidade) -> pd.DataFrame:
    """Aplica as regras de padronização em cada coluna relevante."""
    df = df.copy()

    df["nome_participante"] = df["nome_participante"].apply(normalizar_texto)
    df["nome_valido"] = df["nome_participante"] != ""

    df["email_institucional"] = df["email_institucional"].apply(normalizar_email)
    df["email_valido"] = df["email_institucional"] != ""
    relatorio.emails_invalidos = int((~df["email_valido"]).sum())

    contador_desconhecidos: dict[str, int] = {}
    for coluna in ["status_programa_corporativo", "status_base_powerbi"]:
        df[coluna] = df[coluna].apply(
            lambda v: normalizar_status(v, contador_desconhecidos)
        )
    relatorio.status_desconhecidos = contador_desconhecidos

    for coluna in ["data_matricula", "data_conclusao"]:
        df[coluna] = df[coluna].apply(normalizar_data)

    return df


def reconciliar_status(df: pd.DataFrame, relatorio: RelatorioQualidade) -> pd.DataFrame:
    """Compara Programa Corporativo x Power BI; o primeiro é a fonte
    de verdade (SSOT) neste cenário."""
    df = df.copy()
    df["divergencia_status"] = (
        df["status_programa_corporativo"] != df["status_base_powerbi"]
    )
    df["status_unificado_ssot"] = df["status_programa_corporativo"]

    relatorio.divergencias_status = int(df["divergencia_status"].sum())
    return df


def preparar_integracao(df: pd.DataFrame, relatorio: RelatorioQualidade) -> pd.DataFrame:
    """Separa identidade (id_sistema_externo) de status de sincronização.

    Antes, um valor como 'PENDENTE_SYNC' era escrito por cima do próprio
    ID, misturando dois conceitos. Agora o ID permanece como veio (ou
    vazio) e um campo à parte indica se a sincronização está pendente.
    """
    df = df.copy()
    df["id_sistema_externo"] = df["id_sistema_externo"].apply(normalizar_texto)

    pendente = df["id_sistema_externo"].str.upper().isin(VALORES_ID_PENDENTE)
    df["status_sincronizacao"] = pendente.map({True: "PENDENTE", False: "SINCRONIZADO"})
    df.loc[pendente, "id_sistema_externo"] = ""

    relatorio.pendentes_sincronizacao = int(pendente.sum())
    return df


def executar_pipeline(df: pd.DataFrame) -> tuple[pd.DataFrame, RelatorioQualidade]:
    """Orquestra as etapas de tratamento. Função pura: não faz I/O,
    o que a torna trivial de testar com DataFrames em memória."""
    relatorio = RelatorioQualidade(registros_recebidos=len(df))

    validar_schema(df)

    com_chave, sem_chave = isolar_registros_sem_matricula(df, relatorio)
    com_chave = remover_duplicidades(com_chave, relatorio)

    df_final = pd.concat([com_chave, sem_chave], ignore_index=True)
    df_final = normalizar_campos(df_final, relatorio)
    df_final = reconciliar_status(df_final, relatorio)
    df_final = preparar_integracao(df_final, relatorio)

    relatorio.registros_finais = len(df_final)
    return df_final, relatorio