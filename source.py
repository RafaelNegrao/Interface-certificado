import os
import psutil
import shutil
import datetime
import pandas as pd
import tkinter as tk
import time
import requests
import PyPDF2
import fitz
import pyautogui
import sys
import subprocess
import math
import pyperclip
import numpy as np
import mplcursors
import calendar  
import smtplib
import locale
import matplotlib.pyplot as plt
from email.utils import formataddr
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
from PyQt5 import QtGui, QtWidgets,QtCore,Qt
from PyQt5.QtWidgets import (
QTableWidgetItem,
QTableWidget,
QApplication,
QMessageBox,
QDesktopWidget,
QInputDialog,
QMainWindow,
QFileDialog,
QRadioButton,
QVBoxLayout,
QPushButton,
QDialog, 
QLineEdit,
QScrollArea,
QWidget,
QGridLayout,
QComboBox,
QLabel,
QTextEdit,
QHBoxLayout,
QSpacerItem,
QSizePolicy
)
from PyQt5.QtCore import QDate, QTime,QUrl, Qt,QTimer,QRect,QRegExp, QDateTime
from PyQt5.QtGui import QDesktopServices,QColor,QRegExpValidator
from Interface import Ui_janela
from firebase_admin import db
from credenciaisBd import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from collections import defaultdict
from interfaceUpdates import AlteracoesInterface
from update import Atualizar
from login import LoginWindow



ref = db.reference("/")



