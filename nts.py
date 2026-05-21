import re

def extrair_dados(texto):
    dados = {}

    # Número da ND
    match = re.search(r"Carta de Débito N\.º:\s*(\d+)", texto)
    if match:
        dados["numero"] = match.group(1)

    # Data de envio
    match = re.search(r"Rio de Janeiro,\s*(\d{2}/\d{2}/\d{4})", texto)
    if match:
        dados["data_envio"] = match.group(1)

    # Data de vencimento
    match = re.search(r"Vencimento:\s*(\d{2}/\d{2}/\d{4})", texto)
    if match:
        dados["data_vencimento"] = match.group(1)

    # CNPJ do destinatário
    match = re.search(r"Destinatário:.*?CNPJ:\s*([\d./-]+)", texto, re.DOTALL)
    if match:
        cnpj = match.group(1)
        cnpj = re.sub(r"\D", "", cnpj)
        dados["cnpj eneva"] = cnpj

    # Motivo
    match = re.search(r"Motivo:\s*(.*?)\s*Quantidade:", texto)
    if match:
        dados["motivo"] = match.group(1).strip()

    # Valor
    match = re.search(r"Valor Total Débito:\s*([\d.,]+)", texto)
    if match:
        valor = match.group(1).replace(".", "").replace(",", ".")
        dados["valor"] = float(valor)

    # Empresa
    dados["remetente"] = "NTS"

    return dados