"""Normalização de campos individuais.

Todas as funções aqui são puras (sem efeito colateral, sem I/O), o que
as torna triviais de testar isoladamente com `assert` simples — não
dependem de DataFrame, arquivo ou estado externo.
"""

from __future__ import annotations

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


def normalizar_data(valor: object) -> str:
    """Converte datas para ISO (YYYY-MM-DD); retorna vazio se inválida.

    Usa format="mixed" porque a base de origem mistura formatos
    (DD/MM/AAAA vindo do Programa Corporativo e AAAA-MM-DD vindo de
    outras integrações) — isso evita ambiguidade e o warning do pandas
    ao tentar aplicar dayfirst em datas que já estão em ISO.
    """
    data = pd.to_datetime(valor, errors="coerce", dayfirst=True, format="mixed")
    return "" if pd.isna(data) else data.strftime("%Y-%m-%d")
