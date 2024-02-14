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
import smtplib
import pyautogui
import sys
import subprocess
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
from PyQt5 import QtGui, QtWidgets,QtCore,Qt
from PyQt5.QtWidgets import QTableWidgetItem,QTableWidget,QApplication,QMessageBox,QDesktopWidget,QInputDialog,QMainWindow,QFileDialog,QRadioButton,QVBoxLayout,QPushButton,QDialog, QLineEdit
from PyQt5.QtCore import QDate, QTime,QUrl, Qt,QTimer,QRect,QRegExp
from PyQt5.QtGui import QDesktopServices,QColor,QRegExpValidator,QPixmap, QImage
from Interface import Ui_janela
from firebase_admin import db
from requests.exceptions import RequestException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from credenciaisBd import obter_credenciais


credenciais = obter_credenciais()

acoes = firebase_admin.credentials.Certificate(credenciais)
firebase_admin.initialize_app(acoes, {'databaseURL':'https://bdpedidos-2078f-default-rtdb.firebaseio.com/'}) 

#Referência raiz do banco de dados
ref = db.reference("/")


class Funcoes_padrao:
    def __init__(self,ui):
        self.ui = ui
        self.acoes = Acoes_banco_de_dados(ui)
    
    def atualizar_barras_metas(self):
        
        try:
            soma = int(ui.campo_certificados_semana_1.text()) + int(ui.campo_certificados_semana_2.text()) + int(ui.campo_certificados_semana_3.text()) + int(ui.campo_certificados_semana_4.text()) + int(ui.campo_certificados_semana_5.text())
            meta_mensal = int(ui.campo_meta_mes.text())  # Convertido para inteiro
            meta_semanal = int(ui.campo_meta_semanal.text())  # Convertido para inteiro

            certificados_semana_1 = int(ui.campo_certificados_semana_1.text())
            ui.barra_meta_semana_1.setMaximum(int(meta_semanal))
            if certificados_semana_1 >= meta_semanal:
                #Meta atingida
                ui.label_meta1.setStyleSheet('background-color: rgb(0, 173, 247);')
                ui.label_meta1.setText(f"Meta atingida!🥳 - {certificados_semana_1}/{meta_semanal}")
            else:
                #Meta não atingida
                ui.label_meta1.setStyleSheet('background-color: rgba(255, 0, 0, 0);')
                ui.label_meta1.setText(f"{certificados_semana_1}/{meta_semanal}")

            certificados_semana_2 = int(ui.campo_certificados_semana_2.text())
            ui.barra_meta_semana_2.setMaximum(int(meta_semanal))
            if certificados_semana_2 >= meta_semanal:
                #Meta atingida
                ui.label_meta2.setStyleSheet('background-color: rgb(0, 173, 247);')
                ui.label_meta2.setText(f"Meta atingida!🥳 - {certificados_semana_2}/{meta_semanal}")
            else:
                #Meta não atingida
                ui.label_meta2.setStyleSheet('background-color: rgba(255, 0, 0, 0);')
                ui.label_meta2.setText(f"{certificados_semana_2}/{meta_semanal}")

            certificados_semana_3 = int(ui.campo_certificados_semana_3.text())
            ui.barra_meta_semana_3.setMaximum(int(meta_semanal))
            if certificados_semana_3 >= meta_semanal:
                #Meta atingida
                ui.label_meta3.setStyleSheet('background-color: rgb(0, 173, 247);')
                ui.label_meta3.setText(f"Meta atingida!🥳 - {certificados_semana_3}/{meta_semanal}")
            else:
                #Meta não atingida
                ui.label_meta3.setStyleSheet('background-color: rgba(255, 0, 0, 0);')
                ui.label_meta3.setText(f"{certificados_semana_3}/{meta_semanal}")

            certificados_semana_4 = int(ui.campo_certificados_semana_4.text())
            ui.barra_meta_semana_4.setMaximum(int(meta_semanal))
            if certificados_semana_4 >= meta_semanal:
                #Meta atingida
                ui.label_meta4.setStyleSheet('background-color: rgb(0, 173, 247);')
                ui.label_meta4.setText(f"Meta atingida!🥳 - {certificados_semana_4}/{meta_semanal}")
            else:
                #Meta não atingida
                ui.label_meta4.setStyleSheet('background-color: rgba(255, 0, 0, 0);')
                ui.label_meta4.setText(f"{certificados_semana_4}/{meta_semanal}")

            certificados_semana_5 = int(ui.campo_certificados_semana_5.text())
            ui.barra_meta_semana_5.setMaximum(int(meta_semanal))
            if certificados_semana_5 >= meta_semanal:
                #Meta atingida
                ui.label_meta5.setStyleSheet('background-color: rgb(0, 173, 247);')
                ui.label_meta5.setText(f"Meta atingida!🥳 - {certificados_semana_5}/{meta_semanal}")
            else:
                #Meta não atingida
                ui.label_meta5.setStyleSheet('background-color: rgba(255, 0, 0, 0);')
                ui.label_meta5.setText(f"{certificados_semana_5}/{meta_semanal}")

            ui.barra_meta_mensal.setMaximum(int(meta_mensal))
            ui.label_meta_mes.setText(f"{soma}/{ui.campo_meta_mes.text()}")
            if soma >= meta_mensal:
                #Meta atingida
                ui.label_meta_mes.setStyleSheet('background-color: rgb(0, 173, 247);')
                ui.label_meta_mes.setText(f"Meta atingida!🥳 - {soma}/{meta_mensal}")
            else:
                #Meta não atingida
                ui.label_meta_mes.setStyleSheet('background-color: rgba(255, 0, 0, 0);')
                ui.label_meta_mes.setText(f"{soma}/{meta_mensal}")

        except Exception as e:
            pass

    def trazer_configuracoes(self):
        #CORRIGIDO ------------------------------------------------------------------
        try:
            ref = db.reference("/Configuracoes")
            # Faz uma solicitação GET para obter as configurações do banco de dados
            configs = ref.get()

            try:
                cor = configs["RGB"]
                r, g, b = map(int, cor.split(','))

                ui.caminho_pasta_principal.setText(configs['DIRETORIO-RAIZ'])
                ui.campo_senha_email_empresa.setText(configs['SENHA'])
                ui.campo_email_empresa.setText(configs['E-MAIL'])
                ui.campo_cor_R.setValue(int(r))
                ui.campo_cor_G.setValue(int(g))
                ui.campo_cor_B.setValue(int(b))
                ui.campo_porcentagem_validacao.setValue(int(configs['PORCENTAGEM']))
                ui.campo_imposto_validacao.setValue(configs['IMPOSTO VALIDACAO'])
                ui.campo_desconto_validacao.setValue(configs['DESCONTO VALIDACAO'])


            except Exception as e:
                pass
        except:
            pass

    def trazer_metas(self):
        #CORRIGIDO ----------------------------------------------------------
        ref = db.reference("/Metas")
        # Faz uma solicitação GET para obter as configurações do banco de dados
        Metas = ref.get()
    
        try:
            valor_semanal = Metas['SEMANAL']
            valor_mensal = Metas['MENSAL']
            ui.campo_meta_semanal.setValue(int(valor_semanal))
            ui.campo_meta_mes.setValue(int(valor_mensal))
        except Exception as e:
            pass       

    def atualizar_meta_clientes(self):
        #CORRIGIDO ----------------------------------------------------------------------------------------
        if ui.tabWidget.currentIndex() == 4:
            # Certifique-se de que req é um dicionário
            ref = db.reference("/Pedidos")
            Pedidos = ref.get()
            
            # Inicializando contadores para cada semana
            semana1 = 0
            semana2 = 0
            semana3 = 0
            semana4 = 0
            semana5 = 0

            # Obter a data do campo ui.campo_data_meta
            mes_meta = ui.campo_data_meta.date().month()
            ano_meta = ui.campo_data_meta.date().year()
            
            for pedido_info in Pedidos:
                # Verificando se o status é aprovado
                if Pedidos[pedido_info]['STATUS'] == "APROVADO":
                    # Obtendo a data do pedido
                    data_pedido = Pedidos[pedido_info]['DATA']
                    
                    # Convertendo a data para o formato desejado (considerando que DATA_PEDIDO é uma string)
                    data_formatada = datetime.datetime.strptime(data_pedido, "%d/%m/%Y")
                    
                    # Verificando se o pedido pertence ao mesmo mês e ano de referência
                    if data_formatada.month == mes_meta and data_formatada.year == ano_meta:
                        # Obtendo a semana do mês
                        semana_do_mes = data_formatada.isocalendar()[1] - (datetime.datetime(data_formatada.year, data_formatada.month, 1).isocalendar()[1] - 1)
                        
                        # Incrementando o contador da semana correspondente
                        if semana_do_mes == 1:
                            semana1 += 1
                        elif semana_do_mes == 2:
                            semana2 += 1
                        elif semana_do_mes == 3:
                            semana3 += 1
                        elif semana_do_mes == 4:
                            semana4 += 1
                        elif semana_do_mes == 5:
                            semana5 += 1

            ui.campo_certificados_semana_1.setText(str(semana1))
            ui.campo_certificados_semana_2.setText(str(semana2))
            ui.campo_certificados_semana_3.setText(str(semana3))
            ui.campo_certificados_semana_4.setText(str(semana4))
            ui.campo_certificados_semana_5.setText(str(semana5))
            # Agora você tem a quantidade de pedidos aprovados para cada semana
            
            ui.barra_meta_semana_1.setValue(semana1)
            ui.barra_meta_semana_2.setValue(semana2)
            ui.barra_meta_semana_3.setValue(semana3)
            ui.barra_meta_semana_4.setValue(semana4)
            ui.barra_meta_semana_5.setValue(semana5)
            total = semana1 + semana2 + semana3 + semana4 + semana5
            ui.barra_meta_mensal.setValue(total)
            ui.barra_meta_mensal.setMaximum(int(ui.campo_meta_mes.text()))
            ui.campo_certificados_mes.setText(str(total))
            self.atualizar_barras_metas()

    def definir_cor(self):
        cor_R = ui.campo_cor_R.value()
        cor_G = ui.campo_cor_G.value()
        cor_B = ui.campo_cor_B.value()
        ui.label_5.setStyleSheet(f"background-color:rgb({cor_R}, {cor_G}, {cor_B});\n")
       
    def Atualizar_meta(self):
        #CORRIGIDO
        ref = db.reference("/Metas")

        # Obtém as metas da interface do usuário
        meta_semana = ui.campo_meta_semanal.text()
        meta_mes = ui.campo_meta_mes.text()

        # Cria um dicionário com as novas metas
        nova_meta = {"MENSAL": meta_mes, "SEMANAL": meta_semana}

        try:
            # Tenta atualizar as metas no banco de dados
            ref.update(nova_meta)
            print("Metas atualizadas com sucesso.")
        except Exception as e:
            # Se ocorrer um erro, tenta adicionar as novas metas
            try:
                ref.set(nova_meta)
                print("Novas metas adicionadas com sucesso.")
            except Exception as e:
                print(f"Erro ao atualizar ou adicionar metas: {e}")
   
    def atualizar_configuracoes(self):
        #CORRIGIDO --------------------------------------------------
        resposta = QMessageBox.question(ui.centralwidget, "Confirmação", "Atualizar configurações?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resposta == QMessageBox.Yes:
            pass
        else:
            return
        
        ref = db.reference("/Configuracoes")
        
        diretorio = ui.caminho_pasta_principal.text()
        email = ui.campo_email_empresa.text()
        senha = ui.campo_senha_email_empresa.text()
        rgb = (f"{ui.campo_cor_R.value()},{ui.campo_cor_G.value()},{ui.campo_cor_B.value()}")
        porcentagem = ui.campo_porcentagem_validacao.value()
        desconto = ui.campo_desconto_validacao.value()
        imposto = ui.campo_imposto_validacao.value()
        nova_config = {"DIRETORIO-RAIZ": diretorio,"E-MAIL":email,"SENHA":senha ,"RGB":rgb,"PORCENTAGEM":porcentagem,"IMPOSTO VALIDACAO":imposto,"DESCONTO VALIDACAO":desconto}

        try:
            ref.update(nova_config)
        except Exception as e:
            try:
                ref.set(nova_config)
                print("Novas metas adicionadas com sucesso.")
            except Exception as e:
                print(f"Erro ao atualizar ou adicionar metas: {e}")

    def atualizar_diretorio_raiz(self):
        widget_pai = ui.centralwidget
        # Abrir o explorer para selecionar a pasta raiz
        resposta = QMessageBox.question(ui.centralwidget, "Confirmação", "Tem certeza que deseja atualizar a pasta raiz?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resposta == QMessageBox.Yes:
            pass
        else:
            return

        diretorio_selecionado = QFileDialog.getExistingDirectory(widget_pai , 'Selecione o diretório raiz')

        if diretorio_selecionado:
            # Atualizar o campo de texto na interface gráfica
            ui.caminho_pasta_principal.setText(diretorio_selecionado)

        else:
            pass

    def converter_todas_imagens_para_pdf(self):
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
            ui.label_confirmacao_converter_pdf.setText("✅")
            #self.mensagem_alerta("Concluído",f"imagens convertidas!")
        else:
            self.escolher_conversao()

    def obter_janela_principal(self,widget):
        # Função para obter a janela principal a partir de um widget
        while widget:
            if isinstance(widget, QMainWindow):
                return widget
            widget = widget.parent()
        return None

    def print_tela(self):
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

                nome_documento, ok = QInputDialog.getText(ui.centralwidget, "Nome da print", "Digite o nome da print:",text=f"DOC ADICIONAL")
                if not ok:           
                    return
                
                if not nome_documento:
                    return
                caminho = f"{caminho}/{nome_documento}.png"
            janela_principal = self.obter_janela_principal(ui.centralwidget)

            if janela_principal:

                janela_principal.setWindowOpacity(0)
            # Aguarda um curto período para garantir que a janela tenha tempo de minimizar
            time.sleep(0.5)

            # Tira um screenshot da tela
            screenshot = pyautogui.screenshot()

            # Restaura a janela principal (opcional)
            if janela_principal:
                #janela_principal.showNormal()
                janela_principal.setWindowOpacity(1)

            # Salva o screenshot no caminho especificado
        
            screenshot.save(caminho)

            ui.label_confirmacao_tirar_print.setText("✅")
            #self.mensagem_alerta("Concluído",f"Print capturada!")
        
        except:
            ui.label_confirmacao_tirar_print.setText("❌")
            self.mensagem_alerta("Erro",f"Não foi possível capturar a tela!")

    def gerar_link_video_conferencia(self):
        
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


        if ui.campo_lista_modalidade.currentText() == "PRESENCIAL":
            ui.label_confirmacao_criar_link_video.setText("❌")
            self.mensagem_alerta("Erro","Não é possível gerar link na modalidade presencial!")
            return
        
        elif ui.campo_link_webex.text() != "":
            ui.label_confirmacao_criar_link_video.setText("❌")
            self.mensagem_alerta("Erro","Não é possível gerar link quando a reunião é feita pelo WEBEX!")
            return


        link = f"https://certisign.omotor.com.br/#/dossie-detail/{pedido}"

        try:
            default_file_name = "LINK VIDEO"
            
            # Obtém o caminho do arquivo diretamente do campo_pasta
            save_path = ui.caminho_pasta.text()

            if not save_path:

                ui.label_confirmacao_criar_link_video.setText("❌")
                self.mensagem_alerta("Pasta ausente","Crie a pasta do cliente!")

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
            
            ui.label_confirmacao_criar_link_video.setText("✅")
            #self.mensagem_alerta("Concluído","Link salvo com sucesso!")

        except:

            ui.label_confirmacao_criar_link_video.setText("❌")
            self.mensagem_alerta("Arquivo existente","Já existe um arquivo LINK_VIDEO na pasta!")

    def pasta_existe(self,diretorio, nome_pasta):
        caminho_pasta = os.path.join(diretorio, nome_pasta)
        return os.path.exists(caminho_pasta)

    def criar_pasta_cliente(self):
        try:
            pedido = ui.campo_pedido.text()
            versao = ui.campo_lista_versao_certificado.currentText()
            hora = ui.campo_hora_agendamento.text()
            data = ui.campo_data_agendamento.text()
            status = ui.campo_lista_status.currentText()
            modalidade = ui.campo_lista_modalidade.currentText()

            if pedido == "" or hora == "00:00" or data == "01/01/2000" or status == "" or modalidade == "" or versao == "":

                ui.label_confirmacao_criar_pasta.setText("❌")
                self.mensagem_alerta("Pasta não criada","Adicione os itens com 🌟 para criar a pasta do cliente!")
                return

            self.formatar_nome()
            nome_pasta = f'{ui.campo_pedido.text()}-{ui.campo_nome.text()}'
            if nome_pasta == '':
                ui.label_confirmacao_criar_pasta.setText("❌")
                self.mensagem_alerta("Pasta não criada","Preencha o NOME do cliente.")
                return

            # Tente criar a pasta no diretório padrão
            diretorio_padrão = ui.caminho_pasta_principal.text()
            pasta_padrão = os.path.join(diretorio_padrão, nome_pasta)

            if not self.pasta_existe(diretorio_padrão, nome_pasta):
                
                os.mkdir(pasta_padrão)
                pasta_padrão = pasta_padrão.replace("/", "\\")
                ui.caminho_pasta.setText(pasta_padrão)
                
                status = ui.campo_lista_status.currentText()
                if status == "APROVADO" or status == "CANCELADO":
                    confirmacao = ""
                else:
                    confirmacao = "✅"

                ui.label_confirmacao_criar_pasta.setText(confirmacao)
                #self.mensagem_alerta("Pasta Criada",f"Pasta do cliente {nome_pasta} criada com sucesso!")
                self.acoes.analise_dados()
            else:
                self.abrir_pasta_cliente()
        except:
            ui.label_confirmacao_criar_pasta.setText("❌")
            #self.mensagem_alerta("Erro","Pasta não criada")

    def procurar_cnh(self):
        url = QUrl("https://sso.acesso.gov.br/login?client_id=portalservicos.denatran.serpro.gov.br&authorization_id=18aa635cf94")
        QDesktopServices.openUrl(url)
        return

    def mensagem_alerta(self,titulo,mensagem):
        QMessageBox.information(ui.centralwidget, titulo, mensagem, QMessageBox.Ok)

    def procurar_oab(self):

        url = QUrl("https://cna.oab.org.br/")
        QDesktopServices.openUrl(url)
        return

    def procurar_rg(self):
        url = QUrl("https://acertid.net.br/acertid/")
        QDesktopServices.openUrl(url)
        return

    def formatar_orgao_rg(self):
        orgao = ui.campo_rg_orgao.text().rstrip()
        ui.campo_rg_orgao.setText(orgao.upper())

    def procurar_cnpj(self):
        cnpj = ui.campo_cnpj.text()
        url_receita = QUrl(f"https://solucoes.receita.fazenda.gov.br/servicos/cnpjreva/Cnpjreva_Solicitacao.asp?cnpj={cnpj}")
        QDesktopServices.openUrl(url_receita)

    def procurar_junta(self):

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

    def formatar_nome(self):
        nome = ui.campo_nome.text().rstrip()  # Obtenha o texto do campo_nome_mae
        ui.campo_nome.setText(nome.upper())

    def formatar_nome_mae(self):
        texto_mae = ui.campo_nome_mae.text()  # Obtenha o texto do campo_nome_mae
        ui.campo_nome_mae.setText(texto_mae.upper())

    def dados_cnpj(self):
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
                ui.campo_cnpj_razao_social.setText(data['nome'])
                uf = data['uf']
                
                if uf != "SP":
                    ui.campo_cnpj_uf.setText(str(uf))
                    ui.campo_lista_junta_comercial.setCurrentText(uf)
                    return
                else:
                    ui.campo_cnpj_uf.setText(str(uf))
                    ui.campo_lista_junta_comercial.setCurrentText(uf)
                    return

            else:
                ui.campo_cnpj_municipio.setText("")
                ui.campo_cnpj_uf.setText("")
                return
        except RequestException:
            ui.campo_cnpj_municipio.setText("")
            ui.campo_cnpj_uf.setText("")
            self.mensagem_alerta("ERRO DE CONEXÃO","Sem conexão com a internet.")
            return
        except Exception as e:
            self.mensagem_alerta("ACESSO BLOQUEADO","Limite de requisições atingido!\nEspere alguns segundos para fazer nova busca!")
            return   

    def procurar_cpf(self):
        
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

    def formatar_cpf(self):
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
            
    def formatar_cnpj(self):
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

    def exportar_excel(self):
        try:
            ref = db.reference("/Pedidos")
            req = ref.get()
            
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

                        try:
                            versao = req[cliente]['VERSAO']
                        except:
                            versao = ""
                            pass

                        try:
                            preco = req[cliente]['PRECO']
                        except:
                            preco = ""
                            pass


                        hora_agendamento = req[cliente]['HORA']    
                        status_agendamento = req[cliente]['STATUS']
                        vendido = req[cliente]['VENDA']
                        modalidade = req[cliente]['MODALIDADE']
                        

                        dados_selecionados.append((pedido, data_agendamento, versao, hora_agendamento,status_agendamento,vendido,modalidade,preco))   

                    elif status_filtro == "TODAS":

                        x += 1

                        pedido = req[cliente]['PEDIDO']
                        data_agendamento = req[cliente]['DATA']

                        try:
                            versao = req[cliente]['VERSAO']
                        except:
                            versao = ""
                            pass

                        try:
                            preco = req[cliente]['PRECO']
                        except:
                            preco = ""
                            pass
                        


                        
                        hora_agendamento = req[cliente]['HORA']    
                        status_agendamento = req[cliente]['STATUS']
                        vendido = req[cliente]['VENDA']
                        modalidade = req[cliente]['MODALIDADE']
                        

                        dados_selecionados.append((pedido, data_agendamento, versao,hora_agendamento,status_agendamento,vendido,modalidade,preco)) 
            
            if x > 0:
                root = tk.Tk()
                root.withdraw()
                caminho_arquivo = filedialog.askdirectory()
                if caminho_arquivo:
                    df=pd.DataFrame(dados_selecionados,columns=['Pedido','Data agendamento','Versão','hora','Status Pedido','Vendido por mim?','Modalidade','Preço'])
                    data_agora = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
                    data_final = ui.campo_data_ate.text()
                    data_inicial = ui.campo_data_de.text()
                    pasta_desktop = os.path.expanduser(f"{caminho_arquivo}")
                    nome_arquivo = os.path.join(pasta_desktop, f"Certificados-emitidos-de {data_inicial.replace('/', '-')} a {data_final.replace('/', '-')}-gerado em{data_agora.replace('/','-')} .xlsx")
                    df.to_excel(nome_arquivo, index=False)
                    self.mensagem_alerta("Arquivo salvo","Arquivo excel gerado!")
                else:
                    return
            else:
                self.mensagem_alerta("Sem dados","Sem dados para o período!")

        except Exception as e:
            self.mensagem_alerta("Arquivo não salvo",f"Arquivo não gerado!\nmotivo: {e}")
            # Lida com exceções aqui
            pass

    def copiar_pedido_tabela(self,event):
        # Obtém a célula atualmente selecionada na tabela
        item = ui.tableWidget.currentItem()
        coluna = item.column()
        # Verifica se há um item selecionado
        if item is not None and coluna == 1:
            # Obtém o texto da célula
            valor_celula = item.text()

            # Copia o valor da célula para a área de transferência
            clipboard = QApplication.clipboard()
            clipboard.setText(valor_celula)
            ui.label_msg_copiado.setText("✅")
        else:
            ui.label_msg_copiado.setText("")
        
    def mesclar_pdf(self):
        try:
            folder_to_open_directory = ui.caminho_pasta.text()
            folder_to_open_raw = r"{}".format(folder_to_open_directory)

            # Obter o nome do documento do usuário
            nome_documento, ok = QInputDialog.getItem(ui.centralwidget, "Nome do Documento", "Escolha o tipo de documento:", ["CNH COMPLETA", "RG COMPLETO","DOC ADICIONAL","DOC COMPLETO","OUTRO"], 0, False)
            
            
            if nome_documento == "OUTRO":
                nome_documento, ok = QInputDialog.getText(ui.centralwidget, "Nome do Documento", "Digite o nome do documento:")
            
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

                file_paths, _ = QFileDialog.getOpenFileNames(ui.centralwidget, "Selecionar PDFs para Mesclar", "", "Arquivos PDF (*.pdf);;Todos os arquivos (*)")

                if not file_paths:
                    return

            for path in file_paths:
                pdf_merger.append(path)

            save_dir = os.path.dirname(file_paths[0])

            save_path = os.path.join(save_dir, f"{nome_documento}.pdf")

            with open(save_path, 'wb') as merged_pdf:
                pdf_merger.write(merged_pdf)

            pdf_merger.close()

            ui.label_confirmacao_mesclar_pdf.setText("✅")
            #self.mensagem_alerta("Concluído","Os arquivos PDF foram mesclados com sucesso!")

        except:
            ui.label_confirmacao_mesclar_pdf.setText("❌")
            pdf_merger.close()
            # Lidar com exceções (você pode adicionar mais detalhes aqui, se necessário)
            return

    def escolher_conversao(self):
        # Criação da janela de diálogo
        dialog = QDialog(ui.centralwidget)
        dialog.setWindowTitle("Selecione o tipo de conversão")
        
        layout_dialog = QVBoxLayout(dialog)

        radio_jpg_to_pdf = QRadioButton("JPG para PDF")
        radio_pdf_to_jpg = QRadioButton("PDF para JPG")
        

        layout_dialog.addWidget(radio_jpg_to_pdf)
        layout_dialog.addWidget(radio_pdf_to_jpg)

        botao_confirmar = QPushButton("Confirmar")
        layout_dialog.addWidget(botao_confirmar)


        def confirmar():
            # Verificar qual RadioButton foi selecionado
            if radio_jpg_to_pdf.isChecked():
                # Chamar a função converter_jpg_to_pdf
                self.converter_jpg_para_pdf()
            elif radio_pdf_to_jpg.isChecked():
                # Chamar a função converter_pdf_to_jpg
                self.converter_pdf_para_jpg()
            dialog.accept()
        botao_confirmar.clicked.connect(confirmar)
        dialog.exec_()

    def converter_jpg_para_pdf(self):
        try:
            image_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.jpeg *.png")], title="Converter JPG/PNG > PDF")
            if not image_paths:
                return
            for image_path in image_paths:
                nome_do_arquivo, _ = os.path.splitext(os.path.basename(image_path))
                imagem = Image.open(image_path)
                imagem.save(f'{os.path.dirname(image_path)}\\{nome_do_arquivo}.pdf', 'PDF', resolution=100.0)
            ui.label_confirmacao_converter_pdf.setText("✅")
            #self.mensagem_alerta("Concluído","As imagens foram convertidas em PDF com sucesso!")
        except:
            ui.label_confirmacao_converter_pdf.setText("❌")

    def converter_pdf_para_jpg(self):
        try:
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
            ui.label_confirmacao_converter_pdf.setText("✅")

        except:
            ui.label_confirmacao_converter_pdf.setText("❌")

            
        #self.mensagem_alerta("Concluído","Os PDFs foram convertidos em JPG com sucesso!")

    def texto_para_pdf(self):
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
            self.mensagem_alerta("Concluído","Texto salvo com sucesso!")
        except:
            self.mensagem_alerta("Erro","Feche o arquivo PDF!")

    def evento_ao_abrir(self,event):
        self.trazer_configuracoes()
        self.trazer_metas()
        self.definir_cor()
        self.carregar_lista_certificados()
        ui.campo_data_meta.setDate(QDate.currentDate())
        self.ui.campo_status_bd.setText("")
        self.ui.campo_status_bd.setToolTip("")
        
    def evento_ao_fechar(self,event):

        
        result = QMessageBox.question(janela, "Confirmação", "Você realmente deseja sair?", QMessageBox.Yes | QMessageBox.No)
        
        if result == QMessageBox.Yes:
            try:
                event.accept()  
            
            except:
                event.accept()
            
        else:
            event.ignore()

    def copiar_campo(self,nome_campo):
        
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
            case'campo_msg_doc_idf':
                try:
                    agora = datetime.datetime.now().time()
                 
                    match agora:
                        case tempo if tempo < datetime.datetime.strptime("12:00", "%H:%M").time():
                            mensagem_inicial = "Bom dia!"
                        case tempo if datetime.datetime.strptime("12:00", "%H:%M").time() < tempo < datetime.datetime.strptime("17:59", "%H:%M").time():
                            mensagem_inicial = "Boa tarde!"
                        case tempo if tempo >= datetime.datetime.strptime("18:00", "%H:%M").time():
                            mensagem_inicial = "Boa noite!"
                            
                            

                    mensagem = f"""{mensagem_inicial} tudo bem?                                                                                      
Irei precisar de uma foto completa do seu documento de identificação, _*FRENTE E VERSO*_, podendo ser _*CNH, RG, OAB.*_                                         
_*Observações:*_ Retire o documento do plástico e abra-o."""
    
                    ui.campo_msg_doc_idf.setPlainText(mensagem)                   
                    QApplication.clipboard().setText(mensagem)
                except:
                    pass

            case'campo_msg_doc_empresa':
                try:
                    mensagem = f"""                                                                                         
Irei precisar tambem do documento de constituição da empresa, podendo ser _*Contrato Social, Certidão de inteiro teor, Estatuto social, Requerimento de empresário.*_"""                  
                    QApplication.clipboard().setText(mensagem)
                except:
                    pass

            case'campo_msg2':
                try:
                    QApplication.clipboard().setText(ui.campo_msg2.toPlainText())
                except:
                    pass
            case'campo_msg3':
                #Campo que contém o e-mail padrão 
                try: 
                        self.email_padrao_webex()        
                        QApplication.clipboard().setText(ui.campo_msg3.toPlainText())
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
            case'campo_msg_agendamento':
                try:
                    QApplication.clipboard().setText(ui.campo_msg_agendamento.text())
                except:
                    pass
            case'campo_assunto_email':
                try:
                    QApplication.clipboard().setText(ui.campo_assunto_email.text())
                except:
                    pass
            case'campo_msg_venda':
                try:
                    QApplication.clipboard().setText(ui.campo_msg_venda.toPlainText())
                except:
                    pass
            case'campo_msg_reembolso':
                try:
                    QApplication.clipboard().setText(ui.campo_msg_reembolso.toPlainText())
                except:
                    pass

    def manter_tela_aberta(self):
        if ui.campo_verifica_tela_cheia.text() == "SIM":
            ui.campo_verifica_tela_cheia.setText("NAO")
            ui.botao_tela_cheia.setText("🔓")
        else:
            ui.campo_verifica_tela_cheia.setText("SIM")
            ui.botao_tela_cheia.setText("🔒")

    def abrir_pasta_cliente(self):
        try:
            caminho_pasta_cliente = ui.caminho_pasta.text()
            QDesktopServices.openUrl(QUrl.fromLocalFile(caminho_pasta_cliente))
        except:
            return

    def email_padrao_webex(self):
        try:
            nome = ui.campo_nome.text()
            pedido = ui.campo_pedido.text()
            link = ui.campo_link_webex.text()
            mensagem = ui.campo_msg3.toPlainText()
            email = ui.campo_email_empresa.text()
            senha = ui.campo_senha_email_empresa.text()
            hora = ui.campo_hora_agendamento.time().toString("HH:mm")
            data = ui.campo_data_agendamento.date().toString("dd/MM/yyyy")
            certificado = ui.campo_lista_versao_certificado.currentText()
            if "e-CNPJ" in certificado:
                versao = "e-CNPJ"
            elif "e-CPF" in certificado:
                versao = "e-CPF"

            
            if versao == "e-CNPJ":
                            texto_formatado = (
f"""Olá {nome.capitalize()}, tudo bem?

Sou o Rafael, agente de registro da AR ACB SERVICOS E NEGOCIOS e estou entrando em contato pois temos uma validação para
seu certificado digital às {hora} do dia {data}, pedido {pedido}.

Para agilizar o processo, peço que o senhor encaminhe para um dos contatos abaixo, os seguintes documentos:
1 - uma foto completa do seu documento de identificação, FRENTE E VERSO, podendo ser CNH, RG, OAB
Observações: Retire o documento do plástico e abra-o.

2 - O documento de constituição da empresa, podendo ser Contrato Social, Certidão de inteiro teor, Estatuto social, Requerimento de empresário.

Para acessar a reunião, clique no link da vídeo-conferência abaixo:
{link}

Em caso de dúvidas, sinta-se à vontade para me contatar pelos seguintes meios:
Whatsapp: (11)97187-2108
E-mail: paranagua@acbdigital.com.br

Att.
Rafael Negrão de Souza
                """
                                    )
                            ui.campo_assunto_email.setText("")
                            ui.campo_assunto_email.setText(f"VALIDAÇÃO PEDIDO {ui.campo_pedido.text()}")
                            ui.campo_msg_agendamento.setText("")
                            ui.campo_msg_agendamento.setText(f"pedido_{ui.campo_pedido.text()}-CLIENTE_{ui.campo_nome.text().capitalize()}")
                            ui.campo_msg3.setPlainText("")
                            ui.campo_msg3.setPlainText(texto_formatado)
                            QApplication.clipboard().setText(ui.campo_msg3.toPlainText())

            elif versao == "e-CPF":
                texto_formatado = (
f"""Olá {nome.capitalize()}, tudo bem?
 
Sou o Rafael, agente de registro da AR ACB SERVICOS E NEGOCIOS e estou entrando em contato pois temos uma validação para
seu certificado digital às {hora} do dia {data}, pedido {pedido}.

Para agilizar o processo, peço que o senhor encaminhe para um dos contatos abaixo, os seguintes documentos:
1 - uma foto completa do seu documento de identificação, FRENTE E VERSO, podendo ser CNH, RG, OAB
Observações: Retire o documento do plástico e abra-o.

Para acessar a reunião, clique no link da vídeo-conferência abaixo:
{link}

Em caso de dúvidas, sinta-se à vontade para me contatar pelos seguintes meios:
Whatsapp: (11)97187-2108
E-mail: paranagua@acbdigital.com.br

Att.
Rafael Negrão de Souza
                """)
                
                ui.campo_assunto_email.setText("")
                ui.campo_assunto_email.setText(f"VALIDAÇÃO PEDIDO {ui.campo_pedido.text()}")
                ui.campo_msg_agendamento.setText("")
                ui.campo_msg_agendamento.setText(f"pedido_{ui.campo_pedido.text()}-CLIENTE_{ui.campo_nome.text().capitalize()}")
                ui.campo_msg3.setPlainText("")
                ui.campo_msg3.setPlainText(texto_formatado)
                QApplication.clipboard().setText(ui.campo_msg3.toPlainText())
        except:
            pass

    def atualizar_aba(self):
        if ui.tabWidget.currentIndex() == 3:
            self.email_padrao_webex()
        elif ui.tabWidget.currentIndex() == 4:
            self.atualizar_meta_clientes()    
        else:
            pass

    def envio_de_email(self):
        # Obtenção dos campos do formulário
        nome = ui.campo_nome.text()
        pedido = ui.campo_pedido.text()
        link = ui.campo_link_webex.text()
        mensagem = ui.campo_msg3.toPlainText()
        email = ui.campo_email_empresa.text()
        senha = ui.campo_senha_email_empresa.text()
        hora = ui.campo_hora_agendamento.time().toString("HH:mm")
        data = ui.campo_data_agendamento.date().toString("dd/MM/yyyy")
        email_cliente = ui.campo_email.text()

        # Lista de variáveis
        variaveis = [nome, pedido, link, hora, data, email_cliente, senha]

        # Mapeia os nomes das variáveis para mensagens correspondentes
        nomes_mensagens = {
            "nome": "Nome",
            "pedido": "Pedido",
            "link": "Link Webex",
            "hora": "Hora",
            "data": "Data",
            "email_cliente": "E-mail",
            "senha": "Senha"
        }

        # Verifica se há alguma variável vazia, exceto para data e hora
        campos_vazios = [nomes_mensagens[nome_variavel] for nome_variavel, valor in zip(["nome", "pedido", "link", "hora", "data", "email_cliente", "senha"], variaveis) if (isinstance(valor, str) and valor == "") or (nome_variavel == "hora" and valor == "00:00") or (nome_variavel == "data" and valor == "01/01/2000")]

        # Verifica se há campos vazios e exibe a mensagem de alerta
        if campos_vazios:
            campos_faltando = "\n• ".join(campos_vazios)
            mensagem_alerta = f"Preencha os seguintes campos para enviar o e-mail!\n• {campos_faltando}"
            self.mensagem_alerta("Erro no envio", mensagem_alerta)
            return

        try:
            # Configurar o objeto MIMEText
            if not ui.checkBox_documentos_webex.isChecked():
                certificado = ui.campo_lista_versao_certificado.currentText()

                if "e-CNPJ" in certificado:
                    versao = "e-CNPJ"
                elif "e-CPF" in certificado:
                    versao = "e-CPF"

                print(versao)
                if versao == "e-CNPJ":
                
                        mensagem_final = f"""
                    Olá <b>{nome.capitalize()}</b>, tudo bem?<br>

                    Sou o Rafael, agente de registro da AR ACB SERVICOS E NEGOCIOS e estou entrando em contato pois temos uma validação para<br>
                    seu certificado digital às <b>{hora}</b> do dia <b>{data}</b>, pedido <b>{pedido}</b>.<br>
    <br>
                    Para agilizar o processo, peço que encaminhe para um dos contatos abaixo, os seguintes documentos:<br>
    <br>
                    <b>1</b> - uma foto completa do seu documento de identificação, <b>FRENTE E VERSO</b>, podendo ser<b> CNH, RG, OAB</b><br>
                    Observações: Retire o documento do plástico e abra-o.<br>
    <br>
                    <b> 2</b> - O documento de constituição da empresa, podendo ser <b>Contrato Social, Certidão de inteiro teor, Estatuto social, Requerimento de empresário.</b><br>
    <br>
                    Para acessar a reunião, clique no link da vídeo-conferência abaixo:<br>
                    <b>{link}</b><br>
    <br>
                    Para o envio de documentos ou esclarecimento de dúvidas, utilize os contatos abaixo:<br>
                    <b>Whatsapp: (11)97187-2108</b><br>
                    <b>E-mail: paranagua@acbdigital.com.br</b><br>
    <br>
                    Att.<br>
                    Rafael Negrão de Souza<br>
                """

                elif versao == "e-CPF ":
                        mensagem_final = f"""
                        Olá <b>{nome.capitalize()}</b>, tudo bem?<br>
    <br>
                        Sou o Rafael, agente de registro da AR ACB SERVICOS E NEGOCIOS e estou entrando em contato pois temos uma validação para<br>
                        seu certificado digital às <b>{hora}</b> do dia <b>{data}</b>, pedido <b>{pedido}</b>.<br>
    <br>
                        Para agilizar o processo, peço que encaminhe para um dos contatos abaixo, os seguintes documentos:<br>
    <br>                    
                        <b> 1</b> - uma foto completa do seu documento de identificação, <b>FRENTE E VERSO</b>, podendo ser <b>CNH, RG, OAB</b><br>
                        Observações: Retire o documento do plástico e abra-o.<br>
    <br>
                        Para acessar a reunião, clique no link da vídeo-conferência abaixo:<br>
                        <b>{link}</b><br>
    <br>
                        Para o envio de documentos ou esclarecimento de dúvidas, utilize os contatos abaixo:<br>
                        <b>Whatsapp: (11)97187-2108</b><br>
                        <b>E-mail: paranagua@acbdigital.com.br</b><br>
    <br>
                        Att.<br>
                        Rafael Negrão de Souza<br>
                    """
                

            else:

                mensagem_final = f"""
                    Olá <b>{nome.capitalize()}</b>, tudo bem?<br>
<br>
                    Sou o Rafael, agente de registro da AR ACB SERVICOS E NEGOCIOS e estou entrando em contato pois temos uma validação para<br>
                    seu certificado digital às <b>{hora}</b> do dia <b>{data}</b>, pedido <b>{pedido}</b>.<br>
<br>
                    Para acessar a reunião, clique no link da vídeo-conferência abaixo:<br>
                    <b>{link}</b><br>
<br>
                    Para o envio de documentos ou esclarecimento de dúvidas, utilize os contatos abaixo:<br>
                    <b>Whatsapp: (11)97187-2108</b><br>
                    <b>E-mail: paranagua@acbdigital.com.br</b><br>
<br>
                    Att.<br>
                    Rafael Negrão de Souza<br>
                """


            mensagem_mime = MIMEText(mensagem_final, "html")

            # Configurações do servidor SMTP
            smtp_server = 'smtp.acbdigital.com.br'  # Substitua pelo seu servidor SMTP
            smtp_port = 587  # Porta do servidor SMTP
            smtp_username = email  # Seu endereço de e-mail
            smtp_password = senha  # Sua senha de e-mail

            # Configurações do e-mail
            sender_email = email
            receiver_email = email_cliente
            subject = ui.campo_assunto_email.text()

            # Criação do objeto MIMEMultipart
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            message.attach(mensagem_mime)

            # Conexão com o servidor SMTP
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                text = message.as_string()
                server.sendmail(sender_email, receiver_email, text)

            self.mensagem_alerta("Pedido", "E-mail enviado com sucesso!")

        except smtplib.SMTPAuthenticationError:
            self.mensagem_alerta("Erro no envio", "Erro ao enviar e-mail\nMotivo: E-mail ou senha inválidos")

        except Exception as e:
            self.mensagem_alerta("Erro no envio", f"Erro ao enviar e-mail\nMotivo: {e}")

    def valor_alterado(self, campo_atual):
        self.atualizar_documentos_tabela()
        if campo_atual is not None:
            nome_campo_atual = campo_atual.objectName()
            novo_valor = self.obter_valor_campo(campo_atual)
            campo_anterior = getattr(self.ui, campo_atual.objectName(), None)

            if campo_anterior is not None:
                valor_anterior = self.obter_valor_campo(campo_anterior)

                if valor_anterior != novo_valor:
                    self.ui.campo_status_bd.setText("❌")
                    self.ui.campo_status_bd.setToolTip("Pedido desatualizado")
                else:
                    self.ui.campo_status_bd.setText("❌")
                    self.ui.campo_status_bd.setToolTip("Pedido desatualizado")
            
            if nome_campo_atual == "campo_lista_versao_certificado":
                self.buscar_preco_certificado()
                pass
        
    def obter_valor_campo(self, campo):
        if isinstance(campo, QtWidgets.QLineEdit) or isinstance(campo, QtWidgets.QComboBox):
            return campo.text() if isinstance(campo, QtWidgets.QLineEdit) else campo.currentText()
        elif isinstance(campo, QtWidgets.QTimeEdit):
            return campo.time().toString("HH:mm")
        elif isinstance(campo, QtWidgets.QDateEdit):
            return campo.date().toString("dd/MM/yyyy")
        else:
            return None

    def visualizar_senha(self):
        if ui.campo_senha_email_empresa.echoMode() == QLineEdit.Normal:
            ui.campo_senha_email_empresa.setEchoMode(QLineEdit.Password)
            ui.botao_ver_senha.setText("👁️")
        elif ui.campo_senha_email_empresa.echoMode() == QLineEdit.Password:
            ui.campo_senha_email_empresa.setEchoMode(QLineEdit.Normal)
            ui.botao_ver_senha.setText("❌")

    def verificar_texto_lista_status(self):
        valor_campo = ui.campo_lista_status.currentText()

        if valor_campo == "APROVADO":
        # Alterar a fonte para verde
            ui.campo_lista_status.setStyleSheet("color: green;font-weight: bold;")
        elif valor_campo == "CANCELADO":
            # Alterar a fonte para vermelha
            ui.campo_lista_status.setStyleSheet("color: red;font-weight: bold;")
        elif valor_campo == "VIDEO REALIZADA":
            # Alterar a fonte para azul
            ui.campo_lista_status.setStyleSheet("color: blue;font-weight: bold;")
        elif valor_campo == "VERIFICAÇÃO":
            # Alterar a fonte para laranja
            ui.campo_lista_status.setStyleSheet("color: orange;font-weight: bold;")
        else:
            # Caso padrão, alterar a fonte para preta
            ui.campo_lista_status.setStyleSheet("color: black;")

    def carregar_lista_certificados(self):
        ref = db.reference("/Certificados")
        certificados = ref.get()

        ui.campo_lista_versao_certificado.clear()  # Limpar qualquer item existente no combobox
        ui.campo_lista_versao_certificado.addItem("")
        ui.campo_lista_versao_certificado.addItems(certificados.keys())  # Adicionar as chaves do dicionário ao combobox
        
        ui.campo_lista_versao_certificado.removeItem(19)
        ui.campo_lista_versao_certificado.removeItem(39)

        ui.campo_lista_versao_certificado.insertItem(1,'e-CNPJ - no computador - 12 meses')
        ui.campo_lista_versao_certificado.insertItem(2,'e-CPF - no computador - 12 meses')
       
    def buscar_preco_certificado(self):
        ref = db.reference("/Certificados")
        lista_certificados = ref.get()

        certificado = ui.campo_lista_versao_certificado.currentText()
        if certificado in lista_certificados:
            # Armazenar o valor da chave correspondente em uma variável
            valor_do_certificado = float(lista_certificados[certificado].replace(',','.'))
            porcentagem_validacao = int(ui.campo_porcentagem_validacao.value())/100
            imposto_de_renda = 1-(ui.campo_imposto_validacao.value()/100)
            desconto_validacao = float(ui.campo_desconto_validacao.text().replace(',','.'))
            
            
            valor_final = ((valor_do_certificado * porcentagem_validacao) * imposto_de_renda) - desconto_validacao
            valor_final_formatado = "{:.2f}".format(valor_final)  # Formatar o valor para duas casas decimais
            ui.campo_preco_certificado.setText(valor_final_formatado)

    def duplicar_pedido(self):
        resposta = QMessageBox.question(ui.centralwidget,'Duplicar pedido', 'Duplicar pedido atual?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resposta == QMessageBox.Yes:
            ui.campo_pedido.setText('')
            ui.campo_pedido.setReadOnly(False)
            ui.campo_cnpj.setText('')
            ui.campo_cnpj_razao_social.setText('')
            ui.campo_cnpj_uf.setText('')
            ui.campo_cnpj_municipio.setText('')
            ui.checkBox_cnh.setChecked(False)
            ui.checkBox_cnpj.setChecked(False)
            ui.checkBox_cpf.setChecked(False)
            ui.checkBox_doc_empresa.setChecked(False)
            ui.checkBox_doc_identificacao.setChecked(False)
            ui.checkBox_oab.setChecked(False)
            ui.checkBox_rg.setChecked(False)
            ui.checkBox_doc_complementar.setChecked(False)
            self.acoes.limpar_labels()
            ui.campo_lista_versao_certificado.setCurrentText("")
            ui.campo_preco_certificado.setText('')
            ui.campo_status_bd.setText('❌')
            return True
        else:
            return False
        
    def atualizar_documentos_tabela(self):
        # Limpar qualquer conteúdo existente na tabela
        self.ui.tabela_documentos.clearContents()

        # Obter o caminho da pasta do cliente
        pasta_cliente = self.ui.caminho_pasta.text()

        # Verificar se o caminho da pasta existe
        if not os.path.exists(pasta_cliente):
            return

        # Obter uma lista de arquivos na pasta do cliente
        documentos = os.listdir(pasta_cliente)

        # Separar os documentos em PDFs e outros documentos
        pdfs = [doc for doc in documentos if doc.lower().endswith('.pdf')]
        outros_documentos = [doc for doc in documentos if not doc.lower().endswith('.pdf')]

        # Preencher a tabela com os PDFs
        num_documentos = len(pdfs)
        self.ui.tabela_documentos.setRowCount(num_documentos)

        for i, documento in enumerate(pdfs):
            # Criar um item de tabela para o nome do documento
            item_nome_documento = QTableWidgetItem(documento)

            # Definir a cor do texto como preta para PDFs
            item_nome_documento.setForeground(QColor(90, 54, 247))

            # Definir o item na tabela
            self.ui.tabela_documentos.setItem(i, 0, item_nome_documento)

        # Preencher a tabela com os outros documentos
        num_outros_documentos = len(outros_documentos)
        self.ui.tabela_documentos.setRowCount(num_documentos + num_outros_documentos)

        for i, documento in enumerate(outros_documentos):
            # Criar um item de tabela para o nome do documento
            item_nome_documento = QTableWidgetItem(documento)

            # Definir a cor do texto como cinza para outros documentos
            item_nome_documento.setForeground(QColor(128, 128, 128))

            # Definir o item na tabela
            self.ui.tabela_documentos.setItem(num_documentos + i, 0, item_nome_documento)

    def abrir_documento_para_edicao(self):
        # Obter o item clicado da tabela
        item = self.ui.tabela_documentos.currentItem()

        # Verificar se um item foi realmente clicado (pode ser None se o usuário clicar em uma célula vazia)
        if item is not None:
            # Obter o nome do documento clicado
            nome_documento = item.text()

            # Obter o caminho completo do documento
            caminho_documento = os.path.join(self.ui.caminho_pasta.text(), nome_documento)
            if os.name == 'nt':  # Verificar se o sistema operacional é Windows
                os.startfile(caminho_documento)  # Abrir o arquivo no Windows
            else:
                subprocess.Popen(['xdg-open', caminho_documento])
            

class Acoes_banco_de_dados:
    def __init__(self,ui):
        self.ui = ui
        self.ref = db.reference("/Pedidos")
    
    def analise_dados(self):
        # Analisa se os campos do pedido estão preenchidos
        try:
            if not self.analise_de_campos():
                return

            if not self.mensagem_confirmacao("Confirmação", f"Salvar pedido como {ui.campo_lista_status.currentText()}?"):
                return

            ref = db.reference("/Pedidos")
            self.num_pedido = ui.campo_pedido.text()

            num_pedido = ui.campo_pedido.text()
            novo_pedido_ref = ref.child(num_pedido)
            
            # Verifica se o nó já existe
            #PEDIDO EXISTE
            if novo_pedido_ref.get() is not None:
                #verificar se o pedido é DEFINITIVO ou TEMPORARIO
                condic = self.verificar_status()
                match condic:
                    #Pedido existente + gravado Definitivo
                    case 'DEFINITIVO':
                        self.forcar_fechamento_de_arquivo_e_deletar_pasta(ui.caminho_pasta.text())
                        novo_pedido_ref.update(self.dicionario_banco_de_dados())
                        self.ui.campo_status_bd.setText("")
                        self.ui.campo_status_bd.setToolTip("")
                        self.limpar_campos_pedido()
                        self.mensagem_alerta("Sucesso","Pedido salvo!") 

                    #Pedido existente + gravado temporariamente
                    case 'TEMPORARIO':
                        novo_pedido_ref.update(self.dicionario_banco_de_dados())
                        self.ui.campo_status_bd.setText("✅")
                        self.ui.campo_status_bd.setToolTip("Pedido Atualizado")
                        self.mensagem_alerta("Sucesso","Pedido salvo!")
            
            #NOVO PEDIDO
            else:
                condic = self.verificar_status()
                match condic:
                    #Pedido existente + gravado Definitivo
                    case 'DEFINITIVO':
                        self.forcar_fechamento_de_arquivo_e_deletar_pasta(ui.caminho_pasta.text())
                        novo_pedido_ref.set(self.dicionario_banco_de_dados())
                        self.ui.campo_status_bd.setText("")
                        self.ui.campo_status_bd.setToolTip("")
                        self.limpar_campos_pedido()
                        self.mensagem_alerta("Sucesso","Pedido salvo!") 

                    #Pedido existente + gravado temporariamente
                    case 'TEMPORARIO':

                        novo_pedido_ref.set(self.dicionario_banco_de_dados())
                        self.ui.campo_status_bd.setText("✅")
                        self.ui.campo_status_bd.setToolTip("Pedido Atualizado")
                        self.mensagem_alerta("Sucesso","Pedido salvo!")
        except:
            self.mensagem_alerta("Erro","Não foi possível salvar os dados. Tente novamente.")
        
    def mensagem_confirmacao(self,titulo,mensagem):
        resposta = QMessageBox.question(ui.centralwidget, titulo, mensagem, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resposta == QMessageBox.Yes:
            return True
        else:
            return False

    def mensagem_alerta(self,titulo,mensagem):
        QMessageBox.information(ui.centralwidget, titulo, mensagem, QMessageBox.Ok)

    def verificar_status(self):
        if ui.campo_lista_status.currentText() != "APROVADO" and ui.campo_lista_status.currentText() != "CANCELADO":
            return"TEMPORARIO"
        else:
            return"DEFINITIVO"
               
    def analise_de_campos(self):


        pedido = ui.campo_pedido.text()
        hora = ui.campo_hora_agendamento.time().toString("HH:mm")
        data = ui.campo_data_agendamento.date().toString("dd/MM/yyyy")    
        versao = ui.campo_lista_versao_certificado.currentText()
        modalidade = ui.campo_lista_modalidade.currentText()
     
        


        # Lista de variáveis
        variaveis = [pedido,hora,data,versao,modalidade]

        # Mapeia os nomes das variáveis para mensagens correspondentes
        nomes_mensagens = {
            "pedido": "Pedido",
            "hora": "Hora",
            "data":"Data",
            "versao":"Versao",
            "modalidade":"Atendimento"
        }

        # Verifica se há alguma variável vazia, exceto para data e hora
        campos_vazios = [nomes_mensagens[nome_variavel] for nome_variavel, valor in zip(["pedido","hora","data","versao","modalidade"], variaveis) if (isinstance(valor, str) and valor == "") or (nome_variavel == "hora" and valor == "00:00") or (nome_variavel == "data" and valor == "01/01/2000")]

        # Verifica se há campos vazios e exibe a mensagem de alerta
        if campos_vazios:
            campos_faltando = "\n⭐ ".join(campos_vazios)
            mensagem_alerta = f"Preencha os seguintes campos para salvar o pedido!\n⭐{campos_faltando}"
            self.mensagem_alerta("Erro no envio", mensagem_alerta)
            return False
        return True

    def limpar_campos_pedido(self):
        try:
            #Dados pedido   
            ui.campo_link_webex.setText("")
            ui.caminho_pasta.setText("")
            ui.campo_cnpj_municipio.setText("")
            ui.campo_cnpj_uf.setText("")
            ui.campo_comentario.setPlainText("")
            ui.campo_nome.setText("")
            ui.campo_rg.setText("")
            ui.campo_cpf.setText("")
            ui.campo_cnh.setText("")
            ui.campo_nome_mae.setText("") 
            ui.campo_cnpj.setText("")
            ui.campo_email.setText("")
            ui.campo_data_nascimento.setDate(QDate(2000, 1, 1))
            ui.campo_seguranca_cnh.setText("")
            ui.campo_msg3.setPlainText("")
            ui.campo_msg_agendamento.setText("")
            ui.campo_assunto_email.setText("")
            ui.campo_lista_junta_comercial.setCurrentText("")
            ui.label_quantidade_bd.setText("")
            ui.tableWidget.setRowCount(0)
            ui.campo_data_nascimento.setDate(QDate(2000, 1, 1))
            ui.campo_pedido.setReadOnly(False)
            ui.campo_pedido.setText("")
            ui.campo_data_agendamento.setDate(QDate(2000, 1, 1))
            ui.campo_hora_agendamento.setTime(QTime.fromString('00:00', "hh:mm"))
            ui.campo_lista_status.setCurrentText("DIGITAÇÃO")
            ui.campo_lista_venda.setCurrentText("NAO")
            ui.campo_lista_modalidade.setCurrentText("")
            ui.label_confirmacao_converter_pdf.setText("")
            ui.label_confirmacao_criar_link_video.setText("")
            ui.label_confirmacao_criar_pasta.setText("")
            ui.label_confirmacao_tirar_print.setText("")
            ui.label_confirmacao_mesclar_pdf.setText("")
            ui.checkBox_documentos_webex.setChecked(False)
            ui.campo_lista_versao_certificado.setCurrentText("")
            ui.campo_status_bd.setText("")
            ui.campo_preco_certificado.setText("")
            ui.campo_valor_estimado.setText("")
            ui.campo_valor_estimado_menor.setText("")
            ui.campo_oab.setText("")
            ui.campo_oab_seccional.setText("")
            ui.campo_cnpj_razao_social.setText("")
            ui.campo_rg_orgao.setText("")
            ui.campo_lista_junta_comercial.setCurrentText("SP")
            ui.tabela_documentos.clearContents()
            ui.tabela_documentos.setRowCount(0)
           
        except Exception as e:
            print(e)

    def apagar_campos_pedido(self):
        if not self.mensagem_confirmacao("","Apagar dados?"):
            return
        try:
            #Dados pedido   
            ui.campo_link_webex.setText(""),
            ui.caminho_pasta.setText(""),
            ui.campo_cnpj_municipio.setText(""),
            ui.campo_cnpj_uf.setText(""),
            ui.campo_comentario.setPlainText(""),
            ui.campo_nome.setText(""),
            ui.campo_rg.setText(""),
            ui.campo_cpf.setText(""),
            ui.campo_cnh.setText(""),
            ui.campo_nome_mae.setText("") ,
            ui.campo_cnpj.setText(""),
            ui.campo_email.setText(""),
            ui.campo_data_nascimento.setDate(QDate(2000, 1, 1)),
            ui.campo_seguranca_cnh.setText(""),
            ui.campo_msg3.setPlainText("")
            ui.campo_msg_agendamento.setText("")
            ui.campo_assunto_email.setText("")
            ui.campo_lista_junta_comercial.setCurrentText("")
            ui.label_quantidade_bd.setText("")
            ui.tableWidget.setRowCount(0)
            ui.campo_data_nascimento.setDate(QDate(2000, 1, 1))
            ui.campo_pedido.setReadOnly(False)
            ui.campo_pedido.setText("")
            ui.campo_data_agendamento.setDate(QDate(2000, 1, 1))
            ui.campo_hora_agendamento.setTime(QTime.fromString('00:00', "hh:mm"))
            ui.campo_lista_status.setCurrentText("DIGITAÇÃO")
            ui.campo_lista_venda.setCurrentText("NAO")
            ui.campo_lista_modalidade.setCurrentText("")
            ui.checkBox_documentos_webex.setChecked(False)
            ui.campo_lista_versao_certificado.setCurrentText("")
            ui.campo_preco_certificado.setText("")
            ui.campo_valor_estimado.setText("")
            ui.campo_valor_estimado_menor.setText("")
            ui.campo_oab.setText("")
            ui.campo_oab_seccional.setText("")
            ui.campo_cnpj_razao_social.setText("")
            ui.campo_rg_orgao.setText("")
            ui.campo_lista_junta_comercial.setCurrentText("SP")
            ui.tabela_documentos.clearContents()
            ui.tabela_documentos.setRowCount(0)
            self.limpar_labels()
        except Exception as e:
            print(e)

    def limpar_labels(self):
        ui.campo_status_bd.setText("")
        ui.label_confirmacao_converter_pdf.setText("")
        ui.label_confirmacao_criar_link_video.setText("")
        ui.label_confirmacao_criar_pasta.setText("")
        ui.label_confirmacao_mesclar_pdf.setText("")
        ui.label_confirmacao_tirar_print.setText("")
    
    def dicionario_banco_de_dados(self):
           
        novos_dados = {"WEBEX":ui.campo_link_webex.text(),
                    "PASTA":ui.caminho_pasta.text(),
                    "MUNICIPIO": ui.campo_cnpj_municipio.text(),
                    "UF":ui.campo_cnpj_uf.text(),
                    "DIRETORIO":ui.campo_comentario.toPlainText(),
                    "CODIGO DE SEG CNH":ui.campo_seguranca_cnh.text(),
                    "NOME":ui.campo_nome.text(),
                    "RG":ui.campo_rg.text(),
                    "CPF":ui.campo_cpf.text(),
                    "CNH":ui.campo_cnh.text(),
                    "MAE":ui.campo_nome_mae.text() ,
                    "CNPJ":ui.campo_cnpj.text(),
                    "EMAIL":ui.campo_email.text(),
                    "NASCIMENTO":ui.campo_data_nascimento.text(),
                    "STATUS":ui.campo_lista_status.currentText(),
                    "PEDIDO":ui.campo_pedido.text() , 
                    "DATA":ui.campo_data_agendamento.text(), 
                    "HORA":ui.campo_hora_agendamento.text(),
                    "VENDA":ui.campo_lista_venda.currentText(),
                    "MODALIDADE":ui.campo_lista_modalidade.currentText(),
                    "VERSAO":ui.campo_lista_versao_certificado.currentText(),
                    "PRECO":ui.campo_preco_certificado.text(),
                    "OAB":ui.campo_oab.text(),
                    "OAB SECCIONAL":ui.campo_oab_seccional.text(),
                    "RAZAO SOCIAL":ui.campo_cnpj_razao_social.text(),
                    "ORGAO RG":ui.campo_rg_orgao.text()
                    }
        if self.verificar_status() == "DEFINITIVO":
            novos_dados.update({
                    "NOME":"",
                    "WEBEX": "",
                    "PASTA": "",
                    "MUNICIPIO": "",
                    "UF": "",
                    "CODIGO DE SEG CNH": "",
                    "RG": "",
                    "CPF": "",
                    "CNH": "",
                    "MAE": "",
                    "CNPJ": "",
                    "EMAIL": "",
                    "NASCIMENTO": "",
                    "OAB":"",
                    "OAB SECCIONAL":"",
                    "RAZAO SOCIAL":"",
                    "ORGAO RG":""
                    })

        return novos_dados

    def forcar_fechamento_de_arquivo_e_deletar_pasta(self,folder_path):
        for _ in range(3):  # Tentar até três vezes
            try:
                shutil.rmtree(folder_path)
                self.mensagem_alerta(" ","Pasta excluída com sucesso")
                break
            except PermissionError as e:
                # Se a exclusão falhar devido a permissões, tenta fechar os arquivos em uso antes da próxima tentativa
                self.fechar_arquivo_em_uso(folder_path)
            except Exception as e:
                if not os.path.exists(folder_path):  # Verifica se a pasta não existe
                    break
                self.mensagem_alerta(" ","Erro ao excluir pasta do cliente")
                break
   
    def fechar_arquivo_em_uso(self,folder_path):
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

    def carregar_dados(self):
        #CORRIGIDO ------------------------------------------------
        try:
            num_pedido = ui.campo_pedido.text()

            if num_pedido == "":
                return

            #Referência para o nó /Pedidos
            self.ref = db.reference("/Pedidos")

            # Verifica se o nó com o número do pedido existe
            pedido_ref = self.ref.child(num_pedido)
            pedido_data = pedido_ref.get()

            if pedido_data:
                # Se existir, o pedido foi encontrado
                self.preencher_dados(pedido_data)
                # Realize as ações necessárias com os detalhes do pedido encontrado
            else:  
               return 'Pedido nao existe'

        except Exception as e:
            pass

    def pegar_valor_tabela(self):
   #evento disparado ao dar double click na tabela
        #Pega o item selecionado
        item = ui.tableWidget.currentItem() 
        pedido = item.text()
        try:
            pedido_ref = self.ref.child(pedido)
            pedido_data = pedido_ref.get()
            if item is not None:
                coluna = item.column()
                if coluna == 1 :            
                    ui.tabWidget.setCurrentIndex(0)  
                    self.limpar_labels()
                    self.preencher_dados(pedido_data)
                    ui.campo_status_bd.setText("✅")
                    return             
        except :
            pass

    def preencher_dados(self,pedido_data):
        #CORRIGIDO------------------------------------------------------------

        self.limpar_campos_pedido()
        try:
            status = pedido_data.get("STATUS")
            ui.campo_lista_status.setCurrentText(status)
            data_nula = QDate(2000, 1, 1)  
            ui.campo_data_nascimento.setDate(data_nula)
            ui.campo_nome.setText(pedido_data.get("NOME")) 
            ui.campo_rg.setText(pedido_data.get("RG"))   
            ui.campo_cpf.setText(pedido_data.get("CPF"))   
            ui.campo_cnh.setText(pedido_data.get("CNH"))  
            ui.campo_cnpj.setText(pedido_data.get("CNPJ"))  
            ui.campo_email.setText(pedido_data.get("EMAIL"))  
            ui.campo_data_nascimento.setDate(QDate.fromString(pedido_data.get("NASCIMENTO"), "dd/MM/yyyy"))  
            ui.campo_pedido.setText(pedido_data.get("PEDIDO")) 
            ui.campo_data_agendamento.setDate(QDate.fromString(pedido_data.get("DATA"), "dd/MM/yyyy"))
            ui.campo_hora_agendamento.setTime(QTime.fromString(pedido_data.get("HORA"), "hh:mm"))
            ui.campo_lista_venda.setCurrentText("NAO")
            ui.campo_lista_venda.setCurrentText(pedido_data.get("VENDA"))
            ui.campo_lista_modalidade.setCurrentText(pedido_data.get("MODALIDADE"))
            ui.campo_pedido.setReadOnly(True)
            ui.campo_seguranca_cnh.setText(pedido_data.get("CODIGO DE SEG CNH"))
            ui.campo_nome_mae.setText(pedido_data.get("MAE"))
            ui.campo_comentario.setText(pedido_data.get("DIRETORIO"))
            ui.campo_cnpj_municipio.setText(pedido_data.get("MUNICIPIO"))
            ui.campo_cnpj_uf.setText(pedido_data.get("UF"))
            ui.caminho_pasta.setText(pedido_data.get("PASTA"))
            ui.campo_link_webex.setText(pedido_data.get("WEBEX"))
            try:
                ui.campo_lista_versao_certificado.setCurrentText(pedido_data.get("VERSAO"))
            except:
                pass
            try:
                ui.campo_rg_orgao.setText(pedido_data.get("ORGAO RG"))
            except:
                pass
            try:
                ui.campo_oab.setText(pedido_data.get("OAB"))
            except:
                pass
            try:
                ui.campo_oab_seccional.setText(pedido_data.get("OAB SECCIONAL"))
            except:
                pass
            try:
                ui.campo_cnpj_razao_social.setText(pedido_data.get("RAZAO SOCIAL"))
            except:
                pass
            

            ui.campo_status_bd.setText("✅")
            ui.campo_status_bd.setToolTip("Pedido Atualizado")
            pasta = ui.caminho_pasta.text()
            if pasta != "": 
                ui.label_confirmacao_criar_pasta.setText("✅")
        except:
            pass
            
    def preencher_tabela(self):
    #CORRIGIDO ---------------------------------------------------------
    #USO DE BANCO DE DADOS
        ui.tableWidget.setRowCount(0)
        valor_estimado = 0
        try:
            ui.tableWidget.clear()
            
            pedidos = self.ref.get()
            # Ordene a lista de acordo com a data em ordem decrescente
            pedidos = sorted(pedidos.values(), key=lambda x: (datetime.datetime.strptime(x['DATA'], "%d/%m/%Y"), datetime.datetime.strptime(x['HORA'], "%H:%M")))

            data_inicial = datetime.datetime.strptime(ui.campo_data_de.text(), "%d/%m/%Y")
            numero_inteiro_inicial = data_inicial.toordinal()
            data_final = datetime.datetime.strptime(ui.campo_data_ate.text(), "%d/%m/%Y")
            numero_inteiro_final = data_final.toordinal()
            status_filtro = ui.campo_lista_status_2.currentText()

            x = 0
            ui.barra_progresso_consulta.setVisible(True)
            ui.barra_progresso_consulta.setValue(0)
            total_pedidos = len(pedidos)
            y = 0
            for pedido_info in pedidos:
                
                data_bd = datetime.datetime.strptime(pedido_info['DATA'], "%d/%m/%Y")
                numero_inteiro_bd = data_bd.toordinal()
                status_servidor = pedido_info['STATUS']
               
                if (numero_inteiro_inicial <= numero_inteiro_bd <= numero_inteiro_final) :

                    if status_filtro == status_servidor or status_filtro == "TODAS":
                    
                        x += 1
                    
                        row_position = ui.tableWidget.rowCount()
                        ui.tableWidget.insertRow(row_position)
                        
                        ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(pedido_info['STATUS']))
                        ui.tableWidget.setItem(row_position, 1, QTableWidgetItem(pedido_info['PEDIDO']))
                        ui.tableWidget.setItem(row_position, 2, QTableWidgetItem(pedido_info['NOME']))
                        ui.tableWidget.setItem(row_position, 3, QTableWidgetItem(pedido_info['DATA']))
                        ui.tableWidget.setItem(row_position, 4, QTableWidgetItem(pedido_info['HORA']))
                        ui.tableWidget.setItem(row_position, 5, QTableWidgetItem(pedido_info['MODALIDADE']))
                        ui.tableWidget.setItem(row_position, 6, QTableWidgetItem(pedido_info['VENDA']))
                        try:
                            ui.tableWidget.setItem(row_position, 7, QTableWidgetItem(pedido_info['VERSAO']))
                        except:
                            pass
                        try:
                            ui.tableWidget.setItem(row_position, 8, QTableWidgetItem(pedido_info['DIRETORIO']))
                        except:
                            pass

                        # Verifica se a chave 'PREÇO' existe no dicionário e se o valor associado a ela pode ser convertido para float
                        
                        try:
                            # Verifica se a chave 'PREÇO' existe no dicionário e se o valor associado a ela pode ser convertido para float
                            if 'PRECO' in pedido_info:
                                # Substitui a vírgula por um ponto no valor do preço
                                preco = float(pedido_info['PRECO'])
                                # Converte o valor para float e soma ao valor estimado
                                valor_estimado += float(preco)
                                valor_formatado = "{:.2f}".format(valor_estimado).replace('.', ',')
                                valor_formatado_menor = "{:.2f}".format(valor_estimado*0.90).replace('.', ',')
                                ui.campo_valor_estimado.setText(f'R$ {valor_formatado}')
                                ui.campo_valor_estimado_menor.setText(f'R$ {valor_formatado_menor}')
                                
                                QApplication.processEvents()
                        except ValueError:
                            pass

                        

                        for col in range(ui.tableWidget.columnCount()):
                            item = ui.tableWidget.item(row_position, col)

                            status = ui.tableWidget.item(row_position,0).text()

                            if item is not None:
                                match status:
                                    case 'DIGITAÇÃO':
                                        item.setBackground(QColor(204, 204, 204))  # Cinza
                                    case 'VIDEO REALIZADA':
                                        item.setBackground(QColor(25, 200, 255))  # Amarelo
                                    case 'VERIFICAÇÃO':
                                        item.setBackground(QColor(255, 167, 91))  # Laranja claro
                                    case 'APROVADO':
                                        item.setBackground(QColor(173, 255, 47))  # Verde limão
                                    case 'CANCELADO':
                                        item.setBackground(QColor(255, 30, 30))  # Vermelho claro   

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
            valor_formatado = "{:.2f}".format(valor_estimado).replace('.', ',')
            valor_formatado_menor = "{:.2f}".format(valor_estimado*0.90).replace('.', ',')


            ui.campo_valor_estimado.setText(f'R$ {valor_formatado}')
            ui.campo_valor_estimado_menor.setText(f'R$ {valor_formatado_menor}')

            ui.label_quantidade_bd.setText(f"{x} registro(s)")
            ui.tableWidget.setHorizontalHeaderLabels(["STATUS","PEDIDO","NOME", "DATA", "HORA", "MODALIDADE", "VENDA","VERSAO","OBSERVAÇÕES"])
            ui.barra_progresso_consulta.setVisible(False)
        except Exception as e:
                print(e)
                ui.tableWidget.setHorizontalHeaderLabels(["STATUS","PEDIDO","NOME", "DATA", "HORA", "MODALIDADE", "VENDA","VERSAO","OBSERVAÇÕES"])
                ui.label_quantidade_bd.setText(f"{x} registro(s)")
                ui.barra_progresso_consulta.setVisible(False)
                pass

    def atualizar_documentos_tabela(self):
        # Limpar qualquer conteúdo existente na tabela
        self.ui.tabela_documentos.clearContents()

        # Obter o caminho da pasta do cliente
        pasta_cliente = self.ui.caminho_pasta.text()

        # Verificar se o caminho da pasta existe
        if not os.path.exists(pasta_cliente):
            return

        # Obter uma lista de arquivos na pasta do cliente
        documentos = os.listdir(pasta_cliente)

        # Separar os documentos em PDFs e outros documentos
        pdfs = [doc for doc in documentos if doc.lower().endswith('.pdf')]
        outros_documentos = [doc for doc in documentos if not doc.lower().endswith('.pdf')]

        # Preencher a tabela com os PDFs
        num_documentos = len(pdfs)
        self.ui.tabela_documentos.setRowCount(num_documentos)

        for i, documento in enumerate(pdfs):
            # Criar um item de tabela para o nome do documento
            item_nome_documento = QTableWidgetItem(documento)

            # Definir a cor do texto como preta para PDFs
            item_nome_documento.setForeground(QColor(90, 54, 247))

            # Definir o item na tabela
            self.ui.tabela_documentos.setItem(i, 0, item_nome_documento)

        # Preencher a tabela com os outros documentos
        num_outros_documentos = len(outros_documentos)
        self.ui.tabela_documentos.setRowCount(num_documentos + num_outros_documentos)

        for i, documento in enumerate(outros_documentos):
            # Criar um item de tabela para o nome do documento
            item_nome_documento = QTableWidgetItem(documento)

            # Definir a cor do texto como cinza para outros documentos
            item_nome_documento.setForeground(QColor(128, 128, 128))

            # Definir o item na tabela
            self.ui.tabela_documentos.setItem(num_documentos + i, 0, item_nome_documento)
            
    


class JanelaOculta:
    def __init__(self, parent):
        self.parent = parent
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_window_size)
        self.animation_step = 5  # Ajuste conforme necessário
        self.animation_duration = 2  # Duração da animação em milissegundos
        self.animation_target_width = 0
        self.animation_target_height = 0
        self.janela = Funcoes_padrao(ui)

    def enterEvent(self, event):
        self.animate_window_resize(469, 668)
        self.janela.atualizar_documentos_tabela()

    def leaveEvent(self, event):
        self.janela.atualizar_documentos_tabela()
        if not ui.campo_verifica_tela_cheia.text()=="SIM":
            cursor_pos = QtGui.QCursor.pos()
            window_pos = self.parent.mapToGlobal(QtCore.QPoint(0, 0))
            window_rect = QRect(window_pos, self.parent.size())

            mouse_dentro_da_janela = window_rect.contains(cursor_pos)

            if not mouse_dentro_da_janela:
                self.animate_window_resize(128, 45)
        
        

    def mousePressEvent(self, event):
        self.animate_window_resize(469, 668)#469

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


app = QtWidgets.QApplication(sys.argv)
janela = QtWidgets.QMainWindow()
desktop = QDesktopWidget()
ui = Ui_janela()
ui.setupUi(janela)

helper = JanelaOculta(janela)
banco_dados = Acoes_banco_de_dados(ui)
funcoes_app = Funcoes_padrao(ui)

#Manipulações
janela.enterEvent = helper.enterEvent
janela.leaveEvent = helper.leaveEvent
janela.mousePressEvent = helper.mousePressEvent
janela.closeEvent = funcoes_app.evento_ao_fechar
janela.showEvent = funcoes_app.evento_ao_abrir

#Alterações nos campos
ui.campo_rg_orgao.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_rg_orgao))
ui.campo_oab_seccional.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_oab_seccional))
ui.campo_oab.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_oab))
ui.campo_nome.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_nome))
ui.campo_cnpj_municipio.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_cnpj_municipio))
ui.caminho_pasta_principal.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.caminho_pasta_principal))
ui.caminho_pasta.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.caminho_pasta))
ui.campo_cnpj.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_cnpj))
ui.campo_cnpj_uf.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_cnpj_uf))
ui.campo_senha_email_empresa.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_senha_email_empresa))
ui.campo_cpf.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_cpf))
ui.campo_cnpj.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_cnpj))
ui.campo_nome_mae.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_nome_mae))
ui.campo_link_webex.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_link_webex))
ui.campo_cnh.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_cnh))
ui.campo_lista_modalidade.currentIndexChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_lista_modalidade))
ui.campo_lista_status.currentIndexChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_lista_status))
ui.campo_lista_venda.currentIndexChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_lista_venda))
ui.campo_hora_agendamento.timeChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_hora_agendamento))
ui.campo_data_agendamento.dateChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_data_agendamento))
ui.campo_email.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_email))
ui.campo_rg.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_rg))
ui.campo_seguranca_cnh.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_seguranca_cnh))
ui.campo_comentario.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_comentario))
ui.campo_data_nascimento.dateChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_data_nascimento))
ui.campo_lista_versao_certificado.currentIndexChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_lista_versao_certificado))