class FuncoesPadrao:
    def __init__(self,ui,parent=None):
        self.ui = ui
        self.parent = parent
        self.dicionario = None
        self.acoes = AcoesBancoDeDados(ui)
        

    def evento_ao_abrir(self,event):
  
        atualizar = Atualizar(parent=self.parent)
        atualizar.verificar_atualizacao()
        self.ui.label_versao.setText(atualizar.versao)
        hora_atual = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M")
        self.login = db.reference(f"Usuario/{ui.campo_usuario.text()}/Hora Login")
        self.login.set(hora_atual)
        
        self.trazer_configuracoes()
        self.trazer_metas()
        self.carregar_lista_certificados()
        
        ui.campo_data_meta.setDate(QDate.currentDate())
        AlteracoesInterface.apagar_label_status_bd(self)
        self.ui.campo_status_bd.setToolTip("")
        banco_dados.contar_verificacao()
        
        self.privilegio = db.reference(f"Usuario/{ui.campo_usuario.text()}/Privilegio").get()

        if self.privilegio != "admin":
            ui.botao_criar_usuario.deleteLater()
            ui.label_novo_usuario.deleteLater()



        dia_atual = datetime.datetime.now().day
        if 1 <= dia_atual <= 5:
            ui.tabWidget.setCurrentIndex(1)
            self.envio_em_massa()
            QApplication.processEvents() 
        

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


    def atualizar_barras_metas(self):
        try:
            def atualizar_semana(semana_num, certificados, meta_semanal):
                # Obtém os widgets da barra e do label dinamicamente
                barra = getattr(ui, f"barra_meta_semana_{semana_num}")
                label = getattr(ui, f"label_meta{semana_num}")
                
                certificados_semana = math.floor(float(certificados.replace(',', '.')))
                
                barra.setMaximum(meta_semanal)
                barra.setValue(certificados_semana)

                if certificados_semana >= meta_semanal:
                    label.setStyleSheet('color: rgb(255,255,255); background-color: rgb(46, 150, 255); border: 1px solid rgb(120,120,120)')  # Azul
                    label.setText(f"Semana {semana_num} | Meta atingida! - R${certificados_semana} / R${meta_semanal}")
                else:
                    label.setStyleSheet('color: rgb(255,255,255); background-color: transparent; border: 1px solid rgb(120,120,120)')
                    label.setText(f"Semana {semana_num} | R${certificados_semana} / R${meta_semanal}")
                
                return certificados_semana

            meta_mensal = int(float(ui.campo_meta_mes.text().replace(',', '.')))
            meta_semanal = int(float(ui.campo_meta_semanal.text().replace(',', '.')))

            soma = 0

            for i in range(1, 6):
                certificados_semana = atualizar_semana(
                    i, 
                    getattr(ui, f"campo_certificados_semana_{i}").text(), 
                    meta_semanal
                )
                soma += certificados_semana  # Acumula os certificados

            # Atualiza a barra de progresso e o label para a meta mensal
            ui.barra_meta_mensal.setMaximum(meta_mensal)
            ui.barra_meta_mensal.setValue(soma)

            # Define o texto e o estilo do label da meta mensal
            if soma >= meta_mensal:
                ui.label_meta_mes.setStyleSheet('color: rgb(255,255,255); background-color: rgb(46, 214, 255); border: 1px solid rgb(120,120,120)')
                ui.label_meta_mes.setText(f"Meta mensal atingida! - R${soma} / R${meta_mensal}")
            else:
                ui.label_meta_mes.setStyleSheet('color: rgb(255,255,255); background-color: transparent; border: 1px solid rgb(120,120,120)')
                ui.label_meta_mes.setText(f"Mensal | R${soma} / R${meta_mensal}")

        except Exception as e:
            print(f"Erro: {e}")


    def trazer_configuracoes(self):
        #CORRIGIDO ------------------------------------------------------------------
        try:
            ref = db.reference(f"Usuario/{ui.campo_usuario.text()}/Dados/Configuracoes")
            # Faz uma solicitação GET para obter as configurações do banco de dados
            configs = ref.get()

            try:
                # Carrega as configurações da interface com base nos dados obtidos

                ui.caminho_pasta_principal.setText(configs['DIRETORIO-RAIZ'])
                ui.campo_email_empresa.setText(configs['E-MAIL'])
                ui.campo_porcentagem_validacao.setValue(int(configs['PORCENTAGEM']))
                ui.campo_imposto_validacao.setValue(configs['IMPOSTO VALIDACAO'])
                ui.campo_desconto_validacao.setValue(configs['DESCONTO VALIDACAO'])
                ui.campo_lista_tipo_criar_pasta.setCurrentText(configs['MODO PASTA'])
                ui.campo_desconto.setValue(configs['DESCONTO TOTAL'])
                ui.campo_cod_rev.setText(configs['COD REV'])
                ui.campo_senha_email.setText(configs['SENHA EMAIL'])
                ui.campo_nome_agente.setText(configs['AGENTE'])
                ui.campo_dias_renovacao.setValue(configs['RNG RENOVACAO'])
                ui.checkBox_transparecer.setChecked(configs['CHECKBOX TRANSP'])
                ui.campo_porcentagem_transparencia.setValue(configs['VALOR TRANS'])
                ui.campo_telefone_sac_cliente.setText(configs['SAC'])
                ui.campo_porcentagem_venda.setValue(configs['PORCENTAGEM VENDA'])
                ui.campo_telefone_alo_parceiro.setText(configs['TELEFONE ALO PARCEIRO'])
               


            except Exception as e:
                print(e)
                pass
        except:
            pass


    def atualizar_configuracoes(self):
        # Confirmação de atualização das configurações
        resposta = QMessageBox.question(ui.centralwidget, "Confirmação", "Atualizar configurações?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if resposta == QMessageBox.Yes:
            pass
        else:
            return

        usuario = ui.campo_usuario.text()  # Obtém o nome do usuário
        ref_configuracoes = db.reference(f"Usuario/{usuario}/Dados/Configuracoes")  # Caminho para as configurações
        ref_senha = db.reference(f"Usuario/{usuario}/Senha")  # Caminho para a senha

        # Recupera os dados da interface
        diretorio = ui.caminho_pasta_principal.text()
        email = ui.campo_email_empresa.text()
        porcentagem = ui.campo_porcentagem_validacao.value()
        desconto = ui.campo_desconto_validacao.value()
        imposto = ui.campo_imposto_validacao.value()
        criar_pasta = ui.campo_lista_tipo_criar_pasta.currentText()
        campo_desconto = ui.campo_desconto.value()
        campo_cod_rev = ui.campo_cod_rev.text()
        senha_email = ui.campo_senha_email.text()
        atendente = ui.campo_nome_agente.text()
        renovacao = ui.campo_dias_renovacao.value()
        transparencia = ui.checkBox_transparecer.isChecked()
        valor_transparencia = ui.campo_porcentagem_transparencia.value()
        nova_senha = ui.campo_senha_usuario.text()  # Obtém a nova senha (do campo de senha)
        sac_cliente = ui.campo_telefone_sac_cliente.text()
        porc_venda = ui.campo_porcentagem_venda.value()
        alo_parceiro = ui.campo_telefone_alo_parceiro.text()


        # Cria um dicionário com as novas configurações
        nova_config = {
            "DIRETORIO-RAIZ": diretorio,
            "E-MAIL": email,
            "PORCENTAGEM": porcentagem,
            "IMPOSTO VALIDACAO": imposto,
            "DESCONTO VALIDACAO": desconto,
            "MODO PASTA": criar_pasta,
            "DESCONTO TOTAL": campo_desconto,
            "COD REV": campo_cod_rev,
            "SENHA EMAIL": senha_email,
            "AGENTE": atendente,
            "RNG RENOVACAO": renovacao,
            "CHECKBOX TRANSP": transparencia,
            "VALOR TRANS": valor_transparencia,
            "SAC": sac_cliente,
            "PORCENTAGEM VENDA": porc_venda,
            "TELEFONE ALO PARCEIRO":alo_parceiro
        }

        try:
            # Atualiza as configurações no banco de dados
            ref_configuracoes.update(nova_config)

            # Verifica se a senha foi alterada
            if nova_senha:
                # Atualiza a senha no caminho correspondente
                ref_senha.set(nova_senha)
                self.mensagem_alerta("Sucesso","Dados atualizados com sucesso!")
            else:
                self.mensagem_alerta("Erro","Erro ao atualizar dados!")

        except Exception as e:
            try:
                # Se não conseguir atualizar, tenta adicionar as configurações
                ref_configuracoes.set(nova_config)
                
            except Exception as e:
                self.mensagem_alerta("Erro",f"Erro ao adicionar configurações: {str(e)}")


    def trazer_metas(self):
        #CORRIGIDO ----------------------------------------------------------
        ref = db.reference(f"Usuario/{ui.campo_usuario.text()}/Dados/Metas")
        Metas = ref.get()
    
        
        valor_semanal = Metas["SEMANAL"]
        valor_mensal = Metas["MENSAL"]
        ui.campo_meta_semanal.setValue(int(valor_semanal))
        ui.campo_meta_mes.setValue(int(valor_mensal))


    def atualizar_meta_clientes(self):
        try:
            # Zerar o QWidget `campo_grafico`
            

            layout = ui.campo_grafico.layout()
            if layout:
                for i in reversed(range(layout.count())):
                    widget = layout.itemAt(i).widget()
                    if widget is not None:
                        widget.deleteLater()  
                QtWidgets.QWidget().setLayout(layout)  

            if ui.tabWidget.currentIndex() == 2:
                ref = db.reference(f"Usuario/{ui.campo_usuario.text()}/Dados/Pedidos")
                
                certificados_ref = db.reference(f"Configuracoes/Certificados")
                certificados = certificados_ref.get()

                mes_meta = ui.campo_data_meta.date().month()  # Pega o mês da data selecionada
                ano_meta = ui.campo_data_meta.date().year()

                Pedidos = ref.order_by_child("DATA").start_at(f"{ano_meta}-{mes_meta:02d}-01T00:00:00Z").end_at(f"{ano_meta}-{mes_meta:02d}-{calendar.monthrange(ano_meta, mes_meta)[1]}T23:59:59Z").get()

                semanas = [0, 0, 0, 0, 0]

                mes_meta = ui.campo_data_meta.date().month()
                ano_meta = ui.campo_data_meta.date().year()

                ultimo_dia = calendar.monthrange(ano_meta, mes_meta)[1]

                for pedido_info in Pedidos:
                    try:
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

                                        if Pedidos[pedido_info].get('VENDA', '') == "SIM":
                                            preco_certificado = Pedidos[pedido_info].get('PRECO CERTIFICADO', None)
                                            
                                            if preco_certificado:
                                                preco_certificado = float(preco_certificado.replace(',', '.'))
                                                porcentagem_venda = ui.campo_porcentagem_venda.value() / 100
                                                semanas[semana_do_mes - 1] += preco_certificado * porcentagem_venda
                                            else:
                                                versao = Pedidos[pedido_info].get('VERSAO', '')
                                                valor = certificados[versao]['VALOR']
                                                valor = float(valor.replace(',', '.')) 
                                                semanas[semana_do_mes - 1] += valor * (ui.campo_porcentagem_venda.value() / 100)
                                    except:
                                        pass
                    except:
                        pass

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

                dias_do_mes = range(1, ultimo_dia + 1)
                categorias_por_dia = {"CPF": defaultdict(int), "CNPJ": defaultdict(int), "VENDAS": defaultdict(int)}
                valores_por_dia = {"CPF": defaultdict(float), "CNPJ": defaultdict(float), "VENDAS": defaultdict(float)}

                for pedido_info in Pedidos:
                    if Pedidos[pedido_info]['STATUS'] == "APROVADO":
                        data_pedido = Pedidos[pedido_info]['DATA']
                        data_formatada = datetime.datetime.strptime(data_pedido, "%Y-%m-%dT%H:%M:%SZ")

                        if data_formatada.month == mes_meta and data_formatada.year == ano_meta:
                            dia = data_formatada.day
                            versao = Pedidos[pedido_info].get('VERSAO', '') 
                            venda = Pedidos[pedido_info].get('VENDA', '')

                            preco = float(Pedidos[pedido_info]['PRECO'].replace(',', '.'))
                            desconto = 1 - (ui.campo_desconto.value() / 100)
                            valor_com_desconto = preco * desconto

                            if "CPF" in versao:
                                categorias_por_dia["CPF"][dia] += 1
                                valores_por_dia["CPF"][dia] += valor_com_desconto
                            elif "CNPJ" in versao:
                                categorias_por_dia["CNPJ"][dia] += 1
                                valores_por_dia["CNPJ"][dia] += valor_com_desconto

                            # Verificar se a chave VENDA é 'SIM'
                            if venda == "SIM":
                                categorias_por_dia["VENDAS"][dia] += 1
                                valores_por_dia["VENDAS"][dia] += valor_com_desconto

                cpf_counts = [categorias_por_dia["CPF"].get(dia, 0) for dia in dias_do_mes]
                cnpj_counts = [categorias_por_dia["CNPJ"].get(dia, 0) for dia in dias_do_mes]
                vendas_counts = [categorias_por_dia["VENDAS"].get(dia, 0) for dia in dias_do_mes]

                cpf_totals = [valores_por_dia["CPF"].get(dia, 0) for dia in dias_do_mes]
                cnpj_totals = [valores_por_dia["CNPJ"].get(dia, 0) for dia in dias_do_mes]
                vendas_totals = [valores_por_dia["VENDAS"].get(dia, 0) for dia in dias_do_mes]

                total_counts = [cpf_counts[i] + cnpj_counts[i] + vendas_counts[i] for i in range(len(dias_do_mes))]

                dias_uteis = pd.bdate_range(start=f"{ano_meta}-{mes_meta:02d}-01", 
                                            end=f"{ano_meta}-{mes_meta:02d}-{ultimo_dia:02d}").day.tolist()

                media_cumulativa = np.cumsum([total_counts[i - 1] for i in dias_uteis]) / np.arange(1, len(dias_uteis) + 1)
                media_cumulativa_cpf = np.cumsum([cpf_counts[dia - 1] for dia in dias_uteis]) / np.arange(1, len(dias_uteis) + 1)
                media_cumulativa_cnpj = np.cumsum([cnpj_counts[dia - 1] for dia in dias_uteis]) / np.arange(1, len(dias_uteis) + 1)

                soma_maxima = max(total_counts)
                max_y = max(soma_maxima, max(media_cumulativa)) + 2

                fig, ax = plt.subplots(figsize=(14, 8))
                fig.subplots_adjust(left=0.08, right=0.92, top=0.88, bottom=0.12)

                fig.patch.set_facecolor((60/255, 62/255, 84/255))
                ax.set_facecolor((60/255, 62/255, 84/255))

                bar_width = 0.6

                ax.bar(dias_do_mes, cnpj_counts, width=bar_width, label="CNPJ", color="orange")
                ax.bar(dias_do_mes, cpf_counts, width=bar_width, bottom=cnpj_counts, label="CPF", color="blue")
                ax.bar(dias_do_mes, vendas_counts, width=bar_width, bottom=[cnpj_counts[i] + cpf_counts[i] for i in range(len(cnpj_counts))], label="Vendas", color="cyan")

                ax.plot(dias_uteis, media_cumulativa, color="red", linestyle="-", linewidth=1, label="Média Acumulada")
                ax.plot(dias_uteis, media_cumulativa_cnpj, color="yellow", linestyle="-", linewidth=1, label="Média Acumulada CNPJ")
                ax.plot(dias_uteis, media_cumulativa_cpf, color="blue", linestyle="-", linewidth=1, label="Média Acumulada CPF")

                fonte_cor = (255/255, 255/255, 255/255)

                ax.set_xlabel("Dias do Mês", fontsize=7, color=fonte_cor)
                ax.set_ylabel("Quantidade de Pedidos", fontsize=7, color=fonte_cor)
                ax.set_xticks(range(1, ultimo_dia + 1))
                ax.set_ylim(0, max_y)
                ax.set_yticks(range(0, int(max_y) + 1, 1))

                for y in range(0, int(max_y)):
                    ax.axhline(y=y, color="gray", linestyle="-", alpha=0.3, linewidth=0.7)

                leg = ax.legend(fontsize=6, labelcolor=fonte_cor)
                leg.get_frame().set_facecolor((60/255, 62/255, 84/255))
                leg.get_frame().set_edgecolor((60/255, 62/255, 84/255))

                ax.tick_params(axis='x', labelsize=6, colors=fonte_cor)
                ax.tick_params(axis='y', labelsize=6, colors=fonte_cor)

                cursor = mplcursors.cursor(ax, hover=True)
                cursor.connect("add", lambda sel: sel.annotation.set_text(
                    f'Dia: {int(sel.target[0])}\n'
                    f'CPF: {cpf_counts[int(sel.target[0]) - 1]}  Valor: R$ {cpf_totals[int(sel.target[0]) - 1]:,.2f}\n'
                    f'CNPJ: {cnpj_counts[int(sel.target[0]) - 1]}  Valor: R$ {cnpj_totals[int(sel.target[0]) - 1]:,.2f}\n'
                    f'Vendas: {vendas_counts[int(sel.target[0]) - 1]}\n'
                    f'TOTAL: R$ {cpf_totals[int(sel.target[0]) - 1] + cnpj_totals[int(sel.target[0]) - 1] + vendas_totals[int(sel.target[0]) - 1]:,.2f}'
                ))

                cursor.connect("add", lambda sel: sel.annotation.set_fontsize(7))

                new_layout = QtWidgets.QVBoxLayout()
                new_layout.addWidget(FigureCanvas(fig))
                ui.campo_grafico.setLayout(new_layout)


            
            try:
                # Remove o layout do campo de horário antes de adicionar o novo gráfico
                layout_horario = ui.campo_grafico_horario.layout()
                if layout_horario:
                    for i in reversed(range(layout_horario.count())):
                        widget = layout_horario.itemAt(i).widget()
                        if widget is not None:
                            widget.deleteLater()
                    QtWidgets.QWidget().setLayout(layout_horario)

                # Inicializa dicionários para pedidos por intervalo de hora
                pedidos_por_intervalo_cpf = defaultdict(int)
                pedidos_por_intervalo_cnpj = defaultdict(int)

                # Define os intervalos de hora (08:00 às 19:00)
                intervalos = [
                    f"{h:02d}:00 - {h + 1:02d}:00" for h in range(8, 19)
                ]  # Intervalos de 08:00 às 19:00
                intervalo_map = {f"{h:02d}": f"{h:02d}:00 - {h + 1:02d}:00" for h in range(8, 19)}

                for pedido_info in Pedidos:
                    if Pedidos[pedido_info]['STATUS'] == "APROVADO":
                        hora = Pedidos[pedido_info]['HORA'][:2]  # Pega somente a hora (hh:mm -> hh)
                        intervalo = intervalo_map.get(hora, None)  # Mapeia para o intervalo correspondente

                        if intervalo:
                            tipo_certificado = Pedidos[pedido_info]['VERSAO']
                            if 'CPF' in tipo_certificado:
                                pedidos_por_intervalo_cpf[intervalo] += 1
                            elif 'CNPJ' in tipo_certificado:
                                pedidos_por_intervalo_cnpj[intervalo] += 1

                # Ordena os intervalos e prepara os dados
                horas = sorted(intervalos)
                pedidos_cpf_counts = [pedidos_por_intervalo_cpf.get(hora, 0) for hora in horas]
                pedidos_cnpj_counts = [pedidos_por_intervalo_cnpj.get(hora, 0) for hora in horas]

                # Gráfico de barras
                fig2, ax2 = plt.subplots(figsize=(14, 8))
                fig2.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)  # Ajusta o espaço para os rótulos
                fig2.patch.set_facecolor((60 / 255, 62 / 255, 84 / 255))  # Fundo geral
                ax2.set_facecolor((60 / 255, 62 / 255, 84 / 255))  # Fundo do gráfico

                ax2.bar(horas, pedidos_cpf_counts, width=0.4, label="CPF", color="blue", align='center')
                ax2.bar(horas, pedidos_cnpj_counts, width=0.4, label="CNPJ", color="orange", bottom=pedidos_cpf_counts, align='center')

                fonte_cor = (255 / 255, 255 / 255, 255 / 255)  # Cor do texto (branco)

                ax2.set_xlabel("Intervalos de Horário", fontsize=7, color=fonte_cor)
                ax2.set_ylabel("Quantidade de Pedidos", fontsize=7, color=fonte_cor)
                ax2.set_xticks(range(len(horas)))
                ax2.set_xticklabels(horas, rotation=45, ha='right', fontsize=6, color=fonte_cor)

                ax2.set_ylim(0, max(pedidos_cpf_counts[i] + pedidos_cnpj_counts[i] for i in range(len(horas))) + 1)

                for y in range(0, max(pedidos_cpf_counts[i] + pedidos_cnpj_counts[i] for i in range(len(horas))) + 1):
                    ax2.axhline(y=y, color="gray", linestyle="-", alpha=0.3, linewidth=0.7)

                leg = ax2.legend(fontsize=6, labelcolor=fonte_cor)
                leg.get_frame().set_facecolor((60 / 255, 62 / 255, 84 / 255))
                leg.get_frame().set_edgecolor((60 / 255, 62 / 255, 84 / 255))

                ax2.tick_params(axis='x', labelsize=6, colors=fonte_cor)
                ax2.tick_params(axis='y', labelsize=6, colors=fonte_cor)

                new_layout_horario = QtWidgets.QVBoxLayout()
                new_layout_horario.addWidget(FigureCanvas(fig2))
                ui.campo_grafico_horario.setLayout(new_layout_horario)

            except Exception as e:
                pass



            try:
                layout_tipo = ui.campo_grafico_tipo_certificado.layout()
                if layout_tipo:
                    for i in reversed(range(layout_tipo.count())):
                        widget = layout_tipo.itemAt(i).widget()
                        if widget is not None:
                            widget.deleteLater()
                    QtWidgets.QWidget().setLayout(layout_tipo)

                total_cpf_aprovado = sum(1 for pedido_info in Pedidos if 'CPF' in Pedidos[pedido_info]['VERSAO'] and Pedidos[pedido_info]['STATUS'] == "APROVADO")
                total_cnpj_aprovado = sum(1 for pedido_info in Pedidos if 'CNPJ' in Pedidos[pedido_info]['VERSAO'] and Pedidos[pedido_info]['STATUS'] == "APROVADO")
                total_cpf_outros = sum(1 for pedido_info in Pedidos if 'CPF' in Pedidos[pedido_info]['VERSAO'] and Pedidos[pedido_info]['STATUS'] != "APROVADO")
                total_cnpj_outros = sum(1 for pedido_info in Pedidos if 'CNPJ' in Pedidos[pedido_info]['VERSAO'] and Pedidos[pedido_info]['STATUS'] != "APROVADO")

                total_a1 = sum(
                    1 for pedido_info in Pedidos
                    if 'no computador' in Pedidos[pedido_info]['VERSAO'].lower() and Pedidos[pedido_info]['STATUS'] == "APROVADO"
                )
                total_a3 = sum(
                    1 for pedido_info in Pedidos
                    if 'no computador' not in Pedidos[pedido_info]['VERSAO'].lower() and Pedidos[pedido_info]['STATUS'] == "APROVADO"
                )

                midia_cartao_leitora = sum(1 for pedido_info in Pedidos if 'cartão e leitora' in Pedidos[pedido_info]['VERSAO'].lower())
                midia_cartao = sum(1 for pedido_info in Pedidos if 'cartão' in Pedidos[pedido_info]['VERSAO'].lower() and 'cartão e leitora' not in Pedidos[pedido_info]['VERSAO'].lower())
                midia_token = sum(1 for pedido_info in Pedidos if 'token' in Pedidos[pedido_info]['VERSAO'].lower())

                fig3, axs3 = plt.subplots(2, 2, figsize=(12, 12))  
                fig3.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.3, hspace=0.3)
                fig3.patch.set_facecolor((60 / 255, 62 / 255, 84 / 255))  

                font_props = {'fontsize': 6, 'color': 'black'}
                fonte_titulo = {'fontsize': 10, 'color': 'white'}

                def filtrar_dados(labels, valores):
                    labels_filtrados = [label for label, valor in zip(labels, valores) if valor > 0]
                    valores_filtrados = [valor for valor in valores if valor > 0]
                    return labels_filtrados, valores_filtrados

                def adicionar_descricao(ax, labels, valores, colors, percentuais):
                    # Adiciona os valores e as porcentagens dentro do gráfico
                    total = sum(valores)
                    for i, (label, valor, color) in enumerate(zip(labels, valores, colors)):
                        percentual = (valor / total) * 100
                        ax.text(0, 0.2 - (i * 0.2), f'{label} [{valor}] {percentual:.1f}%', ha='center', va='center', fontsize=8, color=color)

                # Gráfico Tipo de Certificado
                labels_certificado, valores_certificado = filtrar_dados(['CPF', 'CNPJ'], [total_cpf_aprovado, total_cnpj_aprovado])
                total_certificado = sum(valores_certificado)

                colors_certificado = ['PowderBlue', 'orange']
                axs3[0, 0].pie(
                    valores_certificado,
                    startangle=90,
                    colors=colors_certificado,
                    textprops=font_props,
                    wedgeprops={'width': 0.1, 'edgecolor': 'none'}, 
                    pctdistance=0.80, 
                    labels=None 
                )
                axs3[0, 0].set_title('Tipo de Certificado', fontdict=fonte_titulo)
                adicionar_descricao(axs3[0, 0], labels_certificado, valores_certificado, colors_certificado, [])

                # Gráfico Relação de Status
                total_aprovados = total_cpf_aprovado + total_cnpj_aprovado
                total_outros = total_cpf_outros + total_cnpj_outros
                labels_status, valores_status = filtrar_dados(['Aprovados', 'Outros'], [total_aprovados, total_outros])
                total_status = sum(valores_status)

                colors_status = ['lightgreen', 'red']
                axs3[0, 1].pie(
                    valores_status,
                    startangle=90,
                    colors=colors_status,
                    textprops=font_props,
                    wedgeprops={'width': 0.1, 'edgecolor': 'none'}, 
                    pctdistance=0.80,  
                    labels=None
                )
                axs3[0, 1].set_title('Relação de Status', fontdict=fonte_titulo)
                adicionar_descricao(axs3[0, 1], labels_status, valores_status, colors_status, [])

                # Gráfico por Tipo de Versão
                labels_versao, valores_versao = filtrar_dados(['A1', 'A3'], [total_a1, total_a3])
                total_versao = sum(valores_versao)

                colors_versao = ['violet', 'Gold']
                axs3[1, 0].pie(
                    valores_versao,
                    startangle=90,
                    colors=colors_versao,
                    textprops=font_props,
                    wedgeprops={'width': 0.1, 'edgecolor': 'none'}, 
                    pctdistance=0.80,  
                    labels=None
                )
                axs3[1, 0].set_title('Quantidade por Tipo de Versão', fontdict=fonte_titulo)
                adicionar_descricao(axs3[1, 0], labels_versao, valores_versao, colors_versao, [])

                # Gráfico por Mídia
                labels_midia, valores_midia = filtrar_dados(['C + L', 'Cartão', 'Token'], [midia_cartao_leitora, midia_cartao, midia_token])
                total_midia = sum(valores_midia)

                colors_midia = ['cyan', 'yellow', 'orangeRed']
                axs3[1, 1].pie(
                    valores_midia,
                    startangle=90,
                    colors=colors_midia,
                    textprops=font_props,
                    wedgeprops={'width': 0.1, 'edgecolor': 'none'}, 
                    pctdistance=0.80,  
                    labels=None
                )
                axs3[1, 1].set_title('Quantidade por Tipo de Mídia', fontdict=fonte_titulo)
                adicionar_descricao(axs3[1, 1], labels_midia, valores_midia, colors_midia, [])

                # Adiciona os gráficos ao layout
                new_layout_tipo_certificado = QtWidgets.QVBoxLayout()
                new_layout_tipo_certificado.addWidget(FigureCanvas(fig3))
                ui.campo_grafico_tipo_certificado.setLayout(new_layout_tipo_certificado)

            except Exception as e:
                pass











        except Exception as e:
            print(f'Erro: {e}')







    def Atualizar_meta(self):
        #CORRIGIDO
        ref = db.reference(f"Usuario/{ui.campo_usuario.text()}/Dados/Metas")

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
        try:
            caminho_pasta = ui.caminho_pasta.text()

            for arquivo in os.listdir(caminho_pasta):
                if arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.heic')):
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
            AlteracoesInterface.animar_label_pular(self,self.ui.botao_converter_todas_imagens_em_pdf)
            self.atualizar_documentos_tabela()
        except:
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
            hora_atual = datetime.datetime.now().strftime("%H_%M_%S")
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
                
                caminho = f"{caminho}/{nome_documento}.png"

            janela_principal = self.obter_janela_principal(ui.centralwidget)

            if janela_principal:

                janela_principal.setWindowOpacity(0)

            time.sleep(0.5)

            screenshot = pyautogui.screenshot()

            if janela_principal:

                janela_principal.setWindowOpacity(1)

            screenshot.save(caminho)
            AlteracoesInterface.confirmar_label_captura_tela(self)

            self.atualizar_documentos_tabela()
    
        except:

            self.atualizar_documentos_tabela()
            AlteracoesInterface.negar_label_captura_tela(self)
            self.mensagem_alerta("Erro",f"Não foi possível capturar a tela!")


    def pasta_existe(self,diretorio, nome_pasta):
        #transformei o texto em um diretório
        caminho_pasta = os.path.join(diretorio, nome_pasta)
        return os.path.exists(caminho_pasta)


    def abrir_pasta_cliente(self):
        try:
            QDesktopServices.openUrl(QUrl.fromLocalFile(ui.caminho_pasta.text()))
            AlteracoesInterface.confirmar_label_criar_pasta(self)

            
        except:
            AlteracoesInterface.negar_label_criar_pasta(self)
            return


    def criar_pasta_cliente(self):
        
        try:
            pedido = ui.campo_pedido.text()
            versao = ui.campo_lista_versao_certificado.currentText()
            hora = ui.campo_hora_agendamento.text()
            data = ui.campo_data_agendamento.text()
            modalidade = ui.campo_lista_modalidade.currentText()

            if pedido == "" or hora == "00:00" or data == "01/01/2000" or modalidade == "" or versao == "":

                AlteracoesInterface.negar_label_criar_pasta(self)
                self.mensagem_alerta("Pasta não criada","Adicione os itens com 🌟 para criar a pasta do cliente!")

                return

            self.formatar_nome()
            tipo = ui.campo_lista_tipo_criar_pasta.currentText()
            if tipo == "NOME":
                if ui.campo_nome.text() == "":
                    self.mensagem_alerta("Pasta não criada","Adicione o nome do cliente!")
                    
                    AlteracoesInterface.negar_label_criar_pasta(self)

                    return
                nome_pasta = f'{ui.campo_nome.text()}'
            
            elif tipo == "PEDIDO":
                nome_pasta = f'{ui.campo_pedido.text()}'
            
            elif tipo == "PEDIDO-NOME":
                if ui.campo_nome.text() == "":
                    self.mensagem_alerta("Pasta não criada","Adicione o nome do cliente!")
                    AlteracoesInterface.negar_label_criar_pasta(self)

                    return
                nome_pasta = f'{str(ui.campo_pedido.text())}-{ui.campo_nome.text()}'

            diretorio_padrão = ui.caminho_pasta_principal.text()
            pasta_padrão = os.path.join(diretorio_padrão, nome_pasta)


            if not self.pasta_existe(diretorio_padrão, nome_pasta):
                
                os.mkdir(pasta_padrão)
                pasta_padrão = pasta_padrão.replace("/", "\\")
                ui.caminho_pasta.setText(pasta_padrão)
                
                status = banco_dados.alteracao_status()

                if status == "APROVADO" or status == "CANCELADO":
                    AlteracoesInterface.zerar_label_criar_pasta(self)
                else:
                    AlteracoesInterface.confirmar_label_criar_pasta(self)

                self.acoes.salvar_pedido()
            #Caso exista, abra
            else:
                self.abrir_pasta_cliente()
        except Exception as e:
            print(e)
            AlteracoesInterface.negar_label_criar_pasta(self)


    def procurar_cnh(self):
        #Abre o link para consulta da CNH
        url = QUrl("https://portalservicos.senatran.serpro.gov.br/#/condutor/validar-cnh")
        QDesktopServices.openUrl(url)
        return


    def mensagem_alerta(self,titulo,mensagem):
        QMessageBox.information(ui.centralwidget, titulo, mensagem, QMessageBox.Ok)


    def procurar_funcional(self):

        nome_pesquisa, ok = QInputDialog.getItem(ui.centralwidget, "Site pesquisa", "Escolha o site de pesquisa:", ["OAB", "CREA","CRM"], 0, False)

        if not ok or not nome_pesquisa:
            return

        match nome_pesquisa:
            case "OAB":
                url = QUrl("https://cna.oab.org.br/")
                QDesktopServices.openUrl(url)
                return
            
            case "CREA":
                url = QUrl("https://consultaprofissional.confea.org.br/")
                QDesktopServices.openUrl(url)
                return

            case "CRM":
                url = QUrl("https://portal.cfm.org.br/busca-medicos")
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
        ui.campo_cnpj_razao_social.setText("")
        ui.campo_nome.setText("") 

        cnpj = ''.join(filter(str.isdigit, ui.campo_cnpj.text()))

        if not cnpj:
            return

        url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"

        try:
            resposta = requests.get(url, timeout=10)

            if resposta.status_code == 200:
                data = resposta.json()
                ui.campo_cnpj_municipio.setText(f'{data["municipio"]}/{data["uf"]}')
                ui.campo_cnpj_razao_social.setText(data["nome"])

                situacao_empresa = data.get("situacao", "").upper()
                if situacao_empresa in ["INATIVA", "INAPTA"]:
                    self.mensagem_alerta("ALERTA", f"A empresa está {situacao_empresa}!")
                    ui.campo_comentario.setPlainText(f"{ui.campo_comentario.toPlainText()}\n•A empresa está {situacao_empresa} ")
                    return

                qsa = data.get("qsa", [])
                uf = data["uf"]

                # Atualizar o campo da lista de Junta Comercial
                ui.campo_lista_junta_comercial.setCurrentText(uf)
                self.atualizar_documentos_tabela()

                # Verificar os nomes do QSA
                if len(qsa) == 1:
                    nome = qsa[0]["nome"]
                    if not ui.campo_nome.text():
                        ui.campo_nome.setText(nome)
                elif len(qsa) > 1:
                    self.selecionar_nome_qsa(qsa)
                else:
                    pass

            elif resposta.status_code == 429:
                self.mensagem_alerta("Limite de Requisições", "Você atingiu o limite de requisições da API.\nTente novamente em alguns segundos.")
            else:
                self.mensagem_alerta("Erro", "CNPJ inválido ou não encontrado.")
                self.atualizar_documentos_tabela()

        except requests.exceptions.Timeout:
            self.mensagem_alerta("Erro de Conexão", "A conexão demorou muito para responder. Verifique sua internet.")
            self.atualizar_documentos_tabela()

        except requests.RequestException:
            self.mensagem_alerta("Erro de Conexão", "Não foi possível conectar à API. Verifique sua internet.")
            self.atualizar_documentos_tabela()

        except Exception as e:
            self.mensagem_alerta("Erro Desconhecido", 
                                "Um erro inesperado ocorreu. Tente novamente mais tarde!")
            self.atualizar_documentos_tabela()


    def selecionar_nome_qsa(self, qsa):
        dialog = QDialog(ui.centralwidget)
        dialog.setWindowTitle("Selecione o Nome do QSA")
        dialog.setMinimumWidth(400)

        layout = QVBoxLayout(dialog)

        label_instrucoes = QLabel("Nomes no QSA:")
        layout.addWidget(label_instrucoes)

        for pessoa in qsa:
            nome = pessoa["nome"]
            botao = QPushButton(nome)
            layout.addWidget(botao)

            # Usando uma função lambda para preservar o valor de 'nome' em cada iteração
            botao.clicked.connect(lambda _, nome=nome: self.selecionar_nome(nome, dialog))

        # Exibir o diálogo
        dialog.exec_()


    def selecionar_nome(self, nome, dialog):
        ui.campo_nome.setText(nome)
        dialog.accept()


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
            pedidos_ref = ref.child(f"Usuario/{ui.campo_usuario.text()}/Dados/Pedidos/").order_by_child("DATA") \
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
            # Pega o texto da célula
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
            
            if not ok or not nome_documento:
                return

            pdf_merger = PyPDF2.PdfMerger()

            try:

                file_paths, _ = QFileDialog.getOpenFileNames(ui.centralwidget, "Selecionar PDFs para Mesclar", folder_to_open_raw, "Arquivos PDF (*.pdf);;Todos os arquivos (*)")

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

            AlteracoesInterface.confirmar_label_mesclar_pdf(self)
            #self.mensagem_alerta("Concluído","Os arquivos PDF foram mesclados com sucesso!")
            self.atualizar_documentos_tabela()


        except:
            AlteracoesInterface.negar_label_mesclar_pdf(self)
            pdf_merger.close()
            self.atualizar_documentos_tabela()

            return
        

    def escolher_conversao(self):
        dialog = QDialog(ui.centralwidget)
        dialog.setWindowTitle("Selecione o tipo de conversão")
        
        layout_dialog = QVBoxLayout(dialog)

        radio_imagem_para_pdf = QRadioButton("Imagem > PDF")
        radio_pdf_para_imagem = QRadioButton("PDF > Imagem")
        
        layout_dialog.addWidget(radio_imagem_para_pdf)
        layout_dialog.addWidget(radio_pdf_para_imagem)

        botao_confirmar = QPushButton("Confirmar")
        layout_dialog.addWidget(botao_confirmar)

        def confirmar():
            if radio_imagem_para_pdf.isChecked():
                self.converter_imagem_para_pdf()
            elif radio_pdf_para_imagem.isChecked():
                self.converter_pdf_para_imagem()
            dialog.accept()

        botao_confirmar.clicked.connect(confirmar)
        dialog.exec_()


    def converter_imagem_para_pdf(self):
        try:
            image_paths = filedialog.askopenfilenames(
                filetypes=[("Image Files", "*.jpg *.jpeg *.png *.heic")], 
                title="Converter Imagem > PDF"
            )
            if not image_paths:
                return
            for image_path in image_paths:
                nome_do_arquivo, _ = os.path.splitext(os.path.basename(image_path))
                imagem = Image.open(image_path).convert('RGB')  # Converte para RGB, necessário para PDFs
                imagem.save(f'{os.path.dirname(image_path)}\\{nome_do_arquivo}.pdf', 'PDF', resolution=100.0)
            AlteracoesInterface.confirmar_label_converter_pdf(self)
        except Exception as e:
            print(f"Erro ao converter imagem para PDF: {e}")
            AlteracoesInterface.negar_label_converter_pdf(self)


    def converter_pdf_para_imagem(self):
        try:
            pdf_paths = filedialog.askopenfilenames(
                filetypes=[("PDF Files", "*.pdf")], 
                title="Converter PDF > Imagem"
            )
            if not pdf_paths:
                return
            for pdf_path in pdf_paths:
                nome_do_arquivo, _ = os.path.splitext(os.path.basename(pdf_path))
                pdf_document = fitz.open(pdf_path)  # PyMuPDF para manipulação de PDFs
                for page_number in range(len(pdf_document)):  # Extrai todas as páginas
                    pagina = pdf_document.load_page(page_number)
                    imagem = pagina.get_pixmap()
                    imagem_pillow = Image.frombytes("RGB", [imagem.width, imagem.height], imagem.samples)
                    imagem_pillow.save(f'{os.path.dirname(pdf_path)}\\{nome_do_arquivo}_page{page_number + 1}.jpg', 'JPEG', quality=95)
            AlteracoesInterface.confirmar_label_converter_pdf(self)
            self.atualizar_documentos_tabela()
        except Exception as e:
            print(f"Erro ao converter PDF para imagem: {e}")
            AlteracoesInterface.negar_label_converter_pdf(self)


    def copiar_campo(self, nome_campo):
        # LISTA DE CAMPOS QUE SERÃO COPIADOS
        campos = [
            'campo_oab',
            'campo_cnh',
            'campo_cnpj',
            'campo_pedido',
            'campo_cpf',
            'campo_seguranca_cnh',
            'campo_rg',
            'campo_nome_mae',
            'campo_nome',
            'campo_pis'

        ]

        if nome_campo in campos:
            try:

                campo = getattr(ui, nome_campo)

                if nome_campo in ['campo_cnpj', 'campo_cpf']:
                    texto = campo.text().replace('.', '').replace('-', '').replace('/', '')
                else:
                    texto = campo.text()

                QApplication.clipboard().setText(texto)

                campo.selectAll()
            except Exception as e:

                print(f"Erro ao copiar o campo {nome_campo}: {e}")


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
            AlteracoesInterface.label_status_bd_desatualizado(self)
            
            self.ui.label_confirmacao_salvar.setText("")
            self.ui.label_confirmacao_excluir.setText("")
            
            nome_campo_atual = campo_atual.objectName()
            if nome_campo_atual == "campo_lista_versao_certificado":
                self.buscar_preco_certificado()
            
            elif nome_campo_atual == "campo_preco_certificado_cheio":
                valor_formatado = f"{float(ui.campo_preco_certificado_cheio.text()):.2f}"
                ui.campo_preco_certificado_cheio.setText(valor_formatado)
                ui.campo_preco_certificado.setText(self.calcular_comissao()["valor_final_formatado"])
                self.atualizar_campos_comissao()


    def obter_valor_campo(self, campo):
        if isinstance(campo, QtWidgets.QLineEdit):
            return campo.text()
        elif isinstance(campo, QtWidgets.QComboBox):
            return campo.currentText()
        elif isinstance(campo, QtWidgets.QTimeEdit):
            return campo.time().toString("HH:mm")
        elif isinstance(campo, QtWidgets.QTextEdit):
            return campo.toPlainText()
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
            ref = db.reference(f"Configuracoes/Certificados")
            
            certificados = ref.get()

            ui.campo_lista_versao_certificado.clear()  
            ui.campo_lista_versao_certificado.addItem("")
            ui.campo_lista_versao_certificado.addItems(certificados.keys()) 

            ui.campo_lista_versao_certificado.insertItem(1,'e-CNPJ - no computador - 12 meses')
            ui.campo_lista_versao_certificado.insertItem(2,'e-CPF - no computador - 12 meses')


    def pegar_link_venda(self):
        try:
            ref = db.reference(f"Configuracoes/Certificados/{ui.campo_lista_versao_certificado.currentText()}")
            certificado = ref.get()
            link_venda = certificado["LINK VENDA"]
            rev = str(ui.campo_cod_rev.text())

            if certificado:
                link = f"{link_venda}{rev}"
                pyperclip.copy(str(link))
        except:
            pass


    def atualizar_documentos_tabela(self):

        self.ui.tabela_documentos.clearContents()

        pasta_cliente = self.ui.caminho_pasta.text()

        if not os.path.exists(pasta_cliente):
            return

        documentos = os.listdir(pasta_cliente)

        pdfs = [doc for doc in documentos if doc.lower().endswith('.pdf')]
        outros_documentos = [doc for doc in documentos if not doc.lower().endswith('.pdf')]

        num_documentos = len(pdfs)
        self.ui.tabela_documentos.setRowCount(num_documentos)

        for i, documento in enumerate(pdfs):

            item_nome_documento = QTableWidgetItem(documento)

            item_nome_documento.setForeground(QColor(220, 0, 0))

            self.ui.tabela_documentos.setItem(i, 0, item_nome_documento)

        num_outros_documentos = len(outros_documentos)
        self.ui.tabela_documentos.setRowCount(num_documentos + num_outros_documentos)

        for i, documento in enumerate(outros_documentos):

            item_nome_documento = QTableWidgetItem(documento)

            item_nome_documento.setForeground(QColor(128, 128, 128))

            self.ui.tabela_documentos.setItem(num_documentos + i, 0, item_nome_documento)


    def abrir_documento_para_edicao(self):
        item = self.ui.tabela_documentos.currentItem()

        if item is not None:
            nome_documento = item.text()

            caminho_documento = os.path.join(self.ui.caminho_pasta.text(), nome_documento)
            if os.name == 'nt':  
                os.startfile(caminho_documento)  
            else:
                subprocess.Popen(['xdg-open', caminho_documento])


    def abrir_janela_mensagem(self):
        self.abrir_nova_janela(janela)


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
        if self.dicionario is None:
            self.dicionario = db.reference(f"Configuracoes/Mensagens").get()

        # Verifica se a janela de mensagens está aberta
        if hasattr(self, 'nova_janela') and self.nova_janela is not None:
            if self.nova_janela.isVisible():
                return 

        self.nova_janela = QDialog(janela_pai)
        self.nova_janela.setFixedSize(484, 673)
        self.nova_janela.setWindowTitle('Mensagens')

        pos = janela_pai.pos()
        self.nova_janela.move(pos.x() - self.nova_janela.width() - 8, pos.y())

        scroll = QScrollArea(self.nova_janela)
        scroll.setFixedSize(484, 673)

        widget = QWidget()
        layout = QGridLayout()

        if not hasattr(self, 'dicionario') or not self.dicionario:
            print("Dicionário de mensagens não está carregado.")
            return

        for chave, valor in sorted(self.dicionario.items(), key=lambda x: x[1].get('posicao', 0)):
            titulo = valor.get("titulo")
            if titulo:
                botao = QPushButton()
                botao.setFixedSize(228, 66)
                botao.setStyleSheet("QPushButton { text-align: justify; }")
                linhas = [titulo[j:j+40] for j in range(0, len(titulo), 40)]
                botao.setText('\n'.join(linhas))

                # Conecta o botão à função genérica de tratamento
                botao.clicked.connect(lambda _, c=chave: self.copiar_com_tratamento(c))

                posicao = valor.get('posicao', 0) - 1
                layout.addWidget(botao, posicao % 9, posicao // 9)  # 1ª coluna: 0-8; 2ª coluna: 9-17

        widget.setLayout(layout)
        scroll.setWidget(widget)
        self.nova_janela.show()


    def copiar_com_tratamento(self, chave):
        mensagem_firebase = self.dicionario[chave].get("mensagem", "")

        mensagem = mensagem_firebase
        if "{{mensagem_inicial}}" in mensagem:
            mensagem_inicial = self.determinar_hora(datetime.datetime.now().time())
            mensagem = mensagem.replace("{{mensagem_inicial}}", mensagem_inicial)

        if "{{nome}}" in mensagem:
            nome = ui.campo_nome_agente.text()
            mensagem = mensagem.replace("{{nome}}", nome)

        if "{{campo_nome}}" in mensagem:
            try:
                nome = ui.campo_nome.text().capitalize().split()[0]
            except:
                nome = ""
            mensagem = mensagem.replace("{{campo_nome}}", nome)

        if "{{midia}}" in mensagem:
            certificado = ui.campo_lista_versao_certificado.currentText().lower()
    
            if "cartão e leitora" in certificado:
                midia = "CARTÃO E LEITORA"
            elif "cartão" in certificado:
                midia = "CARTÃO"
            elif "token" in certificado:
                midia = "TOKEN"
            else:
                midia = ""
            
            mensagem = mensagem.replace("{{midia}}", midia)

        if "{{cod_rev}}" in mensagem:
            rev = ui.campo_cod_rev.text()
            mensagem = mensagem.replace("{{cod_rev}}", rev)

        if "{{pedido}}" in mensagem:
            pedido = ui.campo_pedido.text()
            mensagem = mensagem.replace("{{pedido}}", pedido)

        if "{{cliente}}" in mensagem:
            cliente = ui.campo_nome.text()
            mensagem = mensagem.replace("{{cliente}}", cliente)
        
        if"{{sac}}" in mensagem:
            sac = ui.campo_telefone_sac_cliente.text()
            mensagem = mensagem.replace("{{sac}}", sac)


        mensagem = mensagem.replace("\\n", "\n")

        clipboard = QApplication.clipboard()
        clipboard.setText(mensagem)

        if hasattr(self, 'nova_janela') and self.nova_janela is not None:
            if self.nova_janela.isVisible():
                self.nova_janela.close()

            self.nova_janela.deleteLater()
            self.nova_janela = None


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

        texto, ok = QInputDialog.getItem(ui.centralwidget, "Mensagens Whatsapp", "Escolha a Mensagem:", ["INICIAR ATENDIMENTO","PROBLEMA PAGAMENTO","ERRO NA VALIDAÇÃO","OUTRO"], 0, False)
        
        if not ok or not texto:
            return 
        
        nome = ui.campo_nome_agente.text()
        
        if texto == 'OUTRO':
                mensagem = f'{mensagem_inicial}, tudo bem?\n'\

        if texto == 'INICIAR ATENDIMENTO':
             
             mensagem = f'{mensagem_inicial}, tudo bem?\n'\
f'Sou o {nome}, agente de registro da ACB Digital e temos um agendamento para seu certificado digital às {ui.campo_hora_agendamento.text()}. \n' \
'Podemos Iniciar o atendimento?'
        
        elif texto == 'ERRO NA VALIDAÇÃO':
            mensagem = f'{mensagem_inicial}, tudo bem?\n'\
f'Sou o {nome} que fez a validação do seu certificado digital.\n'\
'Estou entrando em contato pois ocorreu um erro na validação do seu pedido.'

        elif texto == 'PROBLEMA PAGAMENTO':
            mensagem = f'{mensagem_inicial}, tudo bem?\n'\
f'Sou o {nome}, agente de registro da ACB Digital e temos um agendamento para seu certificado digital às *{ui.campo_hora_agendamento.text()}*. \n' \
'Porém, verifiquei que o pagamento para seu pedido ainda *não foi reconhecido no sistema*.\n'\
f'Para prosseguirmos com a validação, preciso que o senhor(a) entre em contato com o suporte pelo contato *{ui.campo_telefone_sac_cliente.text()}* para que possam fazer a liberação do pedido.'

        numero = ui.campo_telefone.text()  
        mensagem = mensagem.replace(' ', '%20')  
        url_mensagem = QUrl(f'https://api.whatsapp.com/send?phone={numero}&text={mensagem}')
        QDesktopServices.openUrl(url_mensagem)


    def envio_de_email(self):
        email = ui.campo_email_empresa.text()
        senha = ui.campo_senha_email.text()

        if not email or not senha:
            self.mensagem_alerta("ERRO","Necessário cadastrar o e-mail do agente na aba 'Configs' para envio")
            return

        try:
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
        

            tipo_mensagem, ok = QInputDialog.getItem(ui.centralwidget, "Envio", "Escolha o conteúdo do E-mail:", ["INICIO DE ATENDIMENTO", "SOLICITAR DOCUMENTOS","PROBLEMA DE PAGAMENTO","RENOVAÇÃO"], 0, False)
            if not ok:
                return
            
            tamanho_fonte = "17px"
            cor_botao_fundo = "rgb(89, 62, 255)"
            cor_botao_texto = "#FFFFFF"
            tamanho_fonte_footer = "12px"
            try:
                primeiro_nome = ui.campo_nome.text().split()[0]
            except:
                primeiro_nome = ""

            match tipo_mensagem:

                case "SOLICITAR DOCUMENTOS":
                    
                    certificado = ui.campo_lista_versao_certificado.currentText()
                    if "CNPJ" in certificado:
                        mensagem_inicial = self.determinar_hora(datetime.datetime.now().time())
                        assunto = f"Validação Certificado Digital - Pedido {ui.campo_pedido.text()}"
                        corpo_html = (
                            f"<!DOCTYPE html>"
                            f"<html lang='pt-BR'>"
                            f"<head>"
                            f"<meta charset='UTF-8'>"
                            f"<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
                            f"<style>"
                            f"  body {{ font-family: 'Montserrat', 'Poppins', Arial, sans-serif; color: #333333; margin: 0; padding: 0; background-color: #f7f7f7; font-size: 16px; }} "
                            f"  .container {{ width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); }} "
                            f"  .header {{ background-color: #4E4BFF; color: white; padding: 20px; border-top-left-radius: 8px; border-top-right-radius: 8px; text-align: center; }} "
                            f"  .header h1 {{ margin: 0; font-size: 24px; }} "
                            f"  .content {{ padding: 20px; }} "
                            f"  .content p, .content ul, .content li {{ font-size: 16px; line-height: 1.6; color: #333333; }} "
                            f"  .btn {{ display: inline-block; padding: 10px 20px; background-color: #4E4BFF; color: #ffffff !important; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 20px; text-align: center; }} "
                            f"  .btn:hover {{ background-color: #3b3ae3; transition: background-color 0.3s ease; }} "
                            f"  .footer {{ background-color: #f1f1f1; text-align: center; padding: 10px; font-size: 14px; color: #888888; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; }} "
                            f"</style>"
                            f"</head>"
                            f"<body>"
                            f"  <div class='container'>"
                            f"    <div class='header'><h1>Validação Certificado Digital</h1></div>"
                            f"    <div class='content'>"
                            f"      <p>{mensagem_inicial} {primeiro_nome.capitalize()}!</p>"
                            f"      <p>Espero que esteja bem.</p>"
                            f"      <p>Sou {nome} e sou agente de registro da ACB Digital.</p>"
                            f"      <p>Temos uma validação agendada para o seu certificado digital às <b>{hora}</b> do dia <b>{data}</b>.</p>"
                            f"      <p>Para agilizar a validação, preciso que o senhor(a) encaminhe respondendo a este e-mail, a relação de documentos abaixo:</p>"
                            f"      <ul>"
                            f"        <b>1 - Uma foto completa de seu documento de identificação(frente e verso), podendo ser um dos listados abaixo:</b>"
                            f"        <ul>"
                            f"          <li>CNH <a href='https://drive.google.com/file/d/1T-LCFCQ49C_L2GMal81GohFylKvoi88x/view?usp=drive_link'>[Exemplo]</a></li>"
                            f"          <li>CNH digital</li>"
                            f"          <li>RG (Apenas a versão física) <a href='https://drive.google.com/file/d/1vGPFx_6VcS7MJlAEXgyj0DNJY0Gp3i9-/view?usp=drive_link'>[Exemplo]</a></li>"
                            f"          <li>CREA</li>"
                            f"          <li>OAB</li>"
                            f"          <li>PASSAPORTE <a href='https://drive.google.com/file/d/1TQEUC5YLYY0yz72R4IY0xgbhKfXFq_Po/view?usp=drive_link'>[Exemplo]</a></li>"
                            f"        </ul>"
                            f"      </ul>"
                            f"      <p><b>Observações:</b><br>"
                            f"      (a) Retire o documento de identificação do plástico e abra-o.<br>"
                            f"      (b) O verso do documento é onde está o QRcode.</p><br>"
                            f"       - Ao lado está um link de exemplo "
                            f"      <ul>"
                            f"       <b>2 - O documento de constituição da empresa, podendo ser:</b>"
                            f"        <ul>"
                            f"          <li>Contrato Social</li>"
                            f"          <li>Certidão de inteiro teor</li>"
                            f"          <li>Estatuto social</li>"
                            f"          <li>Requerimento de empresário</li>"
                            f"        </ul>"
                            f"      </ul>"
                            f"      <a href='mailto:{ui.campo_email_empresa.text()}?subject=Documentos - Pedido {ui.campo_pedido.text()}' target='_blank' class='btn'>Enviar Documentos</a>"
                            f"    </div>"
                            f"    <div class='footer'>ACB Digital &copy; 2025. Todos os direitos reservados.</div>"
                            f"  </div>"
                            f"</body>"
                            f"</html>"
                        )

                    elif "CPF" in certificado and "OAB" in certificado:
                        mensagem_inicial = self.determinar_hora(datetime.datetime.now().time())
                        assunto = f"Validação Certificado Digital - Pedido {ui.campo_pedido.text()}"
                        corpo_html = (
                            f"<!DOCTYPE html>"
                            f"<html lang='pt-BR'>"
                            f"<head>"
                            f"<meta charset='UTF-8'>"
                            f"<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
                            f"<style>"
                            f"  body {{ font-family: 'Montserrat', 'Poppins', Arial, sans-serif; color: #333333; margin: 0; padding: 0; background-color: #f7f7f7; font-size: 16px; }} "
                            f"  .container {{ width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); }} "
                            f"  .header {{ background-color: #4E4BFF; color: white; padding: 20px; border-top-left-radius: 8px; border-top-right-radius: 8px; text-align: center; }} "
                            f"  .header h1 {{ margin: 0; font-size: 24px; }} "
                            f"  .content {{ padding: 20px; }} "
                            f"  .content p, .content ul, .content li {{ font-size: 16px; line-height: 1.6; color: #333333; }} "
                            f"  .btn {{ display: inline-block; padding: 10px 20px; background-color: #4E4BFF; color: #ffffff !important; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 20px; text-align: center; }} "
                            f"  .btn:hover {{ background-color: #3b3ae3; transition: background-color 0.3s ease; }} "
                            f"  .footer {{ background-color: #f1f1f1; text-align: center; padding: 10px; font-size: 14px; color: #888888; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; }} "
                            f"</style>"
                            f"</head>"
                            f"<body>"
                            f"  <div class='container'>"
                            f"    <div class='header'><h1>Validação Certificado Digital</h1></div>"
                            f"    <div class='content'>"
                            f"      <p>{mensagem_inicial} {primeiro_nome.capitalize()}!</p>"
                            f"      <p>Espero que esteja bem.</p>"
                            f"      <p>Sou {nome} e sou agente de registro da ACB Digital.</p>"
                            f"      <p>Temos uma validação agendada para o seu certificado digital às <b>{hora}</b> do dia <b>{data}</b>.</p>"
                            f"      <p>Para agilizar a validação, preciso que o senhor(a) encaminhe respondendo a este e-mail, uma foto completa de seu documento de identificação <b>OAB<b>, frente e verso</p><br>"
                            f"      <a href='mailto:{ui.campo_email_empresa.text()}?subject=Documentos - Pedido {ui.campo_pedido.text()}' target='_blank' class='btn'>Enviar Documentos</a>"
                            f"    </div>"
                            f"    <div class='footer'>ACB Digital &copy; 2025. Todos os direitos reservados.</div>"
                            f"  </div>"
                            f"</body>"
                            f"</html>"
                        )
                    
                    elif "CPF" in certificado:
                        mensagem_inicial = self.determinar_hora(datetime.datetime.now().time())
                        assunto = f"Validação Certificado Digital - Pedido {ui.campo_pedido.text()}"
                        corpo_html = (
                            f"<!DOCTYPE html>"
                            f"<html lang='pt-BR'>"
                            f"<head>"
                            f"<meta charset='UTF-8'>"
                            f"<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
                            f"<style>"
                            f"  body {{ font-family: 'Montserrat', 'Poppins', Arial, sans-serif; color: #333333; margin: 0; padding: 0; background-color: #f7f7f7; font-size: 16px; }} "
                            f"  .container {{ width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); }} "
                            f"  .header {{ background-color: #4E4BFF; color: white; padding: 20px; border-top-left-radius: 8px; border-top-right-radius: 8px; text-align: center; }} "
                            f"  .header h1 {{ margin: 0; font-size: 24px; }} "
                            f"  .content {{ padding: 20px; }} "
                            f"  .content p, .content ul, .content li {{ font-size: 16px; line-height: 1.6; color: #333333; }} "
                            f"  .btn {{ display: inline-block; padding: 10px 20px; background-color: #4E4BFF; color: #ffffff !important; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 20px; text-align: center; }} "
                            f"  .btn:hover {{ background-color: #3b3ae3; transition: background-color 0.3s ease; }} "
                            f"  .footer {{ background-color: #f1f1f1; text-align: center; padding: 10px; font-size: 14px; color: #888888; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; }} "
                            f"</style>"
                            f"</head>"
                            f"<body>"
                            f"  <div class='container'>"
                            f"    <div class='header'><h1>Validação Certificado Digital</h1></div>"
                            f"    <div class='content'>"
                            f"      <p>{mensagem_inicial} {primeiro_nome.capitalize()}!</p>"
                            f"      <p>Espero que esteja bem.</p>"
                            f"      <p>Sou {nome} e sou agente de registro da ACB Digital.</p>"
                            f"      <p>Temos uma validação agendada para o seu certificado digital às <b>{hora}</b> do dia <b>{data}</b>.</p>"
                            f"      <p>Para agilizar a validação, preciso que o senhor(a) encaminhe respondendo a este e-mail, a relação de documentos abaixo:</p>"
                            f"      <ul>"
                            f"        <b>1 - Uma foto completa de seu documento de identificação(frente e verso), podendo ser um dos listados abaixo:</b>"
                            f"        <ul>"
                            f"          <li>CNH <a href='https://drive.google.com/file/d/1T-LCFCQ49C_L2GMal81GohFylKvoi88x/view?usp=drive_link'>[Exemplo]</a></li>"
                            f"          <li>CNH digital</li>"
                            f"          <li>RG (Apenas a versão física) <a href='https://drive.google.com/file/d/1vGPFx_6VcS7MJlAEXgyj0DNJY0Gp3i9-/view?usp=drive_link'>[Exemplo]</a></li>"
                            f"          <li>CREA</li>"
                            f"          <li>OAB</li>"
                            f"          <li>PASSAPORTE <a href='https://drive.google.com/file/d/1TQEUC5YLYY0yz72R4IY0xgbhKfXFq_Po/view?usp=drive_link'>[Exemplo]</a></li>"
                            f"        </ul>"
                            f"      </ul>"
                            f"      <p><b>Observações:</b><br>"
                            f"      (a) Retire o documento de identificação do plástico e abra-o.<br>"
                            f"      (b) O verso do documento é onde está o QRcode.</p><br>"
                            f"      <a href='mailto:{ui.campo_email_empresa.text()}?subject=Documentos - Pedido {ui.campo_pedido.text()}' target='_blank' class='btn'>Enviar Documentos</a>"
                            f"    </div>"
                            f"    <div class='footer'>ACB Digital &copy; 2025. Todos os direitos reservados.</div>"
                            f"  </div>"
                            f"</body>"
                            f"</html>"
                        )



                case 'INICIO DE ATENDIMENTO':
                    mensagem_inicial = self.determinar_hora(datetime.datetime.now().time())
                    assunto = f"Validação Certificado Digital - Pedido {ui.campo_pedido.text()}"
                    
                    corpo_html = (
                        f"<!DOCTYPE html>"
                        f"<html lang='pt-BR'>"
                        f"<head>"
                        f"<meta charset='UTF-8'>"
                        f"<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
                        f"<style>"
                        f"  body {{ font-family: 'Montserrat', 'Poppins', Arial, sans-serif; color: #333333; margin: 0; padding: 0; background-color: #f7f7f7; text-align: left; font-size: {tamanho_fonte}; }} "
                        f"  .container {{ width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); text-align: left; }} "
                        f"  .header {{ background-color: #4E4BFF; color: white; padding: 20px; border-top-left-radius: 8px; border-top-right-radius: 8px; text-align: center; }} "
                        f"  .header h1 {{ margin: 0; font-size: 24px; color: white; font-family: 'Poppins', Arial, sans-serif; text-align: center; }} "
                        f"  .content {{ padding: 20px; text-align: left; }} "
                        f"  .content p {{ font-size: {tamanho_fonte}; line-height: 1.6; color: #333333; text-align: left; }} "
                        f"  .btn {{ display: inline-block; padding: 10px 20px; background-color: {cor_botao_fundo} !important; color: {cor_botao_texto} !important; text-decoration: none; border-radius: 5px; font-weight: bold; font-family: 'Montserrat', Arial, sans-serif; text-align: left; }} "
                        f"  .footer {{ background-color: #f1f1f1; text-align: center; padding: 10px; font-size: {tamanho_fonte_footer}; color: #888888; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; font-family: 'Poppins', Arial, sans-serif; }} "
                        f"  .align-left {{ text-align: left; font-size: 18px; }} "
                        f"</style>"
                        f"</head>"
                        f"<body>"
                        f"  <div class='container'>"
                        f"    <div class='header'><h1>Validação Certisign</h1></div>"
                        f"    <div class='content'>"
                        f"      <p>{mensagem_inicial} {primeiro_nome.capitalize()}!</p>"
                        f"      <p>Espero que esteja bem.</p>"
                        f"      <P>Sou {nome} e sou agente de registro da ACB Digital.</p>"
                        f"      <p>Estou entrando em contato para informar que temos uma validação agendada para o seu certificado digital às <b>{hora}</b> do dia <b>{data}</b>.</p>"
                        f"      <p>Atenciosamente,<br>{nome}</p>"
                        f"    </div>"
                        f"    <div class='footer'>ACB Digital &copy; 2024. Todos os direitos reservados.</div>"
                        f"  </div>"
                        f"</body>"
                        f"</html>"
                    )

                case 'PROBLEMA DE PAGAMENTO':
                    mensagem_inicial = self.determinar_hora(datetime.datetime.now().time())
                    assunto = f"Validação Certificado Digital - Pedido {ui.campo_pedido.text()}"
                    
                    corpo_html = (
                        f"<!DOCTYPE html>"
                        f"<html lang='pt-BR'>"
                        f"<head>"
                        f"<meta charset='UTF-8'>"
                        f"<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
                        f"<style>"
                        f"  body {{ font-family: 'Montserrat', 'Poppins', Arial, sans-serif; color: #333333; margin: 0; padding: 0; background-color: #f7f7f7; text-align: left; font-size: {tamanho_fonte}; }} "
                        f"  .container {{ width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); text-align: left; }} "
                        f"  .header {{ background-color: #4E4BFF; color: white; padding: 20px; border-top-left-radius: 8px; border-top-right-radius: 8px; text-align: center; }} "
                        f"  .header h1 {{ margin: 0; font-size: 24px; color: white; font-family: 'Poppins', Arial, sans-serif; text-align: center; }} "
                        f"  .content {{ padding: 20px; text-align: left; }} "
                        f"  .content p {{ font-size: {tamanho_fonte}; line-height: 1.6; color: #333333; text-align: left; }} "
                        f"  .btn {{ display: inline-block; padding: 10px 20px; background-color: {cor_botao_fundo} !important; color: {cor_botao_texto} !important; text-decoration: none; border-radius: 5px; font-weight: bold; font-family: 'Montserrat', Arial, sans-serif; text-align: left; }} "
                        f"  .footer {{ background-color: #f1f1f1; text-align: center; padding: 10px; font-size: {tamanho_fonte_footer}; color: #888888; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; font-family: 'Poppins', Arial, sans-serif; }} "
                        f"  .align-left {{ text-align: left; font-size: 18px; }} "
                        f"</style>"
                        f"</head>"
                        f"<body>"
                        f"  <div class='container'>"
                        f"    <div class='header'><h1>Validação Certisign</h1></div>"
                        f"    <div class='content'>"
                        f"      <p>{mensagem_inicial} {primeiro_nome.capitalize()}!</p>"
                        f"      <p>Espero que esteja bem.</p>"
                        f"      <P>Sou {nome} e sou agente de registro da ACB Digital.</p>"
                        f"      <p>Temos uma validação agendada para o seu certificado digital às <b>{hora}</b> do dia <b>{data}</b>.</p>"
                        f"      <p>No entanto, o pagamento ainda não foi reconhecido em nosso sistema. Para prosseguirmos com a validação, é necessário que o pagamento seja confirmado.</p>"
                        f"      <p>Peço que entre em contato com o suporte pelo telefone {ui.campo_telefone_sac_cliente.text()} para regularizar a situação.</p>"
                        f"      <p>Agradeço a compreensão.</p>"
                        f"      <p><br>Atenciosamente,<br>{nome}</p>"
                        f"    </div>"
                        f"    <div class='footer'>ACB Digital &copy; 2024. Todos os direitos reservados.</div>"
                        f"  </div>"
                        f"</body>"
                        f"</html>"
                    )
                    
                case 'RENOVAÇÃO':
                    # Ajustando o caminho correto com base na estrutura apresentada
                    
                    ref_link_venda = db.reference(f"Configuracoes/Certificados/{ui.campo_lista_versao_certificado.currentText()}/LINK VENDA")
                    certificado = ref_link_venda.get()
                    link_venda = f'{certificado}{ui.campo_cod_rev.text()}'
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
                        f"      <h1>Renovação do Certificado Digital</h1>"
                        f"    </div>"
                        f"    <div class='content'>"
                        f"      <p>{mensagem_inicial} {primeiro_nome.capitalize()}</p>"
                        f"      <p>Espero que esteja bem.</p>"
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

            if ui.campo_email.text():
                remetente = ui.campo_email_empresa.text()
                destinatarios = ui.campo_email.text()
                senha = ui.campo_senha_email.text()

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
        except:
            pass


    def mostrar_senha(self):
        if ui.campo_senha_email.echoMode() == QLineEdit.Password:
            ui.campo_senha_email.setEchoMode(QLineEdit.Normal)
        else:
            ui.campo_senha_email.setEchoMode(QLineEdit.Password)


    def mostrar_senha_usuario(self):
        if ui.campo_senha_usuario.echoMode() == QLineEdit.Password:
            ui.campo_senha_usuario.setEchoMode(QLineEdit.Normal)
        else:
            ui.campo_senha_usuario.setEchoMode(QLineEdit.Password)


    def envio_em_massa(self):
        email = ui.campo_email_empresa.text()
        senha = ui.campo_senha_email.text()

        if not email or not senha:
            self.mensagem_alerta("ERRO","Necessário cadastrar o e-mail do agente na aba 'Configs' para envio")
            return

        try:
            if not banco_dados.mensagem_confirmacao("Confirmação", f"Enviar email de renovação em massa?\n\nDe: {datetime.date.today().strftime('%d/%m/%Y')} \nAté {(datetime.date.today() + datetime.timedelta(days=ui.campo_dias_renovacao.value())).strftime('%d/%m/%Y')}"):

                return

            ui.tableWidget.setRowCount(0)  
            ui.tableWidget.setColumnCount(5) 
            ui.tableWidget.setHorizontalHeaderLabels(["PEDIDO OR","EMAIL", "ENVIADO?", "RETORNO", "PRAZO RESTANTE"]) 
            ui.tableWidget.setColumnWidth(0, 89)
            ui.tableWidget.setColumnWidth(1, 117)
            ui.tableWidget.setColumnWidth(2, 67)
            ui.tableWidget.setColumnWidth(3, 115)
            ui.tableWidget.setColumnWidth(4, 187)  

            pedidos_ref = ref.child(f"Usuario/{ui.campo_usuario.text()}/Dados/Pedidos").order_by_child("STATUS").equal_to("APROVADO")
            pedidos = pedidos_ref.get()

            ref_link_venda = db.reference(f"Configuracoes/Certificados")

            lista_certificados = ref_link_venda.get()
            range_validacao = ui.campo_dias_renovacao.value()

            if not pedidos:
                self.mensagem_alerta("Erro", "Nenhum pedido encontrado para as datas selecionadas.")
                QApplication.processEvents() 
                return

            total_pedidos = len(pedidos)
            progresso_atual = 0
            ui.barra_progresso_consulta.setMaximum(total_pedidos)
            QApplication.processEvents()  

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
                cliente_email = pedido_info.get("EMAIL", "")
                data_formatada_validacao = banco_dados.iso_para_data(pedido_info["DATA"]).toString("dd/MM/yyyy")

                email_ja_enviado = pedido_info.get("EMAIL RENOVACAO")

                data_validade_formatada = data_validade.strftime("%d/%m/%Y")

                msg_diferenca = (
                    f'Venceu há {abs(diferenca)} dias.\nVence em: {data_validade_formatada}' if diferenca < 0 else 
                    f'Restam {diferenca} dias.\nVence em: {data_validade_formatada}' if diferenca > 0 else 
                    f'Vence em: {data_validade_formatada}'      
                )

                motivo = ""
                enviado = "❌"
                enviar_email = False

                if not cliente_email:
                    motivo = "SEM EMAIL CADASTRADO"
                    ne += 1
                elif not pedido_info.get("VERSAO"):
                    motivo = "SEM PRODUTO CADASTRADO"
                    ne += 1
                elif pedido_info["STATUS"] != "APROVADO":
                    motivo = "PEDIDO NÃO APROVADO"
                    ne += 1
                elif not (0 <= diferenca <= range_validacao):
                    motivo = "FORA DO PRAZO DE RENOVAÇÃO"
                    ne += 1
                elif email_ja_enviado == "SIM":
                    motivo = "EMAIL JÁ ENVIADO"
                    ne += 1
                else:
                    motivo = "ENVIADO COM SUCESSO"
                    enviado = "✅"
                    enviar_email = True
                    env += 1

                    ref.child(f"Usuario/{ui.campo_usuario.text()}/Dados/Pedidos/").child(pedido_info["PEDIDO"]).update({"EMAIL RENOVACAO": "SIM"})


                row_position = ui.tableWidget.rowCount()
                ui.tableWidget.insertRow(row_position)

                pedido_item = QTableWidgetItem(str(pedido_info.get("PEDIDO", "")))
                pedido_item.setTextAlignment(Qt.AlignCenter)
                ui.tableWidget.setItem(row_position, 0, pedido_item)

                email_item = QTableWidgetItem(cliente_email)
                email_item.setTextAlignment(Qt.AlignCenter)
                ui.tableWidget.setItem(row_position, 1, email_item)

                enviado_item = QTableWidgetItem(enviado)
                enviado_item.setTextAlignment(Qt.AlignCenter)
                ui.tableWidget.setItem(row_position, 2, enviado_item)

                motivo_item = QTableWidgetItem(motivo)
                motivo_item.setTextAlignment(Qt.AlignCenter)
                ui.tableWidget.setItem(row_position, 3, motivo_item)

                prazo_item = QTableWidgetItem(str(msg_diferenca))  
                prazo_item.setTextAlignment(Qt.AlignCenter)
                ui.tableWidget.setItem(row_position, 4, prazo_item)

                QApplication.processEvents()
                
                # VERIFICA SE ENVIA OU NÃO O EMAIL
                if not enviar_email or pedido_info["VERSAO"] not in lista_certificados:
                    progresso_atual += 1
                    ui.barra_progresso_consulta.setValue(progresso_atual)
                    QApplication.processEvents()  
                
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

                        if diferenca > 0:
                            # CERTIFICADO VÁLIDO
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
                                f"      <p>Olá {primeiro_nome.capitalize()}</p>"
                                f"      <p>Espero que esteja bem.</p>"
                                f"      <p>Sou {nome}, agente de Registro da ACB Digital.</p>"
                                f"      <p>Fizemos a validação para seu certificado digital, modelo"
                                f"      <p><b>{pedido_info['VERSAO']}</b> no dia <b>{data_formatada_validacao}</b>.</p>"
                                f"      <p>Verifiquei que ele está próximo à data <b>vencimento</b> e entendemos a importância do certificado digital para seus negócios.</p>"
                                f"      <p>Para agilizar o processo de renovação, oferecemos a opção de renovar clicando no botão abaixo.</p>"
                                f"      <p><a href='{link_venda}' class='btn'>RENOVAR AGORA</a></p>"
                                f"      <p>Caso queira fazer a vídeo conferência, contate-me através do email:</p>"
                                f"      <p><a href='mailto:{ui.campo_email_empresa.text()}?subject=VALIDAÇÃO%20CERTIFICADO%20DIGITAL&body=Olá%20{ui.campo_nome_agente.text().split()[0].capitalize()},%20gostaria%20de%20agendar%20a%20validação%20para%20meu%20certificado%20digital.%0A%0ACPF:%0AData:%0AHora:' class='btn'>{ui.campo_email_empresa.text()}</a></p>"
                                f"      <p>Agradecemos pela confiança em nossos serviços e estamos à disposição para ajudá-lo!</p>"
                                f"      <br>" 
                                f"      <p>Atenciosamente,</p>"
                                f"      <p>{nome}</p>"
                                f"    </div>"
                                f"    <div class='footer'>"
                                f"      <p>ACB Serviços e Negócios &copy; 2025. Todos os direitos reservados.</p>"
                                f"    </div>"
                                f"  </div>"
                                f"</body>"
                                f"</html>"
                            )
                        
                        elif diferenca == 0:
                            # VENCE HOJE
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
                                f"      <p>Olá {primeiro_nome.capitalize()}!</p>"
                                f"      <p>Espero que esteja bem.</p>"
                                f"      <p>Sou {nome}, agente de Registro da ACB Digital.</p>"
                                f"      <p>Fizemos a validação para seu certificado digital, modelo"
                                f"      <p><b>{pedido_info['VERSAO']}</b> no dia <b>{data_formatada_validacao}</b>.</p>"
                                f"      <p>Verifiquei que ele vence <b>Hoje</b> e entendemos a importância do certificado digital para seus negócios.</p>"
                                f"      <p>Para agilizar o processo de renovação, oferecemos a opção de renovar clicando no botão abaixo.</p>"
                                f"      <p><a href='{link_venda}' class='btn'>RENOVAR AGORA</a></p>"
                                f"      <p>Caso queira fazer a vídeo conferência, contate-me através do email:</p>"
                                f"      <p><a href='mailto:{ui.campo_email_empresa.text()}?subject=VALIDAÇÃO%20CERTIFICADO%20DIGITAL&body=Olá%20{ui.campo_nome_agente.text().split()[0].capitalize()},%20gostaria%20de%20agendar%20a%20validação%20para%20meu%20certificado%20digital.%0A%0ACPF:%0AData:%0AHora:' class='btn'>{ui.campo_email_empresa.text()}</a></p>"
                                f"      <p>Agradecemos pela confiança em nossos serviços e estamos à disposição para ajudá-lo!</p>"
                                f"      <br>" 
                                f"      <p>Atenciosamente,</p>"
                                f"      <p>{nome}</p>"
                                f"    </div>"
                                f"    <div class='footer'>"
                                f"      <p>ACB Serviços e Negócios &copy; 2025. Todos os direitos reservados.</p>"
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
        except:
            pass


    def limpar_tabela(self):
        ui.campo_relatorio.setPlainText("")
        ui.campo_lista_status_2.setCurrentText("TODAS")
        ui.tableWidget.setRowCount(0)
        ui.label_quantidade_bd.setText("")

        for col in range(ui.tableWidget.columnCount()):
            ui.tableWidget.setColumnHidden(col, False)
        ui.tableWidget.setRowCount(0)
        ui.tableWidget.setColumnCount(6)
        self.ajuste_largura_col()


    def ajuste_largura_col(self):
        ui.tableWidget.setHorizontalHeaderLabels(["STATUS", "PEDIDO", "DATA", "HORA", "NOME", "VERSAO"])
        for col in range(ui.tableWidget.columnCount()):
                ui.tableWidget.setColumnWidth(col, 96)


    def mesclar_pdf_pasta_cliente(self):
        try:
            # Obter o caminho da pasta
            folder_to_open_directory = ui.caminho_pasta.text().strip()
            if not os.path.isdir(folder_to_open_directory):
                QMessageBox.warning(ui.centralwidget, "Erro", "O caminho especificado na pasta é inválido!")
                return

            # Obter os itens selecionados na tabela **antes de abrir qualquer diálogo**
            itens_selecionados = ui.tabela_documentos.selectedItems()
            if not itens_selecionados:
                QMessageBox.warning(ui.centralwidget, "Erro", "Nenhum documento foi selecionado na tabela!")
                return

            # Armazenar os nomes dos arquivos selecionados antes de abrir o diálogo
            nomes_arquivos = set(item.text().strip() for item in itens_selecionados)

            # Solicitar o nome do novo documento mesclado
            nome_documento, ok = QInputDialog.getItem(ui.centralwidget, "Nome do Documento", "Escolha o tipo de documento:", ["CNH COMPLETA", "RG COMPLETO","OAB COMPLETO","DOC ADICIONAL","DOC COMPLETO","OUTRO"], 0, False)
            
            if not ok or not nome_documento.strip():
                return  # Caso o usuário cancele ou não insira um nome válido

            if nome_documento == "OUTRO":
                nome_documento, ok = QInputDialog.getText(ui.centralwidget, "Nome do Documento", "Digite o nome do documento:")

            if not ok or not nome_documento.strip():
                return  # Caso o usuário cancele ou não insira um nome válido

            # Verificar os caminhos dos arquivos
            file_paths = [os.path.join(folder_to_open_directory, nome_arquivo) for nome_arquivo in nomes_arquivos]
            arquivos_existentes = [arquivo for arquivo in file_paths if os.path.isfile(arquivo)]

            if not arquivos_existentes:
                QMessageBox.warning(ui.centralwidget, "Erro", "Nenhum dos arquivos selecionados foi encontrado!")
                return

            # Verificar se alguns arquivos selecionados estão ausentes
            if len(arquivos_existentes) < len(file_paths):
                QMessageBox.warning(ui.centralwidget, "Aviso", "Alguns arquivos selecionados não foram encontrados!")

            # Mesclar os PDFs
            pdf_merger = PyPDF2.PdfMerger()
            for path in arquivos_existentes:
                pdf_merger.append(path)

            # Salvar o arquivo mesclado
            save_path = os.path.join(folder_to_open_directory, f"{nome_documento.strip()}.pdf")
            with open(save_path, 'wb') as merged_pdf:
                pdf_merger.write(merged_pdf)

            pdf_merger.close()

            # Exibir mensagem de sucesso e atualizar a tabela
            AlteracoesInterface.animar_label_pular(self,self.ui.botao_agrupar_PDF_pasta_cliente)
            self.atualizar_documentos_tabela()

        except Exception as e:
            QMessageBox.critical(ui.centralwidget, "Erro", f"Erro ao mesclar os documentos: {str(e)}")
            if 'pdf_merger' in locals():
                pdf_merger.close()
            self.atualizar_documentos_tabela()


    def calcular_comissao(self):
        porcentagem_validacao = int(ui.campo_porcentagem_validacao.value()) / 100
        imposto_de_renda = 1 - (ui.campo_imposto_validacao.value() / 100)
        desconto_validacao = float(ui.campo_desconto_validacao.text().replace(',', '.'))
        valor_certificado = float(ui.campo_preco_certificado_cheio.text().replace(',', '.'))

        valor_final = ((valor_certificado * porcentagem_validacao) * imposto_de_renda) - desconto_validacao
        if valor_final < 0:
            valor_final = 0

        valor_final_formatado = "{:,.2f}".format(valor_final).replace('.', ',').replace(',', '.', 1)

        return {
            "porcentagem_validacao": porcentagem_validacao,
            "imposto_de_renda": imposto_de_renda,
            "desconto_validacao": desconto_validacao,
            "valor_final": valor_final,
            "valor_final_formatado": valor_final_formatado
        }


    def buscar_preco_certificado(self):
        certificados = db.reference(f"Configuracoes/Certificados")
        lista_certificados = certificados.get()
        certificado = ui.campo_lista_versao_certificado.currentText()

        if certificado in lista_certificados:
            valor_do_certificado = float(lista_certificados[certificado]["VALOR"].replace(',', '.'))
            ui.campo_preco_certificado_cheio.setText(f"{valor_do_certificado:,.2f}".replace('.', ',').replace(',', '.', 1))

            self.atualizar_campos_comissao()

            midias = ["cartão", "token"]
            if any(midia in certificado.lower() for midia in midias):
                ui.alerta_midia.setText("⚠️")
                ui.alerta_midia.setToolTip("Certificado com Mídia\nLembre-se de pegar o endereço para envio")
            else:
                ui.alerta_midia.setText("")
                ui.alerta_midia.setToolTip("")


    def atualizar_campos_comissao(self):
        comissao = self.calcular_comissao()

        ui.campo_preco_certificado.setText(comissao["valor_final_formatado"])

        self.explica_valor(comissao)


    def explica_valor(self, comissao):
        valor_certificado = float(ui.campo_preco_certificado_cheio.text().replace(',', '.'))

        tooltip_text = (
            f"COMO CHEGUEI NESSE VALOR?\n"
            f"\n"
            f"Valor do certificado: R${valor_certificado:,.2f}".replace('.', ',').replace(',', '.', 1) + "\n"
            f"Porcentagem na validação ({comissao['porcentagem_validacao'] * 100:.1f}%): R${valor_certificado * comissao['porcentagem_validacao']:,.2f}".replace('.', ',').replace(',', '.', 1) + "\n"
            f"\n"
            f"(=)Valor Bruto: R${valor_certificado * comissao['porcentagem_validacao']:,.2f}".replace('.', ',').replace(',', '.', 1) + "\n"
            f"(-)Imposto de renda ({(1 - comissao['imposto_de_renda']) * 100:.1f}%): -R${valor_certificado * comissao['porcentagem_validacao'] * (1 - comissao['imposto_de_renda']):,.2f}".replace('.', ',').replace(',', '.', 1) + "\n"
            f"(=)Valor líquido: R${valor_certificado * comissao['porcentagem_validacao'] * comissao['imposto_de_renda']:,.2f}".replace('.', ',').replace(',', '.', 1) + "\n"
            f"(-) Desconto adicional: -R${comissao['desconto_validacao']:,.2f}".replace('.', ',').replace(',', '.', 1) + "\n"
            f"---------------------------------\n"
            f"Valor final: R${comissao['valor_final_formatado']}\n\n"
            f"*Esse valor é apenas uma aproximação"
        )

        ui.campo_preco_certificado.setToolTip(tooltip_text)
        





