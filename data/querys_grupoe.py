from data.dbconnect import get_dataframe_from_query
import streamlit as st

@st.cache_data
def general_costs(day1, day2):
    return get_dataframe_from_query(f"""
SELECT
    DATE_FORMAT(CEC.Primeiro_Dia_Mes_Vencimento, '%m/%Y') AS 'Mês/Ano',
    SUM(CASE WHEN CEC.ID_Categoria = 100 THEN CEC.Valor END) AS 'C1 Impostos',
    SUM(CASE WHEN CEC.ID_Categoria = 104 THEN CEC.Valor END) AS 'C2 Custos de Ocupação',
    SUM(CASE WHEN CEC.ID_Categoria = 101 THEN CEC.Valor END) AS 'C3 Despesas com Pessoal Interno',
    SUM(CASE WHEN CEC.ID_Categoria = 105 THEN CEC.Valor END) AS 'C4 Despesas com Pessoal Terceirizado',
    SUM(CASE WHEN CEC.ID_Categoria = 102 THEN CEC.Valor END) AS 'C5 Despesas Operacionais com Shows',
    SUM(CASE WHEN CEC.ID_Categoria = 103 THEN CEC.Valor END) AS 'C6 Despesas com Clientes',
    SUM(CASE WHEN CEC.ID_Categoria = 108 THEN CEC.Valor END) AS 'C7 Despesas com Softwares e Licenças',
    SUM(CASE WHEN CEC.ID_Categoria = 107 THEN CEC.Valor END) AS 'C8 Despesas com Marketing',
    SUM(CASE WHEN CEC.ID_Categoria = 106 THEN CEC.Valor END) AS 'C9 Despesas Financeiras',
    SUM(CEC.Valor) AS 'Custos Totais'
FROM View_Custos_Eshows_Consolidados CEC
WHERE CEC.Primeiro_Dia_Mes_Vencimento >= '{day1}'
AND CEC.Primeiro_Dia_Mes_Vencimento <= '{day2}'
GROUP BY DATE_FORMAT(CEC.Primeiro_Dia_Mes_Vencimento, '%m/%Y')
ORDER BY STR_TO_DATE('Mês/Ano', '%m/%Y') DESC;
""", use_grupoe=True)

@st.cache_data
def cost_details(day1, day2):
    return get_dataframe_from_query(F"""
SELECT 
CEC.Categoria_de_Custo AS 'CATEGORIA DE CUSTO', 
CEC.Classificacao_Primaria AS 'CLASSIFICAÇÃO PRIMÁRIA', 
CEC.Valor AS 'VALOR', 
DATE_FORMAT(CEC.Primeiro_Dia_Mes_Vencimento, '%Y/%m') AS 'DATA'
FROM View_Custos_Eshows_Consolidados CEC
WHERE CEC.Primeiro_Dia_Mes_Vencimento >= '{day1}'
AND CEC.Primeiro_Dia_Mes_Vencimento <= '{day2}'
""", use_grupoe=True)

@st.cache_data
def ratings_rank(data):
    return get_dataframe_from_query(f"""
SELECT
DATE_FORMAT(CEC.Data_Vencimento, '%m/%Y') AS 'Mês/Ano',
CEC.Classificacao_Primaria AS 'CLASSIFICAÇÃO PRIMÁRIA', 
SUM(CEC.Valor) AS 'VALOR'

FROM View_Custos_Eshows_Consolidados CEC
WHERE CEC.Primeiro_Dia_Mes_Vencimento LIKE '{data}%'

GROUP BY CEC.Classificacao_Primaria, CEC.Primeiro_Dia_Mes_Vencimento
ORDER BY SUM(CEC.Valor) DESC
""", use_grupoe=True)

