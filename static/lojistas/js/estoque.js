// static/js/estoque.js
document.addEventListener('DOMContentLoaded', function () {

    /* ---------- CONFIG BÁSICA DATATABLES ---------- */
    const estoqueTable = $('#estoqueTable').DataTable({
      language : { url:'//cdn.datatables.net/plug-ins/2.0.7/i18n/pt-BR.json' },
      ajax     : { url: ESTOQUE_API_URL, dataSrc:'' },
      columns  : [
        { data:'codigo' },
        { data:'nome_produto' },
        { data:'categoria' },
        { data:'subcategoria' },
        /* ▸ Coluna “Disponível” ---------------------- */
        { data:'quantidade' },
        /* ▸ Picker de quantidade a reservar ---------- */
        { data:null, render:(d,t,r)=>`
            <input type="number"
                   class="form-control form-control-sm quantity-picker"
                   min="1" max="${r.quantidade}" value="1">`
        },
        /* ▸ Valor unitário --------------------------- */
        { data:'valor', render:(d)=>`R$ ${parseFloat(d).toFixed(2).replace('.',',')}` },
        /* ▸ Botão Adicionar -------------------------- */
        { data:null, className:'dt-center',
          defaultContent:'<button class="btn btn-success btn-sm add-to-cart">Add</button>' }
      ]
    });
  
    /* ---------- FILTRO SUBCATEGORIA --------------- */
    document.getElementById('subcategoriaFiltro').addEventListener('change', e=>{
        estoqueTable.column(3).search(e.target.value).draw();
    });
  
    /* ---------- TABELA DE SELECIONADOS ------------ */
    const carrinhoTable = $('#selecionadosTable').DataTable({
      language : { url:'//cdn.datatables.net/plug-ins/2.0.7/i18n/pt-BR.json' },
      ordering : false,
      searching: false,
      paging   : false,
      columns  : [
        { data:'nome_produto' },
        { data:'quantidade',
          render:(d)=>`<input type="number" class="form-control form-control-sm selected-qty" min="1" value="${d}">`
        },
        { data:null, render:(d)=>`R$ ${(d.valor*d.quantidade).toFixed(2).replace('.',',')}` },
        { data:null, className:'dt-center',
          defaultContent:'<button class="btn btn-danger btn-sm remove-from-cart">❌</button>' }
      ]
    });
  
    /* ---------- ADICIONAR AO CARRINHO ------------- */
    $('#estoqueTable tbody').on('click','button.add-to-cart',function(){
        const linha = estoqueTable.row($(this).closest('tr'));
        const info  = linha.data();
        const qtd   = $(this).closest('tr').find('.quantity-picker').val()*1;
  
        if(qtd>info.quantidade){
          return alert('Quantidade selecionada excede o estoque disponível.');
        }
  
        /* empurra para carrinho */
        carrinhoTable.row.add({...info, quantidade:qtd}).draw();
        atualizarTotal();
    });
  
    /* ---------- REMOVER DO CARRINHO --------------- */
    $('#selecionadosTable tbody').on('click','button.remove-from-cart',function(){
        carrinhoTable.row($(this).closest('tr')).remove().draw();
        atualizarTotal();
    });
  
    /* ---------- ATUALIZAR TOTAL GERAL ------------- */
    function atualizarTotal(){
      let total=0;
      carrinhoTable.rows().every(function(){
          const d=this.data();
          total += d.quantidade * d.valor;
      });
      document.getElementById('totalGeral').textContent =
          total.toFixed(2).replace('.',',');
    }
  
    /* ---------- FINALIZAR RESERVA ----------------- */
    document.getElementById('finalizarCompraBtn').addEventListener('click',()=>{
        if(!carrinhoTable.rows().count()){ return alert('Escolha ao menos 1 item.'); }
  
        const pedido = carrinhoTable.rows().data().toArray().map(p=>({
            nome_produto : p.nome_produto,
            quantidade   : p.quantidade,
            valor_unitario : p.valor,
            valor_total    : (p.quantidade*p.valor).toFixed(2)
        }));
  
        $.post(FINALIZAR_URL,{
            csrfmiddlewaretoken: CSRF_TOKEN,
            pedido: JSON.stringify(pedido),
            tem_pedido_em_andamento:false
        })
        .done(()=>{ alert('Reserva enviada!'); carrinhoTable.clear().draw(); atualizarTotal(); })
        .fail(()=>{ alert('Erro ao enviar reserva.'); });
    });
  
  });
  