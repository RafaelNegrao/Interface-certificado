import datetime
import pandas as pd
import tkinter as tk
import os
import time
import psutil
import requests
import PyPDF2
import fitz
import pyautogui
import sys
import subprocess
import math
import pyperclip
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
from PyQt5 import QtGui, QtWidgets,QtCore,Qt
from PyQt5.QtWidgets import QTableWidgetItem,QTableWidget,QApplication,QMessageBox,QDesktopWidget,QInputDialog,QMainWindow,QFileDialog,QRadioButton,QVBoxLayout,QPushButton,QDialog, QLineEdit,QScrollArea,QWidget,QGridLayout
from PyQt5.QtCore import QDate, QTime,QUrl, Qt,QTimer,QRect,QRegExp,QMimeData, QDateTime
from PyQt5.QtGui import QDesktopServices,QColor,QRegExpValidator,QGuiApplication
from Interface import Ui_janela
from firebase_admin import db
from requests.exceptions import RequestException
from credenciaisBd import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import send2trash



#Referência raiz do banco de dados
ref = db.reference("/")

class Funcoes_padrao:
    def __init__(self,ui,parent=None):
        self.ui = ui
        self.acoes = Acoes_banco_de_dados(ui)
        self.parent = parent

    def atualizar_barras_metas(self):
        try:
            # Calcula a soma dos valores das semanas
            soma = math.floor(float(ui.campo_certificados_semana_1.text().replace(',', '.'))) + \
                math.floor(float(ui.campo_certificados_semana_2.text().replace(',', '.'))) + \
                math.floor(float(ui.campo_certificados_semana_3.text().replace(',', '.'))) + \
                math.floor(float(ui.campo_certificados_semana_4.text().replace(',', '.'))) + \
                math.floor(float(ui.campo_certificados_semana_5.text().replace(',', '.')))

            # Recupera as metas mensal e semanal, convertendo os valores para inteiro
            meta_mensal = int(float(ui.campo_meta_mes.text().replace(',', '.')))  # Convertido para inteiro
            meta_semanal = int(float(ui.campo_meta_semanal.text().replace(',', '.')))  # Convertido para inteiro

            # Atualiza a barra de progresso e o label para a semana 1
            certificados_semana_1 = math.floor(float(ui.campo_certificados_semana_1.text().replace(',', '.')))
            ui.barra_meta_semana_1.setMaximum(meta_semanal)
            ui.barra_meta_semana_1.setValue(certificados_semana_1)  # Atualiza o valor da barra de progresso
            
            if certificados_semana_1 >= meta_semanal:
                # Se a meta foi atingida
                ui.label_meta1.setStyleSheet('background-color: rgb(0, 173, 247);color:rgb(113,66,230);')
                ui.label_meta1.setText(f"Meta atingida! - R${certificados_semana_1} / R${meta_semanal}")
            else:
                # Se não foi...
                ui.label_meta1.setStyleSheet('background-color: rgba(255, 0, 0, 0);color:rgb(113,66,230)')
                ui.label_meta1.setText(f"R${certificados_semana_1} / R${meta_semanal}")

            certificados_semana_2 = math.floor(float(ui.campo_certificados_semana_2.text().replace(',', '.')))
            # Repete o processo para as semanas 2 a 5# ...# Código para atualizar as outras semanas (igual ao trecho anterior)# ...# Atualiza a barra de progresso e o label para a meta mensal
            ui.barra_meta_semana_2.setMaximum(meta_semanal)
            ui.barra_meta_semana_2.setValue(certificados_semana_2)  # Atualiza o valor da barra de progresso
            
            if certificados_semana_2 >= meta_semanal:
                #Meta atingida
                ui.label_meta2.setStyleSheet('background-color: rgb(0, 173, 247);color:rgb(113,66,230)')
                ui.label_meta2.setText(f"Meta atingida! - R${certificados_semana_2} / R${meta_semanal}")
            else:
                #Meta não atingida
                ui.label_meta2.setStyleSheet('background-color: rgba(255, 0, 0, 0);color:rgb(113,66,230)')
                ui.label_meta2.setText(f"R${certificados_semana_2} / R${meta_semanal}")

            certificados_semana_3 = math.floor(float(ui.campo_certificados_semana_3.text().replace(',', '.')))
            ui.barra_meta_semana_3.setMaximum(meta_semanal)
            ui.barra_meta_semana_3.setValue(certificados_semana_3)  # Atualiza o valor da barra de progresso
            if certificados_semana_3 >= meta_semanal:
                #Meta atingida
                ui.label_meta3.setStyleSheet('background-color: rgb(0, 173, 247);color:rgb(113,66,230)')
                ui.label_meta3.setText(f"Meta atingida! - R${certificados_semana_3} / R${meta_semanal}")
            else:
                #Meta não atingida
                ui.label_meta3.setStyleSheet('background-color: rgba(255, 0, 0, 0);color:rgb(113,66,230)')
                ui.label_meta3.setText(f"R${certificados_semana_3} / R${meta_semanal}")

            certificados_semana_4 = math.floor(float(ui.campo_certificados_semana_4.text().replace(',', '.')))
            ui.barra_meta_semana_4.setMaximum(meta_semanal)
            ui.barra_meta_semana_4.setValue(certificados_semana_4)  # Atualiza o valor da barra de progresso
            if certificados_semana_4 >= meta_semanal:
                #Meta atingida
                ui.label_meta4.setStyleSheet('background-color: rgb(0, 173, 247);color:rgb(113,66,230)')
                ui.label_meta4.setText(f"Meta atingida! - R${certificados_semana_4} / R${meta_semanal}")
            else:
                #Meta não atingida
                ui.label_meta4.setStyleSheet('background-color: rgba(255, 0, 0, 0);color:rgb(113,66,230)')
                ui.label_meta4.setText(f"R${certificados_semana_4} / R${meta_semanal}")

            certificados_semana_5 = math.floor(float(ui.campo_certificados_semana_5.text().replace(',', '.')))
            ui.barra_meta_semana_5.setMaximum(meta_semanal)
            ui.barra_meta_semana_5.setValue(certificados_semana_5)  # Atualiza o valor da barra de progresso
            if certificados_semana_5 >= meta_semanal:
                #Meta atingida
                ui.label_meta5.setStyleSheet('background-color: rgb(0, 173, 247);color:rgb(113,66,230)')
                ui.label_meta5.setText(f"Meta atingida! - R${certificados_semana_5} / R${meta_semanal}")
            else:
                #Meta não atingida
                ui.label_meta5.setStyleSheet('background-color: rgba(255, 0, 0, 0);color:rgb(113,66,230)')
                ui.label_meta5.setText(f"R${certificados_semana_5} / R${meta_semanal}")

            ui.barra_meta_mensal.setMaximum(meta_mensal)
            ui.barra_meta_mensal.setValue(soma)  # Atualiza o valor da barra de progresso
            ui.label_meta_mes.setText(f"R${soma} / R${ui.campo_meta_mes.text()}")
            if soma >= meta_mensal:
                #Meta atingida
                ui.label_meta_mes.setStyleSheet('background-color: rgb(0, 173, 247);color:rgb(113,66,230)')
                ui.label_meta_mes.setText(f"Meta atingida! - R${soma} / R${meta_mensal}")
            else:
                #Meta não atingida
                ui.label_meta_mes.setStyleSheet('background-color: rgba(255, 0, 0, 0);color:rgb(113,66,230)')
                ui.label_meta_mes.setText(f"R${soma} / R${meta_mensal}")
        except:
            pass

    def trazer_configuracoes(self):
        #CORRIGIDO ------------------------------------------------------------------
        try:
            ref = db.reference("/Configuracoes")
            # Faz uma solicitação GET para obter as configurações do banco de dados
            configs = ref.get()

            try:
                # Carrega as configurações da interface com base nos dados obtidos
                cor = configs["RGB"]
                r, g, b = map(int, cor.split(','))

                ui.caminho_pasta_principal.setText(configs['DIRETORIO-RAIZ'])
                ui.campo_email_empresa.setText(configs['E-MAIL'])
                ui.campo_cor_R.setValue(int(r))
                ui.campo_cor_G.setValue(int(g))
                ui.campo_cor_B.setValue(int(b))
                ui.campo_porcentagem_validacao.setValue(int(configs['PORCENTAGEM']))
                ui.campo_imposto_validacao.setValue(configs['IMPOSTO VALIDACAO'])
                ui.campo_desconto_validacao.setValue(configs['DESCONTO VALIDACAO'])
                ui.campo_lista_tipo_criar_pasta.setCurrentText(configs['MODO PASTA'])
                ui.campo_desconto.setValue(configs['DESCONTO TOTAL'])
                ui.campo_cod_rev.setText(configs['COD REV'])
                ui.campo_senha_email.setText(configs['SENHA EMAIL'])
                ui.campo_nome_agente.setText(configs['AGENTE'])
                ui.campo_dias_renovacao.setValue(configs['RNG RENOVACAO'])


            except Exception as e:
                print(e)
                pass
        except:
            pass

    def atualizar_configuracoes(self):
        # CORRIGIDO --------------------------------------------------
        # Confirmação de atualização das configurações
        resposta = QMessageBox.question(ui.centralwidget, "Confirmação", "Atualizar configurações?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if resposta == QMessageBox.Yes:
            pass
        else:
            return
        
        ref = db.reference("/Configuracoes")
        # Recupera o diretório da interface
        diretorio = ui.caminho_pasta_principal.text()
        email = ui.campo_email_empresa.text()
        rgb = (f"{ui.campo_cor_R.value()},{ui.campo_cor_G.value()},{ui.campo_cor_B.value()}")
        porcentagem = ui.campo_porcentagem_validacao.value()
        desconto = ui.campo_desconto_validacao.value()
        imposto = ui.campo_imposto_validacao.value()
        criar_pasta = ui.campo_lista_tipo_criar_pasta.currentText()
        campo_desconto = ui.campo_desconto.value()
        campo_cod_rev = ui.campo_cod_rev.text()
        senha_email = ui.campo_senha_email.text()
        atendente = ui.campo_nome_agente.text()
        renovacao = ui.campo_dias_renovacao.value()
        # Cria um dicionário com as novas configurações
        nova_config = {
            "DIRETORIO-RAIZ": diretorio,
            "E-MAIL":email,
            "RGB":rgb,
            "PORCENTAGEM":porcentagem,
            "IMPOSTO VALIDACAO":imposto,
            "DESCONTO VALIDACAO":desconto,
            "MODO PASTA":criar_pasta,
            "DESCONTO TOTAL":campo_desconto,
            "COD REV":campo_cod_rev,
            "SENHA EMAIL":senha_email,
            "AGENTE":atendente,
            "RNG RENOVACAO": renovacao,
            }

        try:
            # Tenta atualizar as configurações no banco de dados
            ref.update(nova_config)
        except Exception as e:
            try:
                # Se não conseguir atualizar, tenta adicionar as configurações
                ref.set(nova_config)
                print("Novas metas adicionadas com sucesso.")
            except Exception as e:
                # Caso dê erro...
                print(f"Erro ao atualizar ou adicionar metas: {e}")

    def trazer_metas(self):
        #CORRIGIDO ----------------------------------------------------------
        ref = db.reference("/Metas")
        # Faz uma solicitação GET para obter as configurações do banco de dados
        Metas = ref.get()
    
        # Carrega as metas na interface gráfica
        valor_semanal = Metas['SEMANAL']
        valor_mensal = Metas['MENSAL']
        ui.campo_meta_semanal.setValue(int(valor_semanal))
        ui.campo_meta_mes.setValue(int(valor_mensal))

    def atualizar_meta_clientes(self):
        if ui.tabWidget.currentIndex() == 2:
            ref = db.reference("/Pedidos")
            Pedidos = ref.get()
            
            # Inicializando contadores para cada semana
            semanas = [0, 0, 0, 0, 0]
            
            # Obter a data do campo ui.campo_data_meta
            mes_meta = ui.campo_data_meta.date().month()
            ano_meta = ui.campo_data_meta.date().year()
            
            for pedido_info in Pedidos:
                if Pedidos[pedido_info]['STATUS'] == "APROVADO":
                    data_pedido = Pedidos[pedido_info]['DATA']
                    data_formatada = datetime.datetime.strptime(data_pedido, "%Y-%m-%dT%H:%M:%SZ")
                    
                    if data_formatada.month == mes_meta and data_formatada.year == ano_meta:
                        semana_do_mes = data_formatada.isocalendar()[1] - (datetime.datetime(data_formatada.year, data_formatada.month, 1).isocalendar()[1] - 1)
                        
                        if semana_do_mes in range(1, 6):
                            try:
                                preco = float(Pedidos[pedido_info]['PRECO'].replace(',', '.'))
                                desconto = 1 - (ui.campo_desconto.value() / 100)
                                semanas[semana_do_mes - 1] += preco * desconto
                            except:
                                pass
            
            # Atualiza os campos da interface gráfica com os valores calculados
            ui.campo_certificados_semana_1.setText(str(semanas[0]))
            ui.campo_certificados_semana_2.setText(str(semanas[1]))
            ui.campo_certificados_semana_3.setText(str(semanas[2]))
            ui.campo_certificados_semana_4.setText(str(semanas[3]))
            ui.campo_certificados_semana_5.setText(str(semanas[4]))
            
            ui.barra_meta_semana_1.setValue(int(semanas[0]))
            ui.barra_meta_semana_2.setValue(int(semanas[1]))
            ui.barra_meta_semana_3.setValue(int(semanas[2]))
            ui.barra_meta_semana_4.setValue(int(semanas[3]))
            ui.barra_meta_semana_5.setValue(int(semanas[4]))
            
            total = sum(semanas)
            ui.barra_meta_mensal.setValue(int(total))
            ui.barra_meta_mensal.setMaximum(int(float(ui.campo_meta_mes.text().replace(',', '.'))))
            ui.campo_certificados_mes.setText(str(total))
            
            self.atualizar_barras_metas()

    def definir_cor(self):
        # Define a cor da borda interna superior da interface
        cor_R = ui.campo_cor_R.value()
        cor_G = ui.campo_cor_G.value()
        cor_B = ui.campo_cor_B.value()
        # Criando a string de folha de estilo com a cor selecionada
    
        # Aplicando a folha de estilo à label
        ui.label_5.setStyleSheet(f"background-color:rgb({cor_R},{cor_G}, {cor_B})")

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
   
    def atualizar_diretorio_raiz(self):
        widget_pai = ui.centralwidget
        # Abrir o explorer para selecionar a pasta raiz
        resposta = QMessageBox.question(ui.centralwidget, "Confirmação", "Tem certeza que deseja atualizar a pasta raiz?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if not resposta == QMessageBox.Yes:
            return
        
        # Abre uma janela do Explorer para selecionar um novo diretório
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
            self.atualizar_documentos_tabela()
        else:
            # Chama a Função de escolher o tipo de conversão de imagem
            self.escolher_conversao()

            # Atualiza a lista de documentos na tabela da janela 'Dados Pedido'
            self.atualizar_documentos_tabela()

    def obter_janela_principal(self,widget):
        # Função para recuperar a janela principal a partir de um widget
        while widget:
            if isinstance(widget, QMainWindow):
                return widget
            widget = widget.parent()
        return None

    def print_tela(self):
        # Tira o print da tela
        try:
            caminho = ui.caminho_pasta.text()

            if not caminho:
                # Se o caminho não estiver definido, pede ao usuário para inserir o nome do arquivo
                nome_documento, ok = QInputDialog.getText(ui.centralwidget, "Nome da print", "Digite o nome da print:",text="DOC ADICIONAL")
                
                # Verifica se o usuário confirmou a entrada
                if not ok:           
                    return
                
                if not nome_documento:
                    return
                
                # Se a pasta não for escolhida, retorna
                caminho_escolhido = QFileDialog.getExistingDirectory(ui.centralwidget, 'Escolher Pasta', '/')
                # Define o caminho completo com o nome do arquivo
                if not caminho_escolhido:      
                    return

                caminho = f"{caminho_escolhido}/{nome_documento}.png"
            else:
                
                # Caso o caminho já esteja definido na interface
                nome_documento, ok = QInputDialog.getText(ui.centralwidget, "Nome da print", "Digite o nome da print:",text=f"DOC ADICIONAL")
                
                # Verifica se o usuário confirmou a entrada
                if not ok:           
                    return
                
                # Se o nome não for inserido, retorna
                if not nome_documento:
                    return
                
                # Define o caminho completo com o nome do arquivo
                caminho = f"{caminho}/{nome_documento}.png"

            # Obtém a janela principal que será escondida durante o screenshot
            janela_principal = self.obter_janela_principal(ui.centralwidget)

            if janela_principal:

                janela_principal.setWindowOpacity(0)
            # Aguarda meio segundo para continuar
            time.sleep(0.5)

            # Tira um screenshot da tela
            screenshot = pyautogui.screenshot()

            # Restaura a janela principal (opcional)
            if janela_principal:
                #janela_principal.showNormal()
                janela_principal.setWindowOpacity(1)

            # Salvei o screenshot no caminho especificado
            screenshot.save(caminho)

            ui.label_confirmacao_tirar_print.setText("✅")

            self.atualizar_documentos_tabela()
        
        except:
            # Em caso de erro, atualiza a tabela e exibe um alerta na interface
            self.atualizar_documentos_tabela()
            ui.label_confirmacao_tirar_print.setText("❌")
            self.mensagem_alerta("Erro",f"Não foi possível capturar a tela!")

    def pasta_existe(self,diretorio, nome_pasta):
        #transformei o texto em um diretório
        caminho_pasta = os.path.join(diretorio, nome_pasta)
        return os.path.exists(caminho_pasta)

    def abrir_pasta_cliente(self):
        try:
            QDesktopServices.openUrl(QUrl.fromLocalFile(ui.caminho_pasta.text()))
            ui.label_confirmacao_criar_pasta.setText('✅')
        except:
            ui.label_confirmacao_criar_pasta.setText('❌')
            return

    def criar_pasta_cliente(self):
        try:
            pedido = ui.campo_pedido.text()
            versao = ui.campo_lista_versao_certificado.currentText()
            hora = ui.campo_hora_agendamento.text()
            data = ui.campo_data_agendamento.text()
            modalidade = ui.campo_lista_modalidade.currentText()

            if pedido == "" or hora == "00:00" or data == "01/01/2000" or modalidade == "" or versao == "":

                ui.label_confirmacao_criar_pasta.setText("❌")
                self.mensagem_alerta("Pasta não criada","Adicione os itens com 🌟 para criar a pasta do cliente!")
                return
         
            self.formatar_nome()
            tipo = ui.campo_lista_tipo_criar_pasta.currentText()
            if tipo == "NOME":
                if ui.campo_nome.text() == "":
                    self.mensagem_alerta("Pasta não criada","Adicione o nome do cliente!")
                    ui.label_confirmacao_criar_pasta.setText("❌")
                    return
                nome_pasta = f'{ui.campo_nome.text()}'
            
            elif tipo == "PEDIDO":
                nome_pasta = f'{ui.campo_pedido.text()}'
            
            elif tipo == "PEDIDO-NOME":
                if ui.campo_nome.text() == "":
                    self.mensagem_alerta("Pasta não criada","Adicione o nome do cliente!")
                    ui.label_confirmacao_criar_pasta.setText("❌")
                    return
                nome_pasta = f'{str(ui.campo_pedido.text())}-{ui.campo_nome.text()}'

            # Tente criar a pasta no diretório padrão
            diretorio_padrão = ui.caminho_pasta_principal.text()
            pasta_padrão = os.path.join(diretorio_padrão, nome_pasta)

            #Verifica se a pasta existe no diretório
            if not self.pasta_existe(diretorio_padrão, nome_pasta):
                
                os.mkdir(pasta_padrão)
                pasta_padrão = pasta_padrão.replace("/", "\\")
                ui.caminho_pasta.setText(pasta_padrão)
                
                status = banco_dados.alteracao_status()
                #Se o status do pedido for Aprovado ou Cancelado, exclua a pasta
                if status == "APROVADO" or status == "CANCELADO":
                    confirmacao = ""
                else:
                    confirmacao = "✅"

                ui.label_confirmacao_criar_pasta.setText(confirmacao)
                self.acoes.salvar_pedido()
            #Caso exista, abra
            else:
                self.abrir_pasta_cliente()
        except Exception as e:
            print(e)
            ui.label_confirmacao_criar_pasta.setText("❌")

    def procurar_cnh(self):
        #Abre o link para consulta da CNH
        url = QUrl("https://portalservicos.senatran.serpro.gov.br/#/condutor/validar-cnh")
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
    
    def procurar_pis(self):
        url = QUrl("https://sal.rfb.gov.br/PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosAntes/selecionarOpcoesCalculoAntes.xhtml")
        QDesktopServices.openUrl(url)
        return

    def formatar_orgao_rg(self):
        orgao = ui.campo_rg_orgao.text().rstrip()
        ui.campo_rg_orgao.setText(orgao.upper())

    def contato_telefone(self):
        if ui.campo_telefone.text() == '':
           return

        self.mensagem_contato()

    def procurar_cnpj(self):
        cnpj = ui.campo_cnpj.text()
        url_receita = QUrl(f"https://solucoes.receita.fazenda.gov.br/servicos/cnpjreva/Cnpjreva_Solicitacao.asp?cnpj={cnpj}")
        QDesktopServices.openUrl(url_receita)

    def dados_cnpj(self):
        ui.campo_cnpj_municipio.setText("") 

        cnpj = ''.join(filter(str.isdigit, ui.campo_cnpj.text()))

        if not cnpj:
            return
        
        url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"

        try:
            resposta = requests.get(url)

            if resposta.status_code == 200:
                data = resposta.json()
                ui.campo_cnpj_municipio.setText(f'{data['municipio']}/{data['uf']}')
                ui.campo_cnpj_razao_social.setText(data['nome'])

                qsa = data.get('qsa', [])
    
                if len(qsa) == 1:
                    if ui.campo_nome.text() == "":
                        ui.campo_nome.setText(qsa[0]['nome'])
                    else:
                        pass
                else:
                    pass

                uf = data['uf']
                
                if uf != "SP":
                    ui.campo_lista_junta_comercial.setCurrentText(uf)
                    self.atualizar_documentos_tabela()
                    return
                else:
                    ui.campo_lista_junta_comercial.setCurrentText(uf)
                    self.atualizar_documentos_tabela()
                    return
                
            else:
                ui.campo_cnpj_municipio.setText("")
                self.atualizar_documentos_tabela()
                return
            
        except RequestException:
            ui.campo_cnpj_municipio.setText("")
            ui.campo_cnpj_uf.setText("")
            self.atualizar_documentos_tabela()
            self.mensagem_alerta("ERRO DE CONEXÃO","Sem conexão com a internet.")
            return
        except Exception as e:
            self.atualizar_documentos_tabela()
            self.mensagem_alerta("ACESSO BLOQUEADO","Limite de requisições atingido!\nEspere alguns segundos para fazer nova busca!")
            return

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

    def formatar_preco_certificado(self):
        if not ui.campo_preco_certificado.text() =="":
            texto = ui.campo_preco_certificado.text()
            preco = float(texto)
            preco = "{:.2f}".format(preco)
            ui.campo_preco_certificado.setText(str(preco))

    def procurar_cpf(self):
        
        cpf = ui.campo_cpf.text()
        nascimento = ui.campo_data_nascimento.text()
        if not nascimento == "01/01/2000":
            url = QUrl(f"https://servicos.receita.fazenda.gov.br/Servicos/CPF/ConsultaSituacao/ConsultaPublica.asp?cpf={cpf}&Nascimento={nascimento}")
            QDesktopServices.openUrl(url)
            self.atualizar_documentos_tabela()
            return
        else:
            url = QUrl(f"https://servicos.receita.fazenda.gov.br/Servicos/CPF/ConsultaSituacao/ConsultaPublica.asp?cpf={cpf}")
            QDesktopServices.openUrl(url)
            self.atualizar_documentos_tabela()
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
            
    def formatar_data_agendamento(self):
        data_agendamento = ui.campo_data_agendamento.date()
        data_atual = QDate.currentDate()

        if data_agendamento < data_atual:
            ui.campo_data_agendamento.setStyleSheet("color: red")
        else:
            ui.campo_data_agendamento.setStyleSheet("color: black")
            
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

    def exportar_excel(self):
        try:
            data_inicial = banco_dados.data_para_iso(QDateTime(ui.campo_data_de.date()))
            data_final = banco_dados.data_para_iso(QDateTime(ui.campo_data_ate.date()))

            # Consulte o banco de dados usando as datas no formato ISO
            pedidos_ref = ref.child("Pedidos").order_by_child("DATA") \
                            .start_at(data_inicial) \
                            .end_at(data_final)
            req = pedidos_ref.get()

            numero_inteiro_inicial = datetime.datetime.strptime(data_inicial, "%Y-%m-%dT%H:%M:%SZ").toordinal()
            numero_inteiro_final = datetime.datetime.strptime(data_final, "%Y-%m-%dT%H:%M:%SZ").toordinal()

            dados_selecionados = []
            x = 0

            for cliente in req:
                data_bd = datetime.datetime.strptime(req[cliente]['DATA'], "%Y-%m-%dT%H:%M:%SZ")
                numero_inteiro_bd = data_bd.toordinal()
                status_filtro = ui.campo_lista_status_2.currentText()
                status_servidor = req[cliente]['STATUS']

                if numero_inteiro_inicial <= numero_inteiro_bd <= numero_inteiro_final:
                    if status_filtro == status_servidor or status_filtro == "TODAS":
                        x += 1
                        pedido = req[cliente]['PEDIDO']
                        data_agendamento = datetime.datetime.strptime(req[cliente]['DATA'], "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y")
                        versao = req[cliente].get('VERSAO', "")
                        nome = req[cliente].get('NOME', "")
                        telefone = req[cliente].get('TELEFONE', "")
                        email = req[cliente].get('EMAIL', "")
                        preco = req[cliente].get('PRECO', "").replace(',', '.')
                        if status_servidor == "APROVADO":
                            validade = datetime.datetime.strptime(req[cliente]["VALIDO ATE"], "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y")
                        else:
                            validade = "-"

                        try:
                            preco = float(preco)
                        except ValueError:
                            preco = 0.0
                        hora_agendamento = req[cliente]['HORA']
                        status_agendamento = req[cliente]['STATUS']
                        vendido = req[cliente]['VENDA']
                        modalidade = req[cliente]['MODALIDADE']
                        if status_servidor == "APROVADO":
                            validade = datetime.datetime.strptime(req[cliente]["VALIDO ATE"], "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y")
                        else:
                            validade = "-"

                        dados_selecionados.append((pedido, nome, telefone, email, data_agendamento, versao, hora_agendamento, status_agendamento, vendido, modalidade, preco,validade))

            if x > 0:
                root = tk.Tk()
                root.withdraw()
                caminho_arquivo = filedialog.askdirectory()
                if caminho_arquivo:
                    df = pd.DataFrame(dados_selecionados, columns=['Pedido', 'Cliente', 'Telefone', 'E-mail', 'Data agendamento', 'Versão', 'Hora', 'Status Pedido', 'Vendido por mim?', 'Modalidade', 'Comissão','Válido até'])
                    data_agora = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
                    data_final_text = ui.campo_data_ate.text()
                    data_inicial_text = ui.campo_data_de.text()
                    pasta_desktop = os.path.expanduser(f"{caminho_arquivo}")
                    nome_arquivo = os.path.join(pasta_desktop, f"Certificados-emitidos-de {data_inicial_text.replace('/', '-')} a {data_final_text.replace('/', '-')}-gerado em {data_agora.replace('/','-')} .xlsx")
                    df.to_excel(nome_arquivo, index=False)
                    self.mensagem_alerta("Arquivo salvo", "Arquivo excel gerado!")
                else:
                    return
            else:
                self.mensagem_alerta("Sem dados", "Sem dados para o período!")
        except Exception as e:
            print(e)
            self.mensagem_alerta("Arquivo não salvo", f"Arquivo não gerado!\nmotivo: {e}")

    def copiar_pedido_tabela(self,event):
        # Obtém a célula atualmente selecionada na tabela
        item = ui.tableWidget.currentItem()
        coluna = item.column()
        # Verifica se há um item selecionado
        if item is not None:
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
            nome_documento, ok = QInputDialog.getItem(ui.centralwidget, "Nome do Documento", "Escolha o tipo de documento:", ["CNH COMPLETA", "RG COMPLETO","OAB COMPLETO","DOC ADICIONAL","DOC COMPLETO","OUTRO"], 0, False)
            
            
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
            self.atualizar_documentos_tabela()


        except:
            ui.label_confirmacao_mesclar_pdf.setText("❌")
            pdf_merger.close()
            self.atualizar_documentos_tabela()
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
            self.atualizar_documentos_tabela()

        except:
            self.atualizar_documentos_tabela()
            ui.label_confirmacao_converter_pdf.setText("❌")

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
        banco_dados.contar_verificacao()

    def evento_ao_fechar(self,event):

        
        result = QMessageBox.question(janela, "Confirmação", "Você realmente deseja sair?", QMessageBox.Yes | QMessageBox.No)
        
        if result == QMessageBox.Yes:
            try:
                event.accept()
                self.nova_janela.close()  
            
            except:
                event.accept()
                
        else:
            event.ignore()

    def copiar_campo(self,nome_campo):
        
        match nome_campo:
            
            case 'campo_oab':
                try:
                    QApplication.clipboard().setText(ui.campo_oab.text())
                    ui.campo_oab.selectAll()
                except:
                    pass
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
            case'campo_pis':
                try:
                    QApplication.clipboard().setText(ui.campo_pis.text())
                    ui.campo_pis.selectAll()
                except:
                    pass
            case'campo_oab':
                try:
                    QApplication.clipboard().setText(ui.campo_oab.text())
                    ui.campo_oab.selectAll()
                except:
                    pass
            
    def manter_tela_aberta(self):
        if ui.campo_verifica_tela_cheia.text() == "SIM":
            ui.campo_verifica_tela_cheia.setText("NAO")
            ui.botao_tela_cheia.setText("🔓")
        else:
            ui.campo_verifica_tela_cheia.setText("SIM")
            ui.botao_tela_cheia.setText("🔒")

    def atualizar_aba(self):
        if ui.tabWidget.currentIndex() == 2:
            self.atualizar_meta_clientes()    
        else:
            pass

    def valor_alterado(self, campo_atual):
        self.atualizar_documentos_tabela()
        if campo_atual is not None:
            nome_campo_atual = campo_atual.objectName()
            novo_valor = self.obter_valor_campo(campo_atual)
            campo_anterior = getattr(self.ui, campo_atual.objectName(), None)

            if campo_anterior is not None and novo_valor is None:
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
    
    def carregar_lista_certificados(self):
       if ui.campo_lista_versao_certificado.currentText() == "":
            ref = db.reference("/Certificados")
            certificados = ref.get()

            ui.campo_lista_versao_certificado.clear()  # Limpar qualquer item existente no combobox
            ui.campo_lista_versao_certificado.addItem("")
            ui.campo_lista_versao_certificado.addItems(certificados.keys())  # Adicionar as chaves do dicionário ao combobox

            ui.campo_lista_versao_certificado.insertItem(1,'e-CNPJ - no computador - 12 meses')
            ui.campo_lista_versao_certificado.insertItem(2,'e-CPF - no computador - 12 meses')

    def pegar_link_venda(self):
        try:
            ref = db.reference(f"/Certificados/{ui.campo_lista_versao_certificado.currentText()}")
            certificado = ref.get()
            link_venda = certificado["LINK VENDA"]
            rev = str(ui.campo_cod_rev.text())

            if certificado:
                link = f"{link_venda}{rev}"
                pyperclip.copy(str(link))
        except:
            pass

    def buscar_preco_certificado(self):        
        ref = db.reference("/Certificados")        
        lista_certificados = ref.get()        
        certificado = ui.campo_lista_versao_certificado.currentText()        
        if certificado in lista_certificados:            
            # Armazenar o valor da chave correspondente em uma variável            
            valor_do_certificado = float(lista_certificados[certificado]["VALOR"].replace(',','.'))            
            ui.campo_preco_certificado_cheio.setText(str(valor_do_certificado))            
            porcentagem_validacao = int(ui.campo_porcentagem_validacao.value()) / 100            
            imposto_de_renda = 1 - (ui.campo_imposto_validacao.value() / 100)            
            desconto_validacao = float(ui.campo_desconto_validacao.text().replace(',','.'))                                    
            valor_final = ((valor_do_certificado * porcentagem_validacao) * imposto_de_renda) - desconto_validacao            
            if valor_final < 0:                
                valor_final = 0            
            valor_final_formatado = "{:.2f}".format(valor_final)  # Formatar o valor para duas casas decimais
            
            # Atualizar apenas o ToolTip
            tooltip_text = (
                f"COMO CHEGUEI NESSE VALOR?\n"
                "\n"
                f"Valor do certificado: R${valor_do_certificado}\n"
                f"Porcentagem na validação ({porcentagem_validacao * 100:.1f}%): R${valor_do_certificado * porcentagem_validacao:.2f}\n"
                "\n"
                f"(=)Valor Bruto: R${valor_do_certificado * porcentagem_validacao:.2f}\n"
                f"(-) Imposto de renda ({(1 - imposto_de_renda) * 100:.1f}%): -R${valor_do_certificado * porcentagem_validacao * (1 - imposto_de_renda):.2f}\n"
                f"(=)Valor líquido: R${valor_do_certificado * porcentagem_validacao * imposto_de_renda:.2f}\n"
                f"(-) Desconto adicional: -R${desconto_validacao}\n"
                f"---------------------------------\n"
                f"Valor final: R${valor_final_formatado}"
            )


            
            ui.campo_preco_certificado.setToolTip(tooltip_text)
            ui.campo_preco_certificado.setText(valor_final_formatado)

    def duplicar_pedido(self):
        resposta = QMessageBox.question(ui.centralwidget,'Duplicar pedido', 'Duplicar pedido atual?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resposta == QMessageBox.Yes:
            pedido = ui.campo_pedido.text()
            ui.campo_pedido.setText('')
            ui.campo_pedido.setReadOnly(False)
            ui.campo_cnpj.setText('')
            ui.campo_cnpj_razao_social.setText('')
            ui.campo_cnpj_municipio.setText('')
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

    def abrir_janela_mensagem(self):
        self.abrir_nova_janela(janela)

    def clique_btn1(self):  
            mensagem_inicial = self.determinar_hora(datetime.datetime.now().time() )
            nome = ui.campo_nome_agente.text()

            mensagem = f'{mensagem_inicial}, tudo bem?\n'\
f'Sou o {nome}, agente de registro da ACB Digital e farei seu atendimento.' 
    
            pyperclip.copy(mensagem)                                                                                                                                    
            return "APRESENTAÇÃO"

    def clique_btn3(self):

        mensagem = 'Para prosseguirmos com a validação, preciso que o Sr(a). me encaminhe aqui pelo Chat uma foto completa do seu documento de identificação, *frente e verso*, podendo ser:\n'\
' •CNH\n'\
' •RG\n'\
' •CREA\n'\
' •OAB\n'\
'\n '\
'Observações: \n' \
' 1. Retire o documento de identificação do plástico e abra-o.\n' \
' 2. O verso do documento é onde está o QRcode.'

        pyperclip.copy(mensagem)                                                                                                                                    
        return "PEDIR DOCUMENTO PESSOAL"
    
    def clique_btn5(self):
        #################### CNPJ
                                                                                                                                            
        mensagem = 'Irei precisar também do Documento de Constituição da Empresa, podendo ser: \n'\
' •Contrato Social\n'\
' •Certidão de inteiro teor\n'\
' •Estatuto social\n'\
' •Requerimento de empresário'                                                               
        pyperclip.copy(mensagem) 
        #return mensagem
        return "PEDIR DOCUMENTO EMPRESA"

    def clique_btn7(self):
        mensagem = 'Obrigado! Um momento.'
        QApplication.clipboard().setText(mensagem)
        return 'OBRIGADO. UM MOMENTO.'

    def clique_btn9(self):
        mensagem = 'Podemos iniciar a vídeo-conferência?'
        QApplication.clipboard().setText(mensagem)
        return 'PODEMOS INICIAR A VÍDEO?'

    def clique_btn11(self):
        mensagem = 'Agradecemos pela disponibilidade!\n'\
        '\n'\
        'Em caso de dúvidas, contate o suporte através do número 4020-9735 ou pelo WhatsApp (11)96400-1221. \n'\
        'Caso precise adquirir mais certificados, pode comprá-los através do link: \n'\
        f'https://loja.certisign.com.br/?cod_rev={ui.campo_cod_rev.text()}. \n'\
        '\n'\
        'Até mais!'
        pyperclip.copy(mensagem) 
        return 'FINALIZADO COM SUCESSO'

    def clique_btn13(self):
        mensagem = 'Estou finalizando o chat devido à ausência de interação.\n'\
        'Caso queira agendar um novo atendimento, pode fazê-lo pelo Whatsapp:(11)96400-1221.\n'\
        'Até mais!'
        pyperclip.copy(mensagem)
        return 'FINALIZADO SEM SUCESSO'

    def clique_btn15(self):
        mensagem = 'Link para reembolso: https://www.certisign.com.br/reembolso'
        QApplication.clipboard().setText(mensagem)
        return 'LINK REEMBOLSO'

    def clique_btn17(self):
        mensagem = 'e-mail: paranagua@acbdigital.com.br'
        QApplication.clipboard().setText(mensagem)
        return 'PARANAGUA@ACBDIGITAL.COM.BR'

    def clique_btn2(self):
    # Observações
        midia = ''
        if 'cartão' in ui.campo_lista_versao_certificado.currentText().lower():
            midia = 'CARTÃO'
        elif 'token' in ui.campo_lista_versao_certificado.currentText().lower(): 
            midia = 'TOKEN'
        
        mensagem = f'Seu pedido contém a mídia {midia}. Gostaria de retirar em um dos nossos escritórios ou prefere que seja enviado para seu endereço?'
                                                                                    
        pyperclip.copy(mensagem) 
        return 'RETIRADA OU ENVIO?'

    def clique_btn4(self):
        mensagem = 'Link postos de atendimento: https://www.certisign.com.br/duvidas-suporte/certificado-digital/locais-atendimento - Basta digitar seu CEP e serão listados os postos mais próximos.'
        QApplication.clipboard().setText(mensagem)
        return 'LINK MAPA POSTOS DE ATENDIMENTO'

    def clique_btn6(self):
        #######################  OAB
        nome = ui.campo_nome_agente.text()
        mensagem_inicial = self.determinar_hora(datetime.datetime.now().time() )
                                                                                                                                            
        mensagem = f'{mensagem_inicial}, tudo bem? \n'\
        f'Sou o {nome}, agente de registro da ACB Digital e farei seu atendimento.\n'\
        'Para prosseguirmos com a validação, preciso que o Sr(a). me encaminhe aqui pelo Chat:\n' \
        '\n ' \
        '•Uma foto completa do seu documento de identificação *OAB*, frente e verso.'
                                                                                                           
        pyperclip.copy(mensagem) 
        return "PEDIR OAB"

    def clique_btn8(self):
        mensagem = f'Link para compra: https://loja.certisign.com.br/?cod_rev={ui.campo_cod_rev.text()}'
        QApplication.clipboard().setText(mensagem)
        return 'LINK PADRÃO DE COMPRA'
  
    def clique_btn10(self):
        mensagem = 'Ainda está ai?'
        QApplication.clipboard().setText(mensagem)
        return 'AINDA ESTÁ AI?'
    
    def clique_btn12(self):
        pedido = ui.campo_pedido.text()
        mensagem = str(f'https://gestaoar.certisign.com.br/GestaoAR/cliente/emissao/{pedido}')
        QApplication.clipboard().setText(mensagem)
        return 'LINK PARA INSTALAÇÃO DO CERTIFICADO'
    
    def clique_btn14(self):
        mensagem = 'SUPORTE CLIENTE: 4020-9735/WHATSAPP:(11) 96400-1221'
        QApplication.clipboard().setText(mensagem)
        return mensagem
    
    def clique_btn16(self):
        mensagem = '''Verifiquei que o pagamento para seu pedido ainda não foi reconhecido em nosso sistema.
Para que possamos prosseguir com a validação, é necessário que o pagamento seja confirmado.
Peço que entre em contato com o suporte pelo telefone *4020-9735* para que possam verificar e regularizar a situação.
'''
        QApplication.clipboard().setText(mensagem)
        return 'PROBLEMA PAGAMENTO'
        
    def clique_btn18(self):

        certificado = ui.campo_lista_versao_certificado.currentText()

        midia = ""
        if "token" in certificado:
            midia = "TOKEN"
        elif "cartão" in certificado:
            midia = "CARTÃO"

        mensagem = f''' 
ENVIO DE MÍDIA
Dados para envio de mídia do(a) Cliente {ui.campo_nome.text()}
mídia:{midia}
Pedido: {ui.campo_pedido.text()}
Endereço: '''
        
        QApplication.clipboard().setText(mensagem)
        return 'E-MAIL ENVIO MÍDIA'
       
    def ocultar_aba_tabela(self):
        ui.tableWidget.setColumnHidden(0, True)
        ui.tableWidget.setColumnHidden(1, True)
        ui.tableWidget.setColumnHidden(2, True)
        ui.tableWidget.setColumnHidden(3, True)
        ui.tableWidget.setColumnHidden(9, True)
    
    def reexibir_aba_tabela(self):
        for col in range(ui.tableWidget.columnCount()):
            ui.tableWidget.setColumnHidden(col, False)

    def definir_hoje(self):
        ui.campo_data_de.setDate(QDate.currentDate())
        ui.campo_data_ate.setDate(QDate.currentDate()) 

    def abrir_nova_janela(self, janela_pai):
        self.nova_janela = QDialog(janela_pai)
        self.nova_janela.setFixedSize(484, 670)  # Ajuste o tamanho da janela para acomodar duas colunas
        self.nova_janela.setWindowTitle('Mensagens')
        self.nova_janela.setStyleSheet(f"color: #{'%02x%02x%02x' % (ui.campo_cor_R.value(), ui.campo_cor_G.value(), ui.campo_cor_B.value())};")

        # Obtém a posição da janela raiz
        pos = janela_pai.pos()

        # Posiciona a nova janela à esquerda da janela raiz e na mesma altura
        self.nova_janela.move(pos.x() - self.nova_janela.width() - 8, pos.y())

        # Cria uma área de rolagem
        scroll = QScrollArea(self.nova_janela)
        scroll.setFixedSize(484, 670)  # Ajuste o tamanho da área de rolagem para acomodar duas colunas

        # Cria um widget para conter os botões
        widget = QWidget()
        layout = QGridLayout()  # Mude para QGridLayout

        # Lista de funções para obter os textos dos botões
        funcoes = [
            self.clique_btn1,
            self.clique_btn2,
            self.clique_btn3,
            self.clique_btn4,
            self.clique_btn5,
            self.clique_btn6,
            self.clique_btn7,
            self.clique_btn8,
            self.clique_btn9,
            self.clique_btn10,
            self.clique_btn11,
            self.clique_btn12,
            self.clique_btn13,
            self.clique_btn14,
            self.clique_btn15,
            self.clique_btn16,
            self.clique_btn17,
            self.clique_btn18
        ]

        # Obtém as mensagens chamando cada função
        nomes = [func() for func in funcoes]

        # Cria 13 botões
        for i, botao_texto in enumerate(nomes):
            if botao_texto is not None:  # Verifica se o texto do botão não é None
                botao = QPushButton()  # Cria um botão sem texto
                botao.setFixedSize(228, 66)  # Define o tamanho do botão
                botao.setStyleSheet("QPushButton { text-align: justify; }")  # Alinha o texto do botão à esquerda

                # Dividir o texto em linhas para caber no botão
                linhas = [botao_texto[j:j+40] for j in range(0, len(botao_texto), 40)]
                botao.setText('\n'.join(linhas))  # Define o texto do botão como várias linhas

                botao.clicked.connect(lambda _, b=botao: self.copiar_e_fechar(b))  # Conecta o sinal clicked ao slot copiar_e_fechar
                layout.addWidget(botao, i // 2, i % 2)  # Adiciona o botão no layout em duas colunas

                # Conecta o botão à função correspondente
                func_name = f'clique_btn{i+1}'
                if hasattr(self, func_name):
                    botao.clicked.connect(getattr(self, func_name))

        widget.setLayout(layout)
        scroll.setWidget(widget)

        self.nova_janela.show()

    def copiar_e_fechar(self, botao):
        clipboard = QGuiApplication.clipboard()
        mime_data = QMimeData()
        mime_data.setText(botao.text())
        clipboard.setMimeData(mime_data)
        self.nova_janela.close()

    def determinar_hora(self,hora):
        match hora:
            case tempo if tempo < datetime.datetime.strptime("12:00", "%H:%M").time():
                return "Bom dia"
            case tempo if datetime.datetime.strptime("12:00", "%H:%M").time() < tempo < datetime.datetime.strptime("17:59", "%H:%M").time():
                return "Boa tarde"
            case tempo if tempo >= datetime.datetime.strptime("18:00", "%H:%M").time():
                return "Boa noite"

    def mensagem_contato(self):
          
        mensagem_inicial = self.determinar_hora(datetime.datetime.now().time() )

        texto, ok = QInputDialog.getItem(ui.centralwidget, "Mensagens Whatsapp", "Escolha a Mensagem:", ["INICIAR ATENDIMENTO", "ERRO NA VALIDAÇÃO","OUTRO"], 0, False)
        
        if not ok or not texto:
            return 
        
        nome_completo = ui.campo_nome.text()
        if nome_completo != '':
            primeiro_nome = nome_completo.split()[0]
            primeiro_nome = primeiro_nome.capitalize()
        else:
            pass
        
        if texto == 'OUTRO':
                mensagem = f'{mensagem_inicial}, tudo bem?\n'\

        if texto == 'INICIAR ATENDIMENTO':
             nome = ui.campo_nome_agente.text()
             mensagem = f'{mensagem_inicial}, tudo bem?\n'\
f'Sou o {nome}, agente de registro da ACB Digital e temos um agendamento para seu certificado digital às {ui.campo_hora_agendamento.text()}. \n' \
'Podemos Iniciar o atendimento?'
        
        elif texto == 'ERRO NA VALIDAÇÃO':
            mensagem = f'{mensagem_inicial}, tudo bem?\n'\
f'Sou o {nome} que fez a validação do seu certificado digital.\n'\
'Estou entrando em contato pois ocorreu um erro na validação do seu pedido.'
            
        numero = ui.campo_telefone.text()  # substitua pelo número de telefone desejado
        mensagem = mensagem.replace(' ', '%20')  # substitui espaços por %20
        url_mensagem = QUrl(f'https://api.whatsapp.com/send?phone={numero}&text={mensagem}')
        QDesktopServices.openUrl(url_mensagem)

    def envio_de_email(self):
        nome = ui.campo_nome_agente.text()
        hora = ui.campo_hora_agendamento.time().toString("HH:mm")
        data = ui.campo_data_agendamento.date().toString("dd/MM/yyyy")    
        email = ui.campo_email.text()
     
        variaveis = [hora,data,email]

        nomes_mensagens = {
            "hora": "Hora",
            "data":"Data",
            "email":"Email",
        }

        campos_vazios = [nomes_mensagens[nome_variavel] for nome_variavel, valor in zip(["hora","data","email"], variaveis) if (isinstance(valor, str) and valor == "") or (nome_variavel == "hora" and valor == "00:00") or (nome_variavel == "data" and valor == "01/01/2000")]

        if campos_vazios:
            campos_faltando = "\n•".join(campos_vazios)
            mensagem_alerta = f"Preencha os seguintes campos para enviar o E-mail! \n•{campos_faltando}"
            self.mensagem_alerta("Erro no envio", mensagem_alerta)
            return
      

        tipo_mensagem, ok = QInputDialog.getItem(ui.centralwidget, "Envio", "Escolha o conteúdo do E-mail:", ["INICIO DE ATENDIMENTO", "PROBLEMA DE PAGAMENTO","RENOVAÇÃO"], 0, False)
        if not ok:
            return
        
        

        match tipo_mensagem:
            case 'INICIO DE ATENDIMENTO':
                mensagem_inicial = self.determinar_hora(datetime.datetime.now().time() )
                assunto = f"Validação Certificado Digital - Pedido {ui.campo_pedido.text()}"                                                                                                                           
                corpo = f'''{mensagem_inicial}, tudo bem? 

Sou o {nome}, agente de registro da ACB Digital.

Estou entrando em contato pois temos uma validação para seu certificado digital às {ui.campo_hora_agendamento.text()} do dia {ui.campo_data_agendamento.text()}.


atenciosamente,

{nome}'''

        
            case 'PROBLEMA DE PAGAMENTO':
                mensagem_inicial = self.determinar_hora(datetime.datetime.now().time() )
                assunto = f"Validação Certificado Digital - Pedido {ui.campo_pedido.text()}"
                corpo = f'''{mensagem_inicial}, Tudo bem?

Sou {nome}, agente de registro da ACB Digital. Estou entrando em contato para informar que temos uma validação agendada para o seu certificado digital às {ui.campo_hora_agendamento.text()} do dia {ui.campo_data_agendamento.text()}. 

No entanto, verifiquei que o pagamento ainda não foi reconhecido em nosso sistema.

Para que possamos prosseguir com a validação, é necessário que o pagamento seja confirmado. 

Peço que entre em contato com o suporte pelo telefone 4020-9735 para que possam verificar e regularizar a situação.

Agradeço a compreensão.


Atenciosamente,

{nome}'''
                
            case 'RENOVAÇÃO':
                ref_link_venda = db.reference(f"/Certificados/{ui.campo_lista_versao_certificado.currentText()}")
                certificado = ref_link_venda.get()
                primeiro_nome = ui.campo_nome.text().split()[0]
                link_venda = f'{certificado["LINK VENDA"]}{ui.campo_cod_rev.text()}'
                mensagem_inicial = self.determinar_hora(datetime.datetime.now().time())
                assunto = f"Renovação Certificado Digital Certisign"
                
                # Corpo do e-mail em HTML
                corpo_html = (
                    f"<!DOCTYPE html>"
                    f"<html lang='pt-BR'>"
                    f"<head>"
                    f"<meta charset='UTF-8'>"
                    f"<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
                    f"<style>"
                    f"  body {{ font-family: Arial, sans-serif; color: #333333; margin: 0; padding: 0; background-color: #f7f7f7; text-align: center; }}"
                    f"  .container {{ width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); text-align: center; }}"
                    f"  .header {{ background-color: #4E4BFF; color: white; padding: 20px; border-top-left-radius: 8px; border-top-right-radius: 8px; }}"
                    f"  .header h1 {{ margin: 0; font-size: 24px; color: white; }}"
                    f"  .content {{ padding: 20px; text-align: center; }}"
                    f"  .content p {{ font-size: 18px; line-height: 1.6; }}"
                    f"  .btn {{ display: inline-block; padding: 10px 20px; background-color: rgb(89, 62, 255) !important; color: #FFFFFF !important; text-decoration: none; border-radius: 5px; font-weight: bold; }}"
                    f"  .footer {{ background-color: #f1f1f1; text-align: center; padding: 10px; font-size: 12px; color: #888888; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; }}"
                    f"</style>"
                    f"</head>"
                    f"<body>"
                    f"  <div class='container'>"
                    f"    <div class='header'>"
                    f"      <h1>Renovação do Certificado Digital</h1>"
                    f"    </div>"
                    f"    <div class='content'>"
                    f"      <p>{mensagem_inicial} {primeiro_nome}, Tudo bem?</p>"
                    f"      <p>Meu nome é {nome} e sou Agente de Registro da ACB Digital.</p>"
                    f"      <p>Verificamos que a validade do seu certificado digital está próxima do <b>vencimento</b>.</p>"
                    f"      <p>Compreendemos a importância de manter a continuidade dos serviços digitais em sua organização. Portanto, gostaríamos de oferecer a renovação do seu certificado.</p>"
                    f"      <p>Para sua conveniência, fornecemos um link para a renovação do seu certificado digital:</p>"
                    f"      <p><a href='{link_venda}' class='btn'>RENOVAR AGORA</a></p>"
                    f"      <p>Agradecemos a oportunidade de continuar a atendê-lo.</p>"
                    f"      <p>Atenciosamente,</p>"
                    f"      <p>{nome}</p>"
                    f"    </div>"
                    f"    <div class='footer'>"
                    f"      <p>ACB Digital &copy; 2024. Todos os direitos reservados.</p>"
                    f"    </div>"
                    f"  </div>"
                    f"</body>"
                    f"</html>"
                )

                # Verifica se o e-mail foi inserido
                if ui.campo_email.text():
                    remetente = ui.campo_email_empresa.text()
                    destinatarios = ui.campo_email.text()
                    senha = ui.campo_senha_email.text()

                    # Usar MIMEMultipart para enviar HTML corretamente
                    msg = MIMEMultipart("alternative")
                    msg['Subject'] = assunto
                    msg['From'] = remetente
                    msg['To'] = destinatarios

                    parte_html = MIMEText(corpo_html, "html")
                    msg.attach(parte_html)

                    try:
                        # Envio do e-mail
                        with smtplib.SMTP_SSL('email-ssl.com.br', 465) as smtp_server:
                            smtp_server.login(remetente, senha)
                            smtp_server.sendmail(remetente, destinatarios, msg.as_string())
                            self.mensagem_alerta("Sucesso", "E-mail enviado com sucesso!")
                    except smtplib.SMTPException as e:
                        self.mensagem_alerta("Erro", f"Erro ao enviar o e-mail: {e}")

    def mostrar_senha(self):
        if ui.campo_senha_email.echoMode() == QLineEdit.Password:
            ui.campo_senha_email.setEchoMode(QLineEdit.Normal)
        else:
            ui.campo_senha_email.setEchoMode(QLineEdit.Password)

    def envio_em_massa(self):
        if not banco_dados.mensagem_confirmacao("Confirmação", f"Enviar email de renovação em massa?"):
            return

        ui.tableWidget.setRowCount(0)  # Limpa a tabela
        ui.tableWidget.setColumnCount(4)  # Altera o número de colunas para 4
        ui.tableWidget.setHorizontalHeaderLabels(["EMAIL", "ENVIADO?", "RETORNO", "PRAZO RESTANTE"])  # Adiciona a nova coluna
        ui.tableWidget.setColumnWidth(0, 126)
        ui.tableWidget.setColumnWidth(1, 126)
        ui.tableWidget.setColumnWidth(2, 126)
        ui.tableWidget.setColumnWidth(3, 126)  # Define a largura da nova coluna

        pedidos_ref = ref.child("Pedidos").order_by_child("STATUS").equal_to("APROVADO")
        pedidos = pedidos_ref.get()

        ref_link_venda = db.reference(f"/Certificados/")
        lista_certificados = ref_link_venda.get()
        range_validacao = ui.campo_dias_renovacao.value()

        if not pedidos:
            self.mensagem_alerta("Erro", "Nenhum pedido encontrado para as datas selecionadas.")
            QApplication.processEvents()  # Atualiza a tela
            return

        total_pedidos = len(pedidos)
        progresso_atual = 0
        ui.barra_progresso_consulta.setMaximum(total_pedidos)
        QApplication.processEvents()  # Atualiza a barra de progresso

        nome = ui.campo_nome_agente.text()

        ui.barra_progresso_consulta.setVisible(True)
        ui.barra_progresso_consulta.setValue(0)
        data_atual = datetime.datetime.now()
        env = 0
        ne = 0
        erro = 0


        for pedido_info in pedidos.values():
            try:
                data_validade = datetime.datetime.strptime(pedido_info["VALIDO ATE"], "%Y-%m-%dT%H:%M:%SZ")
            except:
                erro += 1
                enviado = "❌"
                motivo = "LONGE DO VENCIMENTO"
                enviar_email = False
                
            data_atual = datetime.datetime.now()

            diferenca = (data_validade - data_atual).days
            if diferenca < 0:
                msg_diferenca = f'Venceu há {abs(diferenca)} dias'
            elif diferenca > 0:
                msg_diferenca = f'Restam {diferenca} dias'
            else:
                msg_diferenca = 'Vence hoje.'

            cliente_email = pedido_info["EMAIL"]
            data_formatada_validacao = banco_dados.iso_para_data(pedido_info["DATA"]).toString("dd/MM/yyyy")

            if not cliente_email:
                enviado = "❌"
                motivo = "SEM EMAIL CADASTRADO"
                ne += 1
                enviar_email = False
            elif not pedido_info["VERSAO"]:
                enviado = "❌"
                motivo = "LONGE DO VENCIMENTO"
                ne += 1
                enviar_email = False
            elif pedido_info["STATUS"] != "APROVADO":
                enviado = "❌"
                motivo = "PEDIDO NÃO APROVADO"
                ne += 1
                enviar_email = False
            elif -range_validacao <= diferenca <= range_validacao:
                enviado = "✅"
                motivo = "ENVIADO COM SUCESSO"
                env += 1
                enviar_email = True
            else:
                enviado = "❌"
                motivo = "FORA DO INTERVALO DE RENOVAÇÃO"
                ne += 1
                enviar_email = False

            # Adiciona os dados na QTableWidget
            row_position = ui.tableWidget.rowCount()
            ui.tableWidget.insertRow(row_position)

            # Configura a célula de "EMAIL"
            email_item = QTableWidgetItem(cliente_email)
            email_item.setTextAlignment(Qt.AlignCenter)
            ui.tableWidget.setItem(row_position, 0, email_item)

            # Configura a célula de "ENVIADO?"
            enviado_item = QTableWidgetItem(enviado)
            enviado_item.setTextAlignment(Qt.AlignCenter)
            ui.tableWidget.setItem(row_position, 1, enviado_item)

            # Configura a célula de "MOTIVO"
            motivo_item = QTableWidgetItem(motivo)
            motivo_item.setTextAlignment(Qt.AlignCenter)
            ui.tableWidget.setItem(row_position, 2, motivo_item)

            # Configura a célula de "PRAZO RESTANTE"
            prazo_item = QTableWidgetItem(str(msg_diferenca))  # Adiciona a variável 'diferenca' na nova coluna
            prazo_item.setTextAlignment(Qt.AlignCenter)
            ui.tableWidget.setItem(row_position, 3, prazo_item)

            # Atualiza a tela após cada adição
            QApplication.processEvents()

            if not enviar_email or pedido_info["VERSAO"] not in lista_certificados:
                progresso_atual += 1
                ui.barra_progresso_consulta.setValue(progresso_atual)
                QApplication.processEvents()  # Atualiza a barra de progresso
            else:
                link_venda_base = f'{lista_certificados[pedido_info["VERSAO"]]["LINK VENDA"]}{ui.campo_cod_rev.text()}'
                email = pedido_info["EMAIL"]
                assunto = f"Renovação Certificado Digital Certisign"

                if email:
                    remetente = ui.campo_email_empresa.text()
                    destinatarios = pedido_info['EMAIL']
                    senha = ui.campo_senha_email.text()
                    primeiro_nome = pedido_info['NOME'].split()[0]
                    link_venda = f"{link_venda_base}"

                    tamanho_fonte = "18px"
                    cor_botao_fundo = "rgb(89, 62, 255)"
                    cor_botao_texto = "#FFFFFF"
                    tamanho_fonte_footer = "12px"

                    corpo_html = (
                        f"<!DOCTYPE html>"
                        f"<html lang='pt-BR'>"
                        f"<head>"
                        f"<meta charset='UTF-8'>"
                        f"<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
                        f"<link href='https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Poppins:wght@400;700&display=swap' rel='stylesheet'>"
                        f"<style>"
                        f"  body {{ font-family: 'Montserrat', 'Poppins', Arial, sans-serif; color: #333333; margin: 0; padding: 0; background-color: #f7f7f7; text-align: center; font-size: {tamanho_fonte}; }} "
                        f"  .container {{ width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); text-align: center; }} "
                        f"  .header {{ background-color: #4E4BFF; color: white; padding: 20px; border-top-left-radius: 8px; border-top-right-radius: 8px; }} "
                        f"  .header h1 {{ margin: 0; font-size: 24px; color: white; font-family: 'Poppins', Arial, sans-serif; }} "
                        f"  .content {{ padding: 20px; text-align: center; }} "
                        f"  .content p {{ font-size: {tamanho_fonte}; line-height: 1.6; color: #333333; }} "
                        f"  .btn {{ display: inline-block; padding: 10px 20px; background-color: {cor_botao_fundo} !important; color: {cor_botao_texto} !important; text-decoration: none; border-radius: 5px; font-weight: bold; font-family: 'Montserrat', Arial, sans-serif; }} "
                        f"  .footer {{ background-color: #f1f1f1; text-align: center; padding: 10px; font-size: {tamanho_fonte_footer}; color: #888888; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; font-family: 'Poppins', Arial, sans-serif; }} "
                        f"  .align-left {{ text-align: left; font-size: 18px; }} "
                        f"</style>"
                        f"</head>"
                        f"<body>"
                        f"  <div class='container'>"
                        f"    <div class='header'>"
                        f"      <h1>Renovação do Certificado Digital Certisign</h1>"
                        f"    </div>"
                        f"    <div class='content'>"
                        f"      <p>Olá {primeiro_nome.capitalize()}, tudo bem?</p>"
                        f"      <p>Sou {nome}, agente de Registro da ACB Digital.</p>"
                        f"      <p>Fizemos a validação para seu certificado digital, modelo"
                        f"      <p><b>{pedido_info['VERSAO']}</b> no dia <b>{data_formatada_validacao}</b>.</p>"
                        f"      <p>Verifiquei que ele está próximo ao <b>vencimento</b> e entendemos a importância do certificado digital para seus negócios.</p>"
                        f"      <p>Desse modo, oferecemos a renovação através do botão abaixo.</p>"
                        f"      <p><a href='{link_venda}' class='btn'>RENOVAR AGORA</a></p>"
                        f"      <p>Caso queira fazer a vídeo conferência, contate-me através do email:</p>"
                        f"      <p><b>{ui.campo_email_empresa.text()}</b></p>"
                        f"      <p>Agradecemos pela confiança em nossos serviços e estamos à disposição para ajudá-lo!</p>"
                        f"      <br>" 
                        f"      <p>Atenciosamente,</p>"
                        f"      <p>{nome}</p>"
                        f"    </div>"
                        f"    <div class='footer'>"
                        f"      <p>ACB Serviços e Negócios &copy; 2024. Todos os direitos reservados.</p>"
                        f"    </div>"
                        f"  </div>"
                        f"</body>"
                        f"</html>"
                    )

                    try:
                        QApplication.processEvents() 
                        msg = MIMEMultipart("alternative")
                        msg['Subject'] = assunto
                        msg['From'] = remetente
                        msg['To'] = destinatarios
                        parte_html = MIMEText(corpo_html, "html")
                        msg.attach(parte_html)

                        with smtplib.SMTP_SSL('email-ssl.com.br', 465) as smtp_server:
                            smtp_server.login(remetente, senha)
                            smtp_server.sendmail(remetente, destinatarios, msg.as_string())

                        progresso_atual += 1
                        ui.barra_progresso_consulta.setValue(progresso_atual)
                        QApplication.processEvents()  # Atualiza a barra de progresso

                    except smtplib.SMTPException as e:
                        ui.barra_progresso_consulta.setVisible(False)
                        QApplication.processEvents()  # Atualiza a barra de progresso
        QApplication.processEvents() 
        ui.barra_progresso_consulta.setVisible(False)
        ui.campo_relatorio.setPlainText(f"Processo finalizado!\nEnviados: {env}\nNão enviado: {ne}\nErro: {erro}")


    

 



class Acoes_banco_de_dados:
    def __init__(self,ui):
        self.ui = ui
        self.ref = db.reference("/Pedidos")
    
    def salvar_pedido(self):
        # Analisa se os campos do pedido estão preenchidos
        try:
            if not self.analise_de_campos():
                return

            if not self.mensagem_confirmacao("Confirmação", f"Salvar pedido como {banco_dados.alteracao_status()}?"):
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
                        self.mensagem_alerta("Sucesso","Pedido salvo!") 
                        self.contar_verificacao()
                        self.limpar_campos_pedido()

                    #Pedido existente + gravado temporariamente
                    case 'TEMPORARIO':
                        novo_pedido_ref.update(self.dicionario_banco_de_dados())
                        self.ui.campo_status_bd.setText("✅")
                        self.ui.campo_status_bd.setToolTip("Pedido Atualizado")
                        #self.mensagem_alerta("Sucesso","Pedido salvo!")
                        self.contar_verificacao()
                        
            
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
                        self.contar_verificacao()

                    #Pedido existente + gravado temporariamente
                    case 'TEMPORARIO':

                        novo_pedido_ref.set(self.dicionario_banco_de_dados())
                        self.ui.campo_status_bd.setText("✅")
                        self.ui.campo_status_bd.setToolTip("Pedido Atualizado")
                        #self.mensagem_alerta("Sucesso","Pedido salvo!")
                        self.contar_verificacao()
                        
        except Exception as e:
            print(e)
            #self.mensagem_alerta("Erro","Não foi possível salvar os dados. Tente novamente.")
        
    def mensagem_confirmacao(self,titulo,mensagem):
        resposta = QMessageBox.question(ui.centralwidget, titulo, mensagem, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resposta == QMessageBox.Yes:
            return True
        else:
            return False

    def mensagem_alerta(self,titulo,mensagem):
        QMessageBox.information(ui.centralwidget, titulo, mensagem, QMessageBox.Ok)

    def verificar_status(self):       
        for radiobutton in ui.groupBox_status.findChildren(QRadioButton):
            if radiobutton.isChecked():
                if radiobutton.text() == "APROVADO" or radiobutton.text() == "CANCELADO":
                    return "DEFINITIVO"
                else:
                    return "TEMPORARIO"
               
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
            ui.rb_digitacao.setChecked(True)
            self.zerar_cor()
            ui.tableWidget.horizontalHeader().setDefaultSectionSize(70)
            ui.caminho_pasta.setText("")
            ui.campo_cnpj_municipio.setText("")
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
            ui.campo_lista_junta_comercial.setCurrentText("")
            ui.label_quantidade_bd.setText("")
            ui.tableWidget.setRowCount(0)
            ui.campo_data_nascimento.setDate(QDate(2000, 1, 1))
            ui.campo_pedido.setReadOnly(False)
            ui.campo_pedido.setText("")
            ui.campo_data_agendamento.setDate(QDate(2000, 1, 1))
            ui.campo_hora_agendamento.setTime(QTime.fromString('00:00', "hh:mm"))
            ui.campo_lista_venda.setCurrentText("NAO")
            ui.campo_lista_modalidade.setCurrentText("")
            ui.label_confirmacao_converter_pdf.setText("")
            ui.label_confirmacao_criar_pasta.setText("")
            ui.label_confirmacao_tirar_print.setText("")
            ui.label_confirmacao_mesclar_pdf.setText("")
            ui.campo_lista_versao_certificado.setCurrentText("")
            ui.campo_status_bd.setText("")
            ui.campo_preco_certificado.setText("")
            ui.campo_cnpj_razao_social.setText("")
            ui.campo_rg_orgao.setText("")
            ui.campo_lista_junta_comercial.setCurrentText("SP")
            ui.tabela_documentos.clearContents()
            ui.tabela_documentos.setRowCount(0)
            ui.campo_pis.setText("")
            ui.campo_telefone.setText("")
            ui.campo_oab.setText("")
            ui.campo_relatorio.setPlainText("")
            ui.campo_preco_certificado_cheio.setText("")
            for col in range(ui.tableWidget.columnCount()):
                ui.tableWidget.setColumnHidden(col, False)
            ui.tableWidget.setRowCount(0)
            ui.tableWidget.setColumnCount(6)
            ui.tableWidget.setHorizontalHeaderLabels(["STATUS", "PEDIDO", "DATA", "HORA", "NOME", "VERSAO"])
            for col in range(ui.tableWidget.columnCount()):
                    ui.tableWidget.setColumnWidth(col, 83)


           
        except Exception as e:
            print(e)

    def apagar_campos_pedido(self):
        if not self.mensagem_confirmacao("","Apagar dados?"):
            return
        try:
            #Dados pedido  
            ui.tableWidget.horizontalHeader().setDefaultSectionSize(70)
            ui.caminho_pasta.setText("")
            ui.campo_cnpj_municipio.setText("")
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
            ui.campo_lista_junta_comercial.setCurrentText("")
            ui.label_quantidade_bd.setText("")
            ui.tableWidget.setRowCount(0)
            ui.campo_data_nascimento.setDate(QDate(2000, 1, 1))
            ui.campo_pedido.setReadOnly(False)
            ui.campo_pedido.setText("")
            ui.campo_data_agendamento.setDate(QDate(2000, 1, 1))
            ui.campo_hora_agendamento.setTime(QTime.fromString('00:00', "hh:mm"))
            ui.campo_lista_venda.setCurrentText("NAO")
            ui.campo_lista_modalidade.setCurrentText("")
            ui.campo_lista_versao_certificado.setCurrentText("")
            ui.campo_preco_certificado.setText("")
            ui.campo_cnpj_razao_social.setText("")
            ui.campo_rg_orgao.setText("")
            ui.campo_lista_junta_comercial.setCurrentText("SP")
            ui.tabela_documentos.clearContents()
            ui.tabela_documentos.setRowCount(0)
            ui.campo_pis.setText("")
            ui.campo_telefone.setText("")
            ui.campo_oab.setText("")
            ui.campo_relatorio.setPlainText("")
            ui.campo_preco_certificado_cheio.setText("")
            for col in range(ui.tableWidget.columnCount()):
                ui.tableWidget.setColumnHidden(col, False)
            ui.tableWidget.setRowCount(0)
            ui.tableWidget.setColumnCount(6)
            ui.tableWidget.setHorizontalHeaderLabels(["STATUS", "PEDIDO", "DATA", "HORA", "NOME", "VERSAO"])
            for col in range(ui.tableWidget.columnCount()):
                    ui.tableWidget.setColumnWidth(col, 83)


            self.limpar_labels()
            self.contar_verificacao()
        except Exception as e:
            print(e)

    def limpar_labels(self):
        self.zerar_cor()
        ui.rb_digitacao.setChecked(True)
        ui.campo_status_bd.setText("")
        ui.label_confirmacao_converter_pdf.setText("")
        ui.label_confirmacao_criar_pasta.setText("")
        ui.label_confirmacao_mesclar_pdf.setText("")
        ui.label_confirmacao_tirar_print.setText("")
         
    def dicionario_banco_de_dados(self):
        data_validacao = datetime.datetime.strptime(ui.campo_data_agendamento.date().toString("yyyy-MM-dd"), "%Y-%m-%d")
        certificado_12 = data_validacao + datetime.timedelta(days=365)
        certificado_18 = data_validacao + datetime.timedelta(days=540)
        certificado_24 = data_validacao + datetime.timedelta(days=720)
        certificado_36 = data_validacao + datetime.timedelta(days=1080)

        # Duração do certificado em meses (pode ser 12, 18, 24, 36 meses)
        certificado = ui.campo_lista_versao_certificado.currentText()
        if "12" in certificado:
            duracao_certificado = certificado_12
        elif "18" in certificado:
            duracao_certificado = certificado_18
        elif "24" in certificado:
            duracao_certificado = certificado_24
        elif "36" in certificado:
            duracao_certificado = certificado_36
     
        novos_dados = {
                    "PASTA":ui.caminho_pasta.text(),
                    "MUNICIPIO": ui.campo_cnpj_municipio.text(),
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
                    "STATUS":self.alteracao_status(),
                    "PEDIDO":ui.campo_pedido.text() , 
                    "DATA": self.data_para_iso(QDateTime(ui.campo_data_agendamento.date())),
                    "HORA":ui.campo_hora_agendamento.text(),
                    "VENDA":ui.campo_lista_venda.currentText(),
                    "MODALIDADE":ui.campo_lista_modalidade.currentText(),
                    "VERSAO":ui.campo_lista_versao_certificado.currentText(),
                    "PRECO":ui.campo_preco_certificado.text(),
                    "RAZAO SOCIAL":ui.campo_cnpj_razao_social.text(),
                    "ORGAO RG":ui.campo_rg_orgao.text(),
                    "PIS":ui.campo_pis.text(),
                    "TELEFONE":ui.campo_telefone.text(),
                    "OAB":ui.campo_oab.text(),
                    "VALIDO ATE":""
                    }
        
        if self.verificar_status() == "DEFINITIVO":
            novos_dados.update({
                    "PASTA": None,
                    "MUNICIPIO": None,
                    "CODIGO DE SEG CNH": None,
                    "RG": None,
                    "CPF": None,
                    "CNH": None,
                    "MAE": None,
                    "CNPJ": None,
                    "NASCIMENTO": None,
                    "RAZAO SOCIAL": None,
                    "ORGAO RG": None,
                    "PIS": None,
                    "OAB": None,
                    "VALIDO ATE":duracao_certificado.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    })

        return novos_dados

    def forcar_fechamento_de_arquivo_e_deletar_pasta(self, folder_path):
        for _ in range(3):  # Tentar até três vezes
            try:
                send2trash.send2trash(folder_path)  # Tentar mover para a lixeira
                self.mensagem_alerta(" ", "Pasta movida para a lixeira")
                break
            except PermissionError as e:
                # Se a exclusão falhar devido a permissões, tenta fechar os arquivos em uso antes da próxima tentativa
                self.fechar_arquivo_em_uso(folder_path)
            except OSError as e:
                # Captura erros de sistema operacional, como o WinError específico
                if e.winerror == -2144927704:
                    self.fechar_arquivo_em_uso(folder_path)  # Tentar fechar arquivos novamente
                else:
                    self.mensagem_alerta(" ", f"Erro inesperado: {e}")
                    break
            except Exception as e:
                if not os.path.exists(folder_path):  # Verifica se a pasta não existe
                    break
                self.mensagem_alerta(" ", f"Erro ao mover pasta do cliente para a lixeira: {e}")
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

    def preencher_status(self,status):
        match status:
            case "APROVADO":
                ui.rb_aprovado.setChecked(True)
                self.alteracao_status()
            case "CANCELADO":
                ui.rb_cancelado.setChecked(True)
                self.alteracao_status()
            case "VERIFICAÇÃO":
                ui.rb_verificacao.setChecked(True)
                self.alteracao_status()
            case "DIGITACÃO":
                ui.rb_digitacao.setChecked(True)
                self.alteracao_status()
            case "VIDEO REALIZADA":
                ui.rb_videook.setChecked(True)
                self.alteracao_status()

    def preencher_dados(self,pedido_data):
        #CORRIGIDO------------------------------------------------------------
        #self.limpar_campos_pedido()
        try:
            status = pedido_data.get("STATUS")
            self.preencher_status(status)    
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
            ui.campo_data_agendamento.setDate(self.iso_para_data(pedido_data.get("DATA")).date())
            ui.campo_hora_agendamento.setTime(QTime.fromString(pedido_data.get("HORA"), "hh:mm"))
            ui.campo_lista_venda.setCurrentText("NAO")
            ui.campo_lista_venda.setCurrentText(pedido_data.get("VENDA"))
            ui.campo_lista_modalidade.setCurrentText(pedido_data.get("MODALIDADE"))
            ui.campo_pedido.setReadOnly(True)
            ui.campo_seguranca_cnh.setText(pedido_data.get("CODIGO DE SEG CNH"))
            ui.campo_nome_mae.setText(pedido_data.get("MAE"))
            ui.campo_comentario.setText(pedido_data.get("DIRETORIO"))
            ui.campo_cnpj_municipio.setText(pedido_data.get("MUNICIPIO"))
            ui.caminho_pasta.setText(pedido_data.get("PASTA"))
            try:
                ui.campo_lista_versao_certificado.setCurrentText(pedido_data.get("VERSAO"))
            except:
                pass
            try:
                ui.campo_rg_orgao.setText(pedido_data.get("ORGAO RG"))
            except:
                pass
            try:
                ui.campo_cnpj_razao_social.setText(pedido_data.get("RAZAO SOCIAL"))
            except:
                pass
            try:
                ui.campo_pis.setText(pedido_data.get("PIS"))
            except:
                pass
            try:
                ui.campo_preco_certificado.setText(pedido_data.get("PRECO"))
            except:
                pass
            try:
                ui.campo_telefone.setText(pedido_data.get("TELEFONE"))
            except:
                pass
            try:
                ui.campo_oab.setText(pedido_data.get("OAB"))
            except:
                pass
            
            ui.campo_status_bd.setText("✅")
            ui.campo_status_bd.setToolTip("Pedido Atualizado")
            pasta = ui.caminho_pasta.text()

            if pasta != "": 
                ui.label_confirmacao_criar_pasta.setText("✅")

            
        except Exception as e:
            print(e)
            pass

    def contar_verificacao(self):
        # Consulta no Firebase para pedidos com status "VERIFICAÇÃO"
        pedidos_verificacao = ref.child("Pedidos").order_by_child("STATUS").equal_to("VERIFICAÇÃO").get()
        # Consulta no Firebase para pedidos com status "VIDEO REALIZADA"
        pedidos_videook = ref.child("Pedidos").order_by_child("STATUS").equal_to("VIDEO REALIZADA").get()

        quantidade_verificacao = 0  # Contador de pedidos com status "VERIFICAÇÃO"
        quantidade_videook = 0  # Contador de pedidos com status "VIDEO REALIZADA"
        verificacao_info = []  # Variável para armazenar a data e o número do pedido de verificação
        videook_info = []  # Variável para armazenar a data e o número do pedido de video realizada

        if pedidos_verificacao:
            for pedido_info in pedidos_verificacao.values():
                quantidade_verificacao += 1
                data_pedido = datetime.datetime.strptime(pedido_info['DATA'], "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y")
                numero_pedido = pedido_info['PEDIDO']
                verificacao_info.append(f"Pedido: {numero_pedido} / Data: {data_pedido}")

        if pedidos_videook:
            for pedido_info in pedidos_videook.values():
                quantidade_videook += 1
                data_pedido = pedido_info['DATA']
                numero_pedido = pedido_info['PEDIDO']
                videook_info.append(f"Pedido: {numero_pedido} / Data: {data_pedido}")

        # Adiciona o setToolTip no ícone campo_status_bd_3
        tooltip_verificacao = f"Quantidade de pedidos em verificação:\n\n"
        tooltip_verificacao += '\n'.join(verificacao_info)
        ui.campo_status_verificacao.setToolTip(f'<div style="color:white; background-color:black;">{tooltip_verificacao}</div>')
        ui.campo_status_verificacao.setToolTip(tooltip_verificacao)

        tooltip_videook = f"Quantidade de pedidos com vídeo realizada:\n\n"
        tooltip_videook += '\n'.join(videook_info)
        ui.campo_status_videook.setToolTip(f'<div style="color:white; background-color:black;">{tooltip_videook}</div>')
        ui.campo_status_videook.setToolTip(tooltip_videook)

        ui.campo_status_verificacao.setText(str(quantidade_verificacao))
        ui.campo_status_videook.setText(str(quantidade_videook))

    def preencher_tabela(self):
        # Convertendo as datas do QDateEdit para QDateTime e, em seguida, para o formato ISO
        data_inicial = self.data_para_iso(QDateTime(ui.campo_data_de.date()))
        data_final = self.data_para_iso(QDateTime(ui.campo_data_ate.date()))

        # Consulte o banco de dados usando as datas no formato ISO
        pedidos_ref = ref.child("Pedidos").order_by_child("DATA") \
                        .start_at(data_inicial) \
                        .end_at(data_final)
        pedidos = pedidos_ref.get()

        for col in range(ui.tableWidget.columnCount()):
            ui.tableWidget.setColumnHidden(col, False)
        ui.tableWidget.setRowCount(0)
        ui.tableWidget.setColumnCount(6)
        ui.tableWidget.setHorizontalHeaderLabels(["STATUS", "PEDIDO", "DATA", "HORA", "NOME", "VERSAO"])
        for col in range(ui.tableWidget.columnCount()):
                ui.tableWidget.setColumnWidth(col, 83)


        valor_estimado = 0
        try:
            pedidos = sorted(pedidos.values(), key=lambda x: (datetime.datetime.strptime(x['DATA'], "%Y-%m-%dT%H:%M:%SZ"), 
                                                            datetime.datetime.strptime(x['HORA'], "%H:%M")))

            numero_inteiro_inicial = datetime.datetime.strptime(data_inicial, "%Y-%m-%dT%H:%M:%SZ").toordinal()
            numero_inteiro_final = datetime.datetime.strptime(data_final, "%Y-%m-%dT%H:%M:%SZ").toordinal()

            valor_cnpj = 0
            valor_cpf = 0
            x = 0
            y = 0
            j = 0
            f = 0
            venda = 0
            total_pedidos = len(pedidos)
            for col in range(ui.tableWidget.columnCount()):
                ui.tableWidget.setColumnWidth(col, 83)
            ui.barra_progresso_consulta.setVisible(False)
            
            # Configura a barra de progresso corretamente
            ui.barra_progresso_consulta.setVisible(True)
            ui.barra_progresso_consulta.setMaximum(total_pedidos)  # Máximo é o total de pedidos
            ui.barra_progresso_consulta.setValue(0)
            
            status_filtro = ui.campo_lista_status_2.currentText()
            
            for pedido_info in pedidos:
                data_bd = datetime.datetime.strptime(pedido_info['DATA'], "%Y-%m-%dT%H:%M:%SZ")
                numero_inteiro_bd = data_bd.toordinal()
                status_servidor = pedido_info['STATUS']
                
                if numero_inteiro_inicial <= numero_inteiro_bd <= numero_inteiro_final:
                    if status_filtro == status_servidor or status_filtro == "TODAS":
                        x += 1
                        row_position = ui.tableWidget.rowCount()
                        ui.tableWidget.insertRow(row_position)
                        try:
                            ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(pedido_info['STATUS']))
                        except:
                            ui.tableWidget.setItem(row_position, 0, QTableWidgetItem("-"))
                        try:
                            ui.tableWidget.setItem(row_position, 1, QTableWidgetItem(pedido_info['PEDIDO']))
                        except:
                            ui.tableWidget.setItem(row_position, 1, QTableWidgetItem("-"))
                        try:
                            ui.tableWidget.setItem(row_position, 2, QTableWidgetItem(datetime.datetime.strptime(pedido_info['DATA'], "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y")))
                        except:
                            ui.tableWidget.setItem(row_position, 2, QTableWidgetItem("-"))
                        try:
                            ui.tableWidget.setItem(row_position, 3, QTableWidgetItem(pedido_info['HORA']))
                        except:
                            ui.tableWidget.setItem(row_position, 3, QTableWidgetItem("-"))
                        try:
                            ui.tableWidget.setItem(row_position, 4, QTableWidgetItem(pedido_info['NOME']))
                        except:
                            ui.tableWidget.setItem(row_position, 4, QTableWidgetItem("-"))
                        try:
                            ui.tableWidget.setItem(row_position, 5, QTableWidgetItem(pedido_info['VERSAO']))
                        except:
                            ui.tableWidget.setItem(row_position, 5, QTableWidgetItem("-"))

                        try:
                            if 'PRECO' in pedido_info:
                                preco = float(pedido_info['PRECO'])
                                valor_estimado += preco

                                if 'e-CNPJ' in pedido_info['VERSAO']:
                                    valor_cnpj += preco
                                    j += 1
                                elif 'e-CPF' in pedido_info['VERSAO']:
                                    valor_cpf += preco
                                    f += 1
                                if pedido_info['VENDA'] == "SIM":
                                    venda += 1
                            QApplication.processEvents()
                        except ValueError:
                            pass

                        for col in range(ui.tableWidget.columnCount()):
                            item = ui.tableWidget.item(row_position, col)
                            status = ui.tableWidget.item(row_position, 0).text()
                            if item is not None:
                                match status:
                                    case 'DIGITAÇÃO':
                                        item.setForeground(QColor(113, 66, 230))
                                    case 'VIDEO REALIZADA':
                                        item.setForeground(QColor(25, 200, 255))
                                    case 'VERIFICAÇÃO':
                                        item.setForeground(QColor(255, 167, 91))
                                    case 'APROVADO':
                                        item.setForeground(QColor(173, 255, 47))
                                    case 'CANCELADO':
                                        item.setForeground(QColor(255, 30, 30))

                        y += 1
                        # Atualiza a barra de progresso de acordo com o total de pedidos
                        ui.barra_progresso_consulta.setValue(y)
                        QApplication.processEvents()

            ui.barra_progresso_consulta.setValue(total_pedidos)  # Finaliza a barra de progresso no valor máximo
            self.contar_verificacao()

            total_venda = valor_cnpj + valor_cpf
            ui.campo_relatorio.setPlainText(f'''(+)e-CNPJ [{j}].......R$ {valor_cnpj:.2f}
(+)e-CPF [{f}].........R$ {valor_cpf:.2f}
(=)Total [{j+f}].........R$ {total_venda:.2f}
(-) {ui.campo_desconto.text()}%..................R$ {total_venda * (float(ui.campo_desconto.text()) / 100):.2f}
-----------------------------------
(=)Total Esperado....R$ {total_venda * (1 - float(ui.campo_desconto.text()) / 100):.2f}
Vendas.........{venda}
''')

            ui.barra_progresso_consulta.setVisible(False)
            ui.label_quantidade_bd.setText(f"{x} registro(s)")
            ui.tableWidget.setHorizontalHeaderLabels(["STATUS", "PEDIDO", "DATA", "HORA", "NOME", "VERSAO"])
            
        except Exception as e:
            print(e)
            ui.campo_relatorio.setPlainText("")
            ui.tableWidget.setHorizontalHeaderLabels(["STATUS", "PEDIDO", "DATA", "HORA", "NOME", "VERSAO"])
            for col in range(ui.tableWidget.columnCount()):
                ui.tableWidget.setColumnWidth(col, 83)
            ui.label_quantidade_bd.setText(f"{x} registro(s)")
            ui.barra_progresso_consulta.setVisible(False)
            self.contar_verificacao()
 
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

    def alteracao_status(self):      
        #AQUI VAI VERIFICAR SE
        if ui.rb_digitacao.isChecked():
            self.zerar_cor()
            ui.rb_digitacao.setStyleSheet("border:none;color:rgb(113,66,230);")  # Cor verde para rb_digitacao

            return 'DIGITAÇÃO'
        elif ui.rb_videook.isChecked():
            self.zerar_cor()
            ui.rb_videook.setStyleSheet("border:none;color: rgb(18,191,255);")  # Cor vermelha para rb_videook
            return 'VIDEO REALIZADA'
        elif ui.rb_verificacao.isChecked():
            self.zerar_cor()
            ui.rb_verificacao.setStyleSheet("border:none;color: orange;")  # Cor azul para rb_verificacao
            return 'VERIFICAÇÃO'
        elif ui.rb_aprovado.isChecked():
            self.zerar_cor()
            ui.rb_aprovado.setStyleSheet("border:none;color:rgb(173, 255, 47);")  # Cor laranja para rb_aprovado
            return 'APROVADO'
        elif ui.rb_cancelado.isChecked():
            self.zerar_cor()
            ui.rb_cancelado.setStyleSheet("border:none;color: red;")  # Cor amarela para rb_cancelado
            return 'CANCELADO'
        
    def zerar_cor(self):
        
        ui.rb_digitacao.setStyleSheet("border:none; color:rgb(170,170,170);")  # Cor verde para rb_digitacao
        ui.rb_videook.setStyleSheet("border:none; color:rgb(170,170,170);")
        ui.rb_verificacao.setStyleSheet("border:none; color:rgb(170,170,170);")
        ui.rb_aprovado.setStyleSheet("border:none; color:rgb(170,170,170);")
        ui.rb_cancelado.setStyleSheet("border:none; color:rgb(170,170,170);")

    def iso_para_data(self,data):
        dt = datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%SZ")
        qdt = QDateTime(dt)
        return qdt

    def data_para_iso(self,data):
        dt = data.toPyDateTime()
        iso_str = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        return iso_str




class JanelaOculta:
    def __init__(self, parent):
        self.parent = parent
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_window_size)
        self.animation_step = 5  # Ajustei para diminuir a animação
        self.animation_duration = 2  # Duração da animação em milissegundos
        self.animation_target_width = 0
        self.animation_target_height = 0
        self.janela = Funcoes_padrao(ui)

    def enterEvent(self, event):
        self.animate_window_resize(525, 683)
        self.janela.atualizar_documentos_tabela()

    def leaveEvent(self, event):
        self.janela.atualizar_documentos_tabela()
        if not ui.campo_verifica_tela_cheia.text()=="SIM":
            cursor_pos = QtGui.QCursor.pos()
            window_pos = self.parent.mapToGlobal(QtCore.QPoint(0, 0))
            window_rect = QRect(window_pos, self.parent.size())

            mouse_dentro_da_janela = window_rect.contains(cursor_pos)

            if not mouse_dentro_da_janela:
                if int(ui.campo_status_videook.text()) == 0 and int(ui.campo_status_verificacao.text()) == 0:
                    self.animate_window_resize(104, 53)
                else:
                    self.animate_window_resize(143, 53)
        
    def mousePressEvent(self, event):
        self.animate_window_resize(525,683)#469

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
ui.campo_nome.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_nome))
ui.campo_cnpj_municipio.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_cnpj_municipio))
ui.caminho_pasta_principal.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.caminho_pasta_principal))
ui.caminho_pasta.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.caminho_pasta))
ui.campo_cnpj.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_cnpj))
ui.campo_cpf.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_cpf))
ui.campo_nome_mae.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_nome_mae))
ui.campo_cnh.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_cnh))
ui.campo_lista_modalidade.currentIndexChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_lista_modalidade))
ui.campo_lista_venda.currentIndexChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_lista_venda))
ui.campo_hora_agendamento.timeChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_hora_agendamento))
ui.campo_data_agendamento.dateChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_data_agendamento))
ui.campo_email.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_email))
ui.campo_rg.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_rg))
ui.campo_seguranca_cnh.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_seguranca_cnh))
ui.campo_comentario.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_comentario))
ui.campo_data_nascimento.dateChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_data_nascimento))
ui.campo_lista_versao_certificado.currentIndexChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_lista_versao_certificado))
ui.campo_pis.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_comentario))
ui.campo_telefone.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_telefone))
ui.campo_preco_certificado.editingFinished.connect(lambda:funcoes_app.formatar_preco_certificado())
ui.campo_oab.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_oab))
ui.rb_aprovado.toggled.connect(lambda:funcoes_app.valor_alterado(ui.rb_aprovado))
ui.rb_cancelado.toggled.connect(lambda:funcoes_app.valor_alterado(ui.rb_cancelado))
ui.rb_digitacao.toggled.connect(lambda:funcoes_app.valor_alterado(ui.rb_digitacao))
ui.rb_verificacao.toggled.connect(lambda:funcoes_app.valor_alterado(ui.rb_verificacao))
ui.rb_videook.toggled.connect(lambda:funcoes_app.valor_alterado(ui.rb_videook))