class AcoesBancoDeDados():
    def __init__(self, ui):
        self.ui = ui
        

    def salvar_pedido(self):
        self.ref = db.reference(f"Usuario/{ui.campo_usuario.text()}/Dados/Pedidos")
        try:
            if not self.analise_de_campos():
                return

            num_pedido = self.ui.campo_pedido.text()
            novo_pedido_ref = self.ref.child(num_pedido)

            # Verifica se o pedido já existe
            pedido_existente = novo_pedido_ref.get() is not None
            condic = self.verificar_status()

            if condic == 'DEFINITIVO' and not self.mensagem_confirmacao("Confirmação", f"Salvar pedido como {banco_dados.alteracao_status()}?"):
                return

            if condic == 'DEFINITIVO':
                self.salvar_definitivo(novo_pedido_ref)
            else:
                self.salvar_temporario(novo_pedido_ref)

            self.atualizar_ui(condic, pedido_existente)

        except Exception as e:
            print(e)


    def salvar_temporario(self, novo_pedido_ref):
        novo_pedido_ref.update(self.dicionario_banco_de_dados())


    def salvar_definitivo(self, novo_pedido_ref):
        self.forcar_fechamento_de_arquivo_e_deletar_pasta(self.ui.caminho_pasta.text())
        self.verificar_midia()
        novo_pedido_ref.set(self.dicionario_banco_de_dados())


    def verificar_midia(self):
        # Determina a mídia com base no certificado
        certificado = self.ui.campo_lista_versao_certificado.currentText().lower()
        if "cartão e leitora" in certificado:
            midia = "CARTÃO E LEITORA"
        elif "cartão" in certificado:
            midia = "CARTÃO"
        elif "token" in certificado:
            midia = "TOKEN"
        else:
            midia = "Mídia não especificada"

        # Verifica se o certificado possui mídia e se está aprovado
        if any(chave in certificado for chave in ["cartão", "token", "leitora"]) and self.ui.rb_aprovado.isChecked() and self.ui.campo_lista_modalidade.currentText() == "VIDEO":
            QMessageBox.warning(
                self.ui.centralwidget,
                "ALERTA",
                "Esse pedido contém mídia.\nEnviar e-mail com os dados do cliente para envio de mídia."
            )

            janela = None

            # Função para enviar o e-mail
            def enviar_email():
                nonlocal janela
                destinatario = input_destinatario.text()
                assunto = input_assunto.text()
                endereco = text_endereco.toPlainText()

                remetente = self.ui.campo_email_empresa.text()
                senha = self.ui.campo_senha_email.text()

                if not endereco.strip():
                    QMessageBox.warning(janela, "Erro", "O campo 'Endereço' está vazio. Preencha o endereço antes de enviar!")
                    return

                if not remetente or not senha:
                    QMessageBox.warning(janela, "Erro", "O e-mail ou a senha do remetente não foram preenchidos!")
                    return

                try:
                    corpo_html = (
                        f"<!DOCTYPE html>"
                        f"<html lang='pt-BR'>"
                        f"<head>"
                        f"<meta charset='UTF-8'>"
                        f"<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
                        f"<link href='https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Poppins:wght@400;700&display=swap' rel='stylesheet'>"
                        f"<style>"
                        f"  body {{ font-family: 'Montserrat', 'Poppins', Arial, sans-serif; color: #333333; margin: 0; padding: 0; background-color: #f7f7f7; }} "
                        f"  .container {{ width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); }} "
                        f"  .header {{ background-color: #4E4BFF; color: white; padding: 20px; border-top-left-radius: 8px; border-top-right-radius: 8px; }} "
                        f"  .header h1 {{ margin: 0; font-size: 24px; }} "
                        f"  .content {{ padding: 20px; }} "
                        f"  .content p {{ font-size: 16px; line-height: 1.6; color: #333333; }} "
                        f"  .footer {{ background-color: #f1f1f1; text-align: center; padding: 10px; font-size: 14px; color: #888888; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; }} "
                        f"</style>"
                        f"</head>"
                        f"<body>"
                        f"  <div class='container'>"
                        f"    <div class='header'>"
                        f"      <h1>Envio de Mídia</h1>"
                        f"    </div>"
                        f"    <div class='content'>"
                        f"      <p><b>Nome do Cliente:</b> {self.ui.campo_nome.text()}</p>"
                        f"      <p><b>Mídia:</b> {midia}</p>"
                        f"      <p><b>Pedido:</b> {self.ui.campo_pedido.text()}</p>"
                        f"      <p><b>Endereço:</b> {endereco}</p>"
                        f"    </div>"
                        f"    <div class='footer'>"
                        f"      <p>ACB Serviços e Negócios &copy; 2025. Todos os direitos reservados.</p>"
                        f"    </div>"
                        f"  </div>"
                        f"</body>"
                        f"</html>"
                    )

                    msg = MIMEMultipart("alternative")
                    msg['Subject'] = assunto
                    msg['From'] = remetente
                    msg['To'] = destinatario
                    msg.add_header('Disposition-Notification-To', remetente)  
                    msg.add_header('Return-Receipt-To', remetente)  
                    msg.attach(MIMEText(corpo_html, "html"))

                    with smtplib.SMTP_SSL('email-ssl.com.br', 465) as smtp_server:
                        smtp_server.login(remetente, senha)
                        smtp_server.sendmail(remetente, destinatario, msg.as_string())

                    QMessageBox.information(janela, "Sucesso", "E-mail enviado com sucesso!")
                    if janela.isVisible():
                        janela.close()

                except smtplib.SMTPException as e:
                    QMessageBox.critical(janela, "Erro", f"Falha ao enviar o e-mail: {e}")

            # Função para cancelar e fechar a janela
            def cancelar():
                if janela.isVisible():
                    janela.close()

            janela = QDialog(self.ui.centralwidget)
            janela.setWindowTitle("Enviar E-mail")
            janela.setFixedSize(550, 300)


            principal_geometry = self.ui.centralwidget.geometry()
            principal_pos = self.ui.centralwidget.mapToGlobal(principal_geometry.topLeft())
            principal_width = principal_geometry.width()

            # Posicionar a janela ao lado da principal
            janela_x = principal_pos.x() - principal_width - 10  # Adicionar margem de 10 pixels
            janela_y = principal_pos.y()
            janela.move(janela_x, janela_y)

            # Definir estilos
            fundo_cor = "rgb(60, 62, 84)"
            campo_texto_cor = "rgb(210, 210, 210)"
            campo_fundo_cor = "rgb(40, 45, 50)"
            estilo_fonte = f"font-family: 'Calibri'; font-size: 14px;"
            
            botao_enviar_hover = "rgb(0, 122, 255)"
            botao_enviar_cor = "rgb(0, 102, 215)"

            botao_cancelar_hover = "rgb(255, 0, 0)"
            botao_cancelar_cor = "rgb(215, 0, 0)"

            janela.setStyleSheet(f"background-color: {fundo_cor}; color: {campo_texto_cor};")


            layout = QVBoxLayout()

            label_destinatario = QLabel("E-mail do Destinatário:")
            input_destinatario = QLineEdit()
            input_destinatario.setText("agendamento@acbdigital.com.br")
            input_destinatario.setStyleSheet(
                f"background-color: {campo_fundo_cor}; color: {campo_texto_cor}; padding: 5px; border-radius: 5px;{estilo_fonte}"
            )
            layout.addWidget(label_destinatario)
            layout.addWidget(input_destinatario)

            spacer = QSpacerItem(30, 200, QSizePolicy.Minimum, QSizePolicy.Expanding)
            layout.addItem(spacer)

            label_assunto = QLabel("Assunto:")
            input_assunto = QLineEdit()
            input_assunto.setText(f"ENVIO DE {midia} - PEDIDO {self.ui.campo_pedido.text()}")
            input_assunto.setStyleSheet(
                f"background-color: {campo_fundo_cor}; color: {campo_texto_cor}; padding: 5px; border-radius: 5px;{estilo_fonte}"
            )
            layout.addWidget(label_assunto)
            layout.addWidget(input_assunto)

            spacer = QSpacerItem(30, 200, QSizePolicy.Minimum, QSizePolicy.Expanding)
            layout.addItem(spacer)

            label_endereco = QLabel("Endereço do cliente:")
            text_endereco = QTextEdit()
            text_endereco.setText(self.ui.campo_comentario.toPlainText())
            text_endereco.setStyleSheet(
                f"background-color: {campo_fundo_cor}; color: {campo_texto_cor}; padding: 5px; border-radius: 5px;{estilo_fonte}"
            )
            layout.addWidget(label_endereco)
            layout.addWidget(text_endereco)

            spacer = QSpacerItem(30, 200, QSizePolicy.Minimum, QSizePolicy.Expanding)
            layout.addItem(spacer)

            layout_botoes = QHBoxLayout()
            botao_enviar = QPushButton("Enviar E-mail")
            botao_enviar.setStyleSheet(
                f"background-color: {botao_enviar_cor}; color: {campo_texto_cor}; padding: 5px; border-radius: 5px;{estilo_fonte}"
            )
            botao_enviar.clicked.connect(enviar_email)
            layout_botoes.addWidget(botao_enviar)

            botao_cancelar = QPushButton("Cancelar")
            botao_cancelar.setStyleSheet(
                f"background-color: {botao_cancelar_cor}; color: {campo_texto_cor}; padding: 5px; border-radius: 5px;{estilo_fonte}"
            )
            botao_cancelar.clicked.connect(cancelar)
            layout_botoes.addWidget(botao_cancelar)

            layout.addLayout(layout_botoes)

            # Adicionar estilos de hover aos botões
            botao_enviar.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {botao_enviar_cor};
                    color: {campo_texto_cor};
                    padding: 5px;
                    border-radius: 5px;{estilo_fonte}
                }}
                QPushButton:hover {{
                    background-color: {botao_enviar_hover};
                }}
                """
            )

            botao_cancelar.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {botao_cancelar_cor};
                    color: {campo_texto_cor};
                    padding: 5px;
                    border-radius: 5px;{estilo_fonte}
                }}
                QPushButton:hover {{
                    background-color: {botao_cancelar_hover};
                }}
                """
            )

            janela.setLayout(layout)
            janela.exec_()


    def atualizar_ui(self, condic, pedido_existente):
        if condic == 'DEFINITIVO':
            self.ui.campo_status_bd.setText("")
            self.ui.campo_status_bd.setToolTip("")
            self.apagar_campos_pedido(0)
            AlteracoesInterface.lixeira_label_criar_pasta(self)

        else:
            AlteracoesInterface.label_status_bd_atualizado(self)
            self.ui.campo_status_bd.setToolTip("Pedido Atualizado")

        AlteracoesInterface.confirmar_label_salvar(self)

        self.contar_verificacao()
        funcoes_app.ajuste_largura_col()
        

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
     
        variaveis = [pedido,hora,data,versao,modalidade]

        nomes_mensagens = {
            "pedido": "Pedido",
            "hora": "Hora",
            "data":"Data",
            "versao":"Versao",
            "modalidade":"Atendimento"
        }

        campos_vazios = [nomes_mensagens[nome_variavel] for nome_variavel, valor in zip(["pedido","hora","data","versao","modalidade"], variaveis) if (isinstance(valor, str) and valor == "") or (nome_variavel == "hora" and valor == "00:00") or (nome_variavel == "data" and valor == "01/01/2000")]

        if campos_vazios:
            campos_faltando = "\n⭐ ".join(campos_vazios)
            mensagem_alerta = f"Preencha os seguintes campos para salvar o pedido!\n⭐{campos_faltando}"
            self.mensagem_alerta("Erro no envio", mensagem_alerta)
            AlteracoesInterface.negar_label_salvar(self)

            return False
        return True


    def apagar_campos_pedido(self,origem):
        if origem == 1:
            if not self.mensagem_confirmacao("","Apagar dados?"):
                return
        try:
            #Dados pedido  
            ui.tableWidget.horizontalHeader().setDefaultSectionSize(96)
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
            ui.campo_funcional.setText("")
            ui.campo_preco_certificado_cheio.setText("")
            ui.campo_email_enviado.setText("")
            ui.alerta_midia.setText("")
            ui.alerta_midia.setToolTip("")
            self.limpar_labels()
            self.contar_verificacao()
            AlteracoesInterface.confirmar_label_excluir(self)



        except Exception as e:
            print(e)


    def limpar_labels(self):
        
       
        ui.rb_digitacao.setChecked(True)
        self.alteracao_status()
        ui.campo_status_bd.setText("")
        ui.label_confirmacao_converter_pdf.setText("")
        ui.label_confirmacao_criar_pasta.setText("")
        ui.label_confirmacao_mesclar_pdf.setText("")
        ui.label_confirmacao_tirar_print.setText("")
        ui.label_confirmacao_salvar.setText("")
        ui.campo_comentario.setStyleSheet("border-radius:7px;border: 1px solid rgb(120,120,120);background-color:rgb(60,62, 84);color:orange")
        ui.label_confirmacao_excluir.setText("")

       
    def dicionario_banco_de_dados(self):


        data_qdate = ui.campo_data_agendamento.date()  # Retorna um QDate
        data_validacao = datetime.datetime(data_qdate.year(), data_qdate.month(), data_qdate.day())


        versao_certificado = str(ui.campo_lista_versao_certificado.currentText()).strip()


        if "12" in versao_certificado:
            dias_duracao = 365
        elif "18" in versao_certificado:
            dias_duracao = 540
        elif "24" in versao_certificado:
            dias_duracao = 720
        elif "36" in versao_certificado:
            dias_duracao = 1080
        else:
            dias_duracao = 0  


        duracao_certificado = data_validacao + datetime.timedelta(days=dias_duracao)

        # Renova status se o email foi enviado
        renova = "SIM" if ui.campo_email_enviado.text() == "SIM" else "NAO"

        # Dados do pedido
        novos_dados = {
            "PASTA": ui.caminho_pasta.text(),
            "MUNICIPIO": ui.campo_cnpj_municipio.text(),
            "DIRETORIO": ui.campo_comentario.toPlainText(),
            "CODIGO DE SEG CNH": ui.campo_seguranca_cnh.text(),
            "NOME": ui.campo_nome.text(),
            "RG": ui.campo_rg.text(),
            "CPF": ui.campo_cpf.text(),
            "CNH": ui.campo_cnh.text(),
            "MAE": ui.campo_nome_mae.text(),
            "CNPJ": ui.campo_cnpj.text(),
            "EMAIL": ui.campo_email.text(),
            "NASCIMENTO": ui.campo_data_nascimento.text(),
            "STATUS": self.alteracao_status(),
            "PEDIDO": ui.campo_pedido.text(),
            "DATA": self.data_para_iso(QDateTime(ui.campo_data_agendamento.date())),  # Passando o QDateTime
            "HORA": ui.campo_hora_agendamento.text(),
            "VENDA": ui.campo_lista_venda.currentText(),
            "MODALIDADE": ui.campo_lista_modalidade.currentText(),
            "VERSAO": ui.campo_lista_versao_certificado.currentText(),
            "PRECO": ui.campo_preco_certificado.text(),
            "RAZAO SOCIAL": ui.campo_cnpj_razao_social.text(),
            "ORGAO RG": ui.campo_rg_orgao.text(),
            "PIS": ui.campo_pis.text(),
            "TELEFONE": ui.campo_telefone.text(),
            "OAB": ui.campo_funcional.text(),
            "EMAIL RENOVACAO": renova,
            "PRECO CERTIFICADO":ui.campo_preco_certificado_cheio.text(),
            "VALIDO ATE": self.data_para_iso(QDateTime.fromString(duracao_certificado.strftime('%Y-%m-%d %H:%M:%S'), 'yyyy-MM-dd HH:mm:ss'))  # Data ajustada com validade
        }

        # Se o status for DEFINITIVO, adiciona a data de validade e limpa campos
        if self.verificar_status() == "DEFINITIVO":
            campos_para_limpar = [
                "PASTA", "MUNICIPIO", "CODIGO DE SEG CNH", "RG", "CPF", "CNH", "MAE", 
                "CNPJ", "NASCIMENTO", "RAZAO SOCIAL", "ORGAO RG", "PIS", "OAB"
            ]
            novos_dados.update({campo: None for campo in campos_para_limpar})

            # Adiciona a data de validade no formato ISO
            novos_dados["VALIDO ATE"] = self.data_para_iso(QDateTime.fromString(duracao_certificado.strftime('%Y-%m-%d %H:%M:%S'), 'yyyy-MM-dd HH:mm:ss'))

        # Filtra as chaves que não são vazias
        dados_filtrados = {chave: valor for chave, valor in novos_dados.items() if valor not in [None, ""]}

        return dados_filtrados


    def forcar_fechamento_de_arquivo_e_deletar_pasta(self,folder_path):
        for _ in range(3):  # Tenta fehar por 3 vezes
            try:
                shutil.rmtree(folder_path)
                return 
                
            except PermissionError as e:
                # Se a exclusão falhar devido a permissões, tenta fechar os arquivos em uso antes da próxima tentativa
                self.fechar_arquivo_em_uso(folder_path)

            except Exception as e:
                if not os.path.exists(folder_path):  # Verifica se a pasta não existe
                    return ""
                return "Erro ao excluir pasta do cliente"


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
        self.ref = db.reference(f"Usuario/{ui.campo_usuario.text()}/Dados/Pedidos/")

        try:
            num_pedido = ui.campo_pedido.text()

            if num_pedido == "":
                return

            pedido_ref = self.ref.child(num_pedido)
            pedido_data = pedido_ref.get()

            if pedido_data:

                self.preencher_dados(pedido_data)

               
            else:  
               return 'Pedido nao existe'

        except Exception as e:
            pass


    def pegar_valor_tabela(self):
        self.ref = db.reference(f"Usuario/{ui.campo_usuario.text()}/Dados/Pedidos/")
   #evento disparado ao dar double click na tabela

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
                    AlteracoesInterface.label_status_bd_atualizado(self)

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


    def preencher_dados(self, pedido_data):
        self.apagar_campos_pedido(0)  # Limpa os campos antes de começar a preencher

        campos = [
            (ui.campo_nome, "NOME"),
            (ui.campo_rg, "RG"),
            (ui.campo_cpf, "CPF"),
            (ui.campo_cnh, "CNH"),
            (ui.campo_cnpj, "CNPJ"),
            (ui.campo_email, "EMAIL"),
            (ui.campo_pedido, "PEDIDO"),
            (ui.campo_seguranca_cnh, "CODIGO DE SEG CNH"),
            (ui.campo_nome_mae, "MAE"),
            (ui.campo_comentario, "DIRETORIO"),
            (ui.campo_cnpj_municipio, "MUNICIPIO"),
            (ui.caminho_pasta, "PASTA"),
            (ui.campo_lista_venda, "VENDA"),
            (ui.campo_lista_modalidade, "MODALIDADE"),
            (ui.campo_lista_versao_certificado, "VERSAO"),
            (ui.campo_rg_orgao, "ORGAO RG"),
            (ui.campo_cnpj_razao_social, "RAZAO SOCIAL"),
            (ui.campo_pis, "PIS"),
            (ui.campo_preco_certificado, "PRECO"),
            (ui.campo_telefone, "TELEFONE"),
            (ui.campo_funcional, "OAB"),
            (ui.campo_email_enviado, "EMAIL RENOVACAO"),
            (ui.campo_preco_certificado_cheio,"PRECO CERTIFICADO")
        ]

        for campo, chave in campos:
            try:
                valor = pedido_data.get(chave)
                if valor:  
                    if isinstance(campo, QComboBox):
                        campo.setCurrentText(valor)
                    else:
                        campo.setText(valor)
            except Exception as e:
                print(f"Erro ao preencher o campo '{chave}': {e}")

        try:
            nascimento = pedido_data.get("NASCIMENTO")
            if nascimento:
                ui.campo_data_nascimento.setDate(QDate.fromString(nascimento, "dd/MM/yyyy"))
        except Exception as e:
            print(f"Erro ao preencher data de nascimento: {e}")

        try:
            data = pedido_data.get("DATA")
            if data:
                ui.campo_data_agendamento.setDate(self.iso_para_data(data).date())
        except Exception as e:
            print(f"Erro ao preencher data de agendamento: {e}")

        try:
            hora = pedido_data.get("HORA")
            if hora:
                ui.campo_hora_agendamento.setTime(QTime.fromString(hora, "hh:mm"))
        except Exception as e:
            print(f"Erro ao preencher hora de agendamento: {e}")

        try:
            status = pedido_data.get("STATUS")
            if status:
                if status == "DIGITAÇÃO":
                    self.ui.groupBox_status.findChild(QtWidgets.QRadioButton, "rb_digitacao").setChecked(True)
                    self.alteracao_status()
                elif status == "VIDEO REALIZADA":
                    self.ui.groupBox_status.findChild(QtWidgets.QRadioButton, "rb_videook").setChecked(True)
                    self.alteracao_status()
                elif status == "VERIFICAÇÃO":
                    self.ui.groupBox_status.findChild(QtWidgets.QRadioButton, "rb_verificacao").setChecked(True)
                    self.alteracao_status()
                elif status == "APROVADO":
                    self.ui.groupBox_status.findChild(QtWidgets.QRadioButton, "rb_aprovado").setChecked(True)
                    self.alteracao_status()
                elif status == "CANCELADO":
                    self.ui.groupBox_status.findChild(QtWidgets.QRadioButton, "rb_cancelado").setChecked(True)
                    self.alteracao_status()

            AlteracoesInterface.label_status_bd_atualizado(self)

            
            ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed) 
            for i in range(ui.tableWidget.columnCount()): 
                ui.tableWidget.horizontalHeader().resizeSection(i, 96)

            
        except Exception as e:
            print(f"Erro ao atualizar o status: {e}")

        # Atualizar o campo de confirmação de pasta
        try:
            if ui.caminho_pasta.text():
                AlteracoesInterface.confirmar_label_criar_pasta(self)
        except Exception as e:
            print(f"Erro ao atualizar confirmação de pasta: {e}")


    def contar_verificacao(self):
        # Consulta no Firebase para pedidos com status "VERIFICAÇÃO"
        pedidos_verificacao = ref.child(f"Usuario/{ui.campo_usuario.text()}/Dados/Pedidos/").order_by_child("STATUS").equal_to("VERIFICAÇÃO").get()
        
        # Consulta no Firebase para pedidos com status "VIDEO REALIZADA"
        pedidos_videook = ref.child(f"Usuario/{ui.campo_usuario.text()}/Dados/Pedidos/").order_by_child("STATUS").equal_to("VIDEO REALIZADA").get()

        quantidade_verificacao = 0  
        quantidade_videook = 0 
        verificacao_info = []  
        videook_info = []  

        if pedidos_verificacao:
            for pedido_info in pedidos_verificacao.values():
                quantidade_verificacao += 1
                data_pedido = datetime.datetime.strptime(pedido_info['DATA'], "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y")
                numero_pedido = pedido_info['PEDIDO']
                verificacao_info.append(f"Pedido: {numero_pedido} / Data: {data_pedido}")

        if pedidos_videook:
            for pedido_info in pedidos_videook.values():
                quantidade_videook += 1
                data_pedido = datetime.datetime.strptime(pedido_info['DATA'], "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y")
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
    #Evento disparado quando clico no botão procurar na aba 'Consulta'
        if hasattr(self, 'carregando_dados') and self.carregando_dados:
            return  # Se já estiver carregando, ignora o clique

        
        try:
            self.carregando_dados = True
            data_inicial = self.data_para_iso(QDateTime(ui.campo_data_de.date()))
            data_final = self.data_para_iso(QDateTime(ui.campo_data_ate.date()))
            
            certificados_ref = ref.child(f"Configuracoes/Certificados")
            certificados = certificados_ref.get()

            pedidos_ref = ref.child(f"Usuario/{ui.campo_usuario.text()}/Dados/Pedidos").order_by_child("DATA").start_at(data_inicial).end_at(data_final)
            pedidos = pedidos_ref.get()

            for col in range(ui.tableWidget.columnCount()):
                ui.tableWidget.setColumnHidden(col, False)
            ui.tableWidget.setRowCount(0)
            ui.tableWidget.setColumnCount(6)
            ui.tableWidget.setHorizontalHeaderLabels(["STATUS", "PEDIDO", "DATA", "HORA", "NOME", "VERSAO"])
            
            funcoes_app.ajuste_largura_col()

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
                funcoes_app.ajuste_largura_col()
                valor_venda = 0

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
                                        try:
                                            valor_venda += (float(pedido_info['PRECO CERTIFICADO'])) * (ui.campo_porcentagem_venda.value()/100)
                                        except:
                                            versao = pedido_info['VERSAO']
                                            valor = certificados[versao]['VALOR']
                                            valor = float(valor.replace(',', '.')) 
                                            valor_venda += valor * (ui.campo_porcentagem_venda.value()/100)


                                QApplication.processEvents()
                            except Exception as e:
                                print (e)

                            for col in range(ui.tableWidget.columnCount()):
                                item = ui.tableWidget.item(row_position, col)
                                status = ui.tableWidget.item(row_position, 0).text()
                                if item is not None:
                                    match status:
                                        case 'DIGITAÇÃO':
                                            item.setForeground(QColor(170, 170, 170))
                                        case 'VIDEO REALIZADA':
                                            item.setForeground(QColor(25, 200, 255))
                                        case 'VERIFICAÇÃO':
                                            item.setForeground(QColor(255, 167, 91))
                                        case 'APROVADO':
                                            item.setForeground(QColor(173, 255, 47))
                                        case 'CANCELADO':
                                            item.setForeground(QColor(255, 30, 30))

                            y += 1
                            ui.barra_progresso_consulta.setValue(y)
                            QApplication.processEvents()

                ui.barra_progresso_consulta.setValue(total_pedidos)  
                self.contar_verificacao()

                total_venda = valor_cnpj + valor_cpf
                total_geral = (total_venda * (1 - float(ui.campo_desconto.text()) / 100)) + valor_venda
                locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

                ui.campo_relatorio.setPlainText(f'''
(+)e-CNPJ [{j}]..................R$ {locale.format_string('%.2f', valor_cnpj, grouping=True) if valor_cnpj != 0 else "0,00"}
(+)e-CPF [{f}]...................R$ {locale.format_string('%.2f', valor_cpf, grouping=True) if valor_cpf != 0 else "0,00"}
(=)Total [{j+f}]...................R$ {locale.format_string('%.2f', total_venda, grouping=True) if total_venda != 0 else "0,00"}
(-){ui.campo_desconto.text()}%..........................R$ {locale.format_string('%.2f', total_venda * (float(ui.campo_desconto.text()) / 100), grouping=True) if total_venda != 0 else "0,00"}
---------------------------------------------
(=)Total Esperado...............R$ {locale.format_string('%.2f', total_venda * (1 - float(ui.campo_desconto.text()) / 100), grouping=True) if total_venda != 0 else "0,00"}
(+)Vendas [{venda}]...................R$ {locale.format_string('%.2f', valor_venda, grouping=True) if valor_venda != 0 else "0,00"}
---------------------------------------------
(=)Total Esperado + Vendas .....R$ {locale.format_string('%.2f', total_geral, grouping=True) if total_geral != 0 else "0,00"}
''')

                ui.barra_progresso_consulta.setVisible(False)
                ui.label_quantidade_bd.setText(f"{x} registro(s)")
                ui.tableWidget.setHorizontalHeaderLabels(["STATUS", "PEDIDO", "DATA", "HORA", "NOME", "VERSAO"])
                
            except Exception as e:
                print(e)
                ui.campo_relatorio.setPlainText("")
                ui.tableWidget.setHorizontalHeaderLabels(["STATUS", "PEDIDO", "DATA", "HORA", "NOME", "VERSAO"])
                
                funcoes_app.ajuste_largura_col()

                ui.label_quantidade_bd.setText(f"{x} registro(s)")

                ui.barra_progresso_consulta.setVisible(False)
                self.contar_verificacao()
        except Exception as e:
            print(e)
            pass

        finally:
            # Marca como não carregando
            self.carregando_dados = False
 

    def atualizar_documentos_tabela(self):
        # Limpar qualquer conteúdo existente na tabela
        self.ui.tabela_documentos.clearContents()

        pasta_cliente = self.ui.caminho_pasta.text()

        if not os.path.exists(pasta_cliente):
            return

        documentos = os.listdir(pasta_cliente)

        pdfs = [doc for doc in documentos if doc.lower().endswith('.pdf')]
        outros_documentos = [doc for doc in documentos if not doc.lower().endswith('.pdf')]

        num_documentos = len(pdfs)
        self.ui.tabela_documentos.setRowCount(num_documentos)

        for i, documento in enumerate(pdfs):

            item_nome_documento = QTableWidgetItem(documento)

            item_nome_documento.setForeground(QColor(255, 0, 0))

            self.ui.tabela_documentos.setItem(i, 0, item_nome_documento)

        num_outros_documentos = len(outros_documentos)
        self.ui.tabela_documentos.setRowCount(num_documentos + num_outros_documentos)

        for i, documento in enumerate(outros_documentos):

            item_nome_documento = QTableWidgetItem(documento)

            item_nome_documento.setForeground(QColor(128, 128, 128))

            self.ui.tabela_documentos.setItem(num_documentos + i, 0, item_nome_documento)


    def alteracao_status(self):
        #AQUI VAI VERIFICAR SE
        if ui.rb_digitacao.isChecked():
            self.zerar_cor()
            ui.rb_digitacao.setStyleSheet("border:none;color: rgb(255,255,255);")  
            return 'DIGITAÇÃO'
        elif ui.rb_videook.isChecked():
            self.zerar_cor()
            ui.rb_videook.setStyleSheet("border:none;color: rgb(18,191,255);")  
            return 'VIDEO REALIZADA'
        elif ui.rb_verificacao.isChecked():
            self.zerar_cor()
            ui.rb_verificacao.setStyleSheet("border:none;color: orange;")  
            return 'VERIFICAÇÃO'
        elif ui.rb_aprovado.isChecked():
            self.zerar_cor()
            ui.rb_aprovado.setStyleSheet("border:none;color:rgb(173, 255, 47);")  
            return 'APROVADO'
        elif ui.rb_cancelado.isChecked():
            self.zerar_cor()
            ui.rb_cancelado.setStyleSheet("border:none;color: red;")  
            return 'CANCELADO'


    def zerar_cor(self):
        
        ui.rb_digitacao.setStyleSheet("border:none; color:rgb(255,255,255);")  
        ui.rb_videook.setStyleSheet("border:none; color:rgb(255,255,255);")
        ui.rb_verificacao.setStyleSheet("border:none; color:rgb(255,255,255);")
        ui.rb_aprovado.setStyleSheet("border:none; color:rgb(255,255,255);")
        ui.rb_cancelado.setStyleSheet("border:none; color:rgb(255,255,255);")


    def iso_para_data(self,data):
        dt = datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%SZ")
        qdt = QDateTime(dt)
        return qdt


    def data_para_iso(self,data):
        dt = data.toPyDateTime()
        iso_str = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        return iso_str


    def abrir_janela_cadastro_usuario(self):
        def cancelar():
            if janela.isVisible():
                janela.close()
                janela.deleteLater()

        janela = QDialog(self.ui.centralwidget)
        janela.setWindowTitle("Cadastro de Novo Usuário")
        janela.setFixedSize(300, 320)

        fundo_cor = "rgb(60, 62, 84)"
        campo_texto_cor = "rgb(210, 210, 210)"
        campo_fundo_cor = "rgb(40, 45, 50)"
        
        botao_confirmar_hover = "rgb(0, 122, 255)"
        botao_confirmar_cor = "rgb(0, 102, 215)"
        
        botao_cancelar_hover = "rgb(255, 0, 0)"
        botao_cancelar_cor = "rgb(215, 0, 0)"
        
        fonte_padrao = "Arial"  # Fonte padrão
        tamanho_fonte = "12pt"  # Tamanho da fonte

        janela.setStyleSheet(f"background-color: {fundo_cor}; color: {campo_texto_cor}; font-family: {fonte_padrao}; font-size: {tamanho_fonte};")

        layout = QVBoxLayout()

        layout_usuario = QHBoxLayout()
        label_usuario = QLabel("Usuário:")
        self.input_usuario = QLineEdit()
        self.input_usuario.setStyleSheet(
            f"background-color: {campo_fundo_cor}; color: {campo_texto_cor}; padding: 5px; border-radius: 5px; font-family: {fonte_padrao}; font-size: {tamanho_fonte};"
        )

        self.label_status_usuario = QLabel("")  
        self.label_status_usuario.setStyleSheet("color: rgb(255, 0, 0);")  

        layout_usuario.addWidget(label_usuario)
        layout_usuario.addWidget(self.label_status_usuario)
        layout.addLayout(layout_usuario)

        layout_usuario_input = QVBoxLayout()
        layout_usuario_input.addWidget(self.input_usuario)
        layout.addLayout(layout_usuario_input)

        layout.addLayout(layout_usuario_input)

                            
        ref = db.reference("/Usuario")
        usuarios_existentes = ref.get()

        def verificar_usuario():
            nome_digitado = self.input_usuario.text().strip()
            if nome_digitado:
                try:
                    if usuarios_existentes and nome_digitado in usuarios_existentes:
                        self.label_status_usuario.setText("Usuário já existe")
                        self.label_status_usuario.setStyleSheet("color: rgb(255, 0, 0);")
                    else:
                        self.label_status_usuario.setText("Usuário disponível")
                        self.label_status_usuario.setStyleSheet("color: rgb(0, 255, 0);")
                except Exception as e:
                    self.label_status_usuario.setText("Erro na verificação")
                    self.label_status_usuario.setStyleSheet("color: rgb(255, 165, 0);")
            else:
                self.label_status_usuario.setText("")

        self.input_usuario.textChanged.connect(verificar_usuario)

        spacer = QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)
        
        label_nome_agente = QLabel("Nome Completo do Agente:")
        self.input_nome = QLineEdit()
        self.input_nome.setStyleSheet(
            f"background-color: {campo_fundo_cor}; color: {campo_texto_cor}; padding: 5px; border-radius: 5px; font-family: {fonte_padrao}; font-size: {tamanho_fonte};"
        )
        layout_nome_agente = QVBoxLayout()
        layout_nome_agente.addWidget(label_nome_agente)
        layout_nome_agente.addWidget(self.input_nome)
        layout.addLayout(layout_nome_agente)

        spacer = QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        label_senha = QLabel("Senha:")
        self.input_senha = QLineEdit()
        self.input_senha.setEchoMode(QLineEdit.Password)
        self.input_senha.setStyleSheet(
            f"background-color: {campo_fundo_cor}; color: {campo_texto_cor}; padding: 5px; border-radius: 5px; font-family: {fonte_padrao}; font-size: {tamanho_fonte};"
        )
        layout_senha = QVBoxLayout()
        layout_senha.addWidget(label_senha)
        layout_senha.addWidget(self.input_senha)
        layout.addLayout(layout_senha)

        spacer = QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        label_privilegio = QLabel("Privilégio:")
        self.input_privilegio = QComboBox()
        self.input_privilegio.addItems(["user", "admin"])
        self.input_privilegio.setStyleSheet(
            f"background-color: {campo_fundo_cor}; color: {campo_texto_cor}; padding: 5px; border-radius: 5px; font-family: {fonte_padrao}; font-size: {tamanho_fonte};"
        )
        layout_privilegio = QVBoxLayout()
        layout_privilegio.addWidget(label_privilegio)
        layout_privilegio.addWidget(self.input_privilegio)
        layout.addLayout(layout_privilegio)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        layout_botoes = QHBoxLayout()
        botao_confirmar = QPushButton("Confirmar")
        botao_confirmar.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {botao_confirmar_cor};
                color: {campo_texto_cor};
                padding: 5px;
                border-radius: 5px;
                font-family: {fonte_padrao};
                font-size: {tamanho_fonte};
            }}
            QPushButton:hover {{
                background-color: {botao_confirmar_hover};
            }}
            """
        )
        layout_botoes.addWidget(botao_confirmar)

        botao_cancelar = QPushButton("Cancelar")
        botao_cancelar.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {botao_cancelar_cor};
                color: {campo_texto_cor};
                padding: 5px;
                border-radius: 5px;
                font-family: {fonte_padrao};
                font-size: {tamanho_fonte};
            }}
            QPushButton:hover {{
                background-color: {botao_cancelar_hover};
            }}
            """
        )
        botao_cancelar.clicked.connect(cancelar)
        layout_botoes.addWidget(botao_cancelar)

        layout.addLayout(layout_botoes)

        def salvar_cadastro():
            novo_usuario = self.input_usuario.text()
            nome = self.input_nome.text().strip()
            senha = self.input_senha.text().strip()
            privilegio = self.input_privilegio.currentText()

            if not nome or not novo_usuario or not senha or not senha:
                QMessageBox.warning(janela, "Erro", "Todos os campos devem ser preenchidos!")
                return

            ref = db.reference("/Usuario")

            usuarios_existentes = ref.get()

            if usuarios_existentes:
                for usuario_existente in usuarios_existentes:
                    if usuario_existente == novo_usuario:
                        QMessageBox.warning(janela, "Erro", "Esse nome de usuário já existe! Por favor, escolha outro.")
                        return

            dicionario_padrao = {
                "Dados": {
                    "Configuracoes": {
                        "AGENTE": nome,
                        "ALERTA": True,
                        "CHECKBOX TRANSP": True,
                        "COD REV": "",
                        "DESCONTO TOTAL": 20,
                        "DESCONTO VALIDACAO": 2.75,
                        "DIRETORIO-RAIZ": "",
                        "E-MAIL": "",
                        "IMPOSTO VALIDACAO": 15,
                        "MODO PASTA": "PEDIDO-NOME",
                        "PORCENTAGEM": 15,
                        "PORCENTAGEM VENDA": 10,
                        "RNG RENOVACAO": 30,
                        "SAC": "11 4003 5596 ou 0800 838 051",
                        "SENHA": senha,
                        "SENHA EMAIL": "",
                        "VALOR TRANS": 10,
                        "TELEFONE ALO PARCEIRO":"4003 5596"
                    },
                    "Metas": {
                        "MENSAL": "4000",
                        "SEMANAL": "800"
                    },
                    "Pedidos": {"1":"1"}
                },
                "Hora Login": "",
                "Senha": senha,
                "Privilegio":privilegio
            }

            try:
                ref.child(novo_usuario).set(dicionario_padrao)
                QMessageBox.information(janela, "Sucesso", "Usuario criado com sucesso!")
                if janela.isVisible():
                    janela.close()
                    janela.deleteLater()

                janela.deleteLater()
            except Exception as e:
                QMessageBox.information(janela, "Erro", f"Ocorreu um erro ao salvar o usuário: {str(e)}")
                if janela.isVisible():
                    janela.close()
                    janela.deleteLater()

        botao_confirmar.clicked.connect(salvar_cadastro)

        janela.setLayout(layout)
        janela.exec_()



