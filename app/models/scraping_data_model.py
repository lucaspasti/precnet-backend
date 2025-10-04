from datetime import datetime
from app.database import db

class Requisicao(db.Model):
    __tablename__ = "requisicoes"

    id = db.Column(db.Integer, primary_key=True)
    numero_oficio = db.Column(db.String(50), nullable=False)
    beneficiario = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    valor_bruto = db.Column(db.Float, nullable=False)
    data_base = db.Column(db.String(7), nullable=False)
    incide_ir = db.Column(db.Boolean, default=True)
    email = db.Column(db.String(120), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
