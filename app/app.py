from flask import Flask, render_template, request, jsonify
import os
import logging
from werkzeug.utils import secure_filename

# Imports locais
from app.database import db, init_db
from app.models.scraping_data_model import Requisicao
from app.services.pdf_parser import parse_pdf
from app.services.calculator import Calculator
from app.services.email_sender import send_email

# Configuração do app Flask
app = Flask(__name__)
init_db(app)

app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Configuração de log
logging.basicConfig(level=logging.INFO)

# 🔹 Cria as tabelas na inicialização
with app.app_context():
    db.create_all()


# 🔹 Página principal (upload)
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        pdf = request.files.get("file")
        email = request.form.get("email")

        if not pdf or pdf.filename == "":
            return jsonify({"error": "Nenhum arquivo PDF enviado"}), 400
        if not email:
            return jsonify({"error": "O e-mail é obrigatório"}), 400

        filename = secure_filename(pdf.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        pdf.save(filepath)

        try:
            # 🔸 1. Extrai dados do PDF
            dados = parse_pdf(filepath)
            if not dados.get("numero_oficio"):
                return jsonify({"error": "Falha ao extrair dados do PDF"}), 400

            # 🔸 2. Cria e salva no banco
            nova_requisicao = Requisicao(
                numero_oficio=dados["numero_oficio"],
                beneficiario=dados["beneficiario"],
                cpf=dados["cpf"],
                valor_bruto=dados["valor_bruto"],
                data_base=dados["data_base"],
                incide_ir=dados["incide_ir"],
                email=email
            )
            db.session.add(nova_requisicao)
            db.session.commit()

            # 🔸 3. Calcula valor atualizado automaticamente
            calc = Calculator()
            resultado = calc.atualizar_valor(
                nova_requisicao.valor_bruto,
                nova_requisicao.data_base,
                nova_requisicao.incide_ir
            )

            # 🔸 4. Envia o e-mail automaticamente
            try:
                send_email(
                    destinatario=email,
                    numero_oficio=nova_requisicao.numero_oficio,
                    resultado=resultado
                )
                email_status = "E-mail enviado com sucesso!"
                app.logger.info(f"E-mail enviado para {email}")
            except Exception as e:
                email_status = f"Falha ao enviar e-mail: {e}"
                app.logger.error(email_status)

            # 🔸 5. Retorna resultado consolidado
            return jsonify({
                "mensagem": "Requisição processada e e-mail enviado!",
                "numero_oficio": nova_requisicao.numero_oficio,
                "beneficiario": nova_requisicao.beneficiario,
                "valor_bruto": resultado["valor_bruto"],
                "valor_corrigido": resultado["valor_corrigido"],
                "valor_liquido": resultado["valor_liquido"],
                "fator_ipca": resultado["fator_ipca"],
                "email": email,
                "status_email": email_status
            })

        except Exception as e:
            app.logger.error(f"Erro ao processar PDF: {e}")
            return jsonify({"error": str(e)}), 500

    return render_template("upload.html")


# 🔹 Rota de debug – mostra todos os registros
@app.route("/debug/requisicoes")
def debug_requisicoes():
    dados = Requisicao.query.all()
    return jsonify([
        {
            "id": r.id,
            "numero_oficio": r.numero_oficio,
            "beneficiario": r.beneficiario,
            "cpf": r.cpf,
            "valor_bruto": r.valor_bruto,
            "data_base": r.data_base,
            "incide_ir": r.incide_ir,
            "email": r.email
        }
        for r in dados
    ])


if __name__ == "__main__":
    app.run(debug=True)
