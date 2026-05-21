import re
from datetime import datetime, timedelta


# LISTA DE FERIADOS (PADRONIZADA COMO date)
FERIADOS = {
    datetime.strptime(d, "%d/%m/%Y").date()
    for d in [
        "01/01/2026","17/02/2026","03/04/2026","05/04/2026","21/04/2026","01/05/2026","04/06/2026","07/09/2026","12/10/2026","02/11/2026","15/11/2026","25/12/2026",
        "01/01/2027","09/02/2027","26/03/2027","28/03/2027","21/04/2027","01/05/2027","27/05/2027","07/09/2027","12/10/2027","02/11/2027","15/11/2027","25/12/2027",
        "01/01/2028","29/02/2028","14/04/2028","16/04/2028","21/04/2028","01/05/2028","15/06/2028","07/09/2028","12/10/2028","02/11/2028","15/11/2028","25/12/2028",
        "01/01/2029","13/02/2029","30/03/2029","01/04/2029","21/04/2029","01/05/2029","31/05/2029","07/09/2029","12/10/2029","02/11/2029","15/11/2029","25/12/2029",
        "01/01/2030","05/03/2030","19/04/2030","21/04/2030","01/05/2030","20/06/2030","07/09/2030","12/10/2030","02/11/2030","15/11/2030","25/12/2030",
        "01/01/2031","25/02/2031","11/04/2031","13/04/2031","21/04/2031","01/05/2031","12/06/2031","07/09/2031","12/10/2031","02/11/2031","15/11/2031","25/12/2031",
        "01/01/2032","10/02/2032","26/03/2032","28/03/2032","21/04/2032","01/05/2032","27/05/2032","07/09/2032","12/10/2032","02/11/2032","15/11/2032","25/12/2032",
        "01/01/2033","01/03/2033","15/04/2033","17/04/2033","21/04/2033","01/05/2033","16/06/2033","07/09/2033","12/10/2033","02/11/2033","15/11/2033","25/12/2033",
        "01/01/2034","21/02/2034","07/04/2034","09/04/2034","21/04/2034","01/05/2034","08/06/2034","07/09/2034","12/10/2034","02/11/2034","15/11/2034","25/12/2034",
        "01/01/2035","06/02/2035","23/03/2035","25/03/2035","21/04/2035","01/05/2035","24/05/2035","07/09/2035","12/10/2035","02/11/2035","15/11/2035","25/12/2035",
        "01/01/2036","26/02/2036","11/04/2036","13/04/2036","21/04/2036","01/05/2036","12/06/2036","07/09/2036","12/10/2036","02/11/2036","15/11/2036"
    ]
}

# DIA ÚTIL
def eh_dia_util(data):
    return data.weekday() < 5 and data not in FERIADOS


# CALCULAR 7º DIA ÚTIL DO MÊS
def calcular_setimo_dia_util(ano, mes):
    count = 0
    data = datetime(ano, mes, 1).date()

    while True:
        if eh_dia_util(data):
            count += 1
            if count == 7:
                return data
        data += timedelta(days=1)


# CALCULAR DIAS ÚTEIS ENTRE DUAS DATAS
def contar_dias_uteis(inicio, fim):
    dias = 0
    data = inicio + timedelta(days=1)

    while data <= fim:
        if eh_dia_util(data):
            dias += 1
        data += timedelta(days=1)

    return dias


# SOMAR DIAS ÚTEIS
def adicionar_dias_uteis(data, dias):
    count = 0
    while count < dias:
        data += timedelta(days=1)
        if eh_dia_util(data):
            count += 1
    return data


# CÁLCULO DE VENCIMENTO
def calcular_vencimento(data_envio_str):
    try:
        data_envio = datetime.strptime(data_envio_str, "%d/%m/%Y").date()
    except:
        return None

    setimo_dia_util = calcular_setimo_dia_util(data_envio.year, data_envio.month)

    # CASO 1: antes ou igual ao 7º dia útil
    if data_envio <= setimo_dia_util:
        vencimento = datetime(data_envio.year, data_envio.month, 21).date()

    # CASO 2: depois do 7º dia útil
    else:
        # quantos dias úteis passou
        atraso = contar_dias_uteis(setimo_dia_util, data_envio)

        # base no dia 21 do mesmo mês
        base = datetime(data_envio.year, data_envio.month, 21).date()

        # soma atraso em dias úteis
        vencimento = adicionar_dias_uteis(base, atraso)

    return vencimento.strftime("%d/%m/%Y")


# PARSER
def extrair_dados(texto):
    dados = {}

    match = re.search(r"NÚMERO DA ND\s*([\d/]+)", texto)
    if match:
        dados["numero"] = match.group(1)

    # REGEX MAIS ROBUSTO PARA DATA
    match = re.search(r"Data\s*:?\s*(\d{2}/\d{2}/\d{4})", texto, re.IGNORECASE)
    if match:
        dados["data_envio"] = match.group(1)

    if "data_envio" in dados:
        dados["data_vencimento"] = calcular_vencimento(dados["data_envio"])

    match = re.search(r"Creditado:.*?CNPJ:\s*([\d./-]+)", texto, re.DOTALL)
    if match:
        dados["cnpj eneva"] = re.sub(r"\D", "", match.group(1))

    motivos = re.findall(r"Débito referente ao\s*(.*?)\s+\d", texto)
    if motivos:
        dados["motivo"] = " | ".join(motivos)

    match = re.search(r"\)\s*([\d.,]+)", texto)
    if match:
        valor = match.group(1).replace(".", "").replace(",", ".")
        dados["valor"] = float(valor)

    dados["remetente"] = "TBG"

    return dados