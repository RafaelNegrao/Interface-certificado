
import datetime
import pandas as pd
import tkinter as tk
import os
import time
import requests
import PyPDF2
import fitz
from winotify import Notification
from PyQt5.QtGui import QDesktopServices,QPixmap,QImage,QFont
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem,QTableWidget,QWidget, QVBoxLayout, QLabel,QApplication,QMessageBox,QTextEdit
from PyQt5.QtCore import QDate, QTime,QUrl, Qt
from Interface import Ui_janela
from data_base import *
import firebase_admin
from firebase_admin import db


credenciais = {
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

acoes = firebase_admin.credentials.Certificate(credenciais)
firebase_admin.initialize_app(acoes, {'databaseURL':'https://bdpedidos-2078f-default-rtdb.firebaseio.com/' }) 
ref = db.reference("/")




def criar_pasta_cliente(ui):
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
        notificacao = Notification(app_id="Pasta não criada", title="", msg="",duration="short")
        notificacao.show()

def limpar_campos(ui):
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
    #ui.tableWidget.setRowCount(0)
    ui.label_quantidade_bd.setText("")
    ui.campo_nome_mae.setText("")
    ui.campo_cnh.setText("")
    ui.campo_seguranca_cnh.setText("")
    ui.campo_link_video.setText("")
    ui.campo_diretorio_pasta.setText("")
    limpar_label_pdf(ui)

def procurar_cnh(ui):
    url = QUrl("https://sso.acesso.gov.br/login?client_id=portalservicos.denatran.serpro.gov.br&authorization_id=18aa635cf94")
    QDesktopServices.openUrl(url)
    return

def procurar_oab(ui):
    url = QUrl("https://cna.oab.org.br/")
    QDesktopServices.openUrl(url)
    return

def procurar_rg(ui):
    url = QUrl("https://acertid.net.br/acertid/")
    QDesktopServices.openUrl(url)
    return

def procurar_cnpj(ui):
    cnpj = ui.campo_cnpj.text()
    url = QUrl(f"https://solucoes.receita.fazenda.gov.br/servicos/cnpjreva/Cnpjreva_Solicitacao.asp?cnpj={cnpj}")
    QDesktopServices.openUrl(url)
    url = QUrl("https://www.jucesponline.sp.gov.br/")
    QDesktopServices.openUrl(url)
    return

def dados_cnpj(ui):
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

def procurar_cpf(ui):
    
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

def formatar_cpf(ui):
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
       
def formatar_data_nascimento(ui):
    nascimento = ui.campo_data_nascimento.text()
    if not nascimento == "01/01/2000":
        ui.campo_digito_ano.setText(nascimento[6:10])
        
def formatar_cnpj(ui):
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

def salvar(ui):

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

                    notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!",duration="short")
                    notificacao.show()
                    return
                
            
                #
                novos_dados = {"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
                notificacao = Notification(app_id="Pedido",title="",msg=f"Pedido {pedido} salvo com sucesso\nStatus:{status}!",duration="short")
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

                    notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!",duration="short")
                    notificacao.show()
                    return
                #
                novos_dados = {"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
                notificacao = Notification(app_id="Pedido",title="",msg=f"Pedido {pedido} salvo com sucesso\nStatus:{status}!",duration="short")
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

            notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!",duration="short")
            notificacao.show()
            return
        
        
        #
        novos_dados = {"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
        notificacao = Notification(app_id="Pedido",title="",msg=f"Pedido {pedido} salvo com sucesso\nStatus:{status}!",duration="short")
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

            notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!",duration="short")
            notificacao.show()
            return
        #
        novos_dados = {"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
        
        notificacao = Notification(app_id="Pedido",title="",msg=f"Pedido {pedido} salvo com sucesso\nStatus:{status}!",duration="short")
        notificacao.show()

        ref.push(novos_dados)
        return

def gravar_dados(ui):
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

                    notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!",duration="short")
                    notificacao.show()
                    return
                

                #
                novos_dados = {"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
                notificacao = Notification(app_id="Pedido",title="",msg=f"Pedido {pedido} atualizado com sucesso\nStatus:{status}!",duration="short")
                notificacao.show()
                ref.child(id).update(novos_dados)
                limpar_campos(ui)
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

                    notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!",duration="short")
                    notificacao.show()
                    return
                #
                novos_dados = {"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
                notificacao = Notification(app_id="Novo pedido",title="",msg=f"Pedido {pedido} atualizado com sucesso\nStatus:{status}!",duration="short")
                notificacao.show()
                ref.child(id).update(novos_dados)
                limpar_campos(ui)
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

            notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!",duration="short")
            notificacao.show()
            return
        

        novos_dados = {"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
        notificacao = Notification(app_id="Pedido",title="",msg=f"Pedido {pedido} salvo com sucesso\nStatus:{status}!",duration="short")
        notificacao.show()
        ref.push(novos_dados)
        limpar_campos(ui)
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

            notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!",duration="short")
            notificacao.show()
            return
        #
        novos_dados = {"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
        
        notificacao = Notification(app_id="Novo pedido",title="",msg=f"Pedido {pedido} criado com sucesso\nStatus:{status}!",duration="short")
        notificacao.show()

        ref.push(novos_dados)
        limpar_campos(ui)
        return

def exportar_excel(ui):
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

def preencher_tabela(ui):
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

def carregar_dados(ui):
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
                        limpar_campos(ui)                     
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

def mesclar_pdf(ui):
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

        del file_paths
        del save_path
        pdf_merger.close()

        # Informar ao usuário que a mesclagem foi concluída
        ui.barra_progresso_mesclar.setVisible(False)
        limpar_label_pdf()
        notificacao = Notification(app_id="Concluído", title="", msg="Os arquivos PDF foram mesclados com sucesso!")
        notificacao.show()
    except:
        limpar_label_pdf(ui)
        ui.barra_progresso_mesclar.setVisible(False)
        return

def converter_jpg_pdf(ui):
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

def texto_para_pdf(ui):
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

def carregar_pdf_na_label(ui):
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

def limpar_label_pdf(ui):
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

def copiar_campo(nome_campo):
    
    match nome_campo:
        
        case 'campo_cnh':
            try:
                QApplication.clipboard().setText(ui.campo_cnh.text())
            except:
                pass
        case'campo_cnpj':
            try:
                QApplication.clipboard().setText(ui.campo_cnpj.text().replace('.','').replace('-','').replace('/',''))
            except:
                pass
        case'campo_pedido':
            try:
                QApplication.clipboard().setText(ui.campo_pedido.text())
            except:
                pass
        case'campo_cpf':
            try:
                QApplication.clipboard().setText(ui.campo_cpf.text().replace('.','').replace('-',''))
            except:
                pass
        case'campo_seguranca_cnh':
            try:
                QApplication.clipboard().setText(ui.campo_seguranca_cnh.text())
            except:
                pass
        case'campo_rg':
            try:
                QApplication.clipboard().setText(ui.campo_rg.text())
            except:
                pass
        case'campo_nome_mae':
            try:
                QApplication.clipboard().setText(ui.campo_nome_mae.text())
            except:
                pass
        case'campo_nome':
            try:
                QApplication.clipboard().setText(ui.campo_nome.text())
            except:
                pass

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


import sys
app = QtWidgets.QApplication(sys.argv)
janela = QtWidgets.QMainWindow()
ui = Ui_janela()
ui.setupUi(janela)


ui.botao_consultar.clicked.connect(lambda:preencher_tabela(ui))
ui.botao_terminar.clicked.connect(lambda:gravar_dados(ui))
ui.botao_procurar.clicked.connect(lambda:exportar_excel(ui))
ui.campo_cpf.editingFinished.connect(lambda:formatar_cpf(ui))
ui.campo_pedido.editingFinished.connect(lambda:carregar_dados(ui))
ui.campo_digito_ano.setReadOnly(True)
ui.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
ui.campo_data_nascimento.editingFinished.connect(lambda:formatar_data_nascimento(ui))
ui.campo_cnpj.editingFinished.connect (lambda:formatar_cnpj(ui))
ui.botao_consulta_cnpj.clicked.connect(lambda:procurar_cnpj(ui))
ui.botao_consulta_cpf.clicked.connect(lambda:procurar_cpf(ui))
ui.botao_consulta_cnh.clicked.connect(lambda:procurar_cnh(ui))
ui.botao_consulta_rg.clicked.connect(lambda:procurar_rg(ui))
ui.tableWidget.itemDoubleClicked.connect(lambda:pegar_valor_tabela(ui))
ui.botao_salvar.clicked.connect(lambda:salvar(ui))
ui.botao_agrupar_PDF.clicked.connect(lambda:mesclar_pdf(ui))
ui.botao_dados_cnpj.clicked.connect(lambda:dados_cnpj(ui))
ui.botao_converter_jpgPDF.clicked.connect(lambda:converter_jpg_pdf(ui))
ui.botao_transf_link_PDF.clicked.connect(lambda:texto_para_pdf(ui))
ui.botao_pasta_cliente.clicked.connect(lambda:criar_pasta_cliente(ui))
ui.campo_data_de.setDate(QDate.currentDate().addDays(1 - QDate.currentDate().day()))
ui.campo_data_ate.setDate(QDate(QDate.currentDate().year(), QDate.currentDate().month(), QDate.currentDate().daysInMonth()))
ui.botao_selecionar_arquivos_mesclar.clicked.connect(lambda:carregar_pdf_na_label(ui))
ui.botao_limpar_PDF.clicked.connect(lambda:limpar_label_pdf(ui))
ui.barra_progresso_jpg.setVisible(False)
ui.barra_progresso_mesclar.setVisible(False)
ui.barra_progresso_pedido.setVisible(False)
ui.barra_progresso_consulta.setVisible(False)
janela.closeEvent = on_close_event
ui.campo_cnh.mousePressEvent = lambda event: copiar_campo("campo_cnh")
ui.campo_cnpj.mousePressEvent = lambda event: copiar_campo("campo_cnpj")
ui.campo_pedido.mousePressEvent = lambda event: copiar_campo("campo_pedido")
ui.campo_cpf.mousePressEvent = lambda event: copiar_campo("campo_cpf")
ui.campo_seguranca_cnh.mousePressEvent = lambda event: copiar_campo("campo_seguranca_cnh")
ui.campo_rg.mousePressEvent = lambda event: copiar_campo("campo_rg")
ui.campo_nome_mae.mousePressEvent = lambda event: copiar_campo("campo_nome_mae")
ui.campo_nome.mousePressEvent = lambda event: copiar_campo("campo_nome")




janela.setWindowTitle("Auxiliar Certificados")
janela.setFixedSize(611, 590)
janela.show()


sys.exit(app.exec_())


