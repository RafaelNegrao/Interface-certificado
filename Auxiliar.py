from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem,QTableWidget,QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QDate, QTime,QUrl, Qt
import datetime
from winotify import Notification
from PyQt5.QtGui import QDesktopServices
import pandas as pd
import os
import firebase_admin
from firebase_admin import db
import tkinter as tk
from tkinter import filedialog
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas



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
    ui.campo_digito_cpf.setText("")
    ui.campo_digito_rg.setText("")
    ui.campo_pedido.setText("")
    ui.campo_oab.setText("")
    ui.campo_novo_noBd.setText("")
    ui.campo_lista_status.setCurrentText("AGUARDANDO")
    ui.campo_lista_status_3.setCurrentText("NAO")
    ui.campo_lista_status_4.setCurrentText("")
    data_nula = QDate(2000, 1, 1)
    hora = QTime.fromString('00:00', "hh:mm")
    ui.campo_data_agendamento.setDate(data_nula)
    ui.campo_data_nascimento.setDate(data_nula)
    ui.campo_hora_agendamento.setTime(hora)
    ui.tableWidget.setRowCount(0)
    ui.label_quantidade_bd.setText("")
    ui.campo_oab.setText("")
    ui.campo_cnh.setText("")
    ui.campo_seguranca_cnh.setText("")

def procurar_cnh():
    url = QUrl("https://sso.acesso.gov.br/login?client_id=portalservicos.denatran.serpro.gov.br&authorization_id=18aa635cf94")
    QDesktopServices.openUrl(url)
    return

def procurar_oab():
    url = QUrl("https://cna.oab.org.br/")
    QDesktopServices.openUrl(url)
    return

def procurar_rg():
    url = QUrl("http://www.teledocumentos.com.br/sistema2/")
    QDesktopServices.openUrl(url)
    return

def procurar_cnpj():
    cnpj = ui.campo_cnpj.text()
    url = QUrl(f"https://solucoes.receita.fazenda.gov.br/servicos/cnpjreva/Cnpjreva_Solicitacao.asp?cnpj={cnpj}")
    QDesktopServices.openUrl(url)
    return

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
        ui.campo_digito_cpf.setText(cpf_formatado[-2:])
    
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
        ui.campo_digito_cpf.setText(cpf_formatado[-2:])
    elif len(novo_cpf)== "":
        return

