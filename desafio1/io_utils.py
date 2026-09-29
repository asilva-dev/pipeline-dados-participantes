"""Leitura e escrita de arquivos.

Isolar I/O aqui significa que testar a lógica de negócio (pipeline.py)
não exige tocar em disco: os testes passam DataFrames diretamente para
`executar_pipeline`. Este módulo só existe para a fronteira real com
o sistema de arquivos.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from desafio1.qualidade import RelatorioQualidade

logger = logging.getLogger(__name__)


def carregar_dados(caminho: Path) -> pd.DataFrame:
    logger.info("Lendo arquivo de entrada: %s", caminho)
    return pd.read_csv(caminho, dtype=str)


def salvar_dados(df: pd.DataFrame, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(caminho, index=False)
    logger.info("Arquivo tratado gerado: %s", caminho)


def salvar_relatorio(relatorio: RelatorioQualidade, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    relatorio.to_dataframe().to_csv(caminho, index=False)
    logger.info("Relatório de qualidade gerado: %s", caminho)
