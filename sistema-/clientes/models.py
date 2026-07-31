from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


class Cliente(models.Model):
    nome = models.CharField(max_length=100)

    cpf = models.CharField(
        max_length=14,
        unique=True,
        blank=True,
        null=True
    )

    telefone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    localizacao = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    status = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


# 🏢 FORNECEDOR
class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)

    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome




# 📦 PRODUTO
class Produto(models.Model):
    nome = models.CharField(max_length=100)

   
    quantidade = models.DecimalField(
    max_digits=10,
    decimal_places=3,
    default=0
    )

    fornecedor = models.CharField(
        max_length=100,
        default='Não informado',
        blank=True,
        null=True
    )
    fornecedor_cadastro = models.ForeignKey(
        Fornecedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produtos'
    )

    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    estoque_minimo = models.DecimalField(
    max_digits=10,
    decimal_places=3,
    default=5
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    data_ultima_compra = models.DateTimeField(null=True, blank=True)

    def lucro_unitario(self):
        return self.preco_venda - self.preco_custo

    def margem_lucro(self):
        if self.preco_custo > 0:
            return ((self.preco_venda - self.preco_custo) / self.preco_custo) * 100
        return 0

    def valor_custo_estoque(self):
        return self.quantidade * self.preco_custo

    def valor_venda_estoque(self):
        return self.quantidade * self.preco_venda

    def lucro_previsto_estoque(self):
        return self.valor_venda_estoque() - self.valor_custo_estoque()

    def status_estoque(self):
        if self.quantidade <= 0:
            return "Sem estoque"
        elif self.quantidade <= self.estoque_minimo:
            return "Estoque baixo"
        return "Estoque normal"

    @property
    def fornecedor_formatado(self):
        if self.fornecedor_cadastro:
            return self.fornecedor_cadastro.nome

        if not self.fornecedor:
            return 'Não informado'

        valor = str(self.fornecedor).strip().lower()

        if valor in ['none', 'null', '']:
            return 'Não informado'

        return self.fornecedor

    def __str__(self):
        return self.nome

# 🧾 VENDA
class Venda(models.Model):
    STATUS_CHOICES = (
        ('ativa', 'Ativa'),
        ('cancelada', 'Cancelada'),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True, db_index=True)

    total = models.DecimalField(max_digits=10, decimal_places=2)
    total_com_juros = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    parcelado = models.BooleanField(default=False)
    quantidade_parcelas = models.IntegerField(default=1)
    juros_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=0)


    FORMA_PAGAMENTO_CHOICES = (
    ('dinheiro', 'Dinheiro'),
    ('pix', 'Pix'),
    ('cartao', 'Cartão'),
    ('fiado', 'Fiado'),
)

    forma_pagamento = models.CharField(
    max_length=20,
    choices=FORMA_PAGAMENTO_CHOICES,
    blank=True,
    null=True
)


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ativa'
    )

    def __str__(self):
        return f"Venda {self.id} - {self.cliente.nome}"
    
# 🧾 NOTA FISCAL
class NotaFiscal(models.Model):
    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    )

    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('emitida', 'Emitida'),
        ('cancelada', 'Cancelada'),
    )

    numero = models.CharField(max_length=50)
    chave_acesso = models.CharField(max_length=100, blank=True, null=True)

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='saida')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    venda = models.ForeignKey(
        Venda,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    observacao = models.TextField(blank=True, null=True)
    data_emissao = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"NF {self.numero} - {self.get_status_display()}"


# 📦 ITEM DA VENDA
class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    quantidade = models.DecimalField(
    max_digits=10,
    decimal_places=3
    )
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lucro = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.produto.nome


# 📆 PARCELAS DA VENDA
class ParcelaVenda(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('paga', 'Paga'),
        ('atrasada', 'Atrasada'),
    )

    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    numero = models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    vencimento = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pendente'
    )

    data_pagamento = models.DateField(null=True, blank=True)
    baixado = models.BooleanField(default=False)

    def atualizar_status(self):
        if self.status == 'pendente' and self.vencimento < date.today():
            self.status = 'atrasada'
            self.save()

    class Meta:
        unique_together = ('venda', 'numero')
        ordering = ['vencimento']

    def __str__(self):
        return f"Parcela {self.numero} - Venda {self.venda.id}"


# 📥 COMPRA
# 📥 COMPRA
class Compra(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    fornecedor = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    fornecedor_cadastro = models.ForeignKey(
        Fornecedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='compras'
    )

    quantidade = models.DecimalField(
    max_digits=10,
    decimal_places=3
    )
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    data = models.DateTimeField(auto_now_add=True, db_index=True)

    def total_compra(self):
        return self.quantidade * self.preco

    def __str__(self):
        return self.produto.nome

# 💸 DESPESA
class Despesa(models.Model):
    CATEGORIA_CHOICES = (
        ('fixa', 'Fixa'),
        ('variavel', 'Variável'),
    )

    nome = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    data = models.DateField(auto_now_add=True)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


# 💰 FINANCEIRO
class Financeiro(models.Model):
    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    )

    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    data = models.DateField(auto_now_add=True, db_index=True)

    venda = models.ForeignKey(
        Venda,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    compra = models.ForeignKey(
        Compra,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    parcela = models.ForeignKey(
        ParcelaVenda,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    despesa = models.ForeignKey(
        Despesa,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def clean(self):
        vinculos = [self.venda, self.compra, self.parcela, self.despesa]
        preenchidos = sum(1 for item in vinculos if item is not None)

        if preenchidos > 1:
            raise ValidationError(
                "O financeiro só pode estar vinculado a uma origem: venda, compra, parcela ou despesa."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.descricao


# 📩 MENSAGEM
class Mensagem(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    mensagem = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

# 🤝 VENDA FIADO
class VendaFiado(models.Model):
    STATUS_CHOICES = (
        ('aberta', 'Aberta'),
        ('quitada', 'Quitada'),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, null=True, blank=True)

    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aberta'
    )

    data = models.DateField(auto_now_add=True)
    observacao = models.TextField(blank=True, null=True)

    def saldo_devedor(self):
        return self.valor_total - self.valor_pago

    def __str__(self):
        return f"{self.cliente.nome} - R$ {self.saldo_devedor()}"


class PagamentoFiado(models.Model):
    venda_fiado = models.ForeignKey(
        VendaFiado,
        on_delete=models.CASCADE,
        related_name='pagamentos'
    )

    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(auto_now_add=True)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pagamento R$ {self.valor} - {self.venda_fiado.cliente.nome}"
    
# 💰 CAIXA PDV
class CaixaPDV(models.Model):
    STATUS_CHOICES = (
        ('aberto', 'Aberto'),
        ('fechado', 'Fechado'),
    )

    usuario = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    data_abertura = models.DateTimeField(auto_now_add=True)
    data_fechamento = models.DateTimeField(null=True, blank=True)

    valor_abertura = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_fechamento = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aberto'
    )

    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Caixa {self.id} - {self.status}"