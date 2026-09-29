"""Normalização de campos individuais.

Todas as funções aqui são puras (sem efeito colateral, sem I/O), o que
as torna triviais de testar isoladamente com `assert` simples — não
dependem de DataFrame, arquivo ou estado externo.
"""

from __future__ import annotations

import re

import pandas as pd

from desafio1.config import EMAIL_PATTERN, STATUS_MAP


def normalizar_texto(valor: object) -> str:
    """Remove espaços desnecessários e trata valores ausentes."""
    if pd.isna(valor):
        return ""
    return str(valor).strip()


def normalizar_email(valor: object) -> str:
    """Retorna o e-mail em minúsculas se for válido; senão, string vazia.

    Importante: Um e-mail inválido
    deve permanecer identificável como ausente, não virar um valor
    fixo compartilhado por vários participantes (isso quebraria
    qualquer join por e-mail e mascararia a causa raiz).
    """
    email = normalizar_texto(valor).lower()
    return email if EMAIL_PATTERN.fullmatch(email) else ""


def normalizar_status(valor: object, contador_desconhecidos: dict[str, int]) -> str:
    """Converte para status padronizado; registra valores não mapeados
    no dicionário `contador_desconhecidos` para revisão posterior."""
    status_bruto = normalizar_texto(valor)
    status = STATUS_MAP.get(status_bruto.lower())

    if status is None:
        if status_bruto:
            contador_desconhecidos[status_bruto] = (
                contador_desconhecidos.get(status_bruto, 0) + 1
            )
        return "Desconhecido"

    return status


def parse_data(valor: object) -> pd.Timestamp:
    """Interpreta a data sem ambiguidade: ISO (AAAA-MM-DD) ou BR (DD/MM/AAAA).

    Formato explícito, em vez de dayfirst=True, porque o pandas pode trocar
    dia e mês em datas ISO ambíguas (ex.: 2023-02-10 virar 2 de outubro),
    dependendo da versão.
    """
    texto = normalizar_texto(valor)
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", texto):
        return pd.to_datetime(texto, format="%Y-%m-%d", errors="coerce")
    return pd.to_datetime(texto, format="%d/%m/%Y", errors="coerce")


def normalizar_data(valor: object) -> str:
    """Converte datas para ISO (YYYY-MM-DD); retorna vazio se inválida."""
    data = parse_data(valor)
    return "" if pd.isna(data) else data.strftime("%Y-%m-%d")