class JanelaOculta:
    def __init__(self, pai):
        self.pai = pai
        self.temporizador_animacao = QTimer()
        self.temporizador_animacao.timeout.connect(self.atualizar_tamanho_janela)
        self.passo_animacao = 5  # Ajustei para diminuir a animação
        self.duracao_animacao = 2  # Duração da animação em milissegundos
        self.largura_destino_animacao = 0
        self.altura_destino_animacao = 0
        self.janela = FuncoesPadrao(ui)
        self.largura = 608
        self.altura = 711


    def evento_entrada(self, evento):
        self.redimensionar_janela_animacao(self.largura, self.altura)
        self.janela.atualizar_documentos_tabela()
        self.pai.setWindowOpacity(1.0)  


    def evento_saida(self, evento):
        self.janela.atualizar_documentos_tabela()

        if not ui.campo_verifica_tela_cheia.text() == "SIM":

            posicao_cursor = QtGui.QCursor.pos()
            posicao_janela = self.pai.mapToGlobal(QtCore.QPoint(0, 0))
            retangulo_janela = QRect(posicao_janela, self.pai.size())

            mouse_dentro_janela = retangulo_janela.contains(posicao_cursor)

            if not mouse_dentro_janela:

                if int(ui.campo_status_videook.text()) == 0 and int(ui.campo_status_verificacao.text()) == 0:
                    self.redimensionar_janela_animacao(108, 50)
                else:
                    self.redimensionar_janela_animacao(151, 50)
        else:
            posicao_cursor = QtGui.QCursor.pos()
            posicao_janela = self.pai.mapToGlobal(QtCore.QPoint(0, 0))
            retangulo_janela = QRect(posicao_janela, self.pai.size())
            transparencia = ui.campo_porcentagem_transparencia.value() / 100
            mouse_dentro_janela = retangulo_janela.contains(posicao_cursor)

            if not mouse_dentro_janela:
                if ui.checkBox_transparecer.isChecked(): 
                    self.pai.setWindowOpacity(transparencia)  
                else:
                    self.pai.setWindowOpacity(1.0)  
            else:
                self.pai.setWindowOpacity(1.0)  

        
    def evento_clique_mouse(self, evento):
        self.redimensionar_janela_animacao(self.largura, self.altura)  # 469


    def redimensionar_janela_animacao(self, largura_destino, altura_destino):
        self.largura_destino_animacao = largura_destino
        self.altura_destino_animacao = altura_destino
        self.temporizador_animacao.stop()
        self.temporizador_animacao.start(int(self.duracao_animacao / self.passo_animacao))


    def atualizar_tamanho_janela(self):
        largura_atual = self.pai.width()
        altura_atual = self.pai.height()

        diferenca_largura = self.largura_destino_animacao - largura_atual
        diferenca_altura = self.altura_destino_animacao - altura_atual

        passo_largura = diferenca_largura / self.passo_animacao
        passo_altura = diferenca_altura / self.passo_animacao

        nova_largura = largura_atual + passo_largura
        nova_altura = altura_atual + passo_altura

        self.pai.setFixedSize(int(nova_largura), int(nova_altura))

        if (passo_largura > 0 and nova_largura >= self.largura_destino_animacao) or \
           (passo_largura < 0 and nova_largura <= self.largura_destino_animacao):
            self.temporizador_animacao.stop()
            self.pai.setFixedSize(self.largura_destino_animacao, self.altura_destino_animacao)






