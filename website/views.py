#!/usr/bin/python
# -*- coding: UTF-8 -*-
# import navigator as navigator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import *
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
import smtplib
import collections


try:
    import simplejson as json
except:
    import json


# Create your views here.
def index(request):
    relatos = RelatarDoenca.objects.all()
    if request.user.is_staff:
        return render(request, 'website/index.html', {"name": '', "base": 'website/base_adm.html', "relatos": relatos})
    elif request.user.id is not None:
        return render(request, 'website/index.html',
                      {"name": request.user.first_name, "base": 'website/base.html', "relatos": relatos})
    else:
        return render(request, 'website/index.html',
                      {"name": '', "base": 'website/base_visitante.html', "relatos": relatos})


def login_user(request):
    relatos = RelatarDoenca.objects.all()
    if request.method == "POST":
        if 'desbloqueio' in request.POST:
            PedidosLogin.objects.create(user=User.objects.get(pk=request.POST['desbloqueio']))
            return render(request, 'website/login.html',
                          {'error_message': 'Aguarde o desbloqueio do administrador', "relatos": relatos})
        cpf = request.POST['cpf']
        password = request.POST['password']
        user = authenticate(username=cpf, password=password)

        if user is not None:
            declined_count = 0
            user_messages = Message.objects.all()
            for message in user_messages:
                if message.user_id == user.id and message.answer == 'Negado.':
                    declined_count += 1
                    if declined_count >= 5:
                        user.is_active = False
                        user.save()
            print("Doenças rejeitadas: " + str(declined_count))
            if user.is_active:
                login(request, user)
                if user.is_staff:
                    return render(request, 'website/index.html',
                                  {"name": '', "base": 'website/base_adm.html', "relatos": relatos})
                else:
                    return render(request, 'website/index.html',
                                  {"name": request.user.first_name, "base": 'website/base.html', "relatos": relatos})
            elif declined_count >= 5:
                return render(request, 'website/login.html', {
                    'error_message': 'Sua conta foi bloqueada, porque você teve muitas doenças cadastradas que foram '
                                     'reprovadas!',
                    'show_button': user.id, 'user': user, "relatos": relatos})
            elif not user.is_active:
                return render(request, 'website/login.html',
                              {'error_message': 'Sua conta foi bloqueada pelo administrador!', 'show_button': user.id,
                               'user': user, "relatos": relatos})

        else:
            return render(request, 'website/login.html', {'error_message': 'Login inválido', "relatos": relatos})
    return render(request, 'website/login.html', {"relatos": relatos})


def cadastrarusuario(request):
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    if request.user.is_authenticated():
        return render(request, 'website/index.html', {"name": request.user.first_name, "base": 'website/base.html'})
    elif request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['username']
            cpf = form.cleaned_data['cpf']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            cpf_exist = User.objects.filter(username=cpf)

            # check validity of cpf
            char_of_cpf = list(cpf)
            last = char_of_cpf.pop()
            penultimate = char_of_cpf.pop()
            weight = 10
            sum_ = 0
            cpf_is_valid = False

            # check penultimate digit
            for num in char_of_cpf:
                sum_ += int(num) * weight
                weight = weight - 1
            rest = 11 - (sum_ % 11)
            if rest > 9 and int(penultimate) == 0:
                cpf_is_valid = True
            elif rest == int(penultimate):
                cpf_is_valid = True

            # check last digit
            if cpf_is_valid:
                cpf_is_valid = False
                char_of_cpf.append(penultimate)
                sum_ = 0
                weight = 11
                for num in char_of_cpf:
                    sum_ += int(num) * weight
                    weight = weight - 1
                rest = 11 - (sum_ % 11)
                if rest > 9 and int(last) == 0:
                    cpf_is_valid = True
                elif rest == int(last):
                    cpf_is_valid = True

            if not cpf_is_valid:
                return render(request, 'website/cadastrarusuario.html',
                              {"form": form, "error_message": "O CPF digitado não é válido"})

            if cpf_exist:
                return render(request, 'website/cadastrarusuario.html',
                              {"form": form, "error_message": "O CPF digitado já está cadastrado no sistema"})

            if password1 != password2:
                return render(request, 'website/cadastrarusuario.html',
                              {"form": form, "error_message": "As senhas devem ser iguais"})
            else:
                user = User.objects.create_user(username=cpf, email=email, password=password1, first_name=name)
                user.save()

                # acessibilidade = configAcessibilidade()
                # acessibilidade.user = request.user
                # acessibilidade.save()

                user = authenticate(username=cpf, password=password1)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return render(request, 'website/index.html', {"name": request.user.first_name, "base":
                            'website/base.html'})
                else:
                    return render(request, 'website/cadastrarusuario.html', context)
        else:
            return render(request, 'website/cadastrarusuario.html', context)
    else:
        return render(request, 'website/cadastrarusuario.html', context)


