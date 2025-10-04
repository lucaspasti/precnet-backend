import requests
from datetime import datetime

def get_ipca_series():
    """
    Consulta o IPCA (série 433) no BACEN.
    Retorna um dicionário no formato {"YYYY-MM": indice_percentual}.
    """
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    series = {}
    for item in data:
        # item["data"] vem como dd/mm/yyyy
        dia, mes, ano = item["data"].split("/")
        key = f"{ano}-{mes.zfill(2)}"
        valor = float(item["valor"].replace(",", "."))
        series[key] = valor

    return series


def get_ipca_acumulado(data_base: str, ipca_series: dict) -> float:
    """
    Calcula o fator acumulado do IPCA desde a data_base até o último índice disponível.
    Exemplo: data_base = '2022-10'
    """
    ano_base, mes_base = map(int, data_base.split("-"))

    # ordena as chaves em ordem cronológica
    chaves = sorted(ipca_series.keys())

    acumulado = 1.0
    iniciou = False
    for chave in chaves:
        ano, mes = map(int, chave.split("-"))
        if (ano == ano_base and mes == mes_base):
            iniciou = True
        if iniciou:
            acumulado *= (1 + ipca_series[chave] / 100)

    return acumulado
