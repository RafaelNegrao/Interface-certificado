import datetime
import pandas as pd
import tkinter as tk
import os
import time
import shutil
import psutil
import requests
import PyPDF2
import fitz
import firebase_admin
import json
from winotify import Notification
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
from PyQt5 import QtGui, QtWidgets,QtCore
from PyQt5.QtWidgets import QTableWidgetItem,QTableWidget,QApplication,QMessageBox,QDesktopWidget,QInputDialog,QMainWindow,QFileDialog,QRadioButton,QVBoxLayout,QPushButton,QDialog
from PyQt5.QtCore import QDate, QTime,QUrl, Qt,QTimer,QRect
from PyQt5.QtGui import QDesktopServices,QColor
from Interface import Ui_janela
from firebase_admin import db
import pyautogui
from reportlab.lib.utils import ImageReader
from requests.exceptions import RequestException


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

def trazer_diretorio_raiz(ui):

    link = "https://configs-5d64c-default-rtdb.firebaseio.com/Configuracoes"
    # Faz uma solicitação GET para obter as configurações do banco de dados
    bd = requests.get(f"{link}.json")
    # Converte a resposta JSON em um dicionário Python
    config = bd.json()
    # Imprime as configurações (opcional, para depuração)
    print(config)
    
def atualizar_diretorio_raiz(ui):
    link = "https://configs-5d64c-default-rtdb.firebaseio.com/Configuracoes"
    # Faz uma solicitação GET para obter as configurações do banco de dados
    bd = requests.get(f"{link}.json")
    # Converte a resposta JSON em um dicionário Python
    config = bd.json()
    # Imprime as configurações (opcional, para depuração)
    print(config)
    # Aqui vou criar a nova config
    nova_config = {"diretorio raiz": "PASSED","ultima_abertura":"10:00","ultima_saida":"15:00"}
    # Acessa o nó 'Configuracoes' no banco de dados e atualiza com as novas configurações
    requests.patch(f'{link}.json',data=json.dumps(nova_config))

def converter_todas_imagens_para_pdf(ui):
    caminho_pasta = ui.caminho_pasta.text()

    if caminho_pasta != "":
        for arquivo in os.listdir(caminho_pasta):
            if arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                imagem_path = os.path.join(caminho_pasta, arquivo)

                # Cria um arquivo PDF com o mesmo nome da imagem
                pdf_path = os.path.splitext(imagem_path)[0] + ".pdf"
                pdf = canvas.Canvas(pdf_path, pagesize=letter)

                # Adiciona a imagem ao PDF mantendo as dimensões originais
                imagem = ImageReader(imagem_path)
                largura, altura = imagem.getSize()
                
                # Ajusta as dimensões do PDF conforme as dimensões da imagem
                pdf.setPageSize((largura, altura))
                pdf.drawImage(imagem, 0, 0, width=largura, height=altura)

                # Fecha o arquivo PDF
                pdf.save()

                
        notificacao = Notification(app_id="Concluído", title="", msg=f"imagens convertidas!")
        notificacao.show()
    else:
        escolher_conversao(ui)

def obter_janela_principal(widget):
    # Função para obter a janela principal a partir de um widget
    while widget:
        if isinstance(widget, QMainWindow):
            return widget
        widget = widget.parent()
    return None

def print_tela(ui):
    try:
        caminho = ui.caminho_pasta.text()

        if not caminho:
            nome_documento, ok = QInputDialog.getText(ui.centralwidget, "Nome da print", "Digite o nome da print:",text="DOC ADICIONAL")
            if not ok:           
                return
            
            if not nome_documento:
                return

            caminho_escolhido = QFileDialog.getExistingDirectory(ui.centralwidget, 'Escolher Pasta', '/')
            if not caminho_escolhido:      
                return

            caminho = f"{caminho_escolhido}/{nome_documento}.png"
        else:

            nome_documento, ok = QInputDialog.getText(ui.centralwidget, "Nome da print", "Digite o nome da print:",text="DOC ADICIONAL")
            if not ok:           
                return
            
            if not nome_documento:
                return
            caminho = f"{caminho}/{nome_documento}.png"
        janela_principal = obter_janela_principal(ui.centralwidget)

        if janela_principal:
            # Minimiza a janela principal
            janela_principal.showMinimized()

        # Aguarda um curto período para garantir que a janela tenha tempo de minimizar
        time.sleep(0.7)

        # Tira um screenshot da tela
        screenshot = pyautogui.screenshot()
        screenshot = pyautogui.screenshot()

        # Restaura a janela principal (opcional)
        if janela_principal:
            janela_principal.showNormal()

        # Salva o screenshot no caminho especificado
    
        
        notificacao = Notification(app_id="Concluído", title="", msg=f"Print capturada!")
        notificacao.show()
        screenshot.save(caminho)
    except Exception as e:
        notificacao = Notification(app_id="Erro", title="", msg=f"Não foi possível capturar a tela!")
        notificacao.show()