def logout_user(request):
    relatos = RelatarDoenca.objects.all()
    logout(request)
    return render(request, 'website/index.html',
                  {"name": '', "base": 'website/base_visitante.html', "relatos": relatos})


def gerenciardoenca(request):
    form = DoencaForm(request.POST or None)

    context = {
        "form": form,
    }

    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=True)
            return render(request, 'website/index.html', {"name": '', "base": 'website/base_adm.html'})
        else:
            return render(request, 'website/gerenciardoenca.html', context)
    else:
        return render(request, 'website/gerenciardoenca.html', context)


def message(request):
    if not request.user.is_authenticated():
        return render(request, 'website/login.html')
    else:
        form = MessageForm(request.POST or None)
        context = {"form": form, }
        if form.is_valid():
            message = form.save(commit=False)
            message.title = form.cleaned_data['title']
            message.text = form.cleaned_data['text']
            message.user = request.user
            message.save()
            return render(request, 'website/message_sent.html', {'message': 'Mensagem enviada com sucesso!'})
        return render(request, 'website/message.html', context)


def ver_doencas(request):
    doencas_results = GerenciarDoenca.objects.all()
    query = request.GET.get("q")
    if doencas_results and query:
        doencas_results = doencas_results.filter(
            Q(doenca__icontains=query)
        ).distinct()
        return render(request, 'website/pesquisar.html', {"doencas": doencas_results})
    return render(request, 'website/pesquisar.html', {"doencas": None})


def adicionarOrgaosSaude(request):
    form = OrgaoSaudeForm(request.POST or None)
    context = {
        "form": form,
    }
    if request.user.is_authenticated() and request.user.is_staff:
        if request.method == 'POST' and form.is_valid():
            form.save(commit=True)
            all_orgaos = OrgaosSaude.objects.all()
            context = {
                'orgaos': all_orgaos,
                'all': True
            }
            return render(request, 'website/ver_orgao_saude.html', context)
        else:
            return render(request, 'website/gerenciar_orgao_saude.html', context)
    else:
        return render(request, 'website/login.html')


def excluirOrgaoSaude(request, orgao_id):
    if not request.user.is_authenticated():
        return render(request, 'website/login.html')
    else:
        orgao = get_object_or_404(OrgaosSaude, pk=orgao_id)
        orgao.delete()
        all_orgaos = OrgaosSaude.objects.all()
        context = {
            'orgaos': all_orgaos,
            'all': True
        }
        return render(request, 'website/ver_orgao_saude.html', context)


def editarOrgaoSaude(request, orgao_id):
    orgao = get_object_or_404(OrgaosSaude, pk=orgao_id)

    form = OrgaoSaudeForm(request.POST or None, instance=orgao)

    context = {
        "form": form,
    }
    if request.user.is_authenticated() and request.user.is_staff:
        if request.method == 'POST' and form.is_valid():
            form.save(commit=True)
            all_orgaos = OrgaosSaude.objects.all()
            context = {
                'orgaos': all_orgaos,
                'all': True
            }
            return render(request, 'website/ver_orgao_saude.html', context)
        else:
            return render(request, 'website/gerenciar_orgao_saude.html', context)
    else:
        return render(request, 'website/login.html')


def gerenciarOrgaosSaude(request):
    if not request.user.is_authenticated():
        return render(request, 'website/login.html')
    else:
        query = request.GET.get("q")
        if query:
            shearched_orgao = OrgaosSaude.objects.filter(
                Q(nome__icontains=query) | Q(sigla__icontains=query)).distinct()
            context = {
                'orgaos': shearched_orgao,
                'all': False
            }
        else:
            all_orgaos = OrgaosSaude.objects.all()
            context = {
                'orgaos': all_orgaos,
                'all': True
            }
        return render(request, 'website/ver_orgao_saude.html', context)


def notifications(request):
    if not request.user.is_authenticated():
        return render(request, 'website/login.html')
    else:
        messages = Message.objects.filter(user=request.user)
        messages = messages.filter(from_adm=True)

        relatos = RelatarDoenca.objects.all()
        configAcessib = configAcessibilidade.objects.get(user=request.user)
        leve = configAcessib.baixo_risco
        grave = configAcessib.alta_gravidade

        doencas = []
        for relato in relatos:
            jaExiste = False
            aux = GerenciarDoenca.objects.get(doenca=relato.doenca.doenca)
            if (leve == 1 and aux.gravidade == 'leve') or (grave == 1 and aux.gravidade == 'grave') or \
                    (aux.gravidade == 'moderada'):
                for doenca in doencas:
                    if doenca.doenca == aux.doenca:
                        jaExiste = True
                        break
                if not jaExiste:
                    doencas.append(aux)

        context = {
            'messages': messages,
            'doencas': doencas
        }
        return render(request, 'website/notifications.html', context)