#Campos botões
ui.botao_duplicar_pedido.clicked.connect(lambda:funcoes_app.duplicar_pedido())
ui.botao_atualizar_meta.clicked.connect(lambda:funcoes_app.Atualizar_meta())
ui.botao_atualizar_configuracoes.clicked.connect(lambda:funcoes_app.atualizar_configuracoes())
ui.botao_consultar.clicked.connect(lambda:banco_dados.preencher_tabela())
ui.botao_excluir_dados.clicked.connect(lambda:banco_dados.apagar_campos_pedido())
ui.botao_procurar.clicked.connect(lambda:funcoes_app.exportar_excel())
ui.botao_consulta_cnpj.clicked.connect(lambda:funcoes_app.procurar_cnpj())
ui.botao_consulta_cpf.clicked.connect(lambda:funcoes_app.procurar_cpf())
ui.botao_consulta_cnh.clicked.connect(lambda:funcoes_app.procurar_cnh())
ui.botao_consulta_rg.clicked.connect(lambda:funcoes_app.procurar_rg())
ui.botao_salvar.clicked.connect(lambda:banco_dados.salvar_pedido())
ui.botao_junta.clicked.connect(lambda:funcoes_app.procurar_junta())
ui.botao_print_direto_na_pasta.clicked.connect(lambda:funcoes_app.print_tela())
ui.botao_print_direto_na_pasta.setFlat(True)
ui.botao_pasta_cliente.clicked.connect(lambda:funcoes_app.criar_pasta_cliente())
ui.botao_tela_cheia.clicked.connect(lambda: funcoes_app.manter_tela_aberta())
ui.botao_tela_cheia.setFlat(True)
ui.botao_converter_todas_imagens_em_pdf.clicked.connect(lambda:funcoes_app.converter_todas_imagens_para_pdf())
ui.botao_converter_todas_imagens_em_pdf.setFlat(True)
ui.botao_agrupar_PDF.setFlat(True)
ui.botao_agrupar_PDF.clicked.connect(lambda:funcoes_app.mesclar_pdf())
ui.botao_dados_cnpj.clicked.connect(lambda:funcoes_app.dados_cnpj())
ui.botao_altera_pasta_principal.clicked.connect(lambda: funcoes_app.atualizar_diretorio_raiz())
ui.botao_definir_cor.clicked.connect(lambda:funcoes_app.definir_cor())
ui.botao_menagem.clicked.connect(lambda:funcoes_app.abrir_janela_mensagem())
ui.botao_consulta_pis.clicked.connect(lambda:funcoes_app.procurar_pis())
ui.botao_hoje.clicked.connect((lambda:funcoes_app.definir_hoje()))
ui.botao_telefone.clicked.connect((lambda:funcoes_app.contato_telefone()))
ui.botao_consulta_oab.clicked.connect((lambda:funcoes_app.procurar_oab()))
ui.botao_enviar_email.clicked.connect((lambda:funcoes_app.envio_de_email()))
ui.rb_aprovado.clicked.connect(lambda:banco_dados.alteracao_status())
ui.rb_cancelado.clicked.connect(lambda:banco_dados.alteracao_status())
ui.rb_videook.clicked.connect(lambda:banco_dados.alteracao_status())
ui.rb_verificacao.clicked.connect(lambda:banco_dados.alteracao_status())
ui.rb_digitacao.clicked.connect(lambda:banco_dados.alteracao_status())
ui.botao_ocultar_senha.clicked.connect(lambda:funcoes_app.mostrar_senha())
ui.botao_link_venda.clicked.connect(lambda:funcoes_app.pegar_link_venda())
ui.botao_envio_massa.clicked.connect(lambda:funcoes_app.envio_em_massa())

