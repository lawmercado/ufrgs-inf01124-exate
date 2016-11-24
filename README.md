# Xate
Xate: uma aplicação para eXtração de Assunto de TExtos

## Dependências
- Python 3;
- NLTK 3.

## Modo de usar
A Xate pode ser utilizada como uma aplicação ou como um módulo.

### Como uma aplicação
Ao executar o seguinte comando:
```
python xate.py
```
Será carregada uma interface gráfica simples. Basta inserir o texto, clicar no botão "Extrair assunto" e obter o assunto do mesmo.

### Como um módulo
```
import xate

[...]

assunto = xate.extrairAssunto(texto)
```

## Licença
Este projeto é licenciado sob a GNU GPL v3. Mais informações sobre a mesma, vide o arquivo [LICENSE.md](https://github.com/luiswebmercado/Xate/blob/master/LICENSE.md).
