# app/models/calculo_model.py
from datetime import datetime
from app.database import db

class Calculo(db.Model):
    __tablename__ = "calculos"

    id = db.Column(db.Integer, primary_key=True)
    requisicao_id = db.Column(db.Integer, db.ForeignKey("requisicoes.id"), nullable=False)
    valor_corrigido = db.Column(db.Float, nullable=False)
    valor_liquido = db.Column(db.Float, nullable=False)
    data_calculo = db.Column(db.DateTime, default=datetime.utcnow)

    requisicao = db.relationship("Requisicao", backref=db.backref("calculos", lazy=True))
