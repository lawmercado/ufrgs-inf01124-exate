# -*- coding: utf-8 -*-

# Xate: Extrator de assunto de Texto
#
# Author: Luís Augusto Weber Mercado <luiswebmercado@gmail.com>
#

"""
Arquivo principal da aplicação Xate

Pode ser carregado como um módulo, se apenas a funcionalidade principal for
desejada. Para executar a aplicação, juntamente com a sua GUI, basta executar o
script.
"""

import pln.core as pln

def extrairAssunto(texto):
    """
    Dado um texto, obtém qual o assunto do mesmo
    
    :param texto: Texto a ser analisado
    :type texto: string
    """    
    
    tokens = pln.obterTokens(texto)
    palavras = [token.lower() for token in tokens if token.isalnum()] # Remove a pontuação
    
    substantivos = [pln.stem(item) for item in pln.obterSubstantivos(palavras)] 
    
    substantivosUnificados = list(set(substantivos))
    
    contagem = []
    
    # Realiza a contagem dos substantivos
    for substantivo in substantivosUnificados:
        ocorrencias = substantivos.count(substantivo)
        
        contagem.append((substantivo, ocorrencias))
    
    # Ordena a contagem em ordem decrescente
    contagem.sort(key = lambda item: item[1], reverse = True)
    
    relacoes = pln.obterSinonimosNaLista([substantivo for substantivo, cont in contagem])
    
    contagem = []
    
    for substantivo, sinonimos in relacoes:
        ocorrencias = 0
        
        ocorrencias += substantivos.count(substantivo)
        
        for sinonimo in sinonimos:
            ocorrencias += substantivos.count(sinonimo)
            
        contagem.append((substantivo, ocorrencias))
    
    contagem.sort(key = lambda item: item[1], reverse = True)
    
    # Pega o primeiro item, ou seja, o mais provável assunto do texto!
    assunto = contagem[0][0]
    
    return assunto

if __name__ == '__main__':
    from tkinter import *
    
    class Xate(object):
        def __init__(self, master = None):
            master.title('Xate: Extrator de assunto de textos')
    
            self.primeiroContainer = Frame(master)
            self.primeiroContainer['padx'] = 5
            self.primeiroContainer.pack()
    
            self.segundoContainer = Frame(master)
            self.segundoContainer.pack()
    
            self.label = Label(self.primeiroContainer, text = 'Informe um texto')
            self.label['font'] = ('Cantarell', '10', 'bold')
            self.label.pack(pady = 10)
    
            self.texto = Text(self.primeiroContainer, height = 15, width = 80)
            self.texto['font'] = ('Cantarell', '10')
            self.texto.pack(side = LEFT, fill = Y)
    
            self.scrollbar = Scrollbar(self.primeiroContainer)
            self.scrollbar.pack(side = RIGHT, fill = Y)
            self.scrollbar.config(command = self.texto.yview)
    
            self.texto.config(yscrollcommand = self.scrollbar.set)
    
            self.botao = Button(self.segundoContainer)
            self.botao['text'] = 'Extrair assunto'
            self.label['font'] = ('Cantarell', '10')
            self.botao['width'] = 30
            self.botao['height'] = 1
            self.botao['command'] = self.acao_extrairAssunto
            self.botao.pack(pady = 10, side = LEFT)
            
            self.botaoLimpar = Button(self.segundoContainer)
            self.botaoLimpar['text'] = 'Limpar texto'
            self.botaoLimpar['font'] = ('Cantarell', '7')
            self.botaoLimpar['width'] = 30
            self.botaoLimpar['height'] = 1
            self.botaoLimpar['command'] = self.acao_limparTexto
            self.botaoLimpar.pack(pady = 10, side = RIGHT)
    
            # Para alinhar a janela no centro da tela
            master.update_idletasks()
            width = master.winfo_width()
            height = master.winfo_height()
            x = (master.winfo_screenwidth() // 2) - (width // 2)
            y = (master.winfo_screenheight() // 2) - (height // 2)
            master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
        def acao_extrairAssunto(self):
            texto = self.texto.get("1.0", END)
    
            if len(texto) > 1:    
                assunto = extrairAssunto(texto)
                
                try:
                    mensagem = 'O assunto do texto é "%s"!' % assunto
                    messagebox.showinfo('Resultado', mensagem)
        
                except:
                    mensagem = 'Não foi possível extrair o assunto do texto!'
                    messagebox.showerror('Erro', mensagem)

        def acao_limparTexto(self):
            self.texto.delete("1.0",END)
    
    root = Tk()
    Xate(root)

    root.mainloop()