#Campos de formatação
ui.campo_cnpj_municipio.setReadOnly(True)
ui.caminho_pasta_principal.setReadOnly(True)
ui.campo_relatorio.setReadOnly(True)
ui.caminho_pasta.setReadOnly(True)
ui.campo_verifica_tela_cheia.setReadOnly(True)
ui.campo_cpf.editingFinished.connect(lambda:funcoes_app.formatar_cpf())
ui.campo_rg_orgao.editingFinished.connect(lambda:funcoes_app.formatar_orgao_rg())
ui.campo_pedido.editingFinished.connect(lambda:banco_dados.carregar_dados()) ##########################################################################
ui.campo_cnpj.editingFinished.connect (lambda:funcoes_app.formatar_cnpj())
ui.campo_meta_semanal.valueChanged.connect(lambda:funcoes_app.atualizar_meta_clientes())
ui.campo_meta_mes.valueChanged.connect(lambda:funcoes_app.atualizar_meta_clientes())
ui.campo_data_meta.dateChanged.connect(lambda:funcoes_app.atualizar_meta_clientes())
ui.campo_nome.editingFinished.connect(lambda:funcoes_app.formatar_nome())
ui.campo_nome.setContextMenuPolicy(Qt.NoContextMenu)
ui.campo_nome_mae.editingFinished.connect(lambda:funcoes_app.formatar_nome_mae())
ui.campo_data_de.setDate(QDate.currentDate())
ui.campo_data_ate.setDate(QDate.currentDate())