#Campos botões
ui.botao_consulta_oab.clicked.connect(lambda:funcoes_app.procurar_oab())
ui.botao_duplicar_pedido.clicked.connect(lambda:funcoes_app.duplicar_pedido())
ui.botao_ver_senha.clicked.connect(lambda:funcoes_app.visualizar_senha())
ui.botao_atualizar_meta.clicked.connect(lambda:funcoes_app.Atualizar_meta())
ui.botao_atualizar_configuracoes.clicked.connect(lambda:funcoes_app.atualizar_configuracoes())
ui.botao_consultar.clicked.connect(lambda:banco_dados.preencher_tabela())
ui.botao_excluir_dados.clicked.connect(lambda:banco_dados.apagar_campos_pedido())
ui.botao_procurar.clicked.connect(lambda:funcoes_app.exportar_excel())
ui.botao_consulta_cnpj.clicked.connect(lambda:funcoes_app.procurar_cnpj())
ui.botao_consulta_cpf.clicked.connect(lambda:funcoes_app.procurar_cpf())
ui.botao_consulta_cnh.clicked.connect(lambda:funcoes_app.procurar_cnh())
ui.botao_consulta_rg.clicked.connect(lambda:funcoes_app.procurar_rg())
ui.botao_salvar.clicked.connect(lambda:banco_dados.analise_dados())
ui.botao_junta.clicked.connect(lambda:funcoes_app.procurar_junta())
ui.botao_print_direto_na_pasta.clicked.connect(lambda:funcoes_app.print_tela())
ui.botao_print_direto_na_pasta.setToolTip("Tira um print da tela")
ui.botao_print_direto_na_pasta.setFlat(True)
ui.botao_pasta_cliente.clicked.connect(lambda:funcoes_app.criar_pasta_cliente())
ui.botao_tela_cheia.clicked.connect(lambda: funcoes_app.manter_tela_aberta())
ui.botao_tela_cheia.setToolTip("Liga/Desliga a tela cheia")
ui.botao_tela_cheia.setFlat(True)
ui.botao_gerar_link.clicked.connect(lambda:funcoes_app.gerar_link_video_conferencia())
ui.botao_gerar_link.setToolTip("Gera a link da vídeo-conferência")
ui.botao_gerar_link.setFlat(True)
ui.botao_converter_todas_imagens_em_pdf.clicked.connect(lambda:funcoes_app.converter_todas_imagens_para_pdf())
ui.botao_converter_todas_imagens_em_pdf.setToolTip("Conversor de JPG/PDF")
ui.botao_converter_todas_imagens_em_pdf.setFlat(True)
ui.botao_enviar_email.clicked.connect(lambda:funcoes_app.envio_de_email())
ui.botao_agrupar_PDF.setToolTip("Mesclar PDF")
ui.botao_agrupar_PDF.setFlat(True)
ui.botao_agrupar_PDF.clicked.connect(lambda:funcoes_app.mesclar_pdf())
ui.botao_dados_cnpj.clicked.connect(lambda:funcoes_app.dados_cnpj())
ui.botao_altera_pasta_principal.clicked.connect(lambda: funcoes_app.atualizar_diretorio_raiz())
ui.botao_definir_cor.clicked.connect(lambda:funcoes_app.definir_cor())
ui.campo_lista_status.currentIndexChanged.connect(lambda : funcoes_app.verificar_texto_lista_status()) 