def gerar_link_video_conferencia(ui):
    
    pedido = ui.campo_pedido.text()
    if not pedido:
        pedido, ok = QInputDialog.getText(ui.centralwidget, "Criar LINK", "Digite o número do PEDIDO:")
        if not ok:
            return

        # Obter o link
        link = f"https://certisign.omotor.com.br/#/dossie-detail/{pedido}"
        save_path, _ = QFileDialog.getSaveFileName(ui.centralwidget, "Salvar PDF", os.path.expanduser("~"), "Arquivos PDF (*.pdf)")

        if not save_path:
            return

        save_dir = os.path.dirname(save_path)

        default_file_name = "LINK VIDEO"

        if not save_path.lower().endswith(".pdf"):
            save_path = os.path.join(save_dir, f"{default_file_name}.pdf")
        c = canvas.Canvas(save_path, pagesize=letter)
        font_size = 14
        x, y = 20, 680
        c.setFont("Helvetica", font_size)
        for line in link.split('\n'):
            c.drawString(x, y, line)
            y -= 15
        c.save()
        

        
        return
    # if ui.caminho_pasta.text() == "":
    #     notificacao = Notification(app_id="Erro", title="", msg=f"É necessário criar a pasta do cliente!")
    #     notificacao.show()
    #     return

    if ui.campo_lista_status_4.currentText() == "PRESENCIAL":
        notificacao = Notification(app_id="Erro", title="", msg=f"Não é possível gerar link na modalidade presencial!")
        notificacao.show()
        return


    link = f"https://certisign.omotor.com.br/#/dossie-detail/{pedido}"

    try:
        default_file_name = "LINK VIDEO"
        
        # Obtém o caminho do arquivo diretamente do campo_pasta
        save_path = ui.caminho_pasta.text()

        if not save_path:
            notificacao = Notification(app_id="Pasta ausente", title="", msg=f"Crie a pasta do cliente!")
            notificacao.show()
            return

        # Adiciona a extensão PDF se não estiver presente
        if not save_path.lower().endswith(".pdf"):
            save_path = os.path.join(save_path, f"{default_file_name}.pdf")
        # Criar um arquivo PDF
        c = canvas.Canvas(save_path, pagesize=letter)
        # Definir o tamanho da fonte e a posição para começar a escrever o texto
        font_size = 14
        x, y = 20, 680  # Posição inicial
        # Adicionar o texto ao PDF
        c.setFont("Helvetica", font_size)
        for line in link.split('\n'):
            c.drawString(x, y, line)
            y -= 15  # Espaçamento entre as linhas
        # Salvar o arquivo PDF
        c.save()
        notificacao = Notification(app_id="Concluído", title="", msg=f"Link salvo com sucesso!")
        notificacao.show()
    except Exception as e:
        notificacao = Notification(app_id="Arquivo existente", title="", msg=f"Já existe um arquivo LINK_VIDEO na pasta!")
        notificacao.show()

def forcar_fechamento_de_arquivo_e_deletar_pasta(folder_path):
    for _ in range(3):  # Tentar até três vezes
        try:
            shutil.rmtree(folder_path)
            notificacao = Notification(app_id="Pasta excluída com sucesso")
            notificacao.show()
            break
        except PermissionError as e:
            # Se a exclusão falhar devido a permissões, tenta fechar os arquivos em uso antes da próxima tentativa
            fechar_arquivo_em_uso(folder_path)
        except Exception as e:
            if not os.path.exists(folder_path):  # Verifica se a pasta não existe
                break
            
            notificacao = Notification(app_id="Erro ao excluir pasta do cliente")
            notificacao.show()
            break
        
def fechar_arquivo_em_uso(folder_path):
    processes = psutil.process_iter(['pid', 'name', 'open_files'])
    for process in processes:
        try:
            open_files = process.info.get('open_files')
            if open_files:
                for file_info in open_files:
                    if folder_path in file_info.path:
                        
                        # Força o fechamento do processo
                        psutil.Process(process.info['pid']).terminate()
                        
                        
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            continue

def criar_pasta_cliente(ui):
    pedido = ui.campo_pedido.text()
    tipo = ui.campo_certificado.text()
    hora  = ui.campo_hora_agendamento.text()
    data = ui.campo_data_agendamento.text()
    status = ui.campo_lista_status.currentText()
    modalidade = ui.campo_lista_status_4.currentText()
    if pedido == "" or tipo == "" or hora == "00:00" or data == "01/01/2000" or status == "" or modalidade == "":
        notificacao = Notification(app_id="Pasta não criada",title="",msg="Adicione os itens com 🌟 para criar a pasta do cliente!",duration="short")
        notificacao.show()
        return
    #Tente criar a pasta 
    #caso não consiga,vá para o except
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
                nova_pasta = nova_pasta.replace("/","\\")
                ui.caminho_pasta.setText(nova_pasta)
                salvar(ui)
                
                notificacao = Notification(app_id="Pasta Criada", title="", msg=f"Pasta do cliente {nome_pasta} criada com sucesso!",duration="short")
                notificacao.show()
            else:
                notificacao = Notification(app_id="Pasta existente", title="", msg=f"Pasta do cliente {nome_pasta} já existe no diretório!",duration="short")
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
    ui.campo_diretorio_pasta.setText("")
    ui.campo_cnpj_municipio.setText("")
    ui.campo_cnpj_uf.setText("")
    ui.caminho_pasta.setText("")
    ui.campo_lista_junta_comercial.setCurrentText("")

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
    url_receita = QUrl(f"https://solucoes.receita.fazenda.gov.br/servicos/cnpjreva/Cnpjreva_Solicitacao.asp?cnpj={cnpj}")
    QDesktopServices.openUrl(url_receita)