app = QtWidgets.QApplication(sys.argv)
janela = QtWidgets.QMainWindow()
desktop = QDesktopWidget()
ui = Ui_janela()
ui.setupUi(janela)

helper = JanelaOculta(janela)
banco_dados = AcoesBancoDeDados(ui)
funcoes_app = FuncoesPadrao(ui)



#Manipulações
janela.enterEvent = helper.evento_entrada
janela.leaveEvent = helper.evento_saida
janela.mousePressEvent = helper.evento_clique_mouse
janela.closeEvent = funcoes_app.evento_ao_fechar
janela.showEvent = funcoes_app.evento_ao_abrir

#Alterações nos campos
ui.campo_preco_certificado_cheio.editingFinished.connect(lambda:funcoes_app.valor_alterado(ui.campo_preco_certificado_cheio))
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
ui.campo_funcional.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_funcional))
ui.rb_aprovado.toggled.connect(lambda:funcoes_app.valor_alterado(ui.rb_aprovado))
ui.rb_cancelado.toggled.connect(lambda:funcoes_app.valor_alterado(ui.rb_cancelado))
ui.rb_digitacao.toggled.connect(lambda:funcoes_app.valor_alterado(ui.rb_digitacao))
ui.rb_verificacao.toggled.connect(lambda:funcoes_app.valor_alterado(ui.rb_verificacao))
ui.rb_videook.toggled.connect(lambda:funcoes_app.valor_alterado(ui.rb_videook))

