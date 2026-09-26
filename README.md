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
python -m desafio1.main --entrada caminho/entrada.csv --saida caminho/saida_tratada.csv --relatorio caminho/relatorio.csv
```
