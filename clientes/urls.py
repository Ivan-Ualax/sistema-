from django.urls import path
from . import views

urlpatterns = [
    #Login
    path('login/', views.login_usuario),
    path('logout/', views.logout_usuario),  
    
    #  HOME
    path('', views.home),

    #  CLIENTES
    path('clientes/', views.lista_clientes),
    path('clientes/add/', views.cadastrar),
    path('clientes/editar/<int:id>/', views.editar_cliente),
    path('clientes/deletar/<int:id>/', views.deletar_cliente),

    #  FINANCEIRO
    path('financeiro/', views.financeiro),
    path('financeiro/editar/<int:id>/', views.editar_financeiro),
    path('financeiro/deletar/<int:id>/', views.deletar_financeiro),
    path('relatorio/financeiro/excel/', views.relatorio_financeiro_excel),

    #  ESTOQUE
    path('estoque/', views.estoque),
    path('estoque/add/', views.adicionar_produto),
    path('estoque/editar/<int:id>/', views.editar_produto),
    path('estoque/deletar/<int:id>/', views.deletar_produto),

    #  VENDAS
    path('vendas/', views.vendas),
    path('vendas/nova/', views.criar_venda),
    path('vendas/deletar/<int:id>/', views.deletar_venda),

    #  COMPRAS
    path('compras/', views.compras),
    path('compras/add/', views.adicionar_compra),
    path('compras/editar/<int:id>/', views.editar_compra),
    path('compras/deletar/<int:id>/', views.deletar_compra),

    #  PARCELAS
    path('parcelas/', views.lista_parcelas),
    path('parcelas/venda/<int:id>/', views.detalhe_parcelas),
    path('parcelas/pagar/<int:id>/', views.marcar_pago),
    path('parcelas/baixar/<int:id>/', views.baixar_parcela),
    path('parcelas/editar/<int:id>/', views.editar_parcela),
    path('parcelas/imprimir/<int:id>/', views.imprimir_parcela),
    path('parcelas/venda/deletar/<int:id>/', views.deletar_venda_parcelada),

    #  INADIMPLÊNCIA
    path('inadimplencia/', views.inadimplencia),

    #  CONTATO
    path('enviar-mensagem/', views.enviar_mensagem),

    #  RELATÓRIO
    path('relatorio/', views.relatorio_lucro),

    #  DESPESAS
    path('despesas/', views.despesas),
    path('despesas/add/', views.adicionar_despesa),
    path('despesas/deletar/<int:id>/', views.deletar_despesa),
    #  PDFs
    path('relatorio/vendas/pdf/', views.relatorio_vendas_pdf),
    path('relatorio/financeiro/pdf/', views.relatorio_financeiro_pdf),
    path('relatorio/inadimplencia/pdf/', views.relatorio_inadimplencia_pdf),

    #  FORNECEDORES
    path('fornecedores/', views.fornecedores),
    path('fornecedores/add/', views.adicionar_fornecedor),
    path('fornecedores/editar/<int:id>/', views.editar_fornecedor),
    path('fornecedores/deletar/<int:id>/', views.deletar_fornecedor),

    #  NOTAS FISCAIS
    path('notas-fiscais/', views.notas_fiscais),
    path('notas-fiscais/add/', views.adicionar_nota_fiscal),
    path('notas-fiscais/deletar/<int:id>/', views.deletar_nota_fiscal),


    # VENDA FIADO
    path('venda-fiado/', views.vendas_fiado),
    path('venda-fiado/nova/', views.criar_venda_fiado),
    path('venda-fiado/<int:id>/', views.detalhe_venda_fiado),
    path('venda-fiado/abater/<int:id>/', views.abater_venda_fiado),
    path('venda-fiado/excluir/<int:id>/', views.excluir_venda_fiado),


    # PDV
    path('pdv/', views.pdv),
    path('pdv/vendas/', views.pdv_vendas),
    path('pdv/abrir-caixa/', views.abrir_caixa),
    path('pdv/fechar-caixa/', views.fechar_caixa),


    path(
    'pdv/pdf-caixa/',
    views.pdf_caixa,
    name='pdf_caixa'
    ),
     ]