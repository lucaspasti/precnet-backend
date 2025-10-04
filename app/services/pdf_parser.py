import pdfplumber
import re

def parse_pdf(file_path: str) -> dict:
    """
    Lê o PDF do ofício requisitório e extrai os dados estruturados.
    Retorna um dicionário com as informações principais.
    """
    with pdfplumber.open(file_path) as pdf:
        text = " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    # Normaliza o texto
    text = re.sub(r"\s+", " ", text)

    # --- Regex principais ---
    numero_oficio = re.search(r"OF[IÍ]CIO\s*N[º°]?:?\s*([\d./A-Z]+)", text)
    beneficiario = re.search(r"III\s*-\s*BENEFICI[ÁA]RIO\s*Nome:\s*([A-Z\s]+)\s*CPF", text)
    cpf = re.search(r"CPF[:\s]*([\d.\/-]+)", text)
    valor_bruto = re.search(r"Valor bruto da requisi[cç][aã]o:\s*R\$?\s*([\d.,]+)", text)
    data_base = re.search(r"Data base do c[aá]lculo:\s*(\d{2}/\d{2}/\d{4})", text)
    incide_ir = re.search(r"Incide IR:\s*(Sim|N[aã]o)", text)

    # --- Conversões seguras ---
    numero_oficio = numero_oficio.group(1).strip() if numero_oficio else None
    beneficiario = beneficiario.group(1).title().strip() if beneficiario else None
    cpf = cpf.group(1).replace(".", "").replace("-", "") if cpf else None
    valor_bruto = (
        float(valor_bruto.group(1).replace(".", "").replace(",", "."))
        if valor_bruto else 0.0
    )
    data_base = (
        "-".join(data_base.group(1).split("/")[::-1])[:7]
        if data_base else None
    )
    incide_ir = incide_ir.group(1).lower() == "sim" if incide_ir else True

    return {
        "numero_oficio": numero_oficio,
        "beneficiario": beneficiario,
        "cpf": cpf,
        "valor_bruto": valor_bruto,
        "data_base": data_base,
        "incide_ir": incide_ir,
    }