#Campos de formatação
ui.campo_cnpj_municipio.setReadOnly(True)
ui.caminho_pasta_principal.setReadOnly(True)
ui.caminho_pasta.setReadOnly(True)
ui.campo_verifica_tela_cheia.setReadOnly(True)
ui.campo_cnpj_uf.setReadOnly(True)
ui.campo_cnpj_uf.setToolTip("⚠ - NECESSÁRIO PEDIR DOCUMENTO DE CONSTITUIÇÃO DA EMPRESA\n✅ - DOC PODE SER OBTIDO NA JUCESP")
ui.campo_status_bd_2.setToolTip("Status dos dados no servidor\n✅ - Pedido atualizado no servidor\n❌ - Pedido desatualizado no servidor")
ui.campo_senha_email_empresa.setEchoMode(QLineEdit.Password)
ui.campo_cpf.editingFinished.connect(lambda:funcoes_app.formatar_cpf())
ui.campo_rg_orgao.editingFinished.connect(lambda:funcoes_app.formatar_orgao_rg())
ui.campo_pedido.editingFinished.connect(lambda:banco_dados.carregar_dados())
ui.campo_cnpj.editingFinished.connect (lambda:funcoes_app.formatar_cnpj())
ui.campo_meta_semanal.valueChanged.connect(lambda:funcoes_app.atualizar_meta_clientes())
ui.campo_meta_mes.valueChanged.connect(lambda:funcoes_app.atualizar_meta_clientes())
ui.campo_data_meta.dateChanged.connect(lambda:funcoes_app.atualizar_meta_clientes())
ui.campo_nome.editingFinished.connect(lambda:funcoes_app.formatar_nome())
ui.campo_nome.setContextMenuPolicy(Qt.NoContextMenu)
ui.campo_nome_mae.editingFinished.connect(lambda:funcoes_app.formatar_nome_mae())
ui.campo_link_webex.editingFinished.connect(lambda:funcoes_app.atualizar_aba())
ui.campo_data_de.setDate(QDate.currentDate())
ui.campo_data_ate.setDate(QDate.currentDate())