def excluirNotificacao(request, message_id):
    if not request.user.is_authenticated():
        return render(request, 'website/login.html')
    else:
        message = get_object_or_404(Message, pk=message_id)
        message.delete()
        messages = Message.objects.filter(user=request.user)
        messages = messages.filter(from_adm=True)
        context = {
            'messages': messages,
        }
        return render(request, 'website/notifications.html', context)


def soliticacoes_doenca(request):
    solicitacoes_list = SolicitarDoenca.objects.all()
    if request.method == 'POST':
        for solicitacao in solicitacoes_list:
            if request.POST.get(str(solicitacao.codigo) + "Rmv", -1) != -1:
                msg = Message.objects.create(title="Resposta à solicitação",
                                             text="Solicitação de cadastro da doença " + solicitacao.doenca,
                                             user=solicitacao.user, from_adm=True)

                solicitacao.delete()
                msg.answer = "Negado."
                msg.save()
            if request.POST.get(str(solicitacao.codigo) + "Add", -1) != -1:
                msg = Message.objects.create(title="Resposta à solicitação",
                                             text="Solicitação de cadastro da doença " + solicitacao.doenca,
                                             user=solicitacao.user, from_adm=True)

                msg.answer = "Aceito."
                if not GerenciarDoenca.objects.all():
                    codigo = 1
                else:
                    codigo = GerenciarDoenca.objects.last().codigo + 1
                GerenciarDoenca.objects.create(codigo=codigo,
                                               doenca=solicitacao.doenca,
                                               gravidade=solicitacao.gravidade,
                                               descricao=solicitacao.descricao,
                                               sintomas=solicitacao.sintomas,
                                               propagacao=solicitacao.propagacao)
                solicitacao.delete()
                msg.save()

    solicitacoes_list = SolicitarDoenca.objects.all()
    if not solicitacoes_list:
        vazio = True
    else:
        vazio = False

    page = request.GET.get('page', 1)
    paginator = Paginator(solicitacoes_list, 10)
    try:
        solicitacoes = paginator.page(page)
    except PageNotAnInteger:
        solicitacoes = paginator.page(1)
    except EmptyPage:
        solicitacoes = paginator.page(paginator.num_pages)
    if request.user.is_authenticated():
        return render(request, 'website/soliticacoes_doenca.html', {'solicitacoes': solicitacoes, 'vazio': vazio})
    else:
        return render(request, 'website/login.html')


def solicitarDoenca(request):
    if not request.user.is_authenticated():
        return render(request, 'website/login.html')
    else:
        form = NovaDoencaForm(request.POST or None)
        context = {
            "form": form,
        }
        if request.method == 'POST' and form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.user = request.user
            if not SolicitarDoenca.objects.all():
                codigo = 1
            else:
                codigo = SolicitarDoenca.objects.last().codigo + 1
            solicitacao.codigo = codigo
            solicitacao.save()
            return render(request, 'website/message_sent.html', {'message': 'Nova doença enviada para avaliação!'})
        else:
            return render(request, 'website/solicitarDoenca.html', context)


def RelatarDoencas(request):
    if not request.user.is_authenticated():
        return render(request, 'website/login.html')
    else:
        form = RelatarDoencaForm(request.POST or None)
        context = {
            "form": form,
        }
        if request.method == 'POST' and form.is_valid():
            relato = form.save(commit=False)
            relato.user = request.user

            relato.data = datetime.now()

            latLon = str(request.POST['botao']).split()

            if len(latLon) == 2:
                relato.latitude = latLon[0]
                relato.longitude = latLon[1]
            else:
                relato.latitude = 0
                relato.longitude = 0
            relato.save()

            geolocator = Nominatim()
            localizacaoRelato = geolocator.reverse(relato.latitude + ', ' + relato.longitude)
            address = localizacaoRelato.address.split(', ')
            for orgao in OrgaosSaude.objects.all():
                if orgao.autarquia == "federal":
                    if address[8] == orgao.pais:
                        flag, txAumento = verificaAumento(relato)
                        if flag:
                            enviaEmail(txAumento, orgao, relato)
                if orgao.autarquia == "estadual":
                    if address[6] == orgao.uf:
                        flag, txAumento = verificaAumento(relato)
                        if flag:
                            enviaEmail(txAumento, orgao, relato)
                if orgao.autarquia == "municipal" or orgao.autarquia == 'distrital':
                    if address[2] == orgao.cidade:
                        flag, txAumento = verificaAumento(relato)
                        if flag:
                            enviaEmail(txAumento, orgao, relato)
            return index(request)
        else:
            return render(request, 'website/relatarDoencas.html', context)


