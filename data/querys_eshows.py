from data.dbconnect import get_dataframe_from_query
import streamlit as st

@st.cache_data
def general_revenue(day1, day2, filters=''):
    return get_dataframe_from_query(f"""
    SELECT 
        DATE_FORMAT(FE.Data, '%m/%Y') AS 'Mês/Ano',
        COUNT(DISTINCT C.ID) AS 'Total Casas',
        COUNT(DISTINCT FE.p_ID) AS 'Total Shows',
        SUM(FE.Valor_Total) AS 'Valor Total',
        SUM(FE.Comissao_Eshows_B2B) AS 'Comissão B2B',
        SUM(
            FE.Comissao_Eshows_B2B
        ) / SUM(FE.Valor_Total) AS 'Take Rate',
        SUM(FE.Comissao_Eshows_B2C) AS 'Comissão B2C',
        SUM(FE.SAAS_Mensalidade) AS 'SAAS Mensalidade',
        SUM(FE.SAAS_Percentual) AS 'SAAS Percentual',
        SUM(FE.Curadoria) AS 'Curadoria',
        SUM(FE.Taxa_Adiantamento) AS 'Taxa Adiantamento',
        SUM(FE.Taxa_Emissao_NF) AS 'Taxa Emissão NF',
        SUM(
            FE.Comissao_Eshows_B2B + 
            FE.Comissao_Eshows_B2C + 
            FE.SAAS_Mensalidade + 
            FE.SAAS_Percentual +  
            FE.Curadoria + 
            FE.Taxa_Adiantamento + 
            FE.Taxa_Emissao_NF
        ) AS 'Faturamento Total',
        SUM(
            FE.Comissao_Eshows_B2B + 
            FE.Comissao_Eshows_B2C + 
            FE.SAAS_Mensalidade + 
            FE.SAAS_Percentual +  
            FE.Curadoria + 
            FE.Taxa_Adiantamento + 
            FE.Taxa_Emissao_NF
        ) / SUM(FE.Valor_Total)
		AS 'Percentual Faturamento'
    FROM View_Faturam_Eshows FE
    INNER JOIN T_COMPANIES C ON FE.c_ID = C.ID
    LEFT JOIN T_GRUPOS_DE_CLIENTES GC ON C.FK_GRUPO = GC.ID
    LEFT JOIN T_KEYACCOUNT_ESTABELECIMENTO KE ON C.FK_KEYACCOUNT = KE.ID
    LEFT JOIN T_OPERADORES OP ON C.FK_OPERADOR = OP.ID
    WHERE FE.Data >= '{day1}'
    AND FE.Data <= DATE_ADD('{day2}', INTERVAL 1 DAY)
    {filters}  -- Aqui o filtro é adicionado dinamicamente
    GROUP BY DATE_FORMAT(FE.Data, '%m/%Y')
    ORDER BY STR_TO_DATE(DATE_FORMAT(FE.Data, '%m/%Y'), '%m/%Y') ASC
    """)

@st.cache_data
def groups_companies(day1, day2, filters=''):
    return get_dataframe_from_query(F"""
SELECT 
GC.NOME,
C.NAME,
KE.NOME AS 'KY'
FROM View_Faturam_Eshows FE
INNER JOIN T_COMPANIES C ON FE.c_ID = C.ID
LEFT JOIN T_GRUPOS_DE_CLIENTES GC ON C.FK_GRUPO = GC.ID
LEFT JOIN T_KEYACCOUNT_ESTABELECIMENTO KE ON C.FK_KEYACCOUNT = KE.ID
LEFT JOIN T_OPERADORES OP ON C.FK_OPERADOR = OP.ID
WHERE FE.Data >= '{day1}'
AND FE.Data <= DATE_ADD('{day2}', INTERVAL 1 DAY)
{filters}
GROUP BY C.NAME
ORDER BY GC.NOME
""")

@st.cache_data
def general_revenue_proposal(day1, day2, filters):
    return get_dataframe_from_query(f"""
SELECT
FE.p_ID AS 'ID PROPOSTA',
FE.Casa AS 'CASAS',
FE.c_ID AS 'ID CASA',
FE.UF AS 'UF',
FE.Cidade AS 'CIDADE',
DATE_FORMAT(FE.Data, '%d/%m/%Y') AS 'DATA',
CASE DAYOFWEEK(FE.Data)
        WHEN 1 THEN 'Domingo'
        WHEN 2 THEN 'Segunda-Feira'
        WHEN 3 THEN 'Terça-Feira'
        WHEN 4 THEN 'Quarta-Feira'
        WHEN 5 THEN 'Quinta-Feira'
        WHEN 6 THEN 'Sexta-Feira'
        WHEN 7 THEN 'Sábado'
    END AS "Dia da Semana",
DATE_FORMAT(FE.Data_Pagamento, '%d/%m/%Y') AS 'PAGAMENTO',
FE.Artista AS 'ARTISTA',
FE.Valor_Bruto AS 'VALOR BRUTO',
FE.Valor_Liquido AS 'VALOR LIQUIDO',
FE.Valor_Liquido / FE.Valor_Bruto AS '% LIQUIDO',
FE.B2C AS 'B2C',
FE.Comissao_Eshows_B2B AS 'COMISSÃO B2B',
FE.Comissao_Eshows_B2C AS 'COMISSÃO B2C',
FE.Taxa_Adiantamento AS 'ADIANTAMENTO',
FE.SAAS_Percentual AS 'SAAS PERCENTUAL',
FE.SAAS_Mensalidade AS 'SAAS MENSALIDADE',

CASE WHEN FE.Fk_Sem_Curadoria = '0' THEN 'SEM'
WHEN FE.Fk_Sem_Curadoria = '1' THEN 'COM'
END 'CURADORIA',

FE.Taxa_Emissao_NF AS 'TAXA EMISSÃO NF',
FE.Valor_Total AS 'VALOR TOTAL',
GC.NOME AS 'Grupo',
KE.KEYACCOUNT AS 'KeyAccount',
O.NOME AS 'Operador'
FROM View_Faturam_Eshows FE
INNER JOIN T_COMPANIES C ON (FE.c_ID = C.ID)
LEFT JOIN T_GRUPOS_DE_CLIENTES GC ON (C.FK_GRUPO = GC.ID)
LEFT JOIN T_KEYACCOUNT_ESTABELECIMENTO KE ON (C.FK_KEYACCOUNT = KE.ID)
LEFT JOIN T_OPERADORES O ON (C.FK_OPERADOR = O.ID)
WHERE FE.Data >= '{day1}'
AND FE.Data <= '{day2}'
{filters}
ORDER BY FE.Data, FE.Casa
""")