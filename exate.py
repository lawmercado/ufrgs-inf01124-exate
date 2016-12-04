# -*- coding: utf-8 -*-

# Exate: Extrator de assunto de Texto
#
# Author: Luís Augusto Weber Mercado <luiswebmercado@gmail.com>
#

"""
Arquivo principal da aplicação Exate

Pode ser carregado como um módulo, se apenas a funcionalidade principal for
desejada. Para executar a aplicação, juntamente com a sua GUI, basta executar o
script.
"""

import pln.core as pln

def extrairAssunto(texto, considerarSinonimos = False):
    """
    Dado um texto, obtém qual o assunto do mesmo

    :param texto: Texto a ser analisado
    :type texto: string
    """

    tokens = pln.obterTokens(texto)
    palavras = [token.lower() for token in tokens if token.isalnum()] # Remove a pontuação

    substantivos = [pln.singularizar(item) for item in pln.obterSubstantivos(palavras)]

    substantivosUnificados = list(set(substantivos))

    contagem = []

    # Realiza a contagem dos substantivos
    for substantivo in substantivosUnificados:
        ocorrencias = substantivos.count(substantivo)

        contagem.append((substantivo, ocorrencias))

    # Ordena a contagem em ordem decrescente
    contagem.sort(key = lambda item: item[1], reverse = True)

    if considerarSinonimos is True:
        # Pega os 10 mais prováveis candidatos a serem assunto do texto
        relacoes = pln.obterSinonimosNaLista([substantivo for substantivo, cont in contagem][0:10])
    
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

    TXT_COR = '#333333'
    BG_COR = '#DFDDE1'
    BG_INTER = '#C8C4C9'
    BG_HIGHLIGHT = '#F4F4F4'

    class Exate(object):
        def __init__(self, master = None):
            master.title('Exate: Extrator de assunto de textos')

            master.configure(background=BG_COR)

            self.primeiroContainer = Frame(master)
            self.primeiroContainer['background'] = BG_COR
            self.primeiroContainer['padx'] = 5
            self.primeiroContainer.pack()

            self.segundoContainer = Frame(master)
            self.segundoContainer['background'] = BG_COR
            self.segundoContainer.pack()

            self.label = Label(self.primeiroContainer, text = 'Informe um texto')
            self.label['background'] = BG_COR
            self.label['foreground'] = TXT_COR
            self.label['font'] = ('Cantarell', '10', 'bold')
            self.label.pack(pady = 10)

            self.texto = Text(self.primeiroContainer, height = 15, width = 80)
            self.texto['font'] = ('Cantarell', '10')
            self.texto['borderwidth'] = 0
            self.texto['foreground'] = TXT_COR
            self.texto['background'] = BG_HIGHLIGHT
            self.texto.bind("<Control-Key-a>", self.acao_textoSelecionarTudo)
            self.texto.bind("<Control-Key-A>", self.acao_textoSelecionarTudo)
            self.texto.pack(side = LEFT, fill = Y)

            self.scrollbar = Scrollbar(self.primeiroContainer)
            self.scrollbar['borderwidth'] = 0
            self.scrollbar['background'] = BG_INTER
            self.scrollbar['troughcolor'] = BG_COR
            self.scrollbar['activebackground'] = BG_HIGHLIGHT
            self.scrollbar.pack(side = RIGHT, fill = Y)
            self.scrollbar.config(command = self.texto.yview)

            self.texto.config(yscrollcommand = self.scrollbar.set)

            self.botao = Button(self.segundoContainer)
            self.botao['text'] = 'Extrair assunto'
            self.botao['font'] = ('Cantarell', '10')
            self.botao['width'] = 30
            self.botao['height'] = 1
            self.botao['background'] = BG_INTER
            self.botao['activebackground'] = BG_HIGHLIGHT
            self.botao['foreground'] = TXT_COR
            self.botao['borderwidth'] = 0
            self.botao['command'] = self.acao_extrairAssunto
            self.botao.pack(pady = 10, side = LEFT)

            self.considerarSinonimos = IntVar()
            self.checkBox = Checkbutton(self.segundoContainer, text = "Considerar sinônimos?", variable = self.considerarSinonimos)
            self.checkBox['text'] = 'Considerar sinônimos'
            self.checkBox['font'] = ('Cantarell', '10')
            self.checkBox['background'] = BG_COR
            self.checkBox['activebackground'] = BG_COR
            self.checkBox['foreground'] = TXT_COR
            self.checkBox['borderwidth'] = 0
            self.checkBox.pack(pady = 13, padx = 10)
            
            # Para alinhar a janela no centro da tela
            master.update_idletasks()
            width = master.winfo_width()
            height = master.winfo_height()
            x = (master.winfo_screenwidth() // 2) - (width // 2)
            y = (master.winfo_screenheight() // 2) - (height // 2)
            master.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        def acao_extrairAssunto(self):
            texto = self.texto.get("1.0", END)
            considerarSinonimos = self.considerarSinonimos.get() == 1

            if len(texto) > 1:
                assunto = extrairAssunto(texto, considerarSinonimos)

                try:
                    mensagem = 'O assunto do texto é "%s"!' % assunto
                    messagebox.showinfo('Resultado', mensagem)

                except:
                    mensagem = 'Não foi possível extrair o assunto do texto!'
                    messagebox.showerror('Erro', mensagem)

        def acao_textoSelecionarTudo(self, event):
            self.texto.tag_add(SEL, "1.0", END)
            self.texto.mark_set(INSERT, "1.0")
            self.texto.see(INSERT)
            return 'break'
            
    root = Tk()
    Exate(root)

    root.mainloop()
