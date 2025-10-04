# app/services/calculator.py
from datetime import datetime
from app.services.ipca_client import get_ipca_series, get_ipca_acumulado

class Calculator:
    def __init__(self):
        self.ipca_series = get_ipca_series()

    def atualizar_valor(self, valor_bruto: float, data_base: str, incide_ir : bool = True):
        """
        Calcula o valor líquido atualizado:
        - Corrige pelo IPCA desde a data base até o último mês
        - Aplica desconto de 3% de IR (se aplicável)
        """
        fator = get_ipca_acumulado(data_base, self.ipca_series)
        valor_corrigido = valor_bruto * fator
        valor_liquido = valor_corrigido * (0.97 if incide_ir else 1.0)

        return {
            "valor_bruto": round(valor_bruto, 2),
            "fator_ipca": round(fator, 6),
            "valor_corrigido": round(valor_corrigido, 2),
            "valor_liquido": round(valor_liquido, 2),
            "atualizado_em": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
