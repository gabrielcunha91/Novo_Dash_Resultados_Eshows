# Resultados Eshows

## Índice
1. [Sobre o Projeto](#sobre-o-projeto)
2. [Funcionalidades](#funcionalidades)
   - [Faturamento Eshows Gerencial](#1-faturamento-eshows-gerencial)
   - [Gerenciamento de Custos](#2-gerenciamento-de-custos)
3. [Tecnologias Utilizadas](#tecnologias-utilizadas)
4. [Como Executar](#como-executar)
5. [Contato](#contato)

## Sobre o Projeto
O Dash **Resultados Eshows** é um dashboard desenvolvido em Streamlit para visualizar o faturamento e os custos da Eshows de forma gerencial e detalhada. O sistema permite a filtragem e análise de dados financeiros, proporcionando uma visão estratégica do desempenho financeiro da empresa.

## Funcionalidades

### 1. Faturamento Eshows Gerencial
- Apresenta uma tabela com o faturamento geral da Eshows.
- Permite a seleção de um grupo de casas para análise específica.
- Após selecionar um grupo, libera a opção de selecionar casas individuais para detalhar ainda mais o faturamento.
- Exibe os dados segmentados por grupo e por casa.
- Libera também uma nova visualização **Abertura Por Proposta**, que ira exibir as propostas

### 2. Gerenciamento de Custos
- Exibe uma tabela com todos os custos por categoria, incluindo:
  - Diferença entre faturamento e custo.
  - Total de custos e representações percentuais.
- Apresenta uma segunda tabela com detalhes específicos das classificações de cada categoria de custo.
  - **Exemplo: `c2_Custos_de_Ocupacao` inclui:**  
    - Aluguel  
    - Manutenção  
    - Utilidades  
    - Equipamentos de Escritório  
    - Materiais de Escritório  
    - Obras e Reformas  
    - Telefone e Internet
    - Entre outros...
  
  - Exibe o total Geral e por classificação.
  -
- #### As proximas tabelas são construidas lado a lado, para um comparação de meses:
- Permite a seleção de dois mêses específico para visualizar custos detalhados e compará-los"
- Inclui dois gráficos de pizza comparativos para melhor visualização dos custos selecionados.
- Exibe tabelas comparativas com o ranking dos maiores custos conforme o Mês selecionado.
- Apresenta tabelas detalhadas com informações adicionais, como ID do custo, nível, fornecedor, pagamento, entre outros.

## Tecnologias Utilizadas
As principais tecnologias utilizadas no projeto são:
- **Python** - Linguagem principal do desenvolvimento.
- **Streamlit** - Framework para construção de dashboards interativos.
- **Pandas** - Manipulação e análise de dados.
- **Streamlit ECharts** - Visualizações interativas avançadas.

## Como Executar

```sh
# Clone este repositório:
git clone https://github.com/Eshows-Tech/streamlit-resultados-eshows.git

# Acesse a pasta do projeto:
cd streamlit-resultados-eshows

# Instale as dependências:
pip install -r requirements.txt

# Execute o dashboard:
streamlit run main.py
```

## Contato
Caso tenha dúvidas ou sugestões, sinta-se à vontade para entrar em contato via [GitHub Issues](https://github.com/Eshows-Tech/streamlit-resultados-eshows/issues).
