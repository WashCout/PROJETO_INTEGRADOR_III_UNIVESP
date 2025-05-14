# admin.py
from django.contrib import admin, messages
from .models import Produto, Lojista, Estoque, Vendas

# 👉 Função de ação personalizada para criar estoque
def criar_estoque_para_produtos(modeladmin, request, queryset):
    precos = {
        'PA': 17.00,
        'PT': 8.00,
        'PG': 10.90,
        'PK': 6.00,
        'M5L': 150.00,
        'MA': 300.00,
        'MT': 200.00,
        'ME': 350.00,
        'PMA': 62.00,
        'PMT': 47.00,
        'PME': 52.00,
    }

    criados = 0
    for produto in queryset:
        if not Estoque.objects.filter(produto=produto).exists():
            Estoque.objects.create(
                produto=produto,
                codigo=produto.codigo,
                quantidade=300,
                valor=precos.get(produto.subcategoria, 0.00)
            )
            criados += 1

    messages.success(request, f"{criados} itens de estoque criados com sucesso.")

# 👉 ProdutoAdmin com a ação adicionada
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome_produto', 'categoria', 'subcategoria', 'descricao')
    search_fields = ('nome_produto', 'categoria')
    list_filter = ('categoria', 'subcategoria')
    actions = [criar_estoque_para_produtos]  # Aqui está o botão mágico!

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
