# -*- coding: utf-8 -*-

# Xate: Extrator de assunto de Texto
#
# Author: Luís Augusto Weber Mercado <luiswebmercado@gmail.com>
#

"""
Módulo principal da unidade de processamento de linguagem natural (PLN)

"""

import nltk
import pln.tagger
import pln.sinonimo

POS_TAG_SUBSTANTIVO = 'n'
MAPA_PLURAL_SINGULAR = [('ãos', 'ão'), ('ões', 'ão'), ('ães', 'ão'), ('is', 'l'), ('ns', 'm'), ('s', ''), ('es', '')]

def obterTokens(texto):
    """
    A partir de um texto, dá início a pipeline de análise

    :param texto: Texto a ser analisado
    :type texto: string
    """
    
    # Tokeniza o texto informado
    tokens = nltk.word_tokenize(texto)
    tokens = [token.lower() for token in tokens]
    
    return tokens

def stem(token):
    """
    Simplifica o token da maneira mais atômica possível
    
    :param token: Token a ser simplificado
    :type token: string
    """    
    
    for plural, singular in MAPA_PLURAL_SINGULAR:
        if token.endswith(plural):
            token = token.replace(plural, singular)
            break
        
    return token

def pos(tokens):
    """
    Utilizando o tagger disponível, faz o Part-of-speech (POS) tagging
    
    :param tokens: Lista de tokens a serem classificados
    :type tokens: list
    
    :return: Lista de tupla com os tokens juntamente com sua respectiva POS tag
    :rtype: list
    """    
    
    return pln.tagger.pos(tokens)
    
def obterSubstantivos(tokens):
    """
    Extrai os substantivos de uma lista de tokens, baseada na sua POS tagging
    
    :param tokens: Lista dos tokens a serem filtradas
    :type tokens: list
    
    :return: Lista com os substantivos
    :rtype: list
    """    
    
    tagged = pos(tokens)    
    
    stopwords = nltk.corpus.stopwords.words('portuguese')
    
    ocorrencias = [token[0] for token in tagged if token[1] == POS_TAG_SUBSTANTIVO and token[0] not in stopwords]

    return ocorrencias
    
def obterSinonimos(token):
    return pln.sinonimo.obterSinonimos(token)
    
def obterSinonimosNaLista(tokens):
    """
    """
    blacklist = []
    relacoes = []
    
    for token in tokens:
        if token not in blacklist:
            relacao = (token, [])
            blacklist.append(token)
            
            sinonimos = obterSinonimos(token)            
            
            print(sinonimos)            
            
            for sinonimo in sinonimos:
                if sinonimo in tokens and sinonimo not in blacklist:
                    relacao[1].append(sinonimo)
                    blacklist.append(sinonimo) # Para que não seja considerado novamente
                                
            relacoes.append(relacao)
                    
    return relacoes    