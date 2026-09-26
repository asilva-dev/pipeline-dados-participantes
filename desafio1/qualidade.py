"""Modelo de dados do relatório de qualidade por execução.

Manter isso separado do pipeline permite evoluir o formato do
relatório (novas métricas, novo formato de saída) sem tocar na lógica
de tratamento dos dados.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass
class RelatorioQualidade:
    """Métricas de execução do pipeline, para rastreabilidade/auditoria."""

    registros_recebidos: int = 0
    registros_sem_matricula: int = 0
    registros_duplicados_removidos: int = 0
    emails_invalidos: int = 0
    status_desconhecidos: dict[str, int] = field(default_factory=dict)
    divergencias_status: int = 0
    pendentes_sincronizacao: int = 0
    registros_finais: int = 0

    def to_dataframe(self) -> pd.DataFrame:
        linhas = {
            "registros_recebidos": self.registros_recebidos,
            "registros_sem_matricula": self.registros_sem_matricula,
            "registros_duplicados_removidos": self.registros_duplicados_removidos,
            "emails_invalidos": self.emails_invalidos,
            "status_desconhecidos_distintos": len(self.status_desconhecidos),
            "status_desconhecidos_detalhe": "; ".join(
                f"{valor}={qtd}" for valor, qtd in self.status_desconhecidos.items()
            ),
            "divergencias_status": self.divergencias_status,
            "pendentes_sincronizacao": self.pendentes_sincronizacao,
            "registros_finais": self.registros_finais,
        }
        return pd.DataFrame([linhas])
