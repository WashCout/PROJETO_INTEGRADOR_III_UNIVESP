from django.db import models
from lojistas.models import Lojista, Produto

class PrevisaoPedido(models.Model):
    lojista = models.ForeignKey(Lojista, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade_sugerida = models.IntegerField()
    data_previsao = models.DateField(auto_now_add=True)
    texto_resumo = models.TextField(blank=True, default="")