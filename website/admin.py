# -*- coding: utf-8 -*-
# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(Message)
admin.site.register(GerenciarDoenca)
admin.site.register(OrgaosSaude)
admin.site.register(RelatarDoenca)
admin.site.register(SolicitarDoenca)
admin.site.register(configAcessibilidade)
admin.site.register(PedidosLogin)
