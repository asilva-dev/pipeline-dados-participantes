"""Ponto de entrada do pipeline de tratamento de dados de participantes.

Uso:
    python3 -m desafio1.main
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from desafio1.io_utils import carregar_dados, salvar_dados, salvar_relatorio
from desafio1.pipeline import SchemaInvalidoError, executar_pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--entrada",
        type=Path,
        default=Path("desafio1/dados_sujos.csv"),
        help="Caminho do CSV de entrada.",
    )
    parser.add_argument(
        "--saida",
        type=Path,
        default=Path("desafio1/dados_tratados.csv"),
        help="Caminho do CSV tratado de saída.",
    )
    parser.add_argument(
        "--relatorio",
        type=Path,
        default=Path("desafio1/relatorio_qualidade.csv"),
        help="Caminho do relatório de qualidade da execução.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        df_bruto = carregar_dados(args.entrada)
        df_tratado, relatorio = executar_pipeline(df_bruto)

        salvar_dados(df_tratado, args.saida)
        salvar_relatorio(relatorio, args.relatorio)

        logger.info("Registros recebidos: %d", relatorio.registros_recebidos)
        logger.info("Registros finais: %d", relatorio.registros_finais)
        if relatorio.status_desconhecidos:
            logger.warning(
                "Status não mapeados encontrados (revisar fonte): %s",
                relatorio.status_desconhecidos,
            )
        return 0

    except SchemaInvalidoError as erro:
        logger.error("Schema inválido: %s", erro)
        return 1
    except Exception:
        logger.exception("Falha inesperada no processamento.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
