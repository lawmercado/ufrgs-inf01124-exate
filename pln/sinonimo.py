# -*- coding: utf-8 -*-

# Exate: Extrator de assunto de Texto
#
# Author: Luís Augusto Weber Mercado <luiswebmercado@gmail.com>
#

"""
Módulo da unidade de processamento de linguagem natural (PLN) para obtenção de
sinônimos

Utiliza como referência o site http://www.sinonimos.com.br/
"""

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

def obterSinonimos(token):
    """
    Obtém a lista de  sinônimos de um dado token

    :param token: Token a ter seus sinônimos obtidos
    :type tokens: string

    :return: Lista com os sinônimos
    :rtype: list
    """

    token = unidecode(token)

    r = requests.get('https://www.dicio.com.br/' + token)

    soup = BeautifulSoup(r.text, "html.parser")
    
    sinonimos = []    
    
    try:
                
        p = soup.find('p', attrs = { 'class': 'adicional sinonimos' })
        
        for a in p.findAll('a'):
            sinonimos.append(a.text)

        return sinonimos

    except AttributeError:
        return []