#Campos botões
ui.botao_criar_usuario.clicked.connect(lambda:banco_dados.abrir_janela_cadastro_usuario())
ui.botao_agrupar_PDF_pasta_cliente.clicked.connect(lambda:funcoes_app.mesclar_pdf_pasta_cliente())
ui.botao_excluir_dados_tabela.clicked.connect(lambda:funcoes_app.limpar_tabela())
ui.botao_atualizar_meta.clicked.connect(lambda:funcoes_app.Atualizar_meta())
ui.botao_atualizar_configuracoes.clicked.connect(lambda:funcoes_app.atualizar_configuracoes())
ui.botao_consultar.clicked.connect(lambda:banco_dados.preencher_tabela())
ui.botao_excluir_dados.clicked.connect(lambda:banco_dados.apagar_campos_pedido(1))
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
ui.botao_converter.clicked.connect(lambda:funcoes_app.escolher_conversao())
ui.botao_agrupar_PDF.setFlat(True)
ui.botao_agrupar_PDF.clicked.connect(lambda:funcoes_app.mesclar_pdf())
ui.botao_dados_cnpj.clicked.connect(lambda:funcoes_app.dados_cnpj())
ui.botao_altera_pasta_principal.clicked.connect(lambda: funcoes_app.atualizar_diretorio_raiz())
ui.botao_menagem.clicked.connect(lambda:funcoes_app.abrir_janela_mensagem())
ui.botao_consulta_pis.clicked.connect(lambda:funcoes_app.procurar_pis())
ui.botao_hoje.clicked.connect((lambda:funcoes_app.definir_hoje()))
ui.botao_telefone.clicked.connect((lambda:funcoes_app.contato_telefone()))
ui.botao_consulta_funcional.clicked.connect((lambda:funcoes_app.procurar_funcional()))
ui.botao_enviar_email.clicked.connect((lambda:funcoes_app.envio_de_email()))
ui.rb_aprovado.clicked.connect(lambda:banco_dados.alteracao_status())
ui.rb_cancelado.clicked.connect(lambda:banco_dados.alteracao_status())
ui.rb_videook.clicked.connect(lambda:banco_dados.alteracao_status())
ui.rb_verificacao.clicked.connect(lambda:banco_dados.alteracao_status())
ui.rb_digitacao.clicked.connect(lambda:banco_dados.alteracao_status())
ui.botao_ocultar_senha.clicked.connect(lambda:funcoes_app.mostrar_senha())
ui.botao_ocultar_senha_usuario.clicked.connect(lambda:funcoes_app.mostrar_senha_usuario())
ui.botao_link_venda.clicked.connect(lambda:funcoes_app.pegar_link_venda())
ui.botao_envio_massa.clicked.connect(lambda:funcoes_app.envio_em_massa())

