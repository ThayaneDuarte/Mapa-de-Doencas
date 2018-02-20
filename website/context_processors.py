from django.conf import settings
from .models import configAcessibilidade
from django.shortcuts import get_object_or_404

def acessibilidadeProc(request):
    if request.user.id is None:
        return { 'visitante': True }
    elif request.user.is_authenticated():
        try:
            instance = configAcessibilidade.objects.get(user_id=request.user.id)
            return { 'tamanho_da_fonte': instance.tamanho_da_fonte, 'alto_contraste': instance.alto_contraste }
        except:
            configAcessibilidade.objects.create(user=request.user)
            return {'tamanho_da_fonte': 0, 'alto_contraste':0}
    return {}
