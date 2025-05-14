# scripts/gerar_previsoes.py
import os, sys, json, warnings, holidays
from datetime import datetime, timedelta
import pandas as pd
from prophet import Prophet
from django import setup

warnings.filterwarnings("ignore")          # silencia avisos do Prophet

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gestor_Pedidos_Frutos.settings')
setup()

from lojistas.models import Vendas, Lojista, Produto, Estoque
from recomendacoes.models import PrevisaoPedido

# ----- configuração ---------------------------------------------------------
LIMITES = {
    'PA': 60, 'PT': 120, 'PG': 120, 'PK': 120,
    'M5L': 2,  'MA': 3,   'MT': 2,   'ME': 2,
    'PMA': 30, 'PMT': 30, 'PME': 30
}
feriados_br = holidays.Brazil(years=[2024, 2025])
HORIZONTE_DIAS = 60       # número de dias para projetar
# ---------------------------------------------------------------------------

def frame_vendas(qs):
    """Retorna DataFrame c/ colunas ds (data) e y (quantidade)."""
    linhas = []
    for v in qs:
        for item in json.loads(v.detalhes):
            linhas.append({
                "ds": v.data.date(),
                "y": int(item["quantidade"]),
                "produto": item["nome_produto"]
            })
    return pd.DataFrame(linhas)

def salvar_previsao(lojista, produto, qtd):
    """Aplica limites e grava PrevisaoPedido."""
    limite = LIMITES.get(produto.subcategoria, 50)
    PrevisaoPedido.objects.create(
        lojista      = lojista,
        produto      = produto,
        quantidade_sugerida = min(max(qtd, 1), limite),
        data_previsao = datetime.now().date()
    )

def gerar():
    PrevisaoPedido.objects.all().delete()

    for lojista in Lojista.objects.all():
        df = frame_vendas(Vendas.objects.filter(
            lojista=lojista, processo='realizado'))

        if df.empty:
            print(f"[-] {lojista} sem histórico.")
            continue

        for produto_nome, grupo in df.groupby("produto"):
            # -----------------------------------------------------------------
            # 1) Caso com apenas 1 linha: fallback simples
            if len(grupo) < 2:
                try:
                    produto = Produto.objects.get(nome_produto=produto_nome)
                    salvar_previsao(lojista, produto, int(grupo["y"].mean()))
                except Produto.DoesNotExist:
                    pass
                continue
            # -----------------------------------------------------------------
            # 2) Prophet para séries ≥ 2 linhas
            modelo = Prophet(
                holidays = pd.DataFrame({
                    "ds": list(feriados_br.keys()),
                    "holiday": list(feriados_br.values())
                }),
                weekly_seasonality=True,
                yearly_seasonality=True,
                daily_seasonality=False,
                n_changepoints=20
            )
            modelo.fit(grupo[["ds", "y"]])

            futuro   = modelo.make_future_dataframe(periods=HORIZONTE_DIAS)
            previsao = modelo.predict(futuro).tail(HORIZONTE_DIAS)
            qtd_pred = int(round(previsao["yhat"].sum()))

            try:
                produto = Produto.objects.get(nome_produto=produto_nome)
                salvar_previsao(lojista, produto, qtd_pred)
            except Produto.DoesNotExist:
                continue

        print(f"[✓] Previsões gravadas para {lojista.nome_loja}")

if __name__ == "__main__":
    gerar()
