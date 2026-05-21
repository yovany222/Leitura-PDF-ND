import re

def extrair_dados(texto):
    dados = {}

    # NUMERO (corrigido - quebra de linha)
    match = re.search(r"N\.º:\s*(\d+)", texto)
    if match:
        dados["numero"] = match.group(1)

    # DATA
    match = re.search(r"Nota de Débito\s*(\d{2}/\d{2}/\d{4})", texto)
    if match:
        dados["data_envio"] = match.group(1)

    # VENCIMENTO
    match = re.search(r"Vencimento:\s*(\d{2}/\d{2}/\d{4})", texto)
    if match:
        dados["data_vencimento"] = match.group(1)

    
    # CNPJ DESTINATÁRIO (somente números)
    match = re.search(r"Destinatário:.*?CNPJ:\s*([\d./-]+)", texto, re.DOTALL)
    if match:
        cnpj = match.group(1)
        cnpj = re.sub(r"\D", "", cnpj)
        dados["cnpj eneva"] = cnpj


    # MOTIVO
    match = re.search(r"Motivo:\s*(.*?)Quantidade", texto, re.DOTALL)
    if match:
        dados["motivo"] = match.group(1).strip()

    # VALOR
    match = re.search(r"Valor Total Débito:\s*R?\$?\s*([\d.,]+)", texto)
    if match:
        valor = match.group(1).replace(".", "").replace(",", ".")
        dados["valor"] = float(valor)

    dados["remetente"] = "TAG"
    return dados