def procurar_junta(ui):
    
    estado = ui.campo_lista_junta_comercial.currentText()

    match  estado:
        case "":
            return
        case 'AC':
            link_consulta  = "https://integrar.ac.gov.br/Portal/pages/imagemProcesso/viaUnica.jsf"
        case 'AL':
            link_consulta  = "https://servicos.juceal.al.gov.br/autenticidade/"
        case 'AM':
            link_consulta  = "https://portalservicos.jucea.am.gov.br/Portal/pages/imagemProcesso/validacaoDownloadViaUnica.jsf?numProtocolo=220176086"
        case 'AP':
            link_consulta  = "https://portalservicos.jucap.ap.gov.br/Portal/pages/imagemProcesso/validacaoDownloadViaUnica.jsf#:~:text=O%20documento%20%C3%A9%20assinado%20digitalmente,documentos%20enviados%20para%20a%20JUCAP."
        case 'BA':
            link_consulta  = "https://regin.juceb.ba.gov.br/AUTENTICACAODOCUMENTOS/AUTENTICACAO.aspx"
        case 'CE':
            link_consulta  = "https://portalservicos.jucec.ce.gov.br/Portal/pages/imagemProcesso/validacaoDownloadViaUnica.jsf"
        case 'DF':
            link_consulta  = "https://portalservicos.jucis.df.gov.br/Portal/pages/imagemProcesso/validacaoDownloadViaUnica.jsf?"
        case 'ES':
            link_consulta  = "https://jucees.es.gov.br/autenticidade"
        case 'GO':
            link_consulta  = "http://servicos.juceg.go.gov.br/validardocumento/"
        case 'MA':
            link_consulta  = "http://portal.jucema.ma.gov.br/certidoes/f/pages/consulta/consulta.xhtml"
        case 'MT':
            link_consulta  = "https://portalservicos.jucemat.mt.gov.br/Portal/pages/imagemProcesso/validacaoDownloadViaUnica.jsf?"
        case 'MS':
            link_consulta  = "https://portalservicos.jucems.ms.gov.br/Portal/pages/imagemProcesso/validacaoDownloadViaUnica.jsf?"
        case 'MG':
            link_consulta  = "https://portalservicos.jucemg.mg.gov.br/Portal/pages/imagemProcesso/viaUnica.jsf;jsessionid=tjYHrIwsaxQnbhw-190v0xASyL5s8qfaaI70o8U9.portalexterno-prod-5b844544c8-blwcb"
        case 'PA':
            link_consulta  = "https://regin.jucepa.pa.gov.br/autenticacaodocumentos/AUTENTICACAO.aspx"
        case 'PB':
            link_consulta  = "https://www.redesim.pb.gov.br/"
        case 'PR':
            link_consulta  = "https://www.empresafacil.pr.gov.br/"
        case 'PE':
            link_consulta  = "https://redesim.jucepe.pe.gov.br/autenticacaodocumentos/autenticacao.aspx"
        case 'PI':
            link_consulta  = "https://www.piauidigital.pi.gov.br/home/"
        case 'RJ':
            link_consulta  = "https://www.jucerja.rj.gov.br/Servicos/ChancelaDigital"
        case 'RS':
            link_consulta  = "https://portalservicos.jucisrs.rs.gov.br/Portal/pages/imagemProcesso/viaUnica.jsf;jsessionid=NB08GoM1hOr-usaegdPmtpFixQD7JdMmbT1Mn18Q.portalexterno-prod-7c665c8897-8sltz"
        case 'RS':
            link_consulta  = "https://projetointegrar.jucerr.rr.gov.br/Portal/pages/imagemProcesso/validacaoDownloadViaUnica.jsf?numProtocolo=210032316#:~:text=Validar%20Documento,-*N%C3%BAmero%20do%20Protocolo&text=O%20novo%20formato%20de%20documento,op%C3%A7%C3%A3o%20'Validar%20por%20Upload'."
        case 'RR':
            link_consulta  = "https://regin.jucesc.sc.gov.br/autenticacaoDocumentos/AUTENTICACAO.aspx"
        case 'SC':
            link_consulta  = "https://regin.jucesc.sc.gov.br/autenticacaoDocumentos/AUTENTICACAO.aspx"
        case 'SE':
            link_consulta  = "https://www.agiliza.se.gov.br/"
        case 'TO':
            link_consulta  = "https://www.simplifica.to.gov.br/"
        case 'RO':
            link_consulta  = "https://www.empresafacil.ro.gov.br/"
        case 'RN':
            link_consulta  = "https://www.redesim.rn.gov.br/"
        case 'SP':
            link_consulta  = "https://www.jucesponline.sp.gov.br/"


    url_junta = QUrl(link_consulta)
    QDesktopServices.openUrl(url_junta)

def formatar_nome(ui):
    nome = ui.campo_nome.text()  # Obtenha o texto do campo_nome_mae
    ui.campo_nome.setText(nome.upper())

def formatar_nome_mae(ui):
    texto_mae = ui.campo_nome_mae.text()  # Obtenha o texto do campo_nome_mae
    ui.campo_nome_mae.setText(texto_mae.upper())

def dados_cnpj(ui):
    ui.campo_cnpj_municipio.setText("")
    ui.campo_cnpj_uf.setText("")  

    cnpj = ''.join(filter(str.isdigit, ui.campo_cnpj.text()))

    if not cnpj:
        return
    
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
    
    try:
        resposta = requests.get(url)

        if resposta.status_code == 200:
            data = resposta.json()
            ui.campo_cnpj_municipio.setText(data['municipio'])
            
            uf = data['uf']
            
            if uf != "SP":
                ui.campo_cnpj_uf.setText(str(uf + "❌"))
                ui.campo_lista_junta_comercial.setCurrentText(uf)
                return
            else:
                ui.campo_cnpj_uf.setText(str(uf + "✅"))
                ui.campo_lista_junta_comercial.setCurrentText(uf)
                return

        else:
            ui.campo_cnpj_municipio.setText("")
            ui.campo_cnpj_uf.setText("")
            return
    except RequestException:
        ui.campo_cnpj_municipio.setText("")
        ui.campo_cnpj_uf.setText("")
        notificacao = Notification(app_id="ERRO DE CONEXÃO", title="", msg="Sem conexão com a internet.", duration="short")
        notificacao.show()
        return
    except Exception as e:
        if hasattr(e, 'response') and e.response.status_code == 429:
            ui.campo_cnpj_municipio.setText("")
            ui.campo_cnpj_uf.setText("")
            notificacao = Notification(app_id="ACESSO BLOQUEADO", title="", msg="Limite de requisições atingido!\nEspere alguns segundos para fazer nova busca!", duration="short")
            notificacao.show()
            return
        else:
            ui.campo_cnpj_municipio.setText('CNPJ INVÁLIDO')
            ui.campo_cnpj_uf.setText('---') 
            return
    finally:
        if 'resposta' in locals() and resposta:
            resposta.close()    

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
    else:
        ui.campo_cnpj_municipio.setText('')
        ui.campo_cnpj_uf.setText('')

