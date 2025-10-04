# app/services/email_sender.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do .env

def send_email(destinatario: str, numero_oficio: str, resultado: dict):
    """
    Envia um e-mail com os dados do cálculo.
    O assunto inclui o número do ofício.
    """

    remetente = os.getenv("EMAIL_USER")
    senha = os.getenv("EMAIL_PASS")
    servidor = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    porta = int(os.getenv("EMAIL_PORT", 587))

    if not remetente or not senha:
        raise ValueError("Credenciais de e-mail não configuradas no .env")

    assunto = f"Ofício nº {numero_oficio} — Resultado PrecNet"

    corpo = f"""
    Prezado(a),

    Seguem os resultados atualizados para o ofício {numero_oficio}:

    • Valor bruto: R$ {resultado['valor_bruto']:,}
    • Fator IPCA: {resultado['fator_ipca']}
    • Valor corrigido: R$ {resultado['valor_corrigido']:,}
    • Valor líquido: R$ {resultado['valor_liquido']:,}
    • Data de atualização: {resultado['atualizado_em']}

    Atenciosamente,
    Equipe PrecNet
    """

    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "plain", "utf-8"))

    with smtplib.SMTP(servidor, porta) as server:
        server.starttls()
        server.login(remetente, senha)
        server.send_message(msg)

    return True