#Eventos
ui.campo_msg_agendamento.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_msg_agendamento")
ui.campo_assunto_email.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_assunto_email")
ui.campo_cnh.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_cnh")
ui.campo_cnpj.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_cnpj")
ui.campo_pedido.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_pedido")
ui.campo_cpf.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_cpf")
ui.campo_seguranca_cnh.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_seguranca_cnh")
ui.campo_rg.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_rg")
ui.campo_nome_mae.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_nome_mae")
ui.campo_nome.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_nome")
ui.campo_msg_doc_idf.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_msg_doc_idf")
ui.campo_msg_doc_idf.setReadOnly(True)
ui.campo_msg_doc_empresa.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_msg_doc_empresa")
ui.campo_msg_doc_empresa.setReadOnly(True)
ui.campo_msg3.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_msg3")
ui.campo_msg3.setReadOnly(True)
ui.campo_msg5.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_msg5")
ui.campo_msg5.setReadOnly(True)
ui.campo_msg6.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_msg6")
ui.campo_msg6.setReadOnly(True)
ui.campo_msg7.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_msg7")
ui.campo_msg7.setReadOnly(True)
ui.campo_msg_reembolso.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_msg_reembolso")
ui.campo_msg_reembolso.setReadOnly(True)
ui.campo_msg_venda.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_msg_venda")
ui.campo_msg_venda.setReadOnly(True)
ui.campo_valor_estimado.setReadOnly(True)
ui.campo_preco_certificado.setReadOnly(True)
ui.campo_cnpj_razao_social.setReadOnly(True)
ui.campo_valor_estimado.setToolTip("Valor estimado em emissão dos certificados")
ui.botao_duplicar_pedido.setToolTip('Duplicar pedido')
ui.tabela_documentos.setEditTriggers(QTableWidget.NoEditTriggers)



regex = QRegExp("[0-9]*")
validator = QRegExpValidator(regex)
ui.campo_pedido.setValidator(validator)

#Eventos tabela
ui.tabWidget.currentChanged.connect(lambda: funcoes_app.atualizar_aba())
ui.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
ui.tableWidget.itemDoubleClicked.connect(lambda:banco_dados.pegar_valor_tabela())
ui.tableWidget.itemClicked.connect(lambda:funcoes_app.copiar_pedido_tabela(None))
ui.tabela_documentos.itemDoubleClicked.connect(lambda: funcoes_app.abrir_documento_para_edicao())


ui.barra_progresso_consulta.setVisible(False)

screen_rect = desktop.screenGeometry(desktop.primaryScreen())

x = screen_rect.width() - janela.width() - 20
y = (screen_rect.height() - janela.height()) // 6

janela.move(x, y)
janela.setWindowTitle("Auxiliar")
janela.setFixedSize(128, 45)           
janela.show()
#ui.label_5.setStyleSheet("background-color:rgb(90,54,247);")

sys.exit(app.exec_())