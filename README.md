# Apresentação do projeto, arquitetura e instruções

# Pipeline de Tratamento e Reconciliação de Dados de Participantes

Pipeline de dados desenvolvido em Python para ingestão, tratamento, normalização, reconciliação de status e geração de relatórios de auditoria de participantes de programas corporativos.

## Arquitetura e Decisões de Projeto

O projeto foi estruturado seguindo princípios de **Clean Code** e separação de responsabilidades:

- **Funções Puras e Testabilidade:** As etapas de normalização e transformação (`pipeline.py` e `normalizadores.py`) operam inteiramente em memória, sem efeitos colaterais de I/O, tornando os testes unitários simples e rápidos.
- **Isolamento de I/O (`io_utils.py`):** A leitura e escrita de arquivos ficam restritas às bordas do sistema.
- **Configuração Centralizada (`config.py`):** Mapeamentos de status, regex de e-mails e colunas obrigatórias ficam isolados, facilitando a manutenção sem alterar a lógica de negócio.
- **Auditoria e Qualidade (`relatorio_qualidade.py`):** Cada execução gera um relatório detalhado com métricas de registros recebidos, duplicidades removidas, e-mails inválidos, divergências de status (SSOT) e pendências de sincronização.

## Tecnologias Utilizadas

- **Python 3.10+**
- **Pandas** para manipulação e estruturação dos dados

## Como Executar

Clone o repositório e execute o pipeline via linha de comando informando os arquivos de entrada e saída:

```bash
python3 -m desafio1.main --entrada desafio1/dados_sujos.csv --saida desafio1/dados_tratados.csv --relatorio desafio1/relatorio_qualidade.csv
```

## Escopo: implementado vs. proposto

**Implementado:** validação de schema, isolamento de registros sem matrícula,
deduplicação determinística por data, normalização de campos, reconciliação
de status (AVA como fonte de verdade), separação entre ID externo e status de
sincronização e relatório de qualidade por execução.

**Proposto (não implementado):** banco relacional, carga idempotente (MERGE),
camadas persistidas, quarentena de registros rejeitados, consumo real da API,
alertas e orquestração.

**Testes:** as funções são puras e foram desenhadas para teste unitário, mas
a suíte de testes automatizados ainda não foi escrita.