def salvar(ui):

    num_pedido = ui.campo_pedido.text()
    req = ref.get()
    for id in req:
        if num_pedido == req[id]['PEDIDO']:
            if ui.campo_lista_status.currentText() != "DIGITAÇÃO" and ui.campo_lista_status.currentText() != "VERIFICAÇÃO":
                resposta = QMessageBox.question(ui.centralwidget, "Confirmação", f"Finalizar o pedido como {ui.campo_lista_status.currentText()}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if resposta == QMessageBox.Yes:
                    pass
                else:
                    return
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
                data_nascimento = ""
                cod_seg_cnh = ""
                diretorio = ""
                municipio = ""
                uf = ""
                caminho_pasta = ""


                if pedido == "" or tipo == "" or hora == "00:00" or data == "01/01/2000" or status == "" or modalidade == "":

                    notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!",duration="short")
                    notificacao.show()
                    return
                
            
                #
                novos_dados = {"PASTA":caminho_pasta,"MUNICIPIO": municipio,"UF":uf,"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
                ##############################################################################################################################
                
                
                folder_to_delete = ui.caminho_pasta.text()
                folder_to_delete_raw = r"{}".format(folder_to_delete)
                forcar_fechamento_de_arquivo_e_deletar_pasta(folder_to_delete_raw)
                
                notificacao = Notification(app_id="Pedido",title="",msg=f"Pedido {pedido} salvo com sucesso\nStatus:{status}!",duration="short")
                notificacao.show()
                ref.child(id).update(novos_dados)
                limpar_campos(ui)
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
                data_nascimento = ui.campo_data_nascimento.text()
                vendido = ui.campo_lista_status_3.currentText()
                modalidade = ui.campo_lista_status_4.currentText()
                cod_seg_cnh = ui.campo_seguranca_cnh.text()
                diretorio = ui.campo_diretorio_pasta.toPlainText()
                municipio = ui.campo_cnpj_municipio.text()
                uf = ui.campo_cnpj_uf.text()
                caminho_pasta = ui.caminho_pasta.text()

                if pedido == "" or tipo == "" or hora == "00:00" or data == "01/01/2000" or status == "" or modalidade == "":

                    notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!",duration="short")
                    notificacao.show()
                    return
                #
                novos_dados = {"PASTA":caminho_pasta,"MUNICIPIO": municipio,"UF":uf,"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
                notificacao = Notification(app_id="Pedido",title="",msg=f"Pedido {pedido} salvo com sucesso\nStatus:{status}!",duration="short")
                notificacao.show()
                ref.child(id).update(novos_dados)
                return
   


        #aqui o pedido não existe e será gravado
        #caso o status seja diferente de Aguardando
        #os dados do cliente serão deletados
    if ui.campo_lista_status.currentText() != "DIGITAÇÃO" and ui.campo_lista_status.currentText() != "VERIFICAÇÃO":
        resposta = QMessageBox.question(ui.centralwidget, "Confirmação", f"Finalizar o pedido como {ui.campo_lista_status.currentText()}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resposta == QMessageBox.Yes:
            pass
        else:
            return
        
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
        data_nascimento = ""
        cod_seg_cnh = ""
        vendido = ui.campo_lista_status_3.currentText()
        diretorio = ""
        municipio = ""
        uf = ""
        caminho_pasta = ""

        if pedido == "" or tipo == "" or hora == "00:00" or data == "01/01/2000" or status == "" or modalidade == "":

            notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!",duration="short")
            notificacao.show()
            return
        
        
        #
        novos_dados = {"PASTA":caminho_pasta,"MUNICIPIO": municipio,"UF":uf,"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
        ##############################################################################################################################
       
        folder_to_delete = ui.caminho_pasta.text()
        folder_to_delete_raw = r"{}".format(folder_to_delete)
        forcar_fechamento_de_arquivo_e_deletar_pasta(folder_to_delete_raw)
        
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
        data_nascimento = ui.campo_data_nascimento.text()
        vendido = ui.campo_lista_status_3.currentText()
        modalidade = ui.campo_lista_status_4.currentText()
        cod_seg_cnh = ui.campo_seguranca_cnh.text()
        diretorio = ui.campo_diretorio_pasta.toPlainText()
        municipio = ui.campo_cnpj_municipio.text()
        uf = ui.campo_cnpj_uf.text()
        caminho_pasta = ui.caminho_pasta.text()
    
        if pedido == "" or tipo == "" or hora == "00:00" or data == "01/01/2000" or status == "" or modalidade == "":

            notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!",duration="short")
            notificacao.show()
            return
        #
        novos_dados = {"PASTA":caminho_pasta,"MUNICIPIO": municipio,"UF":uf,"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
        
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
                resposta = QMessageBox.question(ui.centralwidget, "Confirmação", f"Finalizar o pedido como {ui.campo_lista_status.currentText()}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if resposta == QMessageBox.Yes:
                    pass
                else:
                    return
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
                data_nascimento = ""
                cod_seg_cnh = ""
                diretorio = ""
                municipio = ""
                uf = ""
                caminho_pasta = ""

                if pedido == "" or tipo == "" or hora == "00:00" or data == "01/01/2000" or status == "" or modalidade == "":

                    notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!",duration="short")
                    notificacao.show()
                    return
                

                #
                novos_dados = {"PASTA":caminho_pasta,"MUNICIPIO": municipio,"UF":uf,"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
                ##############################################################################################################################
                
                folder_to_delete = ui.caminho_pasta.text()
                folder_to_delete_raw = r"{}".format(folder_to_delete)
                forcar_fechamento_de_arquivo_e_deletar_pasta(folder_to_delete_raw)
                
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
                data_nascimento = ui.campo_data_nascimento.text()
                vendido = ui.campo_lista_status_3.currentText()
                modalidade = ui.campo_lista_status_4.currentText()
                cod_seg_cnh = ui.campo_seguranca_cnh.text()
                diretorio = ui.campo_diretorio_pasta.toPlainText()
                municipio = ui.campo_cnpj_municipio.text()
                uf = ui.campo_cnpj_uf.text()
                caminho_pasta = ui.caminho_pasta.text()

                if pedido == "" or tipo == "" or hora == "00:00" or data == "01/01/2000" or status == "" or modalidade == "":

                    notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!",duration="short")
                    notificacao.show()
                    return
                #
                novos_dados = {"PASTA":caminho_pasta,"MUNICIPIO": municipio,"UF":uf,"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
                notificacao = Notification(app_id="Novo pedido",title="",msg=f"Pedido {pedido} atualizado com sucesso\nStatus:{status}!",duration="short")
                notificacao.show()
                ref.child(id).update(novos_dados)
                limpar_campos(ui)
                return
   
    if ui.campo_lista_status.currentText() != "DIGITAÇÃO" and ui.campo_lista_status.currentText() != "VERIFICAÇÃO":
        resposta = QMessageBox.question(ui.centralwidget, "Confirmação", f"Finalizar o pedido como {ui.campo_lista_status.currentText()}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resposta == QMessageBox.Yes:
            pass
        else:
            return
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
        data_nascimento = ""
        cod_seg_cnh = ""
        diretorio = ""
        municipio = ""
        uf = ""
        caminho_pasta = ""

        if pedido == "" or tipo == "" or hora == "00:00" or data == "01/01/2000" or status == "" or modalidade == "":

            notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!",duration="short")
            notificacao.show()
            return
        

        novos_dados = {"PASTA":caminho_pasta,"MUNICIPIO": municipio,"UF":uf,"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
        notificacao = Notification(app_id="Pedido",title="",msg=f"Pedido {pedido} salvo com sucesso\nStatus:{status}!",duration="short")
        
        ##############################################################################################################################
        
        folder_to_delete = ui.caminho_pasta.text()
        folder_to_delete_raw = r"{}".format(folder_to_delete)
        forcar_fechamento_de_arquivo_e_deletar_pasta(folder_to_delete_raw)
        
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
        data_nascimento = ui.campo_data_nascimento.text()
        vendido = ui.campo_lista_status_3.currentText()
        modalidade = ui.campo_lista_status_4.currentText()
        cod_seg_cnh = ui.campo_seguranca_cnh.text()
        diretorio = ui.campo_diretorio_pasta.toPlainText()
        municipio = ui.campo_cnpj_municipio.text()
        uf = ui.campo_cnpj_uf.text()
        caminho_pasta = ui.caminho_pasta.text()

        if pedido == "" or tipo == "" or hora == "00:00" or data == "01/01/2000" or status == "" or modalidade == "":

            notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!",duration="short")
            notificacao.show()
            return
        #
        novos_dados = {"PASTA":caminho_pasta,"MUNICIPIO": municipio,"UF":uf,"DIRETORIO":diretorio,"PEDIDO":pedido , "DATA":data, "HORA":hora, "TIPO":tipo, "STATUS":status,"NOME":nome,"RG":rg,"CPF":cpf,"CNH":cnh,"MAE":mae ,"CNPJ":cnpj,"EMAIL":email,"NASCIMENTO":data_nascimento,"VENDIDO POR MIM?":vendido,"MODALIDADE":modalidade,"CODIGO DE SEG CNH":cod_seg_cnh}
        
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
        req = sorted(req.values(), key=lambda x: (datetime.datetime.strptime(x['DATA'], "%d/%m/%Y"), datetime.datetime.strptime(x['HORA'], "%H:%M")))

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
                    try:
                        ui.tableWidget.setItem(row_position, 8, QTableWidgetItem(pedido_info['DIRETORIO']))
                    except:
                        pass

                    for col in range(ui.tableWidget.columnCount()):
                        item = ui.tableWidget.item(row_position, col)

                        # Obter a data e hora da célula
                        data_celula = ui.tableWidget.item(row_position, 2).text()
                        hora_celula = ui.tableWidget.item(row_position, 3).text()

                        # Converter as strings em objetos datetime
                        data_hora_celula = datetime.datetime.strptime(f"{data_celula} {hora_celula}", "%d/%m/%Y %H:%M")

                        # Verificar se a célula não está vazia
                        if item is not None:
                            # Comparar com a data e hora atuais
                            if data_hora_celula <= datetime.datetime.now():
                                #item.setBackground(QColor(227, 225, 225))   
                                pass                       
                            else:
                                # Configurar o fundo para azul claro para todas as outras células
                                item.setBackground(QColor(177, 215, 252))  # Azul claro
                        
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
        ui.tableWidget.setHorizontalHeaderLabels(["PEDIDO","NOME", "DATA", "HORA", "MODALIDADE", "STATUS", "VENDA","TIPO","OBSERVAÇÕES"])
        ui.barra_progresso_consulta.setVisible(False)
    except Exception as e:
            ui.tableWidget.setHorizontalHeaderLabels(["PEDIDO","NOME", "DATA", "HORA", "MODALIDADE", "STATUS", "VENDA","TIPO","OBSERVAÇÕES"])
            ui.label_quantidade_bd.setText(f"{x} registro(s)")
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
                ui.campo_lista_status_3.setCurrentText("NAO")
                ui.campo_lista_status_3.setCurrentText(req[pedido]['VENDIDO POR MIM?'])
                ui.campo_lista_status_4.setCurrentText(req[pedido]['MODALIDADE'])
                ui.campo_seguranca_cnh.setText(req[pedido]['CODIGO DE SEG CNH'])
                ui.campo_diretorio_pasta.setText(req[pedido]['DIRETORIO'])
                ui.campo_cnpj_municipio.setText(req[pedido]['MUNICIPIO'])
                ui.campo_cnpj_uf.setText(req[pedido]['UF'])
                ui.caminho_pasta.setText(req[pedido]['PASTA'])

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

def copiar_pedido_tabela(event):
    # Obtém a célula atualmente selecionada na tabela
    item = ui.tableWidget.currentItem()
    coluna = item.column()
    # Verifica se há um item selecionado
    if item is not None and coluna == 0:
        # Obtém o texto da célula
        valor_celula = item.text()

        # Copia o valor da célula para a área de transferência
        clipboard = QApplication.clipboard()
        clipboard.setText(valor_celula)
        ui.label_msg_copiado.setText("COPIADO!")
    else:
        ui.label_msg_copiado.setText("")
    
def pegar_valor_tabela(event):
   #evento disparado ao dar double click na tabela

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
                        ui.campo_lista_status_3.setCurrentText("NAO")
                        ui.campo_lista_status_3.setCurrentText(req[id]['VENDIDO POR MIM?'])
                        ui.campo_lista_status_4.setCurrentText(req[id]['MODALIDADE'])
                        ui.campo_pedido.setReadOnly(True)
                        ui.campo_seguranca_cnh.setText(req[id]['CODIGO DE SEG CNH'])
                        ui.campo_nome_mae.setText(req[id]['MAE'])
                        ui.campo_novo_noBd.setText("✅")
                        ui.campo_diretorio_pasta.setText(req[id]['DIRETORIO'])
                        ui.campo_cnpj_municipio.setText(req[id]['MUNICIPIO'])
                        ui.campo_cnpj_uf.setText(req[id]['UF'])
                        try:
                            ui.caminho_pasta.setText(req[id]['PASTA'])
                        except:
                            pass
                        return
                        
    except Exception as e:
        pass

def mesclar_pdf(ui):
    try:
        folder_to_open_directory = ui.caminho_pasta.text()
        folder_to_open_raw = r"{}".format(folder_to_open_directory)

        # Obter o nome do documento do usuário
        nome_documento, ok = QInputDialog.getText(ui.centralwidget, "Nome do Documento", "Digite o nome do documento:", text="CNH COMPLETA")

        # Verificar se o usuário cancelou a operação ou não forneceu um nome
        if not ok or not nome_documento:
            return

        # Criar um objeto PdfMerger para mesclar os PDFs
        pdf_merger = PyPDF2.PdfMerger()

        try:
            # Tentar abrir o diretório especificado
            file_paths, _ = QFileDialog.getOpenFileNames(ui.centralwidget, "Selecionar PDFs para Mesclar", folder_to_open_raw, "Arquivos PDF (*.pdf);;Todos os arquivos (*)")

            # Verificar se o usuário cancelou a seleção ou não escolheu nenhum arquivo
            if not file_paths:
                return

        except Exception as e:
            # Se não for possível abrir o diretório especificado, abrir o diálogo padrão
            file_paths, _ = QFileDialog.getOpenFileNames(ui.centralwidget, "Selecionar PDFs para Mesclar", "", "Arquivos PDF (*.pdf);;Todos os arquivos (*)")

            # Verificar se o usuário cancelou a seleção ou não escolheu nenhum arquivo
            if not file_paths:
                return

        # Adicionar os PDFs ao PdfMerger
        for path in file_paths:
            pdf_merger.append(path)

        # Usar o caminho da pasta do primeiro PDF como diretório padrão
        save_dir = os.path.dirname(file_paths[0])

        # Construir o caminho completo para o arquivo a ser salvo
        save_path = os.path.join(save_dir, f"{nome_documento}.pdf")

        # Mesclar os arquivos PDF
        with open(save_path, 'wb') as merged_pdf:
            pdf_merger.write(merged_pdf)

        # Fechar o objeto PdfMerger
        pdf_merger.close()

        # Notificar o usuário sobre a conclusão
        notificacao = Notification(app_id="Concluído", title="", msg="Os arquivos PDF foram mesclados com sucesso!")
        notificacao.show()

    except Exception as e:
        pdf_merger.close()
        # Lidar com exceções (você pode adicionar mais detalhes aqui, se necessário)
        return

def escolher_conversao(ui):
    # Criação da janela de diálogo
    dialog = QDialog(ui.centralwidget)
    dialog.setWindowTitle("Selecione o tipo de conversão")
    
    # Layout vertical para adicionar RadioButtons
    layout_dialog = QVBoxLayout(dialog)

    # Criando os RadioButtons
    radio_jpg_to_pdf = QRadioButton("JPG para PDF")
    radio_pdf_to_jpg = QRadioButton("PDF para JPG")
    
    # Adicionando os RadioButtons ao layout
    layout_dialog.addWidget(radio_jpg_to_pdf)
    layout_dialog.addWidget(radio_pdf_to_jpg)

    # Botão para confirmar e fechar a janela de diálogo
    botao_confirmar = QPushButton("Confirmar")
    layout_dialog.addWidget(botao_confirmar)

    # Função para ser executada ao clicar no botão de confirmação
    def confirmar():
        # Verificar qual RadioButton foi selecionado
        if radio_jpg_to_pdf.isChecked():
            # Chamar a função converter_jpg_to_pdf
            converter_jpg_para_pdf(ui)
        elif radio_pdf_to_jpg.isChecked():
            # Chamar a função converter_pdf_to_jpg
            converter_pdf_para_jpg(ui)
        dialog.accept()
    botao_confirmar.clicked.connect(confirmar)
    dialog.exec_()

def converter_jpg_para_pdf(ui):
    image_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.jpeg *.png")], title="Converter JPG/PNG > PDF")
    if not image_paths:
        return
    for image_path in image_paths:
        nome_do_arquivo, _ = os.path.splitext(os.path.basename(image_path))
        imagem = Image.open(image_path)
        imagem.save(f'{os.path.dirname(image_path)}\\{nome_do_arquivo}.pdf', 'PDF', resolution=100.0)

    notificacao = Notification(app_id="Concluído", title="", msg="As imagens foram convertidas em PDF com sucesso!")
    notificacao.show()

def converter_pdf_para_jpg(ui):
    pdf_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")], title="Converter PDF > img")
    if not pdf_paths:
        return
    for pdf_path in pdf_paths:
        nome_do_arquivo, _ = os.path.splitext(os.path.basename(pdf_path))
        pdf_document = fitz.open(pdf_path)
        primeira_pagina = pdf_document.load_page(0)
        imagem = primeira_pagina.get_pixmap()
        imagem_pillow = Image.frombytes("RGB", [imagem.width, imagem.height], imagem.samples)
        imagem_pillow.save(f'{os.path.dirname(pdf_path)}\\{nome_do_arquivo}.jpg', 'JPEG', quality=95)

    notificacao = Notification(app_id="Concluído", title="", msg="Os PDFs foram convertidos em JPG com sucesso!")
    notificacao.show()

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

def evento_ao_abrir(event):
    pass

def evento_ao_fechar(event):

    
    result = QMessageBox.question(janela, "Confirmação", "Você realmente deseja sair?", QMessageBox.Yes | QMessageBox.No)
    
    if result == QMessageBox.Yes:
        try:
            event.accept()  
          
        except:
            event.accept()
           
    else:
        event.ignore()

def copiar_campo(nome_campo):
    
    match nome_campo:
        
        case 'campo_cnh':
            try:
                QApplication.clipboard().setText(ui.campo_cnh.text())
                ui.campo_cnh.selectAll()
            except:
                pass
        case'campo_cnpj':
            try:
                QApplication.clipboard().setText(ui.campo_cnpj.text().replace('.','').replace('-','').replace('/',''))
                ui.campo_cnpj.selectAll()
            except:
                pass
        case'campo_pedido':
            try:
                QApplication.clipboard().setText(ui.campo_pedido.text())
                ui.campo_pedido.selectAll()
            except:
                pass
        case'campo_cpf':
            try:
                QApplication.clipboard().setText(ui.campo_cpf.text().replace('.','').replace('-',''))
                ui.campo_cpf.selectAll()
            except:
                pass
        case'campo_seguranca_cnh':
            try:
                QApplication.clipboard().setText(ui.campo_seguranca_cnh.text())
                ui.campo_seguranca_cnh.selectAll()
            except:
                pass
        case'campo_rg':
            try:
                QApplication.clipboard().setText(ui.campo_rg.text())
                ui.campo_rg.selectAll()
            except:
                pass
        case'campo_nome_mae':
            try:
                QApplication.clipboard().setText(ui.campo_nome_mae.text())
                ui.campo_nome_mae.selectAll()
            except:
                pass
        case'campo_nome':
            try:
                QApplication.clipboard().setText(ui.campo_nome.text())
                ui.campo_nome.selectAll()
            except:
                pass
        case'campo_msg1':
            try:
                QApplication.clipboard().setText(ui.campo_msg1.toPlainText())
            except:
                pass
        case'campo_msg2':
            try:
                QApplication.clipboard().setText(ui.campo_msg2.toPlainText())
            except:
                pass
        case'campo_msg3':
            try:
                QApplication.clipboard().setText(ui.campo_msg3.toPlainText())
            except:
                pass
        case'campo_msg4':
            try:
                QApplication.clipboard().setText(ui.campo_msg4.toPlainText())
            except:
                pass
        case'campo_msg5':
            try:
                QApplication.clipboard().setText(ui.campo_msg5.toPlainText())
            except:
                pass
        case'campo_msg6':
            try:
                QApplication.clipboard().setText(ui.campo_msg6.toPlainText())
            except:
                pass
        case'campo_msg7':
            try:
                QApplication.clipboard().setText(ui.campo_msg7.toPlainText())
            except:
                pass

def manter_tela_aberta(ui):
    if ui.campo_verifica_tela_cheia.text() == "SIM":
        ui.campo_verifica_tela_cheia.setText("NAO")
        ui.botao_tela_cheia.setText("🔓")
    else:
        ui.campo_verifica_tela_cheia.setText("SIM")
        ui.botao_tela_cheia.setText("🔒")

class JanelaOcultaHelper:
    def __init__(self, parent):
        self.parent = parent
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_window_size)
        self.animation_step = 5  # Ajuste conforme necessário
        self.animation_duration = 2  # Duração da animação em milissegundos
        self.animation_target_width = 0
        self.animation_target_height = 0

    def enterEvent(self, event):
        self.animate_window_resize(469, 640)
        

    def leaveEvent(self, event):
        if not ui.campo_verifica_tela_cheia.text()=="SIM":
            cursor_pos = QtGui.QCursor.pos()
            window_pos = self.parent.mapToGlobal(QtCore.QPoint(0, 0))
            window_rect = QRect(window_pos, self.parent.size())

            mouse_dentro_da_janela = window_rect.contains(cursor_pos)

            if not mouse_dentro_da_janela:
                self.animate_window_resize(256, 38)

    def mousePressEvent(self, event):
        self.animate_window_resize(469, 640)

    def animate_window_resize(self, target_width, target_height):
        self.animation_target_width = target_width
        self.animation_target_height = target_height
        self.animation_timer.stop()
        self.animation_timer.start(int(self.animation_duration / self.animation_step))

    def update_window_size(self):
        current_width = self.parent.width()
        current_height = self.parent.height()

        width_difference = self.animation_target_width - current_width
        height_difference = self.animation_target_height - current_height

        width_step = width_difference / self.animation_step
        height_step = height_difference / self.animation_step

        new_width = current_width + width_step
        new_height = current_height + height_step

        self.parent.setFixedSize(int(new_width), int(new_height))

        if (width_step > 0 and new_width >= self.animation_target_width) or \
           (width_step < 0 and new_width <= self.animation_target_width):
            self.animation_timer.stop()
            self.parent.setFixedSize(self.animation_target_width, self.animation_target_height)


import sys
app = QtWidgets.QApplication(sys.argv)
janela = QtWidgets.QMainWindow()
desktop = QDesktopWidget()
ui = Ui_janela()
ui.setupUi(janela)


helper = JanelaOcultaHelper(janela)
janela.enterEvent = helper.enterEvent
janela.leaveEvent = helper.leaveEvent
janela.mousePressEvent = helper.mousePressEvent
ui.botao_consultar.clicked.connect(lambda:preencher_tabela(ui))
ui.botao_terminar.clicked.connect(lambda:gravar_dados(ui))
ui.botao_procurar.clicked.connect(lambda:exportar_excel(ui))
ui.campo_cpf.editingFinished.connect(lambda:formatar_cpf(ui))
ui.campo_pedido.editingFinished.connect(lambda:carregar_dados(ui))
ui.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
ui.campo_cnpj.editingFinished.connect (lambda:formatar_cnpj(ui))
ui.campo_nome.editingFinished.connect(lambda:formatar_nome(ui))
ui.campo_nome_mae.editingFinished.connect(lambda:formatar_nome_mae(ui))
ui.botao_consulta_cnpj.clicked.connect(lambda:procurar_cnpj(ui))
ui.botao_consulta_cpf.clicked.connect(lambda:procurar_cpf(ui))
ui.botao_consulta_cnh.clicked.connect(lambda:procurar_cnh(ui))
ui.botao_consulta_rg.clicked.connect(lambda:procurar_rg(ui))
ui.tableWidget.itemDoubleClicked.connect(lambda:pegar_valor_tabela(ui))
ui.tableWidget.itemClicked.connect(lambda:copiar_pedido_tabela(ui))
ui.botao_salvar.clicked.connect(lambda:salvar(ui))
ui.botao_junta.clicked.connect(lambda:procurar_junta(ui))
ui.botao_print_direto_na_pasta.clicked.connect(lambda:print_tela(ui))
ui.botao_agrupar_PDF.clicked.connect(lambda:mesclar_pdf(ui))
ui.botao_pasta_cliente.clicked.connect(lambda:criar_pasta_cliente(ui))
ui.botao_tela_cheia.clicked.connect(lambda: manter_tela_aberta(ui))
ui.botao_gerar_link.clicked.connect(lambda:gerar_link_video_conferencia(ui))
ui.botao_converter_todas_imagens_em_pdf.clicked.connect(lambda:converter_todas_imagens_para_pdf(ui))
ui.campo_data_de.setDate(QDate.currentDate())
ui.campo_data_ate.setDate(QDate.currentDate())
ui.barra_progresso_pedido.setVisible(False)
ui.barra_progresso_consulta.setVisible(False)
ui.campo_nome.setContextMenuPolicy(Qt.NoContextMenu)
janela.closeEvent = evento_ao_fechar
#janela.showEvent = evento_ao_abrir
ui.campo_cnh.mousePressEvent = lambda event: copiar_campo("campo_cnh")
ui.campo_cnpj.mousePressEvent = lambda event: copiar_campo("campo_cnpj")
ui.campo_pedido.mousePressEvent = lambda event: copiar_campo("campo_pedido")
ui.campo_cpf.mousePressEvent = lambda event: copiar_campo("campo_cpf")
ui.campo_seguranca_cnh.mousePressEvent = lambda event: copiar_campo("campo_seguranca_cnh")
ui.campo_rg.mousePressEvent = lambda event: copiar_campo("campo_rg")
ui.campo_nome_mae.mousePressEvent = lambda event: copiar_campo("campo_nome_mae")
ui.campo_nome.mousePressEvent = lambda event: copiar_campo("campo_nome")
ui.campo_msg1.mousePressEvent = lambda event: copiar_campo("campo_msg1")
ui.campo_msg2.mousePressEvent = lambda event: copiar_campo("campo_msg2")
ui.campo_msg3.mousePressEvent = lambda event: copiar_campo("campo_msg3")
ui.campo_msg4.mousePressEvent = lambda event: copiar_campo("campo_msg4")
ui.campo_msg5.mousePressEvent = lambda event: copiar_campo("campo_msg5")
ui.campo_msg6.mousePressEvent = lambda event: copiar_campo("campo_msg6")
ui.campo_msg7.mousePressEvent = lambda event: copiar_campo("campo_msg7")
ui.campo_cnpj_municipio.setReadOnly(True)
ui.campo_msg1.setReadOnly(True)
ui.campo_msg2.setReadOnly(True)
ui.campo_msg3.setReadOnly(True)
ui.campo_msg4.setReadOnly(True)
ui.campo_msg5.setReadOnly(True)
ui.campo_msg6.setReadOnly(True)
ui.campo_msg7.setReadOnly(True)
ui.campo_cnpj_uf.setReadOnly(True)
ui.campo_cnpj_uf.setToolTip("⚠ - NECESSÁRIO PEDIR DOCUMENTO DE CONSTITUIÇÃO DA EMPRESA\n✅ - DOC PODE SER OBTIDO NA JUCESP")
ui.botao_print_direto_na_pasta.setToolTip("Tira um print da tela")
ui.botao_print_direto_na_pasta.setFlat(True)
ui.botao_gerar_link.setToolTip("Gera a link da vídeo-conferência")
ui.botao_gerar_link.setFlat(True)
ui.botao_converter_todas_imagens_em_pdf.setToolTip("Conversor de JPG/PDF")
ui.botao_converter_todas_imagens_em_pdf.setFlat(True)
ui.botao_tela_cheia.setToolTip("Liga/Desliga a tela cheia")
ui.botao_tela_cheia.setFlat(True)
ui.botao_agrupar_PDF.setToolTip("Mesclar PDF")
ui.botao_agrupar_PDF.setFlat(True)
ui.botao_dados_cnpj.clicked.connect(lambda:dados_cnpj(ui))


screen_rect = desktop.screenGeometry(desktop.primaryScreen())

x = screen_rect.width() - janela.width() - 20
y = (screen_rect.height() - janela.height()) // 6

janela.move(x, y)
janela.setWindowTitle("Auxiliar")
janela.setFixedSize(256, 38)           
janela.show()


sys.exit(app.exec_())


