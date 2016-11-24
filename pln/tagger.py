# -*- coding: utf-8 -*-

# Xate: Extrator de assunto de Texto
#
# Author: Luís Augusto Weber Mercado <luiswebmercado@gmail.com>
#

"""
Módulo da unidade de processamento de linguagem natural (PLN) para treinamento
e obtenção de um POS tagger

"""

import nltk
from pickle import dump, load

_tagger = None
CAMINHO_DUMP = 'dump_tagger.pkl'

def simplificarTag(t):
    tag = t.lower()

    if "+" in tag:
        tag = tag[tag.index("+") + 1:]
        
    if tag.startswith("v"):
        tag = "v"
    elif tag.startswith("pro"):
        tag = "pro"
    elif tag.startswith("prep"):
        tag = "prp"
    elif tag.startswith("c") or tag.startswith("k"):
        tag = "c"
    elif tag.startswith("pden"):
        tag = "adv"
    
    return tag

def pos(tokens):
    global _tagger
    
    if _tagger is None:
        input = open(CAMINHO_DUMP, 'rb')
        _tagger = load(input)
        input.close()
        
    return _tagger.tag(tokens)
    
if __name__ == '__main__':
    print('Gerando dados para treino...')
    data = []
    
    sentencas_floresta = nltk.corpus.floresta.tagged_sents()
    data += [[(w.lower(), simplificarTag(t)) for (w, t) in sentenca] for sentenca in sentencas_floresta if sentenca]
    
    sentencas_mac_morpho = nltk.corpus.mac_morpho.tagged_sents()
    data += [[(w.lower(), simplificarTag(t)) for (w, t) in sentenca] for sentenca in sentencas_mac_morpho if sentenca]
    
    base = data
    teste = data
    
    print('Treinando tagger. Isso pode demorar...')
    _tagger = nltk.NgramTagger(4, base, backoff=nltk.TrigramTagger(base, backoff=nltk.BigramTagger(base, backoff=nltk.UnigramTagger(base, backoff=nltk.DefaultTagger('n')))))
    
    
    print('Tagger treinado com sucesso! Precisão de %.1f!' % (_tagger.evaluate(teste) * 100))
    
    try:
        print('Salvando tagger...')
        
        output = open(CAMINHO_DUMP, 'wb')
        dump(_tagger, output, -1)
        output.close()
        
        print('Tagger salvo em "dump_tagger.pkl"!')
        
    except:
        print('ERRO: Não foi possível salvar o tagger.')