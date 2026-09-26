"""Constantes e regras de configuração do pipeline.

Isolar essas definições num módulo próprio significa que ajustar uma
regra de negócio (por exemplo, adicionar um novo status válido) não
exige tocar em lógica de normalização, pipeline ou I/O.
"""

from __future__ import annotations

import re

STATUS_MAP: dict[str, str] = {
    "concluido": "Concluído",
    "concluído": "Concluído",
    "em andamento": "Em andamento",
    "matriculado": "Matriculado",
    "cancelado": "Cancelado",
}

EMAIL_PATTERN = re.compile(r"^[\w.\-+]+@[\w.\-]+\.[A-Za-z]{2,}$")

VALORES_ID_PENDENTE = {"", "N/A", "ERRO_SYNC", "PENDENTE"}

COLUNAS_OBRIGATORIAS = [
    "matricula",
    "nome_participante",
    "email_institucional",
    "status_programa_corporativo",
    "status_base_powerbi",
    "data_matricula",
    "data_conclusao",
    "id_sistema_externo",
]
