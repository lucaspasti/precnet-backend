from datetime import datetime
from app.database import db

class EmailEnvio(db.Model):
    __tablename__ = "emails_enviados"

    id = db.Column(db.Integer, primary_key=True)
    requisicao_id = db.Column(db.Integer, db.ForeignKey("requisicoes.id"), nullable=False)
    email_destino = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), default="pendente")
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)

    requisicao = db.relationship("Requisicao", backref=db.backref("emails", lazy=True))
