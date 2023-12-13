import requests
import json
import sys

link = "https://configs-5d64c-default-rtdb.firebaseio.com/Configs"
dados = {"CPF":"14959789743","Nome":"Leo","Idade":"27","Sobrenome":"Negrão"}

dicio = requests.get(f'{link}/.json')
dic = dicio.json()

try:
    for id in dic:
        chave = dic[id]['CPF']
        if chave == "14959789743":
            print('RAFA')

    sys.exit()


except Exception :
    
    requisicao = requests.patch(f'{link}/{id}.json',data = json.dumps(dados))






#print(dic)