#Campos de formatação
ui.tabela_documentos.setSelectionMode(QTableWidget.MultiSelection) 
ui.campo_senha_usuario.setReadOnly(False) 
ui.campo_usuario.setReadOnly(True) 
ui.campo_comentario.setAcceptRichText(False)    
ui.caminho_pasta_principal.setReadOnly(True)
ui.campo_relatorio.setReadOnly(True)
ui.caminho_pasta.setReadOnly(True)
ui.campo_verifica_tela_cheia.setReadOnly(True)
ui.campo_cpf.editingFinished.connect(lambda:funcoes_app.formatar_cpf())
ui.campo_rg_orgao.editingFinished.connect(lambda:funcoes_app.formatar_orgao_rg())
ui.campo_pedido.editingFinished.connect(lambda:banco_dados.carregar_dados()) ##########################################################################
ui.campo_cnpj.editingFinished.connect (lambda:funcoes_app.formatar_cnpj())
ui.campo_meta_semanal.editingFinished.connect(lambda:funcoes_app.atualizar_meta_clientes())
ui.campo_meta_mes.editingFinished.connect(lambda:funcoes_app.atualizar_meta_clientes())
ui.campo_data_meta.editingFinished.connect(lambda:funcoes_app.atualizar_meta_clientes())
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
ui.campo_funcional.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_funcional")
ui.campo_preco_certificado.setReadOnly(False)
ui.campo_preco_certificado_cheio.setReadOnly(False)
ui.tabela_documentos.setEditTriggers(QTableWidget.NoEditTriggers)

