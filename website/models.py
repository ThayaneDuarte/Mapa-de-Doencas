# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class GerenciarDoenca(models.Model):
    doenca     = models.CharField(max_length = 100)
    codigo     = models.IntegerField(primary_key=True)
    gravidade  = models.CharField(max_length = 250)
    descricao  = models.CharField(max_length = 250)
    sintomas   = models.CharField(max_length = 250)
    propagacao = models.CharField(max_length = 250)
    def __str__(self):
        return self.doenca

class Message(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000, null=True)
    # time = models.DateTimeField('Date published')
    user = models.ForeignKey(User, null=True)
    from_adm = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class OrgaosSaude(models.Model):
    nome = models.CharField(max_length = 50)
    cnpj = models.IntegerField(unique=True)
    email = models.CharField(max_length = 50)
    autarquia = models.CharField(max_length = 15)
    sigla = models.CharField(max_length = 8)
    rua = models.CharField(max_length = 50)
    numero = models.IntegerField()
    complemento = models.CharField(max_length = 20)
    bairro = models.CharField(max_length = 50)
    cidade = models.CharField(max_length = 50)
    uf = models.CharField(max_length = 2)
    pais = models.CharField(max_length = 50)
    cep = models.IntegerField()
    def __str__(self):
        return self.nome

class SolicitarDoenca(models.Model):
    user = models.ForeignKey(User, null=False)
    doenca     = models.CharField(max_length = 100)
    codigo     = models.IntegerField()
    gravidade  = models.CharField(max_length = 250)
    descricao  = models.CharField(max_length = 250)
    sintomas   = models.CharField(max_length = 250)
    propagacao = models.CharField(max_length = 250)
    def __str__(self):
        return self.doenca

class RelatarDoenca(models.Model):
    user = models.ForeignKey(User, null=False)
    doenca = models.ForeignKey(GerenciarDoenca, null=False)
    descricao = models.CharField(max_length=150)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    data = models.DateField(null=False)
    def __str__(self):
         return self.doenca.doenca + " - " + self.user.username + " - " + str(self.data)

class configAcessibilidade(models.Model):
    user = models.ForeignKey(User, null=True)
    alto_contraste = models.IntegerField(default=0)
    tamanho_da_fonte = models.IntegerField(default=0)
    baixo_risco = models.IntegerField(default=1)
    alta_gravidade = models.IntegerField(default=1)


class PedidosLogin(models.Model):
    user = models.ForeignKey(User)
    def __str__(self):
        return "O usuário {} requisitou ativação".format(self.user.username)