def formatar_rg():
    rg = ui.campo_rg.text()
    rg_novo = rg.replace(".","").replace("-","")
    if len(rg_novo) <= 7:
        ui.campo_rg.setText(rg_novo)
        pass

    elif  len(rg_novo) == 9:
        a = rg_novo[:2]
        b = rg_novo[2:5]
        c = rg_novo[5:8]
        d = rg_novo[8:9]
        rg_formatado = f"{a}.{b}.{c}-{d}"
        ui.campo_rg.setText("")
        ui.campo_rg.setText(rg_formatado)
        ui.campo_digito_rg.setText(rg_formatado[-1:])

    elif len(rg_novo) == 8:
        rg_novo = rg.zfill(9)
        a = rg_novo[:2]
        b = rg_novo[2:5]
        c = rg_novo[5:8]
        d = rg_novo[8:9]
        rg_formatado = f"{a}.{b}.{c}-{d}"
        ui.campo_rg.setText("")
        ui.campo_rg.setText(rg_formatado)
        ui.campo_digito_rg.setText(rg_formatado[-1:])

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
            if ui.campo_lista_status.currentText() != "AGUARDANDO":
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
                oab = ""
                cnpj = ""
                email = ""
                dig_cpf = ""
                dig_rg = ""
                dig_ano = ""
                data_nascimento = ""
                cod_seg_cnh = ""
                if pedido == "" or tipo == "" or hora == "" or data == "" or status == "" or modalidade == "":

                    notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!")
                    notificacao.show()
                    return
                #
                novos_dados = {"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"OAB":oab ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"DIGITO CPF":dig_cpf,"DIGITO RG":dig_rg,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
                notificacao = Notification(app_id="Pedido",title="",msg=f"Pedido {pedido} salvo com sucesso\nStatus:{status}!")
                notificacao.show()
                ref.child(id).update(novos_dados)
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
                oab = ui.campo_oab.text()
                cnpj = ui.campo_cnpj.text()
                email = ui.campo_email.text()
                dig_cpf = ui.campo_digito_cpf.text()
                dig_rg = ui.campo_digito_rg.text()
                dig_ano = ui.campo_digito_ano.text()
                data_nascimento = ui.campo_data_nascimento.text()
                vendido = ui.campo_lista_status_3.currentText()
                modalidade = ui.campo_lista_status_4.currentText()
                cod_seg_cnh = ui.campo_seguranca_cnh.text()

                if pedido == "" or tipo == "" or hora == "" or data == "" or status == "" or modalidade == "":

                    notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!")
                    notificacao.show()
                    return
                #
                novos_dados = {"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"OAB":oab ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"DIGITO CPF":dig_cpf,"DIGITO RG":dig_rg,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
                notificacao = Notification(app_id="Pedido",title="",msg=f"Pedido {pedido} salvo com sucesso\nStatus:{status}!")
                notificacao.show()
                ref.child(id).update(novos_dados)
                return
   
    if ui.campo_lista_status.currentText() == "Aprovado":
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
        oab = ""
        cnpj = ""
        email = ""
        dig_cpf = ""
        dig_rg = ""
        dig_ano = ""
        data_nascimento = ""
        cod_seg_cnh = ""
        vendido = ui.campo_lista_status_3.currentText()
        if pedido == "" or tipo == "" or hora == "" or data == "" or status == "" or modalidade == "":

            notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!")
            notificacao.show()
            return
        #
        novos_dados = {"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"OAB":oab ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"DIGITO CPF":dig_cpf,"DIGITO RG":dig_rg,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
        notificacao = Notification(app_id="Pedido",title="",msg=f"Pedido {pedido} salvo com sucesso\nStatus:{status}!")
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
        oab = ui.campo_oab.text()
        cnpj = ui.campo_cnpj.text()
        email = ui.campo_email.text()
        dig_cpf = ui.campo_digito_cpf.text()
        dig_rg = ui.campo_digito_rg.text()
        dig_ano = ui.campo_digito_ano.text()
        data_nascimento = ui.campo_data_nascimento.text()
        vendido = ui.campo_lista_status_3.currentText()
        modalidade = ui.campo_lista_status_4.currentText()
        cod_seg_cnh = ui.campo_seguranca_cnh.text()
        if pedido == "" or tipo == "" or hora == "" or data == "" or status == "" or modalidade == "":

            notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!")
            notificacao.show()
            return
        #
        novos_dados = {"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"OAB":oab ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"DIGITO CPF":dig_cpf,"DIGITO RG":dig_rg,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
        
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
            if ui.campo_lista_status.currentText() != "AGUARDANDO":
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
                oab = ""
                cnpj = ""
                email = ""
                dig_cpf = ""
                dig_rg = ""
                dig_ano = ""
                data_nascimento = ""
                cod_seg_cnh = ""

                if pedido == "" or tipo == "" or hora == "" or data == "" or status == "" or modalidade == "":

                    notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!")
                    notificacao.show()
                    return
                #
                novos_dados = {"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"OAB":oab ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"DIGITO CPF":dig_cpf,"DIGITO RG":dig_rg,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
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
                oab = ui.campo_oab.text()
                cnpj = ui.campo_cnpj.text()
                email = ui.campo_email.text()
                dig_cpf = ui.campo_digito_cpf.text()
                dig_rg = ui.campo_digito_rg.text()
                dig_ano = ui.campo_digito_ano.text()
                data_nascimento = ui.campo_data_nascimento.text()
                vendido = ui.campo_lista_status_3.currentText()
                modalidade = ui.campo_lista_status_4.currentText()
                cod_seg_cnh = ui.campo_seguranca_cnh.text()

                if pedido == "" or tipo == "" or hora == "" or data == "" or status == "" or modalidade == "":

                    notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!")
                    notificacao.show()
                    return
                #
                novos_dados = {"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"OAB":oab ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"DIGITO CPF":dig_cpf,"DIGITO RG":dig_rg,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
                notificacao = Notification(app_id="Novo pedido",title="",msg=f"Pedido {pedido} atualizado com sucesso\nStatus:{status}!")
                notificacao.show()
                ref.child(id).update(novos_dados)
                limpar_campos()
                return
   
    if ui.campo_lista_status.currentText() != "AGUARDANDO":
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
        oab = ""
        cnpj = ""
        email = ""
        dig_cpf = ""
        dig_rg = ""
        dig_ano = ""
        data_nascimento = ""
        cod_seg_cnh = ""

        if pedido == "" or tipo == "" or hora == "" or data == "" or status == "" or modalidade == "":

            notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!")
            notificacao.show()
            return
        #
        novos_dados = {"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"OAB":oab ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"DIGITO CPF":dig_cpf,"DIGITO RG":dig_rg,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
        notificacao = Notification(app_id="Novo pedido",title="",msg=f"Pedido {pedido} criado com sucesso\nStatus:{status}!")
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
        oab = ui.campo_oab.text()
        cnpj = ui.campo_cnpj.text()
        email = ui.campo_email.text()
        dig_cpf = ui.campo_digito_cpf.text()
        dig_rg = ui.campo_digito_rg.text()
        dig_ano = ui.campo_digito_ano.text()
        data_nascimento = ui.campo_data_nascimento.text()
        vendido = ui.campo_lista_status_3.currentText()
        modalidade = ui.campo_lista_status_4.currentText()
        cod_seg_cnh = ui.campo_seguranca_cnh.text()

        if pedido == "" or tipo == "" or hora == "" or data == "" or status == "" or modalidade == "":

            notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!")
            notificacao.show()
            return
        #
        novos_dados = {"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"OAB":oab ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"DIGITO ANO":dig_ano,"DIGITO CPF":dig_cpf,"DIGITO RG":dig_rg,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
        
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

                elif status_filtro == "":

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
        for pedido_info in req:
            data_bd = datetime.datetime.strptime(pedido_info['DATA'], "%d/%m/%Y")
            numero_inteiro_bd = data_bd.toordinal()
            status_servidor = pedido_info['STATUS']
            
            if (numero_inteiro_inicial <= numero_inteiro_bd <= numero_inteiro_final) :

                if status_filtro == status_servidor or status_filtro == "":
                
                    x += 1
                
                    row_position = ui.tableWidget.rowCount()
                    ui.tableWidget.insertRow(row_position)

                    ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(pedido_info['PEDIDO']))
                    ui.tableWidget.setItem(row_position, 1, QTableWidgetItem(pedido_info['DATA']))
                    ui.tableWidget.setItem(row_position, 2, QTableWidgetItem(pedido_info['HORA']))
                    ui.tableWidget.setItem(row_position, 3, QTableWidgetItem(pedido_info['MODALIDADE']))
                    ui.tableWidget.setItem(row_position, 4, QTableWidgetItem(pedido_info['STATUS']))
                    ui.tableWidget.setItem(row_position, 5, QTableWidgetItem(pedido_info['VENDIDO POR MIM?']))
                    ui.tableWidget.setItem(row_position, 6, QTableWidgetItem(pedido_info['TIPO']))
        
        ui.label_quantidade_bd.setText(f"{x} registro(s)")
        ui.tableWidget.setHorizontalHeaderLabels(["PEDIDO", "DATA", "HORA", "MODALIDADE", "STATUS", "VENDA","TIPO"])

    except Exception as e:
            pass

def carregar_dados():
    #USO DE BANCO DE DADOS
    #Carrega os dados nos campos da aba 'Dados' ao dar double click
    try:   
        num_pedido = ui.campo_pedido.text()
        req = ref.get()


        for pedido in req:
            pedido_servidor = req[pedido]['PEDIDO']
            if num_pedido == pedido_servidor:
                ui.campo_pedido.setReadOnly(True)
                #traga os dados
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
                ui.campo_oab.setText(req[pedido]['OAB'])
                ui.campo_cnpj.setText(req[pedido]['CNPJ'])
                ui.campo_email.setText(req[pedido]['EMAIL'])
                ui.campo_data_nascimento.setDate(QDate.fromString(req[pedido]['NASCIMENTO'], "dd/MM/yyyy"))
                ui.campo_digito_ano.setText(req[pedido]['DIGITO ANO'])
                ui.campo_digito_cpf.setText(req[pedido]['DIGITO CPF'])
                ui.campo_digito_rg.setText(req[pedido]['DIGITO RG'])
                ui.campo_lista_status_3.setCurrentText("NAO")
                ui.campo_lista_status_3.setCurrentText(req[pedido]['VENDIDO POR MIM?'])
                ui.campo_lista_status_4.setCurrentText(req[pedido]['MODALIDADE'])
                ui.campo_seguranca_cnh.setText(req[pedido]['CODIGO DE SEG CNH'])
                return
                
    except Exception as e:
       
        # Lida com exceções aqui
        return
    ui.campo_novo_noBd.setText("")

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
                        ui.campo_oab.setText(req[id]["OAB"])  
                        ui.campo_cnpj.setText(req[id]["CNPJ"])  
                        ui.campo_email.setText(req[id]["EMAIL"])  
                        ui.campo_data_nascimento.setDate(QDate.fromString(req[id]["NASCIMENTO"], "dd/MM/yyyy"))  
                        ui.campo_pedido.setText(req[id]["PEDIDO"]) 
                        ui.campo_data_agendamento.setDate(QDate.fromString(req[id]["DATA"], "dd/MM/yyyy"))
                        ui.campo_hora_agendamento.setTime(QTime.fromString(req[id]["HORA"], "hh:mm"))
                        ui.campo_digito_ano.setText(req[id]["DIGITO ANO"])
                        ui.campo_digito_cpf.setText(req[id]["DIGITO CPF"])
                        ui.campo_digito_rg.setText(req[id]["DIGITO RG"])
                        ui.campo_lista_status_3.setCurrentText("NAO")
                        ui.campo_lista_status_3.setCurrentText(req[id]['VENDIDO POR MIM?'])
                        ui.campo_lista_status_4.setCurrentText(req[id]['MODALIDADE'])
                        ui.campo_pedido.setReadOnly(True)
                        ui.campo_seguranca_cnh.setText(req[id]['CODIGO DE SEG CNH'])
                        ui.campo_novo_noBd.setText("✅")
                        return
                        
    except Exception as e:
        pass

def mesclar_pdf():
    # Abrir o explorador de arquivos para selecionar os arquivos PDF
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")],title="Agrupar PDF")
    
    # Verificar se o usuário selecionou arquivos
    if not file_paths:
        return
    
    # Criar um objeto PdfMerger para mesclar os PDFs
    pdf_merger = PyPDF2.PdfMerger()
    
    # Adicionar cada arquivo PDF à PdfMerger
    for path in file_paths:
        pdf_merger.append(path)
    
    # Abrir o explorador de arquivos para selecionar o local de salvamento
    save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")],title="Local de download")
    
    # Verificar se o usuário selecionou um local de salvamento
    if not save_path:
        return
    
    # Salvar o arquivo mesclado no local especificado
    with open(save_path, 'wb') as merged_pdf:
        pdf_merger.write(merged_pdf)
    
    # Informar ao usuário que a mesclagem foi concluída
    notificacao = Notification(app_id="Concluído",title="",msg=f"Os arquivos PDF foram mesclados com sucesso!")
    notificacao.show()

def converter_jpg_pdf():
    # Abrir o explorador de arquivos para selecionar a imagem
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif")],title="Converter JPG > PDF")
    
    # Verificar se o usuário selecionou um arquivo de imagem
    if not image_path:
        return
    
    # Abrir o explorador de arquivos para selecionar o local de salvamento do PDF
    save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")],title="Local de download")
    
    # Verificar se o usuário selecionou um local de salvamento
    if not save_path:
        return
    
    # Criar um arquivo PDF e adicionar a imagem a ele
    c = canvas.Canvas(save_path, pagesize=letter)
    c.drawImage(image_path, 0, 0, width=letter[0], height=letter[1])
    c.save()
    

    notificacao = Notification(app_id="Concluído",title="",msg=f"A imagem foi convertida em PDF com sucesso!")
    notificacao.show()
  
def texto_para_pdf():
    # Obter o texto que você deseja converter em PDF (substitua esta linha pelo seu texto)
    
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
    notificacao = Notification(app_id="Concluído",title="",msg=f"Texto salvo com sucesso!")
    notificacao.show()
    
class Ui_janela(object):
    def setupUi(self, janela):
        janela.setObjectName("janela")
        janela.resize(611, 612)
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
        self.tabWidget.setGeometry(QtCore.QRect(10, 0, 591, 571))
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
        self.label = QtWidgets.QLabel(self.tab_5)
        self.label.setGeometry(QtCore.QRect(10, 10, 81, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab_5)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 241, 16))
        self.label_2.setObjectName("label_2")
        self.campo_data_agendamento = QtWidgets.QDateEdit(self.tab_5)
        self.campo_data_agendamento.setGeometry(QtCore.QRect(300, 30, 151, 31))
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
        self.label_3.setGeometry(QtCore.QRect(300, 10, 131, 20))
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
        self.botao_terminar.setGeometry(QtCore.QRect(440, 500, 131, 31))
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
        self.label_12 = QtWidgets.QLabel(self.tab_5)
        self.label_12.setGeometry(QtCore.QRect(10, 480, 131, 16))
        self.label_12.setObjectName("label_12")
        self.campo_cnh = QtWidgets.QLineEdit(self.tab_5)
        self.campo_cnh.setGeometry(QtCore.QRect(10, 400, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_cnh.setFont(font)
        self.campo_cnh.setObjectName("campo_cnh")
        self.label_10 = QtWidgets.QLabel(self.tab_5)
        self.label_10.setGeometry(QtCore.QRect(20, 230, 81, 16))
        self.label_10.setObjectName("label_10")
        self.botao_consulta_cnh = QtWidgets.QPushButton(self.tab_5)
        self.botao_consulta_cnh.setGeometry(QtCore.QRect(290, 400, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_cnh.setFont(font)
        self.botao_consulta_cnh.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_cnh.setObjectName("botao_consulta_cnh")
        self.label_13 = QtWidgets.QLabel(self.tab_5)
        self.label_13.setGeometry(QtCore.QRect(170, 480, 61, 16))
        self.label_13.setObjectName("label_13")
        self.campo_email = QtWidgets.QLineEdit(self.tab_5)
        self.campo_email.setGeometry(QtCore.QRect(10, 350, 561, 31))
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
        self.botao_salvar = QtWidgets.QPushButton(self.tab_5)
        self.botao_salvar.setGeometry(QtCore.QRect(350, 500, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.botao_salvar.setFont(font)
        self.botao_salvar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_salvar.setStyleSheet("border-radius:10px;\n"
"background-color:rgb(73, 218, 107);")
        self.botao_salvar.setObjectName("botao_salvar")
        self.campo_seguranca_cnh = QtWidgets.QLineEdit(self.tab_5)
        self.campo_seguranca_cnh.setGeometry(QtCore.QRect(330, 400, 241, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_seguranca_cnh.setFont(font)
        self.campo_seguranca_cnh.setObjectName("campo_seguranca_cnh")
        self.botao_consulta_rg = QtWidgets.QPushButton(self.tab_5)
        self.botao_consulta_rg.setGeometry(QtCore.QRect(540, 250, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_rg.setFont(font)
        self.botao_consulta_rg.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_rg.setObjectName("botao_consulta_rg")
        self.label_6 = QtWidgets.QLabel(self.tab_5)
        self.label_6.setGeometry(QtCore.QRect(10, 280, 81, 16))
        self.label_6.setObjectName("label_6")
        self.label_15 = QtWidgets.QLabel(self.tab_5)
        self.label_15.setGeometry(QtCore.QRect(10, 380, 61, 20))
        self.label_15.setObjectName("label_15")
        self.campo_digito_rg = QtWidgets.QLineEdit(self.tab_5)
        self.campo_digito_rg.setGeometry(QtCore.QRect(330, 250, 201, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.campo_digito_rg.setFont(font)
        self.campo_digito_rg.setText("")
        self.campo_digito_rg.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_digito_rg.setObjectName("campo_digito_rg")
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
        self.botao_consulta_oab = QtWidgets.QPushButton(self.tab_5)
        self.botao_consulta_oab.setGeometry(QtCore.QRect(540, 450, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_oab.setFont(font)
        self.botao_consulta_oab.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_oab.setObjectName("botao_consulta_oab")
        self.campo_digito_ano = QtWidgets.QLineEdit(self.tab_5)
        self.campo_digito_ano.setGeometry(QtCore.QRect(170, 500, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.campo_digito_ano.setFont(font)
        self.campo_digito_ano.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_digito_ano.setObjectName("campo_digito_ano")
        self.label_11 = QtWidgets.QLabel(self.tab_5)
        self.label_11.setGeometry(QtCore.QRect(10, 330, 81, 16))
        self.label_11.setObjectName("label_11")
        self.campo_rg = QtWidgets.QLineEdit(self.tab_5)
        self.campo_rg.setGeometry(QtCore.QRect(10, 250, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_rg.setFont(font)
        self.campo_rg.setPlaceholderText("")
        self.campo_rg.setObjectName("campo_rg")
        self.label_8 = QtWidgets.QLabel(self.tab_5)
        self.label_8.setGeometry(QtCore.QRect(330, 280, 141, 20))
        self.label_8.setObjectName("label_8")
        self.campo_digito_cpf = QtWidgets.QLineEdit(self.tab_5)
        self.campo_digito_cpf.setGeometry(QtCore.QRect(330, 300, 201, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.campo_digito_cpf.setFont(font)
        self.campo_digito_cpf.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_digito_cpf.setObjectName("campo_digito_cpf")
        self.botao_consulta_cnpj = QtWidgets.QPushButton(self.tab_5)
        self.botao_consulta_cnpj.setGeometry(QtCore.QRect(290, 450, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_cnpj.setFont(font)
        self.botao_consulta_cnpj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_cnpj.setObjectName("botao_consulta_cnpj")
        self.label_9 = QtWidgets.QLabel(self.tab_5)
        self.label_9.setGeometry(QtCore.QRect(340, 230, 61, 20))
        self.label_9.setObjectName("label_9")
        self.campo_cpf = QtWidgets.QLineEdit(self.tab_5)
        self.campo_cpf.setGeometry(QtCore.QRect(10, 300, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_cpf.setFont(font)
        self.campo_cpf.setText("")
        self.campo_cpf.setPlaceholderText("")
        self.campo_cpf.setObjectName("campo_cpf")
        self.campo_oab = QtWidgets.QLineEdit(self.tab_5)
        self.campo_oab.setGeometry(QtCore.QRect(330, 450, 201, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_oab.setFont(font)
        self.campo_oab.setStyleSheet("")
        self.campo_oab.setText("")
        self.campo_oab.setObjectName("campo_oab")
        self.botao_consulta_cpf = QtWidgets.QPushButton(self.tab_5)
        self.botao_consulta_cpf.setGeometry(QtCore.QRect(540, 300, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_cpf.setFont(font)
        self.botao_consulta_cpf.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_cpf.setObjectName("botao_consulta_cpf")
        self.campo_cnpj = QtWidgets.QLineEdit(self.tab_5)
        self.campo_cnpj.setGeometry(QtCore.QRect(10, 450, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_cnpj.setFont(font)
        self.campo_cnpj.setPlaceholderText("")
        self.campo_cnpj.setObjectName("campo_cnpj")
        self.label_14 = QtWidgets.QLabel(self.tab_5)
        self.label_14.setGeometry(QtCore.QRect(10, 430, 171, 16))
        self.label_14.setObjectName("label_14")
        self.label_18 = QtWidgets.QLabel(self.tab_5)
        self.label_18.setGeometry(QtCore.QRect(330, 430, 141, 20))
        self.label_18.setObjectName("label_18")
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
        self.label_16 = QtWidgets.QLabel(self.tab_5)
        self.label_16.setGeometry(QtCore.QRect(330, 380, 201, 20))
        self.label_16.setObjectName("label_16")
        self.label_24 = QtWidgets.QLabel(self.tab_5)
        self.label_24.setGeometry(QtCore.QRect(10, 180, 201, 16))
        self.label_24.setObjectName("label_24")
        self.botao_pasta_cliente = QtWidgets.QPushButton(self.tab_5)
        self.botao_pasta_cliente.setGeometry(QtCore.QRect(540, 200, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_pasta_cliente.setFont(font)
        self.botao_pasta_cliente.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_pasta_cliente.setObjectName("botao_pasta_cliente")
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
        self.campo_cnh.raise_()
        self.botao_consulta_cnh.raise_()
        self.campo_email.raise_()
        self.botao_salvar.raise_()
        self.campo_seguranca_cnh.raise_()
        self.botao_consulta_rg.raise_()
        self.campo_digito_rg.raise_()
        self.campo_nome.raise_()
        self.botao_consulta_oab.raise_()
        self.campo_digito_ano.raise_()
        self.campo_rg.raise_()
        self.campo_digito_cpf.raise_()
        self.botao_consulta_cnpj.raise_()
        self.campo_cpf.raise_()
        self.campo_oab.raise_()
        self.botao_consulta_cpf.raise_()
        self.campo_cnpj.raise_()
        self.campo_data_nascimento.raise_()
        self.label_24.raise_()
        self.label_2.raise_()
        self.label.raise_()
        self.label_23.raise_()
        self.label_10.raise_()
        self.label_6.raise_()
        self.label_11.raise_()
        self.label_15.raise_()
        self.label_14.raise_()
        self.label_12.raise_()
        self.label_18.raise_()
        self.label_16.raise_()
        self.label_8.raise_()
        self.label_9.raise_()
        self.label_13.raise_()
        self.botao_pasta_cliente.raise_()
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_6)
        self.groupBox_5.setGeometry(QtCore.QRect(10, 10, 561, 91))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.groupBox_5.setFont(font)
        self.groupBox_5.setObjectName("groupBox_5")
        self.campo_data_de = QtWidgets.QDateEdit(self.groupBox_5)
        self.campo_data_de.setGeometry(QtCore.QRect(20, 40, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.campo_data_de.setFont(font)
        self.campo_data_de.setStyleSheet("")
        self.campo_data_de.setObjectName("campo_data_de")
        self.label_19 = QtWidgets.QLabel(self.groupBox_5)
        self.label_19.setGeometry(QtCore.QRect(30, 20, 81, 16))
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.groupBox_5)
        self.label_20.setGeometry(QtCore.QRect(170, 20, 81, 16))
        self.label_20.setObjectName("label_20")
        self.campo_data_ate = QtWidgets.QDateEdit(self.groupBox_5)
        self.campo_data_ate.setGeometry(QtCore.QRect(160, 40, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.campo_data_ate.setFont(font)
        self.campo_data_ate.setStyleSheet("")
        self.campo_data_ate.setObjectName("campo_data_ate")
        self.botao_consultar = QtWidgets.QPushButton(self.groupBox_5)
        self.botao_consultar.setGeometry(QtCore.QRect(480, 40, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.botao_consultar.setFont(font)
        self.botao_consultar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consultar.setStyleSheet("")
        self.botao_consultar.setObjectName("botao_consultar")
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
        self.campo_lista_status_2.setItemText(0, "")
        self.campo_lista_status_2.addItem("")
        self.campo_lista_status_2.addItem("")
        self.campo_lista_status_2.addItem("")
        self.tableWidget = QtWidgets.QTableWidget(self.tab_6)
        self.tableWidget.setGeometry(QtCore.QRect(10, 110, 561, 391))
        self.tableWidget.setMinimumSize(QtCore.QSize(561, 0))
        self.tableWidget.setMaximumSize(QtCore.QSize(750, 16777215))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(10)
        self.tableWidget.setFont(font)
        self.tableWidget.setAutoScrollMargin(16)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
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
        self.botao_procurar = QtWidgets.QPushButton(self.tab_6)
        self.botao_procurar.setGeometry(QtCore.QRect(440, 510, 131, 31))
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
        self.label_quantidade_bd.setGeometry(QtCore.QRect(200, 510, 221, 31))
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
        self.groupBox_3.setGeometry(QtCore.QRect(10, 30, 571, 121))
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setGeometry(QtCore.QRect(10, 20, 181, 16))
        self.label_7.setObjectName("label_7")
        self.botao_transf_link_PDF = QtWidgets.QPushButton(self.groupBox_3)
        self.botao_transf_link_PDF.setGeometry(QtCore.QRect(380, 80, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.botao_transf_link_PDF.setFont(font)
        self.botao_transf_link_PDF.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_transf_link_PDF.setObjectName("botao_transf_link_PDF")
        self.campo_link_video = QtWidgets.QLineEdit(self.groupBox_3)
        self.campo_link_video.setGeometry(QtCore.QRect(10, 40, 551, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_link_video.setFont(font)
        self.campo_link_video.setText("")
        self.campo_link_video.setPlaceholderText("")
        self.campo_link_video.setObjectName("campo_link_video")
        self.botao_agrupar_PDF = QtWidgets.QPushButton(self.tab)
        self.botao_agrupar_PDF.setGeometry(QtCore.QRect(130, 330, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.botao_agrupar_PDF.setFont(font)
        self.botao_agrupar_PDF.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_agrupar_PDF.setStyleSheet("")
        self.botao_agrupar_PDF.setObjectName("botao_agrupar_PDF")
        self.botao_converter_jpgPDF = QtWidgets.QPushButton(self.tab)
        self.botao_converter_jpgPDF.setGeometry(QtCore.QRect(130, 250, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.botao_converter_jpgPDF.setFont(font)
        self.botao_converter_jpgPDF.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_converter_jpgPDF.setStyleSheet("")
        self.botao_converter_jpgPDF.setObjectName("botao_converter_jpgPDF")
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
        janela.setTabOrder(self.campo_nome, self.campo_rg)
        janela.setTabOrder(self.campo_rg, self.campo_cpf)
        janela.setTabOrder(self.campo_cpf, self.campo_email)
        janela.setTabOrder(self.campo_email, self.campo_cnh)
        janela.setTabOrder(self.campo_cnh, self.campo_seguranca_cnh)
        janela.setTabOrder(self.campo_seguranca_cnh, self.campo_cnpj)
        janela.setTabOrder(self.campo_cnpj, self.campo_oab)
        janela.setTabOrder(self.campo_oab, self.campo_data_nascimento)
        janela.setTabOrder(self.campo_data_nascimento, self.campo_data_de)
        janela.setTabOrder(self.campo_data_de, self.campo_data_ate)
        janela.setTabOrder(self.campo_data_ate, self.campo_lista_status_2)
        janela.setTabOrder(self.campo_lista_status_2, self.botao_consulta_cnh)
        janela.setTabOrder(self.botao_consulta_cnh, self.botao_consulta_rg)
        janela.setTabOrder(self.botao_consulta_rg, self.botao_consulta_oab)
        janela.setTabOrder(self.botao_consulta_oab, self.botao_consultar)
        janela.setTabOrder(self.botao_consultar, self.botao_procurar)
        janela.setTabOrder(self.botao_procurar, self.campo_digito_rg)
        janela.setTabOrder(self.campo_digito_rg, self.tabWidget)
        janela.setTabOrder(self.tabWidget, self.campo_digito_ano)
        janela.setTabOrder(self.campo_digito_ano, self.campo_digito_cpf)
        janela.setTabOrder(self.campo_digito_cpf, self.tableWidget)
        janela.setTabOrder(self.tableWidget, self.botao_salvar)
        janela.setTabOrder(self.botao_salvar, self.botao_consulta_cpf)
        janela.setTabOrder(self.botao_consulta_cpf, self.botao_consulta_cnpj)
        janela.setTabOrder(self.botao_consulta_cnpj, self.botao_terminar)

    def retranslateUi(self, janela):
        _translate = QtCore.QCoreApplication.translate
        janela.setWindowTitle(_translate("janela", "MainWindow"))
        self.campo_lista_status.setItemText(0, _translate("janela", "AGUARDANDO"))
        self.campo_lista_status.setItemText(1, _translate("janela", "APROVADO"))
        self.campo_lista_status.setItemText(2, _translate("janela", "CANCELADO"))
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
        self.label_12.setText(_translate("janela", "NASCIMENTO"))
        self.label_10.setText(_translate("janela", "RG"))
        self.botao_consulta_cnh.setText(_translate("janela", "🔍"))
        self.label_13.setText(_translate("janela", "díg ANO"))
        self.botao_salvar.setText(_translate("janela", "SALVAR"))
        self.botao_consulta_rg.setText(_translate("janela", "🔍"))
        self.label_6.setText(_translate("janela", "CPF"))
        self.label_15.setText(_translate("janela", "CNH"))
        self.botao_consulta_oab.setText(_translate("janela", "🔍"))
        self.label_11.setText(_translate("janela", "e-MAIL"))
        self.label_8.setText(_translate("janela", "últimos 2 dígitos - CPF"))
        self.botao_consulta_cnpj.setText(_translate("janela", "🔍"))
        self.label_9.setText(_translate("janela", " dígito - RG"))
        self.botao_consulta_cpf.setText(_translate("janela", "🔍"))
        self.label_14.setText(_translate("janela", "CNPJ"))
        self.label_18.setText(_translate("janela", "OAB"))
        self.label_16.setText(_translate("janela", "código de segurança - CNH"))
        self.label_24.setText(_translate("janela", "NOME COMPLETO"))
        self.botao_pasta_cliente.setText(_translate("janela", "🗂"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("janela", "Dados"))
        self.groupBox_5.setTitle(_translate("janela", "BUSCA"))
        self.label_19.setText(_translate("janela", "DE:"))
        self.label_20.setText(_translate("janela", "ATÉ:"))
        self.botao_consultar.setText(_translate("janela", "🔍"))
        self.label_21.setText(_translate("janela", "STATUS"))
        self.campo_lista_status_2.setItemText(1, _translate("janela", "AGUARDANDO"))
        self.campo_lista_status_2.setItemText(2, _translate("janela", "APROVADO"))
        self.campo_lista_status_2.setItemText(3, _translate("janela", "CANCELADO"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("janela", "PEDIDO"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("janela", "DATA"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("janela", "HORA"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("janela", "MODALIDADE"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("janela", "STATUS"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("janela", "VENDA"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("janela", "TIPO"))
        self.botao_procurar.setText(_translate("janela", "EXPORTAR EXCEL"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("janela", "Consulta"))
        self.groupBox_3.setTitle(_translate("janela", "TRANSFORMAR  LINK DA VÍDEO-CONFERÊNCIA  EM   PDF"))
        self.label_7.setText(_translate("janela", "TEXTO"))
        self.botao_transf_link_PDF.setText(_translate("janela", "TRANSFORMAR EM PDF"))
        self.botao_agrupar_PDF.setText(_translate("janela", "AGRUPAR PDF"))
        self.botao_converter_jpgPDF.setText(_translate("janela", "CONVERTER JPEG  >  PDF"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("janela", "PDF"))

class TelaLogin(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(70, 70, 300, 100)
        self.setGeometry(
            QtWidgets.QStyle.alignedRect(
            Qt.LeftToRight,
            Qt.AlignCenter,
            self.size(),
            QtWidgets.QApplication.desktop().availableGeometry()
                    )
                        )
        layout = QVBoxLayout()

        self.label_usuario = QLabel("Usuário:")
        self.input_usuario = QLineEdit(self)

        self.label_senha = QLabel("Senha:")
        self.input_senha = QLineEdit(self)
        self.input_senha.setEchoMode(QLineEdit.Password)

        self.botao_login = QPushButton("Login")
        self.botao_login.clicked.connect(self.verificar_login)

        layout.addWidget(self.label_usuario)
        layout.addWidget(self.input_usuario)
        layout.addWidget(self.label_senha)
        layout.addWidget(self.input_senha)
        layout.addWidget(self.botao_login)

        self.setLayout(layout)

    def verificar_login(self):
        usuario = self.input_usuario.text()
        senha = self.input_senha.text()

        # Verifique aqui se o usuário e senha são válidos, por exemplo, comparando com dados armazenados em algum lugar.
        # Este é apenas um exemplo básico.

        if usuario == "Rafael" and senha == "30625629":
            # Você pode adicionar aqui a lógica para abrir a próxima janela ou realizar ação desejada após o login.
              # Chama a função para abrir a janela principal
            self.close()
            janela.show()
        else:
            notificacao = Notification(app_id=f"Senha incorreta",title="",msg=f"A senha fornecida está incorreta")
            notificacao.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    janela = QtWidgets.QMainWindow()
    login = QtWidgets.QMainWindow()
    ui = Ui_janela()
    ui.setupUi(janela)
    tela_login = TelaLogin()
    
    tela_login.show()
    
    ui.botao_consultar.clicked.connect(preencher_tabela)
    ui.botao_terminar.clicked.connect(gravar_dados)
    ui.botao_procurar.clicked.connect(exportar_excel)
    ui.campo_cpf.editingFinished.connect(formatar_cpf)
    ui.campo_rg.editingFinished.connect(formatar_rg)
    ui.campo_pedido.editingFinished.connect(carregar_dados)
    ui.campo_digito_ano.setReadOnly(True)
    ui.campo_digito_cpf.setReadOnly(True)
    ui.campo_digito_rg.setReadOnly(True)
    ui.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
    ui.campo_data_nascimento.editingFinished.connect(formatar_data_nascimento)
    ui.campo_cnpj.editingFinished.connect (formatar_cnpj)
    ui.botao_consulta_cnpj.clicked.connect(procurar_cnpj)
    ui.botao_consulta_cpf.clicked.connect(procurar_cpf)
    ui.botao_consulta_cnh.clicked.connect(procurar_cnh)
    ui.botao_consulta_oab.clicked.connect(procurar_oab)
    ui.botao_consulta_rg.clicked.connect(procurar_rg)
    ui.tableWidget.itemDoubleClicked.connect(pegar_valor_tabela)
    ui.botao_salvar.clicked.connect(salvar)
    ui.botao_agrupar_PDF.clicked.connect(mesclar_pdf)
    ui.botao_converter_jpgPDF.clicked.connect(converter_jpg_pdf)
    ui.botao_transf_link_PDF.clicked.connect(texto_para_pdf)
    ui.botao_pasta_cliente.clicked.connect(criar_pasta_cliente)
    ui.campo_data_de.setDate(QDate.currentDate().addDays(1 - QDate.currentDate().day()))
    ui.campo_data_ate.setDate(QDate(QDate.currentDate().year(), QDate.currentDate().month(), QDate.currentDate().daysInMonth()))




    janela.setWindowTitle("Dados Certificado - Certisign")
    janela.setFixedSize(611, 612)
    
    sys.exit(app.exec_())
