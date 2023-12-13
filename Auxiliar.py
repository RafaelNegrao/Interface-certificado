from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem,QTableWidget,QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,QApplication,QMessageBox,QTextEdit
from PyQt5.QtCore import QDate, QTime,QUrl, Qt
import datetime
from winotify import Notification
from PyQt5.QtGui import QDesktopServices,QPixmap,QImage,QFont
import pandas as pd
import os
import firebase_admin
from firebase_admin import db
import tkinter as tk
from tkinter import filedialog
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import fitz
from PIL import Image
import time
import requests
import tkinter as tk



#configurando banco de dados#####################################################################################

credentials = {
  "type": "service_account",
  "project_id": "bdpedidos-2078f",
  "private_key_id": "4a82f1f1c7dd76534b65ddc14a6d87e8dacf7dec",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC+6Yo/ebh6RrTC\nV5/tLTCQx+1adPKLTGoBuqsGgj2+WdKbwRkW/i4pnH3cK/uDmRmcftqmUtrYScxU\n4iksJ4Mo+yZe1rruul+pyTlLETlsGlhtyxdjexDGXo3t1ZPMhuSX24O4OdqqB6MO\nc0BCwY/GDNQcyX+gGKwJfwSWfpBOcU19mzUwmdUHli6GfNhnpZDdRT6bDPhLAip+\ngdGeDD1mON3hccanOGvuz/zHoaSV7CyhteNS6Wkwqvbx2CuTImnN6bJ5apWWh4nB\nv42UmrymOOpUldWximuCXQFlC+qEaQVy/964ZyC6sSsGYel6/xWerN426FL7H8/S\nCQfGHpjRAgMBAAECggEAAMtftS+gVsDHJBGatJ70zhDbfGvgcoDNnUSDcfbGNZJt\nQhM8oVkmSOJUQOQmiMjxBnwdy2FjdJoY3yWNx7xByQm6gm7OmlSRo+lfvF/N1PBU\nRQQe6BSkBRYof5vdMt7THYzxS84+ZbJyuWWrYO4FjiORhvbajBq3UkSCVDxG4Jgb\nsEdWewqplXtSpNhQDERlOfQGrzxtc7v7m6P27HX3nhvCKYr0Fu4P9IYx9XJUrUvV\n9pI48+8sbzuvR1vVPSmcvufk5JHqc8y5nAShSPM2F9gpeypwyHyYu59knMNqzhiR\n1SNOqvW4KYO14+1IurnIG7olV3FoTqdsnfb59eIiAQKBgQDv6uB5qQh03iDJkfC/\ntR+8oOhT54tJHiQd5yuY+IWdTb7L98aeO7vvGD3OfGb1H0TC5TXxhCVJNv7wXL2v\nx58TGg7hla+Cd/OpJNIFxNUDpeaWf+cwGFdd7rI9yxZqpQI75UZY7VTkDI8w9rsE\nuvLmPoReab3M9TwXx7C0G2QQsQKBgQDLtbSFiF9ODpd46bnKpG2hN9WuHAAqqj8V\n7fcmaWqom2jI8mkfaRBgIFHlJHhj6YADCOXFrNqTdRFUDWv+JV3gV0KqXnqvWL7O\n4m+XwvgatYWEVgeaq53+fFlpePE2CY9aY8DyTISlMav9Wgx2gmrh7HVGY7rIes9Z\nZtq+aMwSIQKBgAsNS9fu5HfVv7bpZSi/pD2hP/KViQIORGWoP4blc+pCKZblzB1/\n7PFfsYEwk+GY1icQPgLpLnqH8QiLjSVq0bYkjijwJ0ygT/Yrvw0K+zEW1F98dt7t\nUCEAnO9hyp+RCGBP+ISiMjXrKjF8PDNElWnr2VcsEdU+Os1xon85f8uRAoGBAJ5E\n8JqG17UntRvmS8lbcym83bHGY4LCfv0kw87+PDX/eKwXWwFieayVr8seSMMnmaPB\n9/NbVv8WB36MZwkwMv2oDk2b1ioCA01ttFHu0yC9Q50L0iCjkb81EarWomHfj5ck\nxbX7KVvHed7/ZYt1zGD3fC5SMb6tXAgT14P0nAjBAoGBANuYQdxtB8R1Ee7WWqj5\n8Aq5xkn+r8yWZSL2GGMrix6x5atbyjBugldIKt39BmpUjlRiWEYMdTFIcdyzPjiZ\nE7lVnd2U0O9t5zVvN/XjEvJh8SuXZL9kGfWy6wwiWIYwEcj7FbBcUdvSPMlmjX5R\neO92IYzhv8grIOH0wHpVdiqe\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-xmo0a@bdpedidos-2078f.iam.gserviceaccount.com",
  "client_id": "105788646445863226974",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xmo0a%40bdpedidos-2078f.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


acoes = firebase_admin.credentials.Certificate(credentials)
firebase_admin.initialize_app(acoes, {'databaseURL':'https://bdpedidos-2078f-default-rtdb.firebaseio.com/' }) 
ref = db.reference("/")

################################################################################################################



def criar_pasta_cliente():
    try:
        nome_pasta = ui.campo_nome.text()
        if nome_pasta == '':
            notificacao = Notification(app_id="Pasta não criada", title="", msg="Preencha o NOME do cliente.")
            notificacao.show()
            return

        # Obtenha o diretório selecionado
        diretorio = filedialog.askdirectory()

        if diretorio:
            # Verifique se a pasta já existe no diretório
            pasta_existente = os.path.exists(os.path.join(diretorio, nome_pasta))
            
            if not pasta_existente:
                # Crie a pasta com o nome da variável no diretório selecionado
                nova_pasta = os.path.join(diretorio, nome_pasta)
                os.mkdir(nova_pasta)
                notificacao = Notification(app_id="Pasta Criada", title="", msg=f"Pasta do cliente {nome_pasta} criada com sucesso!")
                notificacao.show()
            else:
                notificacao = Notification(app_id="Pasta existente", title="", msg=f"Pasta do cliente {nome_pasta} já existe no diretório!")
                notificacao.show()
        else:
            return
    except Exception as e:
        notificacao = Notification(app_id="Pasta não criada", title="", msg="")
        notificacao.show()

def limpar_campos():
    ui.campo_pedido.setReadOnly(False)
    ui.campo_certificado.setReadOnly(False)
    ui.campo_nome.setText("")
    ui.campo_cpf.setText("") 
    ui.campo_rg.setText("")
    ui.campo_email.setText("")
    ui.campo_certificado.setText("")
    ui.campo_cnpj.setText("")
    ui.campo_digito_ano.setText("")
    ui.campo_pedido.setText("")
    ui.campo_nome_mae.setText("")
    ui.campo_novo_noBd.setText("")
    ui.campo_lista_status.setCurrentText("DIGITAÇÃO")
    ui.campo_lista_status_3.setCurrentText("NAO")
    ui.campo_lista_status_4.setCurrentText("")
    data_nula = QDate(2000, 1, 1)
    hora = QTime.fromString('00:00', "hh:mm")
    ui.campo_data_agendamento.setDate(data_nula)
    ui.campo_data_nascimento.setDate(data_nula)
    ui.campo_hora_agendamento.setTime(hora)
    ui.tableWidget.setRowCount(0)
    ui.label_quantidade_bd.setText("")
    ui.campo_nome_mae.setText("")
    ui.campo_cnh.setText("")
    ui.campo_seguranca_cnh.setText("")
    ui.campo_link_video.setText("")
    ui.campo_diretorio_pasta.setText("")
    limpar_label_pdf()

def procurar_cnh():
    url = QUrl("https://sso.acesso.gov.br/login?client_id=portalservicos.denatran.serpro.gov.br&authorization_id=18aa635cf94")
    QDesktopServices.openUrl(url)
    return

def procurar_oab():
    url = QUrl("https://cna.oab.org.br/")
    QDesktopServices.openUrl(url)
    return

def procurar_rg():
    url = QUrl("https://acertid.net.br/acertid/")
    QDesktopServices.openUrl(url)
    return

def procurar_cnpj():
    cnpj = ui.campo_cnpj.text()
    url = QUrl(f"https://solucoes.receita.fazenda.gov.br/servicos/cnpjreva/Cnpjreva_Solicitacao.asp?cnpj={cnpj}")
    QDesktopServices.openUrl(url)
    url = QUrl("https://www.jucesponline.sp.gov.br/")
    QDesktopServices.openUrl(url)
    return

def dados_cnpj():
    global tela_cnpj  # Utiliza a variável global para garantir o acesso fora da função
    cnpj = ''.join(filter(str.isdigit, ui.campo_cnpj.text()))
    if cnpj == '':
        return
    
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"

    try:
        resposta = requests.get(url)
        data = resposta.json()

        if resposta.status_code == 200:
    # Remove os caracteres '{' e '[' dos dicionários aninhados
            data = {chave: valor if not isinstance(valor, dict) else {k: v.replace('[', '').replace('{', '').replace(']', '').replace('}', '') if isinstance(v, str) else v for k, v in valor.items()} for chave, valor in data.items()}

            # Ajusta a formatação da chave 'Qsa'
            if 'qsa' in data and isinstance(data['qsa'], list):
                qsa_formatado = "    ".join([f"{k}: {v}" for item in data['qsa'] for k, v in item.items()])
                data['qsa'] = qsa_formatado

            chaves_desejadas = ['abertura', 'situacao', 'tipo', 'nome', 'fantasia', 'natureza_juridica', 'qsa', 'municipio', 'uf', 'capital_social', 'email']

            dados_filtrados = {chave: valor for chave, valor in data.items() if chave in chaves_desejadas}

            texto_formatado = "\n".join([f"{chave.capitalize()}: {valor}" for chave, valor in dados_filtrados.items()])

            # Atualiza a variável global
            tela_cnpj = TelaCNPJ(texto_formatado)
            tela_cnpj.show()

        else:
            exibir_mensagem_erro(f"Erro na requisição: {data.get('message', 'N/A')}")
    except Exception as e:
        exibir_mensagem_erro(f"Erro na requisição: {str(e)}")

def exibir_mensagem_erro(mensagem):
    QMessageBox.warning(None, "Erro", mensagem)

def procurar_cpf():
    
    cpf = ui.campo_cpf.text()
    nascimento = ui.campo_data_nascimento.text()
    if not nascimento == "01/01/2000":
        url = QUrl(f"https://servicos.receita.fazenda.gov.br/Servicos/CPF/ConsultaSituacao/ConsultaPublica.asp?cpf={cpf}&Nascimento={nascimento}")
        QDesktopServices.openUrl(url)
        return
    else:
        url = QUrl(f"https://servicos.receita.fazenda.gov.br/Servicos/CPF/ConsultaSituacao/ConsultaPublica.asp?cpf={cpf}")
        QDesktopServices.openUrl(url)
        return

def formatar_cpf():
    cpf = ui.campo_cpf.text()
    novo_cpf = cpf.replace(".","").replace("-","")
    if len(novo_cpf) == 11:
        a = novo_cpf[:3]
        b = novo_cpf[3:6]
        c = novo_cpf[6:9]
        d = novo_cpf[9:11]
        cpf_formatado = f"{a}.{b}.{c}-{d}"
        ui.campo_cpf.clear()
        ui.campo_cpf.setText(cpf_formatado)
        
    
#digito_cpf =  cpf[-2:]
    elif len(novo_cpf) <= 11 and len(cpf) > 0:
        cpf_formatado = cpf.zfill(11)
        a = cpf_formatado[:3]
        b = cpf_formatado[3:6]
        c = cpf_formatado[6:9]
        d = cpf_formatado[9:11]
        cpf_formatado = f"{a}.{b}.{c}-{d}"
        ui.campo_cpf.setText("")
        ui.campo_cpf.setText(cpf_formatado)
        
    elif len(novo_cpf)== "":
        return   

def formatar_data_nascimento():
    nascimento = ui.campo_data_nascimento.text()
    if not nascimento == "01/01/2000":
        ui.campo_digito_ano.setText(nascimento[6:10])
        
def formatar_cnpj():
    cnpj = ui.campo_cnpj.text()
    cnpj_sp = cnpj.replace(".","").replace("/","").replace("-","")
    if len(cnpj_sp) == 14:
        a = cnpj_sp[:2]
        b = cnpj_sp[2:5]
        c = cnpj_sp[5:8]
        d = cnpj_sp[8:12]
        e = cnpj_sp[12:14]
        cnpj_formatado = f"{a}.{b}.{c}/{d}-{e}"
        ui.campo_cnpj.setText("")
        ui.campo_cnpj.setText(cnpj_formatado)
    elif len(cnpj_sp) == 18:
        pass

def salvar():

    num_pedido = ui.campo_pedido.text()
    req = ref.get()
    for id in req:
        if num_pedido == req[id]['PEDIDO']:
            if ui.campo_lista_status.currentText() != "DIGITAÇÃO" and ui.campo_lista_status.currentText() != "VERIFICAÇÃO":
                #aqui o pedido existente será gravado
                #caso o status seja diferente de Aguardando
                #os dados do cliente serão deletados
                pedido = ui.campo_pedido.text()
                tipo = ui.campo_certificado.text()
                hora  = ui.campo_hora_agendamento.text()
                data = ui.campo_data_agendamento.text()
                status = ui.campo_lista_status.currentText()
                vendido = ui.campo_lista_status_3.currentText()
                modalidade = ui.campo_lista_status_4.currentText()
                nome = ""
                cpf = ""
                rg = ""
                cpf = ""
                cnh = ""
                mae = ""
                cnpj = ""
                email = ""
                dig_ano = ""
                data_nascimento = ""
                cod_seg_cnh = ""
                diretorio = ""


                if pedido == "" or tipo == "" or hora == "00:00" or data == "01/01/2000" or status == "" or modalidade == "":

                    notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!")
                    notificacao.show()
                    return
                
            
                #
                novos_dados = {"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
                notificacao.show()
                ref.child(id).update(novos_dados)
                return
            
            
            
            #Aqui ele vai somente salvar os dados no servidor
            #e mante-los nos campos
            
            else:
                pedido = ui.campo_pedido.text()
                tipo = ui.campo_certificado.text()
                hora  = ui.campo_hora_agendamento.text()
                data = ui.campo_data_agendamento.text()
                status = ui.campo_lista_status.currentText()
                nome = ui.campo_nome.text()
                cpf = ui.campo_cpf.text()
                rg = ui.campo_rg.text()
                cpf = ui.campo_cpf.text()
                cnh = ui.campo_cnh.text()
                mae = ui.campo_nome_mae.text()
                cnpj = ui.campo_cnpj.text()
                email = ui.campo_email.text()
                dig_ano = ui.campo_digito_ano.text()
                data_nascimento = ui.campo_data_nascimento.text()
                vendido = ui.campo_lista_status_3.currentText()
                modalidade = ui.campo_lista_status_4.currentText()
                cod_seg_cnh = ui.campo_seguranca_cnh.text()
                diretorio = ui.campo_diretorio_pasta.text()

                if pedido == "" or tipo == "" or hora == "00:00" or data == "01/01/2000" or status == "" or modalidade == "":

                    notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!")
                    notificacao.show()
                    return
                #
                novos_dados = {"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
                notificacao = Notification(app_id="Pedido",title="",msg=f"Pedido {pedido} salvo com sucesso\nStatus:{status}!")
                notificacao.show()
                ref.child(id).update(novos_dados)
                return
   


        #aqui o pedido não existe e será gravado
        #caso o status seja diferente de Aguardando
        #os dados do cliente serão deletados
    if ui.campo_lista_status.currentText() != "DIGITAÇÃO" and ui.campo_lista_status.currentText() != "VERIFICAÇÃO":
        
        pedido = ui.campo_pedido.text()
        tipo = ui.campo_certificado.text()
        hora  = ui.campo_hora_agendamento.text()
        data = ui.campo_data_agendamento.text()
        status = ui.campo_lista_status.currentText()
        vendido = ui.campo_lista_status_3.currentText()
        modalidade = ui.campo_lista_status_4.currentText()
        nome = ""
        cpf = ""
        rg = ""
        cpf = ""
        cnh = ""
        mae = ""
        cnpj = ""
        email = ""
        dig_ano = ""
        data_nascimento = ""
        cod_seg_cnh = ""
        vendido = ui.campo_lista_status_3.currentText()
        diretorio = ""

        if pedido == "" or tipo == "" or hora == "00:00" or data == "01/01/2000" or status == "" or modalidade == "":

            notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!")
            notificacao.show()
            return
        
        
        #
        novos_dados = {"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
        notificacao.show()
        ref.push(novos_dados)
        return
    else:
        pedido = ui.campo_pedido.text()
        tipo = ui.campo_certificado.text()
        hora  = ui.campo_hora_agendamento.text()
        data = ui.campo_data_agendamento.text()
        status = ui.campo_lista_status.currentText()
        nome = ui.campo_nome.text()
        cpf = ui.campo_cpf.text()
        rg = ui.campo_rg.text()
        cpf = ui.campo_cpf.text()
        cnh = ui.campo_cnh.text()
        mae = ui.campo_nome_mae.text()
        cnpj = ui.campo_cnpj.text()
        email = ui.campo_email.text()
        dig_ano = ui.campo_digito_ano.text()
        data_nascimento = ui.campo_data_nascimento.text()
        vendido = ui.campo_lista_status_3.currentText()
        modalidade = ui.campo_lista_status_4.currentText()
        cod_seg_cnh = ui.campo_seguranca_cnh.text()
        diretorio = ui.campo_diretorio_pasta.text()
    
        if pedido == "" or tipo == "" or hora == "00:00" or data == "01/01/2000" or status == "" or modalidade == "":

            notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!")
            notificacao.show()
            return
        #
        novos_dados = {"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
        
        notificacao = Notification(app_id="Pedido",title="",msg=f"Pedido {pedido} salvo com sucesso\nStatus:{status}!")
        notificacao.show()

        ref.push(novos_dados)
        return

def gravar_dados():
#USO DO BANCO DE DADOS
    num_pedido = ui.campo_pedido.text()
    req = ref.get()
    for id in req:
        if num_pedido == req[id]['PEDIDO']:
            if ui.campo_lista_status.currentText() != "DIGITAÇÃO" and ui.campo_lista_status.currentText() != "VERIFICAÇÃO":
                #aqui o pedido existente será gravado
                #caso o status seja diferente de Aguardando
                #os dados do cliente serão deletados
                pedido = ui.campo_pedido.text()
                tipo = ui.campo_certificado.text()
                hora  = ui.campo_hora_agendamento.text()
                data = ui.campo_data_agendamento.text()
                status = ui.campo_lista_status.currentText()
                vendido = ui.campo_lista_status_3.currentText()
                modalidade = ui.campo_lista_status_4.currentText()
                nome = ""
                cpf = ""
                rg = ""
                cpf = ""
                cnh = ""
                mae = ""
                cnpj = ""
                email = ""
                dig_ano = ""
                data_nascimento = ""
                cod_seg_cnh = ""
                diretorio = ""

                if pedido == "" or tipo == "" or hora == "00:00" or data == "01/01/2000" or status == "" or modalidade == "":

                    notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!")
                    notificacao.show()
                    return
                

                #
                novos_dados = {"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
                notificacao = Notification(app_id="Pedido",title="",msg=f"Pedido {pedido} atualizado com sucesso\nStatus:{status}!")
                notificacao.show()
                ref.child(id).update(novos_dados)
                limpar_campos()
                return
            
            
            
            else:
                pedido = ui.campo_pedido.text()
                tipo = ui.campo_certificado.text()
                hora  = ui.campo_hora_agendamento.text()
                data = ui.campo_data_agendamento.text()
                status = ui.campo_lista_status.currentText()
                nome = ui.campo_nome.text()
                cpf = ui.campo_cpf.text()
                rg = ui.campo_rg.text()
                cpf = ui.campo_cpf.text()
                cnh = ui.campo_cnh.text()
                mae = ui.campo_nome_mae.text()
                cnpj = ui.campo_cnpj.text()
                email = ui.campo_email.text()
                dig_ano = ui.campo_digito_ano.text()
                data_nascimento = ui.campo_data_nascimento.text()
                vendido = ui.campo_lista_status_3.currentText()
                modalidade = ui.campo_lista_status_4.currentText()
                cod_seg_cnh = ui.campo_seguranca_cnh.text()
                diretorio = ui.campo_diretorio_pasta.text()

                if pedido == "" or tipo == "" or hora == "00:00" or data == "01/01/2000" or status == "" or modalidade == "":

                    notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!")
                    notificacao.show()
                    return
                #
                novos_dados = {"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
                notificacao = Notification(app_id="Novo pedido",title="",msg=f"Pedido {pedido} atualizado com sucesso\nStatus:{status}!")
                notificacao.show()
                ref.child(id).update(novos_dados)
                limpar_campos()
                return
   
    if ui.campo_lista_status.currentText() != "DIGITAÇÃO" and ui.campo_lista_status.currentText() != "VERIFICAÇÃO":
        #aqui o pedido não existe e será gravado
        #caso o status seja diferente de Aguardando
        #os dados do cliente serão deletados
        pedido = ui.campo_pedido.text()
        tipo = ui.campo_certificado.text()
        hora  = ui.campo_hora_agendamento.text()
        data = ui.campo_data_agendamento.text()
        status = ui.campo_lista_status.currentText()
        vendido = ui.campo_lista_status_3.currentText()
        modalidade = ui.campo_lista_status_4.currentText()
        nome = ""
        cpf = ""
        rg = ""
        cpf = ""
        cnh = ""
        mae = ""
        cnpj = ""
        email = ""
        dig_ano = ""
        data_nascimento = ""
        cod_seg_cnh = ""
        diretorio = ""

        if pedido == "" or tipo == "" or hora == "00:00" or data == "01/01/2000" or status == "" or modalidade == "":

            notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!")
            notificacao.show()
            return
        

        novos_dados = {"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
        notificacao.show()
        ref.push(novos_dados)
        limpar_campos()
        return
    else:
        pedido = ui.campo_pedido.text()
        tipo = ui.campo_certificado.text()
        hora  = ui.campo_hora_agendamento.text()
        data = ui.campo_data_agendamento.text()
        status = ui.campo_lista_status.currentText()
        nome = ui.campo_nome.text()
        cpf = ui.campo_cpf.text()
        rg = ui.campo_rg.text()
        cpf = ui.campo_cpf.text()
        cnh = ui.campo_cnh.text()
        mae = ui.campo_nome_mae.text()
        cnpj = ui.campo_cnpj.text()
        email = ui.campo_email.text()
        dig_ano = ui.campo_digito_ano.text()
        data_nascimento = ui.campo_data_nascimento.text()
        vendido = ui.campo_lista_status_3.currentText()
        modalidade = ui.campo_lista_status_4.currentText()
        cod_seg_cnh = ui.campo_seguranca_cnh.text()
        diretorio = ui.campo_diretorio_pasta.text()

        if pedido == "" or tipo == "" or hora == "00:00" or data == "01/01/2000" or status == "" or modalidade == "":

            notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!")
            notificacao.show()
            return
        #
        novos_dados = {"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
        
        notificacao = Notification(app_id="Novo pedido",title="",msg=f"Pedido {pedido} criado com sucesso\nStatus:{status}!")
        notificacao.show()

        ref.push(novos_dados)
        limpar_campos()
        return

def exportar_excel():
    try:
        req =ref.get()
        
        data_inicial = datetime.datetime.strptime(ui.campo_data_de.text(), "%d/%m/%Y")
        numero_inteiro_inicial = data_inicial.toordinal()
        data_final = datetime.datetime.strptime(ui.campo_data_ate.text(), "%d/%m/%Y")
        numero_inteiro_final = data_final.toordinal()

        dados_selecionados=[]
        x = 0
        for cliente in req:
            data_bd = datetime.datetime.strptime(req[cliente]['DATA'], "%d/%m/%Y")
            numero_inteiro_bd = data_bd.toordinal()

            status_filtro = ui.campo_lista_status_2.currentText()
            status_servidor = req[cliente]['STATUS']

            if (numero_inteiro_inicial <= numero_inteiro_bd <= numero_inteiro_final):
                if status_filtro == status_servidor:
                
                    x += 1
                    pedido = req[cliente]['PEDIDO']
                    data_agendamento = req[cliente]['DATA']
                    tipo_pedido = req[cliente]['TIPO']
                    hora_agendamento = req[cliente]['HORA']    
                    status_agendamento = req[cliente]['STATUS']
                    vendido = req[cliente]['VENDIDO POR MIM?']
                    modalidade = req[cliente]['MODALIDADE']

                    dados_selecionados.append((pedido, data_agendamento, tipo_pedido, hora_agendamento,status_agendamento,vendido,modalidade))   

                elif status_filtro == "TODAS":

                    x += 1

                    pedido = req[cliente]['PEDIDO']
                    data_agendamento = req[cliente]['DATA']
                    tipo_pedido = req[cliente]['TIPO']
                    hora_agendamento = req[cliente]['HORA']    
                    status_agendamento = req[cliente]['STATUS']
                    vendido = req[cliente]['VENDIDO POR MIM?']
                    modalidade = req[cliente]['MODALIDADE']
                    dados_selecionados.append((pedido, data_agendamento, tipo_pedido, hora_agendamento,status_agendamento,vendido,modalidade)) 
        
        if x > 0:
            root = tk.Tk()
            root.withdraw()
            caminho_arquivo = filedialog.askdirectory()
            if caminho_arquivo:
                df=pd.DataFrame(dados_selecionados,columns=['Pedido','Data agendamento','Tipo de certificado','hora','Status Pedido','Vendido por mim?','Modalidade'])
                data_agora = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
                data_final = ui.campo_data_ate.text()
                data_inicial = ui.campo_data_de.text()
                pasta_desktop = os.path.expanduser(f"{caminho_arquivo}")
                nome_arquivo = os.path.join(pasta_desktop, f"Certificados-emitidos-de {data_inicial.replace('/', '-')} a {data_final.replace('/', '-')}-gerado em{data_agora.replace('/','-')} .xlsx")
                df.to_excel(nome_arquivo, index=False)
                notificacao = Notification(app_id="Arquivo salvo",title="",msg=f"Arquivo excel gerado!")
                notificacao.show()
            else:
                return
        else:
            notificacao = Notification(app_id="Sem dados",title="",msg=f"Sem dados para o período!")
            notificacao.show()

    except Exception as e:
        notificacao = Notification(app_id=f"Arquivo não salvo  motivo:{e}",title="",msg=f"Arquivo não gerado!\nmotivo: {e}")
        notificacao.show()
        # Lida com exceções aqui
        pass

def preencher_tabela():
    #USO DE BANCO DE DADOS
    ui.tableWidget.setRowCount(0)
    try:
        ui.tableWidget.clear()
        
        req = ref.get()
        # Ordene a lista de acordo com a data em ordem decrescente
        req = sorted(req.values(), key=lambda x: datetime.datetime.strptime(x['DATA'], "%d/%m/%Y"), reverse=True)

        data_inicial = datetime.datetime.strptime(ui.campo_data_de.text(), "%d/%m/%Y")
        numero_inteiro_inicial = data_inicial.toordinal()
        data_final = datetime.datetime.strptime(ui.campo_data_ate.text(), "%d/%m/%Y")
        numero_inteiro_final = data_final.toordinal()
        status_filtro = ui.campo_lista_status_2.currentText()

        x = 0
        ui.barra_progresso_consulta.setVisible(True)
        ui.barra_progresso_consulta.setValue(0)
        total_pedidos = len(req)
        y = 0
        for pedido_info in req:
            
            data_bd = datetime.datetime.strptime(pedido_info['DATA'], "%d/%m/%Y")
            numero_inteiro_bd = data_bd.toordinal()
            status_servidor = pedido_info['STATUS']
            
            if (numero_inteiro_inicial <= numero_inteiro_bd <= numero_inteiro_final) :

                if status_filtro == status_servidor or status_filtro == "TODAS":
                
                    x += 1
                
                    row_position = ui.tableWidget.rowCount()
                    ui.tableWidget.insertRow(row_position)

                    ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(pedido_info['PEDIDO']))
                    ui.tableWidget.setItem(row_position, 1, QTableWidgetItem(pedido_info['NOME']))
                    ui.tableWidget.setItem(row_position, 2, QTableWidgetItem(pedido_info['DATA']))
                    ui.tableWidget.setItem(row_position, 3, QTableWidgetItem(pedido_info['HORA']))
                    ui.tableWidget.setItem(row_position, 4, QTableWidgetItem(pedido_info['MODALIDADE']))
                    ui.tableWidget.setItem(row_position, 5, QTableWidgetItem(pedido_info['STATUS']))
                    ui.tableWidget.setItem(row_position, 6, QTableWidgetItem(pedido_info['VENDIDO POR MIM?']))
                    ui.tableWidget.setItem(row_position, 7, QTableWidgetItem(pedido_info['TIPO']))
                    y += 1
                    porcentagem = (y/total_pedidos)*100
                    ui.barra_progresso_consulta.setValue(int(porcentagem))
                    QApplication.processEvents()
                    
        
        total = 100
        while porcentagem <= total:
            ui.barra_progresso_consulta.setValue(int(porcentagem))
            porcentagem +=1
            QApplication.processEvents()
            
        
        ui.barra_progresso_consulta.setValue(100)
        ui.label_quantidade_bd.setText(f"{x} registro(s)")
        ui.tableWidget.setHorizontalHeaderLabels(["PEDIDO","NOME", "DATA", "HORA", "MODALIDADE", "STATUS", "VENDA","TIPO"])
        ui.barra_progresso_consulta.setVisible(False)
    except Exception as e:
            ui.barra_progresso_consulta.setVisible(False)
            pass

def carregar_dados():
    #USO DE BANCO DE DADOS
    #Verifica se o pedido existe no servidor quando um novo pedido é digitado no campo PEDIDO
    try:
        num_pedido = ui.campo_pedido.text()
        req = ref.get()
        num_pedidos_total = len(req)
        num_pedidos_processados = 0

        for pedido in req:
            ui.barra_progresso_pedido.setVisible(True)
            pedido_servidor = req[pedido]['PEDIDO']
            if num_pedido == pedido_servidor:
                ui.campo_pedido.setReadOnly(True)
                # Traga os dados
                data = QDate.fromString(req[pedido]['DATA'], "dd/MM/yyyy")
                hora = QTime.fromString(req[pedido]['HORA'], "hh:mm")

                ui.campo_novo_noBd.setText("✅")
                ui.campo_data_agendamento.setDate(data)
                ui.campo_hora_agendamento.setTime(hora)
                ui.campo_pedido.setText(req[pedido]['PEDIDO'])
                ui.campo_certificado.setText(req[pedido]['TIPO'])
                ui.campo_lista_status.setCurrentText(req[pedido]['STATUS'])
                ui.campo_nome.setText(req[pedido]['NOME'])
                ui.campo_rg.setText(req[pedido]['RG'])
                ui.campo_cpf.setText(req[pedido]['CPF'])
                ui.campo_cnh.setText(req[pedido]['CNH'])
                ui.campo_nome_mae.setText(req[pedido]['MAE'])
                ui.campo_cnpj.setText(req[pedido]['CNPJ'])
                ui.campo_email.setText(req[pedido]['EMAIL'])
                ui.campo_data_nascimento.setDate(QDate.fromString(req[pedido]['NASCIMENTO'], "dd/MM/yyyy"))
                ui.campo_digito_ano.setText(req[pedido]['DIGITO ANO'])
                ui.campo_lista_status_3.setCurrentText("NAO")
                ui.campo_lista_status_3.setCurrentText(req[pedido]['VENDIDO POR MIM?'])
                ui.campo_lista_status_4.setCurrentText(req[pedido]['MODALIDADE'])
                ui.campo_seguranca_cnh.setText(req[pedido]['CODIGO DE SEG CNH'])
                ui.campo_diretorio_pasta.setText(req[pedido]['DIRETORIO'])

            # Atualize a barra de progresso
            num_pedidos_processados += 1
            progresso = int((num_pedidos_processados / num_pedidos_total) * 100)
            ui.barra_progresso_pedido.setValue(progresso)
            QApplication.processEvents()
            ui.barra_progresso_pedido.setVisible(False)

    except Exception as e:
        ui.barra_progresso_pedido.setVisible(False)
        ui.campo_novo_noBd.setText("")
        return
        
def pegar_valor_tabela(event):
   #evento disparado ao dar double click

    req = ref.get()
    item = ui.tableWidget.currentItem()  # Obtenha o item selecionado
    try:
        if item is not None:
            coluna = item.column()
            valor = item.text()

            if coluna == 0 :    
                   
                for id in req:
                    if req[id]["PEDIDO"] == valor: 
                        limpar_campos()                     
                        ui.tabWidget.setCurrentIndex(0)
                        
                        status = req[id]["STATUS"]  
                        ui.campo_lista_status.setCurrentText(status)
                        ui.campo_certificado.setText(req[id]["TIPO"])    
                        
                        data_nula = QDate(2000, 1, 1)  
                        ui.campo_data_nascimento.setDate(data_nula)
                        ui.campo_nome.setText(req[id]["NOME"]) 
                        ui.campo_rg.setText(req[id]["RG"])   
                        ui.campo_cpf.setText(req[id]["CPF"])   
                        ui.campo_cnh.setText(req[id]["CNH"])  
                        ui.campo_cnpj.setText(req[id]["CNPJ"])  
                        ui.campo_email.setText(req[id]["EMAIL"])  
                        ui.campo_data_nascimento.setDate(QDate.fromString(req[id]["NASCIMENTO"], "dd/MM/yyyy"))  
                        ui.campo_pedido.setText(req[id]["PEDIDO"]) 
                        ui.campo_data_agendamento.setDate(QDate.fromString(req[id]["DATA"], "dd/MM/yyyy"))
                        ui.campo_hora_agendamento.setTime(QTime.fromString(req[id]["HORA"], "hh:mm"))
                        ui.campo_digito_ano.setText(req[id]["DIGITO ANO"])
                        ui.campo_lista_status_3.setCurrentText("NAO")
                        ui.campo_lista_status_3.setCurrentText(req[id]['VENDIDO POR MIM?'])
                        ui.campo_lista_status_4.setCurrentText(req[id]['MODALIDADE'])
                        ui.campo_pedido.setReadOnly(True)
                        ui.campo_seguranca_cnh.setText(req[id]['CODIGO DE SEG CNH'])
                        ui.campo_nome_mae.setText(req[id]['MAE'])
                        ui.campo_novo_noBd.setText("✅")
                        ui.campo_diretorio_pasta.setText(req[id]['DIRETORIO'])
                        return
                        
    except Exception as e:
        pass

def mesclar_pdf():
    try:
        labels = [ui.label_PDF1, ui.label_PDF2, ui.label_PDF3, ui.label_PDF4, ui.label_PDF5]

        quantidade_labels_com_imagem = 0

        # Verifique cada label na lista
        for label in labels:
            # Obtenha o pixmap da label
            pixmap = label.pixmap()

            # Verifique se a label tem um pixmap e se o pixmap não é nulo (ou seja, se a label tem uma imagem)
            if pixmap is not None and not pixmap.isNull():
                quantidade_labels_com_imagem += 1

        # Agora, 'quantidade_labels_com_imagem' contém o número de labels com imagem

        if quantidade_labels_com_imagem == 0:
            notificacao = Notification(app_id="Arquivo não gerado", title="", msg="Selecione os arquivos!")
            notificacao.show()
            return

        # Criar um objeto PdfMerger para mesclar os PDFs
        pdf_merger = PyPDF2.PdfMerger()

        # Lista de caminhos dos PDFs armazenados nas labels
        file_paths = [label.pdf_path for label in labels if hasattr(label, 'pdf_path')]

        # Verificar se há caminhos de PDF válidos na lista antes de adicionar ao PdfMerger
        for path in file_paths:
            if path:
                pdf_merger.append(path)

        # Abrir o explorador de arquivos para selecionar o local de salvamento
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")],
                                                title="Local de download")

        # Verificar se o usuário selecionou um local de salvamento
        if not save_path:
            return

        # Configurar a barra de progresso
        ui.barra_progresso_mesclar.setMaximum(len(file_paths))
        ui.barra_progresso_mesclar.setValue(0)
        ui.barra_progresso_mesclar.setVisible(True)

        # Mesclar os arquivos PDF
        for i, path in enumerate(file_paths):
            # Atualizar a barra de progresso
            ui.barra_progresso_mesclar.setValue(i + 1)
            time.sleep(0.1)
            QApplication.processEvents()

        # Salvar o arquivo mesclado no local especificado
        with open(save_path, 'wb') as merged_pdf:
            pdf_merger.write(merged_pdf)

        for label in labels:
            if hasattr(label, 'setPixmap'):
                label.setPixmap(QtGui.QPixmap())  # Define o pixmap como nulo


        # Informar ao usuário que a mesclagem foi concluída
        ui.barra_progresso_mesclar.setVisible(False)
        limpar_label_pdf()
        notificacao = Notification(app_id="Concluído", title="", msg="Os arquivos PDF foram mesclados com sucesso!")
        notificacao.show()
    except:
        limpar_label_pdf()
        ui.barra_progresso_mesclar.setVisible(False)
        return

def converter_jpg_pdf():
    try:
        # Abre o explorer para selecionar múltiplos arquivos
        image_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.jpeg *.png")], title="Converter JPG/PNG > PDF")

        # Verificar se o usuário selecionou algum arquivo de imagem
        if not image_paths:
            return

        # Iterar sobre cada caminho de imagem selecionado
        for image_path in image_paths:
            # Extrair o nome do arquivo (sem a extensão) do caminho
            nome_do_arquivo, _ = os.path.splitext(os.path.basename(image_path))

            # Abrir o explorador de arquivos para selecionar o local de salvamento do PDF
            save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")], initialfile=nome_do_arquivo, title="Local de download")

            # Verificar se o usuário selecionou um local de salvamento
            if not save_path:
                continue  # Continue para o próximo arquivo se o usuário não selecionar um local

            # Carregar a imagem
            with Image.open(image_path) as img:
                # Definir o tamanho padrão
                target_width, target_height = 1920, 1080

                # Calcular as dimensões da imagem mantendo o aspect ratio
                aspect_ratio = img.width / img.height
                if aspect_ratio > 1:
                    new_width = target_width
                    new_height = int(target_width / aspect_ratio)
                else:
                    new_width = int(target_height * aspect_ratio)
                    new_height = target_height

                # Criar um arquivo PDF com as dimensões calculadas
                c = canvas.Canvas(save_path, pagesize=(new_width, new_height))

                # Desenhar a imagem no PDF mantendo o aspect ratio
                c.drawImage(image_path, 0, 0, width=new_width, height=new_height)

                c.save()

            # Limpar as variáveis que contêm o PDF e a imagem
            del img
            del c

        # Atualizar a barra de progresso para refletir a conclusão do processo
        ui.barra_progresso_jpg.setVisible(True)
        ui.barra_progresso_jpg.setValue(100)
        QApplication.processEvents()

        # Aguardar um curto período para a barra de progresso ser exibida antes de ocultá-la
        

        # Limpar a barra de progresso e exibir a notificação de conclusão
        ui.barra_progresso_jpg.setVisible(False)
        notificacao = Notification(app_id="Concluído", title="", msg="As imagens foram convertidas em PDF com sucesso!")
        notificacao.show()

    except Exception as e:
        # Em caso de exceção, lidar com o erro apropriado
        ui.barra_progresso_jpg.setVisible(False)
        print(f"Erro: {e}")
        return

def texto_para_pdf():
    # Obter o texto que você deseja converter em PDF (substitua esta linha pelo seu texto)
    try:
        texto = ui.campo_link_video.text()
        default_file_name = "LINK VIDEO"
        # Abrir o explorador de arquivos para selecionar o local de salvamento do PDF
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")],initialfile=default_file_name,title="Local de download")
        
        # Verificar se o usuário selecionou um local de salvamento
        if not save_path:
            return
        
        # Criar um arquivo PDF
        c = canvas.Canvas(save_path, pagesize=letter)
        
        # Definir o tamanho da fonte e a posição para começar a escrever o texto
        font_size = 14
        x, y = 20, 680  # Posição inicial
        
        # Adicionar o texto ao PDF
        c.setFont("Helvetica", font_size)
        for line in texto.split('\n'):
            c.drawString(x, y, line)
            y -= 15  # Espaçamento entre as linhas
        
        # Salvar o arquivo PDF
        c.save()
        ui.campo_link_video.setText("")
        notificacao = Notification(app_id="Concluído",title="",msg=f"Texto salvo com sucesso!")
        notificacao.show()
    except Exception as e:
        notificacao = Notification(app_id="Erro",title="",msg=f"Feche o arquivo PDF!")
        notificacao.show()

def carregar_pdf_na_label():
    labels = [ui.label_PDF1, ui.label_PDF2, ui.label_PDF3, ui.label_PDF4, ui.label_PDF5]
    options = {}
    options['filetypes'] = [('Arquivos PDF', '*.pdf'), ('Todos os Arquivos', '*.*')]
    options['multiple'] = True

    file_paths = filedialog.askopenfilenames(**options)

    if file_paths:
        labels = [ui.label_PDF1, ui.label_PDF2, ui.label_PDF3, ui.label_PDF4, ui.label_PDF5]

        for i, pdf_path in enumerate(file_paths):
            if i < len(labels):
                pdf_document = fitz.open(pdf_path)
                pdf_page = pdf_document.load_page(0)
                pdf_image = pdf_page.get_pixmap()

                # Redimensiona a imagem para caber no tamanho da label
                image = QImage(pdf_image.samples, pdf_image.width, pdf_image.height, pdf_image.stride, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(image.scaled(labels[i].width(), labels[i].height(), Qt.KeepAspectRatio))

                # Exibe a imagem na label
                labels[i].setPixmap(pixmap)

                # Armazena o caminho do PDF na label
                labels[i].pdf_path = pdf_path

def limpar_label_pdf():
    ui.label_PDF1.clear()
    ui.label_PDF2.clear()
    ui.label_PDF3.clear()
    ui.label_PDF4.clear()
    ui.label_PDF5.clear()
    ui.label_PDF1.pdf_path = None
    ui.label_PDF2.pdf_path = None
    ui.label_PDF3.pdf_path = None
    ui.label_PDF4.pdf_path = None
    ui.label_PDF5.pdf_path = None

def on_close_event(event):

    
    result = QMessageBox.question(janela, "Confirmação", "Você realmente deseja sair?", QMessageBox.Yes | QMessageBox.No)
    
    if result == QMessageBox.Yes:
        try:
            tela_cnpj.close()
            event.accept()  # Aceita o evento de fechamento
        except:
            event.accept()  
            
    else:
        event.ignore()  # Ignora o evento de fechamento
    
class Ui_janela(object):
    def setupUi(self, janela):
        janela.setObjectName("janela")
        janela.resize(611, 607)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        janela.setPalette(palette)
        janela.setAutoFillBackground(False)
        janela.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(janela)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 0, 591, 561))
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setObjectName("tabWidget")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.campo_lista_status = QtWidgets.QComboBox(self.tab_5)
        self.campo_lista_status.setGeometry(QtCore.QRect(390, 130, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.campo_lista_status.setFont(font)
        self.campo_lista_status.setStyleSheet("")
        self.campo_lista_status.setEditable(False)
        self.campo_lista_status.setObjectName("campo_lista_status")
        self.campo_lista_status.addItem("")
        self.campo_lista_status.addItem("")
        self.campo_lista_status.addItem("")
        self.campo_lista_status.addItem("")
        self.label = QtWidgets.QLabel(self.tab_5)
        self.label.setGeometry(QtCore.QRect(10, 10, 81, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab_5)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 241, 16))
        self.label_2.setObjectName("label_2")
        self.campo_data_agendamento = QtWidgets.QDateEdit(self.tab_5)
        self.campo_data_agendamento.setGeometry(QtCore.QRect(310, 30, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_data_agendamento.setFont(font)
        self.campo_data_agendamento.setStyleSheet("")
        self.campo_data_agendamento.setObjectName("campo_data_agendamento")
        self.label_17 = QtWidgets.QLabel(self.tab_5)
        self.label_17.setGeometry(QtCore.QRect(390, 110, 101, 16))
        self.label_17.setObjectName("label_17")
        self.campo_certificado = QtWidgets.QLineEdit(self.tab_5)
        self.campo_certificado.setGeometry(QtCore.QRect(10, 80, 561, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.campo_certificado.setFont(font)
        self.campo_certificado.setObjectName("campo_certificado")
        self.campo_pedido = QtWidgets.QLineEdit(self.tab_5)
        self.campo_pedido.setGeometry(QtCore.QRect(10, 30, 221, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.campo_pedido.setFont(font)
        self.campo_pedido.setText("")
        self.campo_pedido.setObjectName("campo_pedido")
        self.campo_hora_agendamento = QtWidgets.QTimeEdit(self.tab_5)
        self.campo_hora_agendamento.setGeometry(QtCore.QRect(460, 30, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_hora_agendamento.setFont(font)
        self.campo_hora_agendamento.setStyleSheet("")
        self.campo_hora_agendamento.setObjectName("campo_hora_agendamento")
        self.label_4 = QtWidgets.QLabel(self.tab_5)
        self.label_4.setGeometry(QtCore.QRect(460, 10, 111, 16))
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(self.tab_5)
        self.label_3.setGeometry(QtCore.QRect(330, 10, 131, 20))
        self.label_3.setObjectName("label_3")
        self.campo_novo_noBd = QtWidgets.QLabel(self.tab_5)
        self.campo_novo_noBd.setGeometry(QtCore.QRect(240, 30, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(16)
        self.campo_novo_noBd.setFont(font)
        self.campo_novo_noBd.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.campo_novo_noBd.setText("")
        self.campo_novo_noBd.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_novo_noBd.setObjectName("campo_novo_noBd")
        self.campo_lista_status_3 = QtWidgets.QComboBox(self.tab_5)
        self.campo_lista_status_3.setGeometry(QtCore.QRect(10, 130, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.campo_lista_status_3.setFont(font)
        self.campo_lista_status_3.setStyleSheet("")
        self.campo_lista_status_3.setEditable(False)
        self.campo_lista_status_3.setObjectName("campo_lista_status_3")
        self.campo_lista_status_3.addItem("")
        self.campo_lista_status_3.addItem("")
        self.label_22 = QtWidgets.QLabel(self.tab_5)
        self.label_22.setGeometry(QtCore.QRect(10, 110, 151, 16))
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.tab_5)
        self.label_23.setGeometry(QtCore.QRect(200, 110, 101, 16))
        self.label_23.setObjectName("label_23")
        self.campo_lista_status_4 = QtWidgets.QComboBox(self.tab_5)
        self.campo_lista_status_4.setGeometry(QtCore.QRect(200, 130, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.campo_lista_status_4.setFont(font)
        self.campo_lista_status_4.setStyleSheet("")
        self.campo_lista_status_4.setEditable(False)
        self.campo_lista_status_4.setObjectName("campo_lista_status_4")
        self.campo_lista_status_4.addItem("")
        self.campo_lista_status_4.setItemText(0, "")
        self.campo_lista_status_4.addItem("")
        self.campo_lista_status_4.addItem("")
        self.botao_terminar = QtWidgets.QPushButton(self.tab_5)
        self.botao_terminar.setGeometry(QtCore.QRect(470, 500, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.botao_terminar.setFont(font)
        self.botao_terminar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_terminar.setStyleSheet("border-radius:10px;\n"
"background-color:rgb(73, 218, 107);")
        self.botao_terminar.setObjectName("botao_terminar")
        self.botao_salvar = QtWidgets.QPushButton(self.tab_5)
        self.botao_salvar.setGeometry(QtCore.QRect(380, 500, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.botao_salvar.setFont(font)
        self.botao_salvar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_salvar.setStyleSheet("border-radius:10px;\n"
"background-color:rgb(0, 180, 210);")
        self.botao_salvar.setObjectName("botao_salvar")
        self.barra_progresso_pedido = QtWidgets.QProgressBar(self.tab_5)
        self.barra_progresso_pedido.setGeometry(QtCore.QRect(10, 30, 221, 6))
        self.barra_progresso_pedido.setProperty("value", 0)
        self.barra_progresso_pedido.setAlignment(QtCore.Qt.AlignCenter)
        self.barra_progresso_pedido.setFormat("")
        self.barra_progresso_pedido.setObjectName("barra_progresso_pedido")
        self.label_11 = QtWidgets.QLabel(self.tab_5)
        self.label_11.setGeometry(QtCore.QRect(10, 230, 81, 16))
        self.label_11.setObjectName("label_11")
        self.botao_dados_cnpj = QtWidgets.QPushButton(self.tab_5)
        self.botao_dados_cnpj.setGeometry(QtCore.QRect(540, 450, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_dados_cnpj.setFont(font)
        self.botao_dados_cnpj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_dados_cnpj.setObjectName("botao_dados_cnpj")
        self.label_12 = QtWidgets.QLabel(self.tab_5)
        self.label_12.setGeometry(QtCore.QRect(10, 480, 131, 16))
        self.label_12.setObjectName("label_12")
        self.botao_consulta_rg = QtWidgets.QPushButton(self.tab_5)
        self.botao_consulta_rg.setGeometry(QtCore.QRect(540, 300, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_rg.setFont(font)
        self.botao_consulta_rg.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_rg.setObjectName("botao_consulta_rg")
        self.label_13 = QtWidgets.QLabel(self.tab_5)
        self.label_13.setGeometry(QtCore.QRect(170, 480, 61, 16))
        self.label_13.setObjectName("label_13")
        self.campo_cnpj = QtWidgets.QLineEdit(self.tab_5)
        self.campo_cnpj.setGeometry(QtCore.QRect(10, 450, 481, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_cnpj.setFont(font)
        self.campo_cnpj.setText("")
        self.campo_cnpj.setPlaceholderText("")
        self.campo_cnpj.setObjectName("campo_cnpj")
        self.label_18 = QtWidgets.QLabel(self.tab_5)
        self.label_18.setGeometry(QtCore.QRect(10, 380, 141, 20))
        self.label_18.setObjectName("label_18")
        self.campo_cpf = QtWidgets.QLineEdit(self.tab_5)
        self.campo_cpf.setGeometry(QtCore.QRect(10, 300, 241, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_cpf.setFont(font)
        self.campo_cpf.setText("")
        self.campo_cpf.setPlaceholderText("")
        self.campo_cpf.setObjectName("campo_cpf")
        self.label_10 = QtWidgets.QLabel(self.tab_5)
        self.label_10.setGeometry(QtCore.QRect(300, 280, 81, 16))
        self.label_10.setObjectName("label_10")
        self.label_14 = QtWidgets.QLabel(self.tab_5)
        self.label_14.setGeometry(QtCore.QRect(10, 430, 171, 16))
        self.label_14.setObjectName("label_14")
        self.campo_data_nascimento = QtWidgets.QDateEdit(self.tab_5)
        self.campo_data_nascimento.setGeometry(QtCore.QRect(10, 500, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_data_nascimento.setFont(font)
        self.campo_data_nascimento.setStyleSheet("")
        self.campo_data_nascimento.setObjectName("campo_data_nascimento")
        self.campo_nome = QtWidgets.QLineEdit(self.tab_5)
        self.campo_nome.setGeometry(QtCore.QRect(10, 200, 521, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_nome.setFont(font)
        self.campo_nome.setText("")
        self.campo_nome.setPlaceholderText("")
        self.campo_nome.setObjectName("campo_nome")
        self.botao_consulta_cnpj = QtWidgets.QPushButton(self.tab_5)
        self.botao_consulta_cnpj.setGeometry(QtCore.QRect(500, 450, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_cnpj.setFont(font)
        self.botao_consulta_cnpj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_cnpj.setObjectName("botao_consulta_cnpj")
        self.botao_consulta_cnh = QtWidgets.QPushButton(self.tab_5)
        self.botao_consulta_cnh.setGeometry(QtCore.QRect(540, 350, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_cnh.setFont(font)
        self.botao_consulta_cnh.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_cnh.setObjectName("botao_consulta_cnh")
        self.label_24 = QtWidgets.QLabel(self.tab_5)
        self.label_24.setGeometry(QtCore.QRect(10, 180, 201, 16))
        self.label_24.setObjectName("label_24")
        self.campo_cnh = QtWidgets.QLineEdit(self.tab_5)
        self.campo_cnh.setGeometry(QtCore.QRect(10, 350, 281, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_cnh.setFont(font)
        self.campo_cnh.setText("")
        self.campo_cnh.setObjectName("campo_cnh")
        self.campo_digito_ano = QtWidgets.QLineEdit(self.tab_5)
        self.campo_digito_ano.setGeometry(QtCore.QRect(170, 500, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.campo_digito_ano.setFont(font)
        self.campo_digito_ano.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_digito_ano.setObjectName("campo_digito_ano")
        self.campo_nome_mae = QtWidgets.QLineEdit(self.tab_5)
        self.campo_nome_mae.setGeometry(QtCore.QRect(10, 400, 561, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_nome_mae.setFont(font)
        self.campo_nome_mae.setStyleSheet("")
        self.campo_nome_mae.setText("")
        self.campo_nome_mae.setObjectName("campo_nome_mae")
        self.label_6 = QtWidgets.QLabel(self.tab_5)
        self.label_6.setGeometry(QtCore.QRect(10, 280, 81, 16))
        self.label_6.setObjectName("label_6")
        self.label_15 = QtWidgets.QLabel(self.tab_5)
        self.label_15.setGeometry(QtCore.QRect(10, 330, 61, 20))
        self.label_15.setObjectName("label_15")
        self.botao_consulta_cpf = QtWidgets.QPushButton(self.tab_5)
        self.botao_consulta_cpf.setGeometry(QtCore.QRect(260, 300, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_cpf.setFont(font)
        self.botao_consulta_cpf.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_cpf.setObjectName("botao_consulta_cpf")
        self.botao_pasta_cliente = QtWidgets.QPushButton(self.tab_5)
        self.botao_pasta_cliente.setGeometry(QtCore.QRect(540, 200, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_pasta_cliente.setFont(font)
        self.botao_pasta_cliente.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_pasta_cliente.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.botao_pasta_cliente.setObjectName("botao_pasta_cliente")
        self.campo_email = QtWidgets.QLineEdit(self.tab_5)
        self.campo_email.setGeometry(QtCore.QRect(10, 250, 561, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.campo_email.setFont(font)
        self.campo_email.setText("")
        self.campo_email.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.campo_email.setPlaceholderText("")
        self.campo_email.setObjectName("campo_email")
        self.campo_rg = QtWidgets.QLineEdit(self.tab_5)
        self.campo_rg.setGeometry(QtCore.QRect(300, 300, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_rg.setFont(font)
        self.campo_rg.setPlaceholderText("")
        self.campo_rg.setObjectName("campo_rg")
        self.label_16 = QtWidgets.QLabel(self.tab_5)
        self.label_16.setGeometry(QtCore.QRect(300, 330, 201, 20))
        self.label_16.setObjectName("label_16")
        self.campo_seguranca_cnh = QtWidgets.QLineEdit(self.tab_5)
        self.campo_seguranca_cnh.setGeometry(QtCore.QRect(300, 350, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_seguranca_cnh.setFont(font)
        self.campo_seguranca_cnh.setObjectName("campo_seguranca_cnh")
        self.campo_diretorio_pasta = QtWidgets.QLineEdit(self.tab_5)
        self.campo_diretorio_pasta.setEnabled(False)
        self.campo_diretorio_pasta.setGeometry(QtCore.QRect(10, 540, 561, 20))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_diretorio_pasta.setFont(font)
        self.campo_diretorio_pasta.setText("")
        self.campo_diretorio_pasta.setPlaceholderText("")
        self.campo_diretorio_pasta.setObjectName("campo_diretorio_pasta")
        self.campo_lista_status.raise_()
        self.campo_data_agendamento.raise_()
        self.label_17.raise_()
        self.campo_certificado.raise_()
        self.campo_pedido.raise_()
        self.campo_hora_agendamento.raise_()
        self.label_4.raise_()
        self.label_3.raise_()
        self.campo_novo_noBd.raise_()
        self.campo_lista_status_3.raise_()
        self.label_22.raise_()
        self.campo_lista_status_4.raise_()
        self.botao_terminar.raise_()
        self.botao_salvar.raise_()
        self.label_2.raise_()
        self.label.raise_()
        self.label_23.raise_()
        self.barra_progresso_pedido.raise_()
        self.label_11.raise_()
        self.botao_dados_cnpj.raise_()
        self.label_12.raise_()
        self.botao_consulta_rg.raise_()
        self.label_13.raise_()
        self.campo_cnpj.raise_()
        self.label_18.raise_()
        self.campo_cpf.raise_()
        self.label_10.raise_()
        self.label_14.raise_()
        self.campo_data_nascimento.raise_()
        self.campo_nome.raise_()
        self.botao_consulta_cnpj.raise_()
        self.botao_consulta_cnh.raise_()
        self.label_24.raise_()
        self.campo_cnh.raise_()
        self.campo_digito_ano.raise_()
        self.campo_nome_mae.raise_()
        self.label_6.raise_()
        self.label_15.raise_()
        self.botao_consulta_cpf.raise_()
        self.botao_pasta_cliente.raise_()
        self.campo_email.raise_()
        self.campo_rg.raise_()
        self.label_16.raise_()
        self.campo_seguranca_cnh.raise_()
        self.campo_diretorio_pasta.raise_()
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_6)
        self.groupBox_5.setGeometry(QtCore.QRect(10, 0, 561, 101))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.groupBox_5.setFont(font)
        self.groupBox_5.setObjectName("groupBox_5")
        self.campo_data_de = QtWidgets.QDateEdit(self.groupBox_5)
        self.campo_data_de.setGeometry(QtCore.QRect(10, 40, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.campo_data_de.setFont(font)
        self.campo_data_de.setStyleSheet("")
        self.campo_data_de.setObjectName("campo_data_de")
        self.label_19 = QtWidgets.QLabel(self.groupBox_5)
        self.label_19.setGeometry(QtCore.QRect(10, 20, 81, 16))
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.groupBox_5)
        self.label_20.setGeometry(QtCore.QRect(160, 20, 81, 16))
        self.label_20.setObjectName("label_20")
        self.campo_data_ate = QtWidgets.QDateEdit(self.groupBox_5)
        self.campo_data_ate.setGeometry(QtCore.QRect(160, 40, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.campo_data_ate.setFont(font)
        self.campo_data_ate.setStyleSheet("")
        self.campo_data_ate.setObjectName("campo_data_ate")
        self.label_21 = QtWidgets.QLabel(self.groupBox_5)
        self.label_21.setGeometry(QtCore.QRect(300, 20, 81, 16))
        self.label_21.setObjectName("label_21")
        self.campo_lista_status_2 = QtWidgets.QComboBox(self.groupBox_5)
        self.campo_lista_status_2.setGeometry(QtCore.QRect(300, 40, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.campo_lista_status_2.setFont(font)
        self.campo_lista_status_2.setStyleSheet("")
        self.campo_lista_status_2.setEditable(False)
        self.campo_lista_status_2.setObjectName("campo_lista_status_2")
        self.campo_lista_status_2.addItem("")
        self.campo_lista_status_2.addItem("")
        self.campo_lista_status_2.addItem("")
        self.campo_lista_status_2.addItem("")
        self.campo_lista_status_2.addItem("")
        self.botao_consultar = QtWidgets.QPushButton(self.groupBox_5)
        self.botao_consultar.setGeometry(QtCore.QRect(480, 40, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.botao_consultar.setFont(font)
        self.botao_consultar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consultar.setStyleSheet("")
        self.botao_consultar.setObjectName("botao_consultar")
        self.barra_progresso_consulta = QtWidgets.QProgressBar(self.groupBox_5)
        self.barra_progresso_consulta.setGeometry(QtCore.QRect(10, 80, 541, 8))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        self.barra_progresso_consulta.setFont(font)
        self.barra_progresso_consulta.setProperty("value", 0)
        self.barra_progresso_consulta.setAlignment(QtCore.Qt.AlignCenter)
        self.barra_progresso_consulta.setFormat("")
        self.barra_progresso_consulta.setObjectName("barra_progresso_consulta")
        self.tableWidget = QtWidgets.QTableWidget(self.tab_6)
        self.tableWidget.setGeometry(QtCore.QRect(10, 110, 561, 381))
        self.tableWidget.setMinimumSize(QtCore.QSize(561, 0))
        self.tableWidget.setMaximumSize(QtCore.QSize(750, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.tableWidget.setFont(font)
        self.tableWidget.setAutoScrollMargin(16)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.botao_procurar = QtWidgets.QPushButton(self.tab_6)
        self.botao_procurar.setGeometry(QtCore.QRect(440, 500, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.botao_procurar.setFont(font)
        self.botao_procurar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_procurar.setStyleSheet("border-radius:10px;\n"
"background-color:rgb(73, 218, 107);\n"
"")
        self.botao_procurar.setObjectName("botao_procurar")
        self.label_quantidade_bd = QtWidgets.QLabel(self.tab_6)
        self.label_quantidade_bd.setGeometry(QtCore.QRect(200, 500, 221, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(10)
        self.label_quantidade_bd.setFont(font)
        self.label_quantidade_bd.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_quantidade_bd.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_quantidade_bd.setText("")
        self.label_quantidade_bd.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_quantidade_bd.setObjectName("label_quantidade_bd")
        self.tabWidget.addTab(self.tab_6, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 20, 571, 91))
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setGeometry(QtCore.QRect(10, 30, 181, 16))
        self.label_7.setObjectName("label_7")
        self.botao_transf_link_PDF = QtWidgets.QPushButton(self.groupBox_3)
        self.botao_transf_link_PDF.setGeometry(QtCore.QRect(380, 10, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.botao_transf_link_PDF.setFont(font)
        self.botao_transf_link_PDF.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_transf_link_PDF.setObjectName("botao_transf_link_PDF")
        self.campo_link_video = QtWidgets.QLineEdit(self.groupBox_3)
        self.campo_link_video.setGeometry(QtCore.QRect(10, 50, 551, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_link_video.setFont(font)
        self.campo_link_video.setText("")
        self.campo_link_video.setPlaceholderText("")
        self.campo_link_video.setObjectName("campo_link_video")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(10, 120, 571, 301))
        self.groupBox.setObjectName("groupBox")
        self.botao_agrupar_PDF = QtWidgets.QPushButton(self.groupBox)
        self.botao_agrupar_PDF.setGeometry(QtCore.QRect(210, 40, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.botao_agrupar_PDF.setFont(font)
        self.botao_agrupar_PDF.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_agrupar_PDF.setStyleSheet("")
        self.botao_agrupar_PDF.setObjectName("botao_agrupar_PDF")
        self.label_PDF1 = QtWidgets.QLabel(self.groupBox)
        self.label_PDF1.setGeometry(QtCore.QRect(10, 120, 101, 121))
        self.label_PDF1.setStyleSheet("")
        self.label_PDF1.setText("")
        self.label_PDF1.setObjectName("label_PDF1")
        self.label_PDF3 = QtWidgets.QLabel(self.groupBox)
        self.label_PDF3.setGeometry(QtCore.QRect(230, 120, 101, 121))
        self.label_PDF3.setStyleSheet("")
        self.label_PDF3.setText("")
        self.label_PDF3.setObjectName("label_PDF3")
        self.label_PDF2 = QtWidgets.QLabel(self.groupBox)
        self.label_PDF2.setGeometry(QtCore.QRect(120, 120, 101, 121))
        self.label_PDF2.setStyleSheet("")
        self.label_PDF2.setText("")
        self.label_PDF2.setObjectName("label_PDF2")
        self.label_PDF5 = QtWidgets.QLabel(self.groupBox)
        self.label_PDF5.setGeometry(QtCore.QRect(450, 120, 101, 121))
        self.label_PDF5.setStyleSheet("")
        self.label_PDF5.setText("")
        self.label_PDF5.setObjectName("label_PDF5")
        self.label_PDF4 = QtWidgets.QLabel(self.groupBox)
        self.label_PDF4.setGeometry(QtCore.QRect(340, 120, 101, 121))
        self.label_PDF4.setStyleSheet("")
        self.label_PDF4.setText("")
        self.label_PDF4.setObjectName("label_PDF4")
        self.botao_selecionar_arquivos_mesclar = QtWidgets.QPushButton(self.groupBox)
        self.botao_selecionar_arquivos_mesclar.setGeometry(QtCore.QRect(10, 40, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.botao_selecionar_arquivos_mesclar.setFont(font)
        self.botao_selecionar_arquivos_mesclar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_selecionar_arquivos_mesclar.setStyleSheet("")
        self.botao_selecionar_arquivos_mesclar.setObjectName("botao_selecionar_arquivos_mesclar")
        self.botao_limpar_PDF = QtWidgets.QPushButton(self.groupBox)
        self.botao_limpar_PDF.setGeometry(QtCore.QRect(400, 40, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.botao_limpar_PDF.setFont(font)
        self.botao_limpar_PDF.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_limpar_PDF.setStyleSheet("")
        self.botao_limpar_PDF.setObjectName("botao_limpar_PDF")
        self.barra_progresso_mesclar = QtWidgets.QProgressBar(self.groupBox)
        self.barra_progresso_mesclar.setGeometry(QtCore.QRect(10, 280, 551, 8))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.barra_progresso_mesclar.setFont(font)
        self.barra_progresso_mesclar.setProperty("value", 0)
        self.barra_progresso_mesclar.setAlignment(QtCore.Qt.AlignCenter)
        self.barra_progresso_mesclar.setFormat("")
        self.barra_progresso_mesclar.setObjectName("barra_progresso_mesclar")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 430, 571, 101))
        self.groupBox_2.setObjectName("groupBox_2")
        self.botao_converter_jpgPDF = QtWidgets.QPushButton(self.groupBox_2)
        self.botao_converter_jpgPDF.setGeometry(QtCore.QRect(190, 20, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.botao_converter_jpgPDF.setFont(font)
        self.botao_converter_jpgPDF.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_converter_jpgPDF.setStyleSheet("")
        self.botao_converter_jpgPDF.setObjectName("botao_converter_jpgPDF")
        self.barra_progresso_jpg = QtWidgets.QProgressBar(self.groupBox_2)
        self.barra_progresso_jpg.setGeometry(QtCore.QRect(10, 70, 551, 8))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.barra_progresso_jpg.setFont(font)
        self.barra_progresso_jpg.setProperty("value", 0)
        self.barra_progresso_jpg.setAlignment(QtCore.Qt.AlignCenter)
        self.barra_progresso_jpg.setFormat("")
        self.barra_progresso_jpg.setObjectName("barra_progresso_jpg")
        self.tabWidget.addTab(self.tab, "")
        janela.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(janela)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 611, 21))
        self.menubar.setObjectName("menubar")
        janela.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(janela)
        self.statusbar.setObjectName("statusbar")
        janela.setStatusBar(self.statusbar)

        self.retranslateUi(janela)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(janela)
        janela.setTabOrder(self.campo_pedido, self.campo_data_agendamento)
        janela.setTabOrder(self.campo_data_agendamento, self.campo_hora_agendamento)
        janela.setTabOrder(self.campo_hora_agendamento, self.campo_certificado)
        janela.setTabOrder(self.campo_certificado, self.campo_lista_status_3)
        janela.setTabOrder(self.campo_lista_status_3, self.campo_lista_status_4)
        janela.setTabOrder(self.campo_lista_status_4, self.campo_lista_status)
        janela.setTabOrder(self.campo_lista_status, self.campo_nome)
        janela.setTabOrder(self.campo_nome, self.campo_email)
        janela.setTabOrder(self.campo_email, self.campo_cpf)
        janela.setTabOrder(self.campo_cpf, self.campo_rg)
        janela.setTabOrder(self.campo_rg, self.campo_cnh)
        janela.setTabOrder(self.campo_cnh, self.campo_seguranca_cnh)
        janela.setTabOrder(self.campo_seguranca_cnh, self.campo_nome_mae)
        janela.setTabOrder(self.campo_nome_mae, self.campo_cnpj)
        janela.setTabOrder(self.campo_cnpj, self.campo_data_nascimento)
        janela.setTabOrder(self.campo_data_nascimento, self.campo_digito_ano)
        janela.setTabOrder(self.campo_digito_ano, self.botao_procurar)
        janela.setTabOrder(self.botao_procurar, self.campo_data_ate)
        janela.setTabOrder(self.campo_data_ate, self.tableWidget)
        janela.setTabOrder(self.tableWidget, self.botao_terminar)
        janela.setTabOrder(self.botao_terminar, self.campo_link_video)
        janela.setTabOrder(self.campo_link_video, self.botao_dados_cnpj)
        janela.setTabOrder(self.botao_dados_cnpj, self.botao_consulta_rg)
        janela.setTabOrder(self.botao_consulta_rg, self.botao_salvar)
        janela.setTabOrder(self.botao_salvar, self.botao_selecionar_arquivos_mesclar)
        janela.setTabOrder(self.botao_selecionar_arquivos_mesclar, self.campo_data_de)
        janela.setTabOrder(self.campo_data_de, self.botao_transf_link_PDF)
        janela.setTabOrder(self.botao_transf_link_PDF, self.botao_consulta_cnpj)
        janela.setTabOrder(self.botao_consulta_cnpj, self.botao_consulta_cnh)
        janela.setTabOrder(self.botao_consulta_cnh, self.botao_converter_jpgPDF)
        janela.setTabOrder(self.botao_converter_jpgPDF, self.campo_lista_status_2)
        janela.setTabOrder(self.campo_lista_status_2, self.tabWidget)
        janela.setTabOrder(self.tabWidget, self.botao_consulta_cpf)
        janela.setTabOrder(self.botao_consulta_cpf, self.botao_pasta_cliente)
        janela.setTabOrder(self.botao_pasta_cliente, self.botao_agrupar_PDF)
        janela.setTabOrder(self.botao_agrupar_PDF, self.botao_limpar_PDF)
        janela.setTabOrder(self.botao_limpar_PDF, self.botao_consultar)
        janela.setTabOrder(self.botao_consultar, self.campo_diretorio_pasta)

    def retranslateUi(self, janela):
        _translate = QtCore.QCoreApplication.translate
        janela.setWindowTitle(_translate("janela", "MainWindow"))
        self.campo_lista_status.setItemText(0, _translate("janela", "DIGITAÇÃO"))
        self.campo_lista_status.setItemText(1, _translate("janela", "VERIFICAÇÃO"))
        self.campo_lista_status.setItemText(2, _translate("janela", "APROVADO"))
        self.campo_lista_status.setItemText(3, _translate("janela", "CANCELADO"))
        self.label.setText(_translate("janela", "🌟 PEDIDO"))
        self.label_2.setText(_translate("janela", "🌟 TIPO CERTIFICADO"))
        self.label_17.setText(_translate("janela", "🌟 STATUS"))
        self.label_4.setText(_translate("janela", "🌟 HORA AGENDA"))
        self.label_3.setText(_translate("janela", "🌟 DATA AGENDA"))
        self.campo_lista_status_3.setItemText(0, _translate("janela", "NAO"))
        self.campo_lista_status_3.setItemText(1, _translate("janela", "SIM"))
        self.label_22.setText(_translate("janela", "🌟 VENDA?"))
        self.label_23.setText(_translate("janela", "🌟 MODALIDADE"))
        self.campo_lista_status_4.setItemText(1, _translate("janela", "VIDEO"))
        self.campo_lista_status_4.setItemText(2, _translate("janela", "PRESENCIAL"))
        self.botao_terminar.setText(_translate("janela", "FINALIZAR"))
        self.botao_salvar.setText(_translate("janela", "SALVAR"))
        self.label_11.setText(_translate("janela", "e-MAIL"))
        self.botao_dados_cnpj.setText(_translate("janela", "📋"))
        self.label_12.setText(_translate("janela", "NASCIMENTO"))
        self.botao_consulta_rg.setText(_translate("janela", "🔍"))
        self.label_13.setText(_translate("janela", "díg ANO"))
        self.label_18.setText(_translate("janela", "NOME DA MÃE"))
        self.label_10.setText(_translate("janela", "RG"))
        self.label_14.setText(_translate("janela", "CNPJ"))
        self.botao_consulta_cnpj.setText(_translate("janela", "🔍"))
        self.botao_consulta_cnh.setText(_translate("janela", "🔍"))
        self.label_24.setText(_translate("janela", "NOME COMPLETO"))
        self.label_6.setText(_translate("janela", "CPF"))
        self.label_15.setText(_translate("janela", "CNH"))
        self.botao_consulta_cpf.setText(_translate("janela", "🔍"))
        self.botao_pasta_cliente.setText(_translate("janela", "📂"))
        self.label_16.setText(_translate("janela", "CÓDIGO DE SEGURANÇA - CNH"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("janela", "Dados pedido"))
        self.groupBox_5.setTitle(_translate("janela", "BUSCA"))
        self.label_19.setText(_translate("janela", "DE:"))
        self.label_20.setText(_translate("janela", "ATÉ:"))
        self.label_21.setText(_translate("janela", "STATUS"))
        self.campo_lista_status_2.setItemText(0, _translate("janela", "TODAS"))
        self.campo_lista_status_2.setItemText(1, _translate("janela", "DIGITAÇÃO"))
        self.campo_lista_status_2.setItemText(2, _translate("janela", "VERIFICAÇÃO"))
        self.campo_lista_status_2.setItemText(3, _translate("janela", "APROVADO"))
        self.campo_lista_status_2.setItemText(4, _translate("janela", "CANCELADO"))
        self.botao_consultar.setText(_translate("janela", "🔍"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("janela", "PEDIDO"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("janela", "NOME"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("janela", "DATA"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("janela", "HORA"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("janela", "MODALIDADE"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("janela", "STATUS"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("janela", "VENDA"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("janela", "TIPO"))
        self.botao_procurar.setText(_translate("janela", "EXPORTAR EXCEL"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("janela", "Consulta"))
        self.groupBox_3.setTitle(_translate("janela", "TRANSFORMAR  LINK DA VÍDEO-CONFERÊNCIA  EM   PDF"))
        self.label_7.setText(_translate("janela", "TEXTO"))
        self.botao_transf_link_PDF.setText(_translate("janela", "TRANSFORMAR EM PDF"))
        self.groupBox.setTitle(_translate("janela", "MESCLAR PDF - MAX 5 ARQUIVOS"))
        self.botao_agrupar_PDF.setText(_translate("janela", "MESCLAR PDF"))
        self.botao_selecionar_arquivos_mesclar.setText(_translate("janela", "SELECIONAR ARQUIVOS"))
        self.botao_limpar_PDF.setText(_translate("janela", "LIMPAR"))
        self.groupBox_2.setTitle(_translate("janela", "CONVERTER JPEG PARA PDF"))
        self.botao_converter_jpgPDF.setText(_translate("janela", "CONVERTER IMG > PDF"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("janela", "PDF"))

class TelaCNPJ(QWidget):
    def __init__(self, dados_formatados):
        super().__init__()

        self.setWindowTitle("Dados CNPJ")
        self.setGeometry(150, 150, 500, 400)  # Ajusta para 200x300

        layout = QVBoxLayout()

        self.label_usuario = QLabel("")
        self.input_usuario = QTextEdit(self)
        self.input_usuario.setPlainText(dados_formatados)  # Preenche o QTextEdit com os dados formatados
        self.input_usuario.setReadOnly(True)  # Desativa a edição

        layout.addWidget(self.label_usuario)
        layout.addWidget(self.input_usuario)

        self.setLayout(layout)

        # Configuração da fonte para o QTextEdit
        fonte = QFont("Calibri", 12)  # Substitua "Calibri" pela fonte desejada
        self.input_usuario.setFont(fonte)

        self.show()
                 
tela_cnpj = None

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    janela = QtWidgets.QMainWindow()
    ui = Ui_janela()
    ui.setupUi(janela)

    
    ui.botao_consultar.clicked.connect(preencher_tabela)
    ui.botao_terminar.clicked.connect(gravar_dados)
    ui.botao_procurar.clicked.connect(exportar_excel)
    ui.campo_cpf.editingFinished.connect(formatar_cpf)
    #ui.campo_rg.editingFinished.connect(formatar_rg)
    ui.campo_pedido.editingFinished.connect(carregar_dados)
    ui.campo_digito_ano.setReadOnly(True)
    ui.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
    ui.campo_data_nascimento.editingFinished.connect(formatar_data_nascimento)
    ui.campo_cnpj.editingFinished.connect (formatar_cnpj)
    ui.botao_consulta_cnpj.clicked.connect(procurar_cnpj)
    ui.botao_consulta_cpf.clicked.connect(procurar_cpf)
    ui.botao_consulta_cnh.clicked.connect(procurar_cnh)
    ui.botao_consulta_rg.clicked.connect(procurar_rg)
    ui.tableWidget.itemDoubleClicked.connect(pegar_valor_tabela)
    ui.botao_salvar.clicked.connect(salvar)
    ui.botao_agrupar_PDF.clicked.connect(mesclar_pdf)
    ui.botao_dados_cnpj.clicked.connect(dados_cnpj)
    ui.botao_converter_jpgPDF.clicked.connect(converter_jpg_pdf)
    ui.botao_transf_link_PDF.clicked.connect(texto_para_pdf)
    ui.botao_pasta_cliente.clicked.connect(criar_pasta_cliente)
    ui.campo_data_de.setDate(QDate.currentDate().addDays(1 - QDate.currentDate().day()))
    ui.campo_data_ate.setDate(QDate(QDate.currentDate().year(), QDate.currentDate().month(), QDate.currentDate().daysInMonth()))
    ui.botao_selecionar_arquivos_mesclar.clicked.connect(carregar_pdf_na_label)
    ui.botao_limpar_PDF.clicked.connect(limpar_label_pdf)
    ui.barra_progresso_jpg.setVisible(False)
    ui.barra_progresso_mesclar.setVisible(False)
    ui.barra_progresso_pedido.setVisible(False)
    ui.barra_progresso_consulta.setVisible(False)
    janela.closeEvent = on_close_event
   


    janela.setWindowTitle("Auxiliar Certificados")
    janela.setFixedSize(611, 590)
    janela.show()
    

    sys.exit(app.exec_())