#Eventos
ui.campo_cnh.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_cnh")
ui.campo_cnpj.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_cnpj")
ui.campo_pedido.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_pedido") #*************************************************************
ui.campo_cpf.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_cpf")
ui.campo_seguranca_cnh.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_seguranca_cnh")
ui.campo_rg.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_rg")
ui.campo_nome_mae.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_nome_mae")
ui.campo_nome.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_nome")
ui.campo_pis.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_pis")
ui.campo_telefone.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_telefone")
ui.campo_oab.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_oab")
ui.campo_preco_certificado.setReadOnly(False)
ui.campo_cnpj_razao_social.setReadOnly(True)
ui.campo_preco_certificado_cheio.setReadOnly(True)
ui.tabela_documentos.setEditTriggers(QTableWidget.NoEditTriggers)

#ToolTip
ui.botao_duplicar_pedido.setToolTip('Duplicar pedido')
ui.campo_status_bd_2.setToolTip("Status dos dados no servidor\n✅ - Pedido atualizado no servidor\n❌ - Pedido desatualizado no servidor")
ui.botao_converter_todas_imagens_em_pdf.setToolTip("Conversor de JPG/PDF")
ui.botao_agrupar_PDF.setToolTip("Mesclar PDF")
ui.botao_print_direto_na_pasta.setToolTip("Tira um print da tela")
ui.botao_tela_cheia.setToolTip("Liga/Desliga a tela cheia")
ui.botao_menagem.setToolTip("Mensagens")
ui.botao_enviar_email.setToolTip("Enviar e-mail para cliente")
ui.campo_status_bd_3.setToolTip("Quantidade de pedidos AGUARDANDO intervenção")

#Validador
regex = QRegExp("[0-9.]*")
validator = QRegExpValidator(regex)
ui.campo_pedido.setValidator(validator)
ui.campo_cpf.setValidator(validator)
ui.campo_cnpj.setValidator(validator)
ui.campo_preco_certificado.setValidator(validator)


#Eventos tabela
ui.tabWidget.currentChanged.connect(lambda: funcoes_app.atualizar_aba())
ui.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
ui.tableWidget.itemDoubleClicked.connect(lambda:banco_dados.pegar_valor_tabela())
ui.tableWidget.itemClicked.connect(lambda:funcoes_app.copiar_pedido_tabela(None))
ui.tabela_documentos.itemDoubleClicked.connect(lambda: funcoes_app.abrir_documento_para_edicao())


ui.barra_progresso_consulta.setVisible(False)

screen_rect = desktop.screenGeometry(desktop.primaryScreen())
ui.campo_senha_email.setEchoMode(QLineEdit.Password)


x = screen_rect.width() - janela.width() - 20
y = (screen_rect.height() - janela.height()) // 5


janela.move(x, y)
janela.setWindowTitle("Auxiliar")
janela.setFixedSize(143, 53)           
janela.show()


sys.exit(app.exec_())