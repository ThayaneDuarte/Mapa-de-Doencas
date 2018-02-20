# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import *


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput, label="Nome", max_length=50, min_length="3")
    cpf = forms.CharField(widget=forms.TextInput, label="CPF (Somente números)", max_length='11', min_length="11")
    email = forms.CharField(widget=forms.EmailInput, label="Email", max_length=50, min_length="6")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Senha", max_length=20, min_length="8")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmação da senha", max_length=20, min_length="8")

    class Meta:
        model = User
        fields = ['username', 'cpf', 'email', 'password1', 'password2']


Gravidade = [('leve', 'Leve'),
             ('moderada', 'Moderada'),
             ('grave', 'Grave')]


class DoencaForm(forms.ModelForm):
    doenca = forms.CharField(widget=forms.TextInput, label="Doença", min_length="3")
    codigo = forms.IntegerField(widget=forms.TextInput, label="Código")
    gravidade = forms.ChoiceField(label="Gravidade", choices=Gravidade)
    descricao = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'cols': 70, 'resize': 'none'}),
                                label="Descrição", max_length=500)
    sintomas = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'cols': 70, 'resize': 'none'}), label="Sintomas",
                               max_length=500)
    propagacao = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'cols': 70, 'resize': 'none'}),
                                 label="Propagação", max_length=500)

    class Meta:
        model = GerenciarDoenca
        fields = ['doenca', 'codigo', 'gravidade', 'descricao', 'sintomas', 'propagacao']


class MessageForm(forms.ModelForm):
    title = forms.CharField(label="Titulo", max_length=100)
    text = forms.CharField(label="Mensagem", max_length=1000, widget=forms.Textarea)

    class Meta:
        model = Message
        fields = ['title', 'text']


sim_nao = [(0, 'Não'), (1, 'Sim')]
normal_grande = [(0, 'Normal'), (1, 'Grande')]


class AcessibilidadeForm(forms.ModelForm):
    alto_contraste = forms.ChoiceField(label="Alto contraste", choices=sim_nao)
    tamanho_da_fonte = forms.ChoiceField(label="Tamanho da fonte", choices=normal_grande)
    baixo_risco = forms.ChoiceField(label="Doenças de baixo risco", choices=sim_nao)
    alta_gravidade = forms.ChoiceField(label="Doenças de alta gravidade", choices=sim_nao)

    class Meta:
        model = configAcessibilidade
        fields = ['alto_contraste', 'tamanho_da_fonte', 'baixo_risco', 'alta_gravidade']


Autarquia = [('global', 'Global'),
             ('federal', 'Federal'),
             ('estadual', 'Estadual'),
             ('destrital', 'Destrital'),
             ('municipal', 'Municipal')]


class OrgaoSaudeForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.TextInput, label="Órgão", max_length="50", min_length="3")
    cnpj = forms.CharField(widget=forms.TextInput, label="CNPJ (Somente números)", max_length="14", min_length="14")
    email = forms.EmailField(label="Email", max_length="50", min_length="6")
    sigla = forms.CharField(widget=forms.TextInput, label="Sigla", max_length="8", min_length="2")
    autarquia = forms.ChoiceField(label="Autarquia", choices=Autarquia)
    rua = forms.CharField(widget=forms.TextInput, label="Rua", max_length="50", min_length="3")
    numero = forms.IntegerField(widget=forms.TextInput, label="Número")
    complemento = forms.CharField(widget=forms.TextInput, label="Complemento", max_length="50")
    bairro = forms.CharField(widget=forms.TextInput, label="Bairro", max_length="50", min_length="3")
    cidade = forms.CharField(widget=forms.TextInput, label="Cidade", max_length="50", min_length="3")
    uf = forms.CharField(widget=forms.TextInput, label="UF", max_length="2", min_length="2")
    pais = forms.CharField(widget=forms.TextInput, label="País", max_length="50", min_length="3")
    cep = forms.IntegerField(widget=forms.TextInput, label="CEP")

    class Meta:
        model = OrgaosSaude
        fields = ['nome', 'cnpj', 'email', 'sigla', 'autarquia', 'rua', 'numero', 'complemento', 'bairro', 'cidade',
                  'uf', 'pais', 'cep']


class RelatarDoencaForm(forms.ModelForm):
    doenca = forms.ModelChoiceField(label="Doença", queryset=GerenciarDoenca.objects.all())
    descricao = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'cols': 70, 'resize': 'none'}),
                                label="Descrição", max_length="150", min_length="3")

    class Meta:
        model = RelatarDoenca
        fields = ['doenca', 'descricao']


class NovaDoencaForm(forms.ModelForm):
    doenca = forms.CharField(widget=forms.TextInput, label="Doença", min_length="3")
    gravidade = forms.ChoiceField(label="Gravidade", choices=Gravidade)
    descricao = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'cols': 70, 'resize': 'none'}),
                                label="Descrição", max_length=500)
    sintomas = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'cols': 70, 'resize': 'none'}), label="Sintomas",
                               max_length=500)
    propagacao = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'cols': 70, 'resize': 'none'}),
                                 label="Propagação", max_length=500)

    class Meta:
        model = SolicitarDoenca
        fields = ['doenca', 'gravidade', 'descricao', 'sintomas', 'propagacao']
