import os
import sys
import django
import random
from datetime import datetime, timedelta
import json

# Adiciona o diretório do projeto ao sys.path manualmente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gestor_Pedidos_Frutos.settings')
django.setup()


from lojistas.models import Produto, Lojista, Vendas

# Configurações
LOJISTAS = [
    "Sorveteria Itanhaém",
    "Sorveteria Peruíbe",
    "Sorveteria São Vicente"
]

QTD_PEDIDOS_POR_LOJISTA = 100

# Função para gerar uma data aleatória dos últimos 2 anos
def gerar_data_aleatoria():
    dias_atras = random.randint(0, 730)
    return datetime.now() - timedelta(days=dias_atras)

# Gerar pedidos simulados
for nome_loja in LOJISTAS:
    try:
        lojista = Lojista.objects.get(nome_loja=nome_loja)
    except:
        print(f"Lojista '{nome_loja}' não encontrado.")
        continue

    produtos = list(Produto.objects.all())
    if not produtos:
        print("Nenhum produto cadastrado.")
        break

    for _ in range(QTD_PEDIDOS_POR_LOJISTA):
        num_itens = random.randint(2, 6)
        itens = random.sample(produtos, num_itens)

        detalhes = []
        for produto in itens:
            quantidade = random.randint(5, 30)
            valor_unitario = float(produto.estoques.first().valor)
            valor_total = round(quantidade * valor_unitario, 2)
            detalhes.append({
                'nome_produto': produto.nome_produto,
                'quantidade': quantidade,
                'valor_unitario': valor_unitario,
                'valor_total': valor_total
            })

        venda = Vendas.objects.create(
            lojista=lojista,
            data=gerar_data_aleatoria(),
            processo='realizado',
            detalhes=json.dumps(detalhes)
        )

    print(f"Pedidos gerados para {nome_loja}")