@st.cache_data
def ratings_rank_details(data):
    return get_dataframe_from_query(f"""
WITH CUSTOS AS (
    # Primeira parte: Custos Internos
    SELECT
  			CDC2.DESCRICAO AS GRUPO_GERAL,
        TCIE.ID AS ID_CUSTO,
        TCP.ID AS ID_NIVEL1,
        TCP.DESCRICAO AS CLASSIFICACAO_NIVEL1,
        TCIE.DESCRICAO AS DESCRICAO,
        TCIE.VALOR AS VALOR,
  			SP.DESCRICAO AS STATUS_PAGAMENTO,
        CDC2.ID AS ID_NIVEL2,
        CAST(CONCAT(YEAR(TCIE.DATA_COMPETENCIA), '-', MONTH(TCIE.DATA_COMPETENCIA), '-01') AS DATE) AS PRIMEIRO_DIA_MES_VENCIMENTO,
        TCIE.DATA_LANCAMENTO AS DATA_LANCAMENTO,
        TCIE.DATA_COMPETENCIA AS DATA_COMPETENCIA,
  			TCIE.DATA_VENCIMENTO AS DATA_VENCIMENTO 
    FROM
        T_CUSTOS_INTERNOS_ESHOWS TCIE
        LEFT JOIN T_CENTROS_DE_CUSTOS CDC ON TCIE.FK_CENTRO_DE_CUSTO = CDC.ID
        LEFT JOIN T_CLASSIFICACAO_PRIMARIA TCP ON TCIE.FK_CLASSIFICACAO_PRIMARIA = TCP.ID
        LEFT JOIN T_CATEGORIAS_DE_CUSTO CDC2 ON TCP.FK_CATEGORIA_CUSTO = CDC2.ID
  			LEFT JOIN T_STATUS_PAGAMENTO SP ON SP.ID = TCIE.STATUS_PAGAMENTO
    WHERE
        TCIE.DATA_VENCIMENTO > '2022-12-31 23:59:59'
        AND TCIE.TAG_INVESTIMENTO <> 1
        AND TCIE.TAG_ESTORNO <> 1

    UNION ALL

    # Segunda parte: Custos Colaboradores
    SELECT
  			CDC2.DESCRICAO AS GRUPO_GERAL,
        TCCE.ID AS ID_CUSTO, 
        TCP.ID AS ID_NIVEL1,
        TCP.DESCRICAO AS CLASSIFICACAO_NIVEL1,
        CONCAT(CDC.DESCRICAO, ' - ', TCP.DESCRICAO) AS DESCRICAO,
        TCCE.VALOR AS VALOR,
  			SP.DESCRICAO AS STATUS_PAGAMENTO,
        CDC2.ID AS ID_NIVEL2,
        CAST(CONCAT(YEAR(TCCE.DATA_VENCIMENTO), '-', MONTH(TCCE.DATA_VENCIMENTO), '-01') AS DATE) AS PRIMEIRO_DIA_MES_VENCIMENTO,
        TCCE.DATA_LANCAMENTO AS DATA_LANCAMENTO, 
        TCCE.DATA_PAGAMENTO AS DATA_COMPETENCIA,
  			TCCE.DATA_VENCIMENTO AS DATA_VENCIMENTO
    FROM
        T_CUSTOS_COLABORADORES_ESHOWS TCCE
        JOIN T_COLABORADORES_ESHOWS TCE ON TCCE.FK_COLABORADOR = TCE.ID
        LEFT JOIN T_CENTROS_DE_CUSTOS CDC ON TCCE.FK_CENTRO_DE_CUSTO = CDC.ID
        LEFT JOIN T_CLASSIFICACAO_PRIMARIA TCP ON TCCE.FK_CLASSIFICACAO_PRIMARIA = TCP.ID
        LEFT JOIN T_CATEGORIAS_DE_CUSTO CDC2 ON TCP.FK_CATEGORIA_CUSTO = CDC2.ID
				LEFT JOIN T_STATUS_PAGAMENTO SP ON SP.ID = TCCE.FK_STATUS_PAGAMENTO
    UNION ALL

    # Terceira parte: Custos Pessoal
    SELECT
  			CDC2.DESCRICAO AS GRUPO_GERAL,
        TCPP.ID AS ID_CUSTO, 
        TCP.ID AS ID_NIVEL1,
        TCP.DESCRICAO AS CLASSIFICACAO_NIVEL1,
        CONCAT(CDC.DESCRICAO, ' - ', TCP.DESCRICAO) AS DESCRICAO,
        TCPP.VALOR AS VALOR,
  			SP.DESCRICAO AS STATUS_PAGAMENTO,
        CDC2.ID AS ID_NIVEL2,
        CAST(CONCAT(YEAR(TCPP.DATA_VENCIMENTO), '-', MONTH(TCPP.DATA_VENCIMENTO), '-01') AS DATE) AS PRIMEIRO_DIA_MES_VENCIMENTO,
        TCPP.DATA_LANCAMENTO AS DATA_LANCAMENTO, 
        TCPP.DATA_PAGAMENTO AS DATA_COMPETENCIA,
  			TCPP.DATA_VENCIMENTO AS DATA_VENCIMENTO
    FROM
        T_CUSTOS_PESSOAL TCPP
        LEFT JOIN T_CENTROS_DE_CUSTOS CDC ON TCPP.CENTRO_DE_CUSTO = CDC.ID
        LEFT JOIN T_CLASSIFICACAO_PRIMARIA TCP ON TCPP.CLASSIFICACAO_PRIMARIA = TCP.ID
        LEFT JOIN T_CATEGORIAS_DE_CUSTO CDC2 ON TCP.FK_CATEGORIA_CUSTO = CDC2.ID
  			LEFT JOIN T_STATUS_PAGAMENTO SP ON SP.ID = TCPP.STATUS_PAGAMENTO
)

# Consulta final
SELECT 
		C.ID_CUSTO AS 'ID CUSTO',
		C.GRUPO_GERAL AS 'GRUPO GERAL',
    C.CLASSIFICACAO_NIVEL1 AS 'NIVEL 1',
    C.VALOR AS 'VALOR',
    C.STATUS_PAGAMENTO AS 'PAGAMENTO',
    DATE_FORMAT(C.DATA_COMPETENCIA, '%d/%m/%Y') AS 'DATA COMPETÊNCIA',
    DATE_FORMAT(C.DATA_VENCIMENTO, '%d/%m/%Y') AS 'DATA VENCIMENTO',
    C.DESCRICAO AS 'DESCRIÇÃO'
FROM CUSTOS C

JOIN 
    (SELECT CLASSIFICACAO_NIVEL1, SUM(VALOR) AS TOTAL_VALOR
     FROM CUSTOS
     WHERE PRIMEIRO_DIA_MES_VENCIMENTO LIKE '{data}%'
     GROUP BY CLASSIFICACAO_NIVEL1
    ) AS TOTAL_CUSTOS
ON C.CLASSIFICACAO_NIVEL1 = TOTAL_CUSTOS.CLASSIFICACAO_NIVEL1

WHERE C.PRIMEIRO_DIA_MES_VENCIMENTO LIKE '{data}%'

ORDER BY TOTAL_CUSTOS.TOTAL_VALOR DESC, C.VALOR ASC;
""", use_grupoe=True)

def collaborator_access(email):
    df = get_dataframe_from_query(f"""
    SELECT
        CE.EMAIL_CORPORATIVO AS 'COLABORADOR',
        GROUP_CONCAT(AD.NIVEL) AS 'NIVEL_ACESSO'		
    FROM T_COLABORADOR_NIVEL_ACESSO NA
    LEFT JOIN T_COLABORADORES_ESHOWS CE ON CE.ID = NA.FK_COLABORADOR
    LEFT JOIN T_NIVEL_ACESSO_DASH AD ON AD.ID = NA.FK_NIVEL_ACESSO
    WHERE CE.EMAIL_CORPORATIVO = '{email}'
    GROUP BY CE.EMAIL_CORPORATIVO
    """, use_grupoe=True)
    
    if not df.empty:
        return df['NIVEL_ACESSO'].iloc[0].split(',')  # Retorna os níveis como lista
    return []