def enviaEmail(txAumento, orgao, relato):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login("mapadedoenca@gmail.com", "qazxsw12")
    msg = "\r\n".join([
        "From: mapadedoenca@gmail.com",
        "To: " + orgao.email,
        "Subject: Alerta de crescimento " + relato.doenca.doenca,
        "",
        "Prezados membros da " + orgao.sigla + ",\n\n" +
        "Comunicamos que a taxa de crescimento de ocorrências de " + relato.doenca.doenca + ", em relação ao último mês, é de " +
        str(txAumento * 100) + "%.\n\nAt.te \n\nEquipe Mapa de Doenas."
    ])

    server.sendmail("mapadedoenca@gmail.com", orgao.email, msg.encode('utf-8'))


def verificaAumento(relato):
    contLastMonth = 0
    contThisMonth = 0
    today = datetime.now()
    first = today.replace(day=1)
    lastMonth = first - timedelta(days=1)
    for relatoDoenca in RelatarDoenca.objects.all():
        if relatoDoenca.doenca.codigo == relato.doenca.codigo:
            if relatoDoenca.data.strftime("%Y%m") == lastMonth.strftime("%Y%m"):
                contLastMonth += 1
            elif relatoDoenca.data.strftime("%Y%m") == today.strftime("%Y%m"):
                contThisMonth += 1
    if contThisMonth >= 10 and contThisMonth / contLastMonth - 1 > 0.1:
        return True, contThisMonth / contLastMonth - 1
    else:
        return False, 0


def acessibilidade(request):
    if not request.user.is_authenticated():
        return render(request, 'website/login.html')
    else:
        instance = get_object_or_404(configAcessibilidade, user_id=request.user.id)
        form = AcessibilidadeForm(request.POST or None, instance=instance)
        if request.method == 'POST' and form.is_valid():
            acessibilidade = form.save(commit=False)
            acessibilidade.user = request.user
            acessibilidade.save()

        return render(request, 'website/acessibilidade.html', {'form': form})


def pedidos_login(request):
    solicitacoes_list = PedidosLogin.objects.all()
    for solicitacao in solicitacoes_list:
        inactive_user = User.objects.get(username=solicitacao.user)
        choosen_one = User.objects.get(username=inactive_user)
        messages_of_choosen_one = Message.objects.filter(user_id=choosen_one.id)
        messages_count = Message.objects.filter(user_id=choosen_one.id).count()
        if 'rmvPedidosLogin' in request.POST:
            if messages_count >= 5:
                messages_of_choosen_one.delete()

            inactive_user.is_active = True
            inactive_user.save()
            PedidosLogin.objects.filter(user=solicitacao.user).delete()

    if not solicitacoes_list:
        vazio = True
    else:
        vazio = False

    page = request.GET.get('page', 1)
    paginator = Paginator(solicitacoes_list, 10)
    try:
        solicitacoes = paginator.page(page)
    except PageNotAnInteger:
        solicitacoes = paginator.page(1)
    except EmptyPage:
        solicitacoes = paginator.page(paginator.num_pages)
    if request.user.is_authenticated():
        pedidos = [
            {'nome': p.user.first_name, 'sobrenome': p.user.last_name, 'cpf': p.user.username, 'email': p.user.email}
            for p in PedidosLogin.objects.all()]
        return render(request, 'website/pedidos_login.html',
                      {'solicitacoes': solicitacoes_list, 'vazio': vazio, 'pedidos': pedidos})
    else:
        return render(request, 'website/login.html')


def estatisticas(request):
    if not request.user.is_authenticated():
        return render(request, 'website/login.html')
    else:
        estat = {}
        numDoencas = GerenciarDoenca.objects.all().count()
        estat['Quantidade de doenças cadastradas no sistema'] = numDoencas
        relatos = RelatarDoenca.objects.all()
        estat['Quantidade de doenças relatadas no sistema'] = relatos.count()
        qtdRelatos = collections.OrderedDict()
        taxaRelatos = collections.OrderedDict()
        for relato in relatos:
            if relato.doenca.doenca in qtdRelatos.keys():
                qtdRelatos[relato.doenca.doenca] = qtdRelatos[relato.doenca.doenca] + 1
            else:
                qtdRelatos[relato.doenca.doenca] = 1
                flag, txAumento = verificaAumento(relato)
                taxaRelatos[relato.doenca.doenca] = txAumento

        return render(request, 'website/estatistica.html',
                      {'estatisticas': estat, 'qtdRelatos': qtdRelatos, 'taxaRelatos': taxaRelatos})