#ToolTip
ui.campo_status_bd_2.setToolTip("Status dos dados no servidor\n✅ - Pedido atualizado no servidor\n❌ - Pedido desatualizado no servidor")
ui.botao_converter_todas_imagens_em_pdf.setToolTip("Converte as imagens da pasta do cliente para PDF")
ui.botao_agrupar_PDF.setToolTip("Mesclar PDF")
ui.botao_print_direto_na_pasta.setToolTip("Tira um print da tela")
ui.botao_tela_cheia.setToolTip("Liga/Desliga a tela cheia")
ui.botao_menagem.setToolTip("Mensagens")
ui.botao_enviar_email.setToolTip("Enviar e-mail para cliente")
ui.campo_status_bd_3.setToolTip("Quantidade de pedidos AGUARDANDO intervenção")
ui.campo_dias_renovacao.setToolTip("Define o intervalo de dias para o envio de emails de renovação. Por exemplo, se definir 15 , serão considerados os próximos 15 dias a partir de hoje.")
ui.botao_converter.setToolTip("Converte de imagens")
ui.botao_agrupar_PDF_pasta_cliente.setToolTip("Mescla as imagens selecionadas na pasta do cliente")
ui.campo_porcentagem_validacao.setToolTip(
    "A porcentagem que o agente de registro irá ganhar na validação do certificado.\n"
    "Exemplo: Se a porcentagem de validação for 30%, isso significa que 15% do valor do certificado fica com você e os outros 15% são destinados à ACB."
)

ui.campo_desconto.setToolTip(
    "A porcentagem que será descontada do valor total dos pedidos aprovados.\n"
    "Exemplo: Se você tem R$ 2.000,00 em pedidos aprovados e vai tirar 10%, o valor do desconto será R$ 200,00.\n"
    "Lembre-se que, como os valores dos certificados podem não ser exatos (devido a pedidos não pagos ou sem valor), "
    "você pode ajustar essa porcentagem para garantir que o total seja o mais próximo possível da sua expectativa."
)

ui.campo_imposto_validacao.setToolTip(
    "A porcentagem do valor que será destinada ao imposto de renda em cada validação.\n"
    "Exemplo: Se o imposto de renda for 20%, e o valor bruto da validação for R$ 1.000,00, o desconto será R$ 200,00."
)
ui.campo_desconto_validacao.setToolTip(
    "O valor em reais que a Certisign cobra por cada certificado validado. Esse valor é dividido igualmente entre o agente de registro e a ACB.\n"
    "Exemplo: Se o valor for R$ 10,00, o agente paga R$ 5,00 e a ACB paga R$ 5,00."
)

ui.caminho_pasta_principal.setToolTip("Caminho da pasta principal onde as pastas dos clientes serão armazenadas")

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
ui.campo_senha_usuario.setEchoMode(QLineEdit.Password)


x = screen_rect.width() - janela.width() - 20
y = (screen_rect.height() - janela.height()) // 5


janela.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
janela.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
janela.move(x, y)
janela.setWindowTitle("Auxiliar")
janela.setFixedSize(151, 50)

janelaLogin = LoginWindow(janela,ui)        
janelaLogin.show()


sys.exit(app.exec_())