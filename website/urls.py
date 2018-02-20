# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'website'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cadastrarusuario/$', views.cadastrarusuario, name='cadastrarusuario'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^gerenciardoenca/$', views.gerenciardoenca, name='gerenciardoenca'),
    url(r'^adicionarOrgaosSaude/$', views.adicionarOrgaosSaude, name='adicionarOrgaosSaude'),
    url(r'^gerenciarOrgaosSaude/$', views.gerenciarOrgaosSaude, name='gerenciarOrgaosSaude'),
    url(r'^editarOrgaoSaude/(?P<orgao_id>[0-9]+)/$', views.editarOrgaoSaude, name='editarOrgaoSaude'),
    url(r'^excluirOrgaoSaude/(?P<orgao_id>[0-9]+)/$', views.excluirOrgaoSaude, name='excluirOrgaoSaude'),
    url(r'^message/$', views.message, name='message'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^pesquisar/$', views.ver_doencas, name='pesquisar'),
    url(r'^notificacao/$', views.notifications, name='notifications'),
    url(r'^relatar/$', views.RelatarDoencas, name='relatarDoencas'),
    url(r'^soliticacoes_doenca/$', views.soliticacoes_doenca, name='soliticacoes_doenca'),
    url(r'^excluirNotificacao/(?P<message_id>[0-9]+)/$', views.excluirNotificacao, name='excluirNotificacao'),
    url(r'^solicitarDoenca/$', views.solicitarDoenca, name='solicitarDoenca'),
    url(r'^acessibilidade/$', views.acessibilidade, name='acessibilidade'),
    url(r'^pedidos_login/$', views.pedidos_login, name='pedidos_login'),
    url(r'^estatisticas/$', views.estatisticas, name='estatisticas'),
    #url(r'^edit/(?P<pk>\d+)$', views.ServerUpdate.as_view(), name='server_edit'),
]
