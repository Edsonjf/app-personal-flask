import pandas as pd
import json



with open('dados.json', 'r', encoding='utf-8') as dados_json:
    dados = dados_json.read()

    print(dados)

#dados = open('dados.json','r', encoding='utf-8').read()

print(type(dados['João']['A']))


