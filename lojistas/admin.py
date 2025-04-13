# admin.py
from django.contrib import admin
from .models import Produto, Lojista, Estoque, Vendas

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome_produto', 'categoria', 'subcategoria', 'descricao')
    search_fields = ('nome_produto', 'categoria')
    list_filter = ('categoria', 'subcategoria')

admin.site.register(Produto, ProdutoAdmin)

class LojistaAdmin(admin.ModelAdmin):
    list_display = ('nome_loja', 'user', 'telefone', 'email')
    search_fields = ('nome_loja', 'email')
    list_filter = ('nome_loja',)

admin.site.register(Lojista, LojistaAdmin)

class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'produto', 'quantidade', 'valor', 'valor_total')
    search_fields = ('produto__nome_produto',)
    list_filter = ('produto__categoria',)

    def valor_total(self, obj):
        return obj.valor_total()
    valor_total.short_description = "Valor Total (R$)"

admin.site.register(Estoque, EstoqueAdmin)

class VendasAdmin(admin.ModelAdmin):
    list_display = ('processo', 'lojista', 'data', 'valor_total')
    search_fields = ('lojista__nome_loja',)
    list_filter = ('processo', 'data')
    date_hierarchy = 'data'

    def valor_total(self, obj):
        return obj.valor_total
    valor_total.short_description = "Valor Total (R$)"

admin.site.register(Vendas, VendasAdmin)