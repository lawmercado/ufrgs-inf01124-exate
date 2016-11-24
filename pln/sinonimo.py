# -*- coding: utf-8 -*-

# Xate: Extrator de assunto de Texto
#
# Author: Luís Augusto Weber Mercado <luiswebmercado@gmail.com>
#

"""
Módulo da unidade de processamento de linguagem natural (PLN) para obtenção de
sinônimos

"""

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

def obterSinonimos(token):
    token = unidecode(token)
    
    r = requests.get('http://www.sinonimos.com.br/' + token)
    
    soup = BeautifulSoup(r.text, "lxml")

    try:
        sinonimos = [a.text for a in soup.findAll(attrs = { 'class': 'sinonimo' })]
        
        return sinonimos
        
    except AttributeError:
        return []