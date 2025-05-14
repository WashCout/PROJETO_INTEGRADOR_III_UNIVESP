from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
import json
from lojistas.models import Vendas, Lojista, Produto, Estoque
from recomendacoes.models import PrevisaoPedido
from django.db.models import Sum

@login_required
def minhas_recomendacoes(request):
    lojista = getattr(request.user, "lojista", None)
    previsoes = PrevisaoPedido.objects.filter(lojista=lojista) if lojista else []

    # gerar texto em LN – destaque p/ top-3 itens
    top3 = (previsoes.order_by('-quantidade_sugerida')[:3]
                     .values_list('produto__nome_produto','quantidade_sugerida'))
    texto = ("Sugestão: priorize "
             + ", ".join([f"{q} un de {nome}" for nome, q in top3])
             + " nas próximas 8 semanas para evitar rupturas de estoque.")

    return render(request, "minhas_recomendacoes.html", {
        "previsoes": previsoes.select_related("produto"),
        "texto": texto,
    })