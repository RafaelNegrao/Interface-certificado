from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from PyQt5.QtWidgets import QTableWidgetItem,QTableWidget,QApplication
from PyQt5.QtCore import QDate, QTime,QUrl
import datetime
from winotify import Notification
from PyQt5.QtGui import QDesktopServices
import pandas as pd
import os
import firebase_admin
from firebase_admin import db

#configurando banco de dados
cred_object = firebase_admin.credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred_object, {'databaseURL':'https://bdpedidos-2078f-default-rtdb.firebaseio.com/' }) 
ref = db.reference("/")

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
    if len(cpf) == 11:
        a = cpf[:3]
        b = cpf[3:6]
        c = cpf[6:9]
        d = cpf[9:11]
        cpf_formatado = f"{a}.{b}.{c}-{d}"
        ui.campo_cpf.clear()
        ui.campo_cpf.setText(cpf_formatado)
        ui.campo_digito_cpf.setText(cpf_formatado[-2:])
#digito_cpf =  cpf[-2:]
    elif len(cpf) <= 11 and len(cpf) > 0:
        cpf_formatado = cpf.zfill(11)
        a = cpf_formatado[:3]
        b = cpf_formatado[3:6]
        c = cpf_formatado[6:9]
        d = cpf_formatado[9:11]
        cpf_formatado = f"{a}.{b}.{c}-{d}"
        ui.campo_cpf.setText("")
        ui.campo_cpf.setText(cpf_formatado)
        ui.campo_digito_cpf.setText(cpf_formatado[-2:])
    elif len(cpf)== "":
        return

def formatar_rg():
    rg = ui.campo_rg.text()
    if len(rg) == 8:
        rg_formatado = rg.zfill(9)
        a = rg_formatado[:2]
        b = rg_formatado[2:5]
        c = rg_formatado[5:8]
        d = rg_formatado[8:9]
        rg_formatado = f"{a}.{b}.{c}-{d}"
        ui.campo_rg.setText("")
        ui.campo_rg.setText(rg_formatado)
        ui.campo_digito_rg.setText(rg_formatado[-1:])

    elif len(rg) == 9:
        a = rg[:2]
        b = rg[2:5]
        c = rg[5:8]
        d = rg[8:9]
        rg_formatado = f"{a}.{b}.{c}-{d}"
        ui.campo_rg.setText("")
        ui.campo_rg.setText(rg_formatado)
        ui.campo_digito_rg.setText(rg_formatado[-1:])

def formatar_data_nascimento():
    nascimento = ui.campo_data_nascimento.text()
    ui.campo_digito_ano.setText(nascimento[6:10])

def formatar_cnpj():
    
    cnpj = ui.campo_cnpj.text()
    #if len(cnpj) == 11: 
    a = cnpj[:2]
    b = cnpj[2:5]
    c = cnpj[5:8]
    d = cnpj[8:12]
    e = cnpj[12:14]
    cnpj_formatado = f"{a}.{b}.{c}/{d}-{e}"
    ui.campo_cnpj.setText("")
    ui.campo_cnpj.setText(cnpj_formatado)
    
def gravar_dados():
#USO DO BANCO DE DADOS
    num_pedido = ui.campo_pedido.text()
    req = ref.get()

    try:
        for id in req:
            pedido_servidor = req[id]['Pedido']
            if num_pedido == pedido_servidor and ui.campo_lista_status.currentText() != "":
                pedido = ui.campo_pedido.text()
                tipo = ui.campo_certificado.text()
                hora  = ui.campo_hora_agendamento.text()
                data = ui.campo_data_agendamento.text()
                status = ui.campo_lista_status.currentText()
                dados_atualizados = {"Pedido":pedido , "Data":data, "Hora":hora, "Tipo":tipo, "Status":status}
                ref.child(id).update(dados_atualizados)
                limpar_campos()
                notificacao = Notification(app_id="Pedido Atualizado",title="",msg=f"Os dados do pedido {pedido} foram atualizados!")
                notificacao.show()
                return
            
        pedido = ui.campo_pedido.text()
        tipo = ui.campo_certificado.text()
        hora = ui.campo_hora_agendamento.text()
        data = ui.campo_data_agendamento.text()
        status = ui.campo_lista_status.currentText()
        if pedido == "" or tipo == "" or hora == "" or data == "" or status == "":

            notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!")
            notificacao.show()
            return
        #
        novos_dados = {"Pedido":pedido , "Data":data, "Hora":hora, "Tipo":tipo, "Status":status}
        
        ref.push(novos_dados)
        limpar_campos()
        return
        
    except Exception as e:
    
        pedido = ui.campo_pedido.text()
        tipo = ui.campo_certificado.text()
        hora = ui.campo_hora_agendamento.text()
        data = ui.campo_data_agendamento.text()
        status = ui.campo_lista_status.currentText()
        if pedido == "" or tipo == "" or hora == "" or data == "" or status == "":

            notificacao = Notification(app_id="Erro no Envio",title="",msg="Adicione os itens com 🌟 para Encerrar o pedido!")
            notificacao.show()
            return
        #
        novos_dados = {"Pedido":pedido , "Data":data, "Hora":hora, "Tipo":tipo, "Status":status}
        
        ref.push(novos_dados)
        limpar_campos()
        return

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
    ui.campo_lista_status.setCurrentText("")
    data_nula = QDate(2000, 1, 1)  
    hora = QTime.fromString('00:00', "hh:mm")
    ui.campo_data_agendamento.setDate(data_nula)
    ui.campo_data_nascimento.setDate(data_nula)
    ui.campo_hora_agendamento.setTime(hora)
    ui.tableWidget.setRowCount(0)
    ui.label_quantidade_bd.setText("")
    ui.campo_oab.setText("")
    ui.campo_cnh.setText("")

def buscar_dados():
    try:
  
        req =ref.get()
        
        data_inicial = datetime.datetime.strptime(ui.campo_data_de.text(), "%d/%m/%Y")
        numero_inteiro_inicial = data_inicial.toordinal()
        data_final = datetime.datetime.strptime(ui.campo_data_ate.text(), "%d/%m/%Y")
        numero_inteiro_final = data_final.toordinal()

        dados_selecionados=[]
        x = 0
        for cliente in req:
            data_bd = datetime.datetime.strptime(req[cliente]['Data'], "%d/%m/%Y")
            numero_inteiro_bd = data_bd.toordinal()

            status_filtro = ui.campo_lista_status_2.currentText()
            status_servidor = req[cliente]['Status']

            if (numero_inteiro_inicial <= numero_inteiro_bd <= numero_inteiro_final):
                if status_filtro == status_servidor:
                
                    x += 1
                    pedido = req[cliente]['Pedido']
                    data_agendamento = req[cliente]['Data']
                    tipo_pedido = req[cliente]['Tipo']
                    hora_agendamento = req[cliente]['Hora']    
                    status_agendamento = req[cliente]['Status']

                    dados_selecionados.append((pedido, data_agendamento, tipo_pedido, hora_agendamento,status_agendamento))   

                elif status_filtro == "":
                    x += 1

                    pedido = req[cliente]['Pedido']
                    data_agendamento = req[cliente]['Data']
                    tipo_pedido = req[cliente]['Tipo']
                    hora_agendamento = req[cliente]['Hora']    
                    status_agendamento = req[cliente]['Status']
                    dados_selecionados.append((pedido, data_agendamento, tipo_pedido, hora_agendamento,status_agendamento)) 
        
        if x > 0:
            df=pd.DataFrame(dados_selecionados,columns=['Pedido','Data agendamento','Tipo de certificado','hora','Status Pedido'])
            data_agora = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
            data_final = ui.campo_data_ate.text()
            data_inicial = ui.campo_data_de.text()
            pasta_desktop = os.path.expanduser("~\\Desktop")
            nome_arquivo = os.path.join(pasta_desktop, f"Certificados-emitidos-de {data_inicial.replace('/', '-')} a {data_final.replace('/', '-')}-gerado em{data_agora.replace('/','-')} .xlsx")
            df.to_excel(nome_arquivo, index=False)
            notificacao = Notification(app_id="Arquivo salvo",title="",msg=f"Arquivo excel salvo na área de trabalho!")
            notificacao.show()
        else:
            notificacao = Notification(app_id="Sem dados",title="",msg=f"Sem dados para o período!")
            notificacao.show()

    except Exception as e:
        print(e)
        notificacao = Notification(app_id="Arquivo não salvo",title="",msg=f"Arquivo não gerado!")
        notificacao.show()
        # Lida com exceções aqui
        pass

def preencher_tabela():
    #USO DE BANCO DE DADOS
    ui.tableWidget.setRowCount(0)
    try:
        ui.tableWidget.clear()
        
        
        req = ref.get()
        
        data_inicial = datetime.datetime.strptime(ui.campo_data_de.text(), "%d/%m/%Y")
        numero_inteiro_inicial = data_inicial.toordinal()
        data_final = datetime.datetime.strptime(ui.campo_data_ate.text(), "%d/%m/%Y")
        numero_inteiro_final = data_final.toordinal()
        status_filtro = ui.campo_lista_status_2.currentText()

        x = 0
        for cliente in req:

            data_bd = datetime.datetime.strptime(req[cliente]['Data'], "%d/%m/%Y")
            numero_inteiro_bd = data_bd.toordinal()
            status_filtro = ui.campo_lista_status_2.currentText()
            status_servidor = req[cliente]['Status']

            if (numero_inteiro_inicial <= numero_inteiro_bd <= numero_inteiro_final) :

                if status_filtro == status_servidor:
                
                    x += 1
                
                    row_position = ui.tableWidget.rowCount()
                    ui.tableWidget.insertRow(row_position)

                    ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(req[cliente]['Pedido']))
                    ui.tableWidget.setItem(row_position, 1, QTableWidgetItem(req[cliente]['Data']))
                    ui.tableWidget.setItem(row_position, 2, QTableWidgetItem(req[cliente]['Tipo']))
                    ui.tableWidget.setItem(row_position, 3, QTableWidgetItem(req[cliente]['Hora']))
                    ui.tableWidget.setItem(row_position, 4, QTableWidgetItem(req[cliente]['Status']))
                    ui.label_quantidade_bd.setText(f"{x} registro(s)")
                elif status_filtro == "":
                    x += 1
                
                    row_position = ui.tableWidget.rowCount()
                    ui.tableWidget.insertRow(row_position)

                    ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(req[cliente]['Pedido']))
                    ui.tableWidget.setItem(row_position, 1, QTableWidgetItem(req[cliente]['Data']))
                    ui.tableWidget.setItem(row_position, 2, QTableWidgetItem(req[cliente]['Tipo']))
                    ui.tableWidget.setItem(row_position, 3, QTableWidgetItem(req[cliente]['Hora']))
                    ui.tableWidget.setItem(row_position, 4, QTableWidgetItem(req[cliente]['Status']))
                    ui.label_quantidade_bd.setText(f"{x} registro(s)")

                
    except Exception as e:
        pass
    ui.label_quantidade_bd.setText(f"{x} registro(s)")
    ui.tableWidget.setHorizontalHeaderLabels(["PEDIDO", "DATA", "TIPO", "HORA", "STATUS"])

def verificar_se_existe():
    #USO DE BANCO DE DADOS
    try:   
        num_pedido = ui.campo_pedido.text()
        req = ref.get()


        for pedido in req:
            pedido_servidor = req[pedido]['Pedido']
            if num_pedido == pedido_servidor:
                ui.campo_pedido.setReadOnly(True)
                #traga os dados
                data = QDate.fromString(req[pedido]['Data'], "dd/MM/yyyy")
                hora = QTime.fromString(req[pedido]['Hora'], "hh:mm")

                ui.campo_novo_noBd.setText("✅")
                ui.campo_data_agendamento.setDate(data)
                ui.campo_hora_agendamento.setTime(hora)
                ui.campo_certificado.setText(req[pedido]['Tipo'])
                ui.campo_lista_status.setCurrentText(req[pedido]['Status'])
        
                return
    except Exception as e:
       
        # Lida com exceções aqui
        pass
    ui.campo_novo_noBd.setText("")

def pegar_valor_tabela(event):
    item = ui.tableWidget.currentItem()  # Obtenha o item selecionado
    if item is not None:
        linha = item.row()
        coluna = item.column()
        valor = item.text()

        if coluna == 0 :    
            
            coluna_data = ui.tableWidget.item(linha, 1).text()
            coluna_tipo = ui.tableWidget.item(linha, 2).text()
            coluna_hora = ui.tableWidget.item(linha, 3).text()
            coluna_status = ui.tableWidget.item(linha, 4).text()

            data = QDate.fromString(coluna_data, "dd/MM/yyyy")
            hora = QTime.fromString(coluna_hora, "hh:mm")    
            ui.tabWidget.setCurrentIndex(0)
            ui.campo_pedido.setText(valor)
            ui.campo_data_agendamento.setDate(data)
            ui.campo_certificado.setText(coluna_tipo)
            ui.campo_hora_agendamento.setTime(hora)
            ui.campo_lista_status.setCurrentText(coluna_status)
            ui.campo_pedido.setReadOnly(True)
            ui.campo_novo_noBd.setText("✅")

class Ui_janela(object):
    def setupUi(self, janela):
        janela.setObjectName("janela")
        janela.resize(599, 693)
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
        self.tabWidget.setGeometry(QtCore.QRect(10, 0, 581, 651))
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setObjectName("tabWidget")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.groupBox = QtWidgets.QGroupBox(self.tab_5)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 561, 151))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("")
        self.groupBox.setObjectName("groupBox")
        self.campo_data_agendamento = QtWidgets.QDateEdit(self.groupBox)
        self.campo_data_agendamento.setGeometry(QtCore.QRect(279, 41, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_data_agendamento.setFont(font)
        self.campo_data_agendamento.setStyleSheet("")
        self.campo_data_agendamento.setObjectName("campo_data_agendamento")
        self.campo_hora_agendamento = QtWidgets.QTimeEdit(self.groupBox)
        self.campo_hora_agendamento.setGeometry(QtCore.QRect(430, 40, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_hora_agendamento.setFont(font)
        self.campo_hora_agendamento.setStyleSheet("")
        self.campo_hora_agendamento.setObjectName("campo_hora_agendamento")
        self.campo_certificado = QtWidgets.QLineEdit(self.groupBox)
        self.campo_certificado.setGeometry(QtCore.QRect(10, 100, 331, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.campo_certificado.setFont(font)
        self.campo_certificado.setObjectName("campo_certificado")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 241, 16))
        self.label_2.setObjectName("label_2")
        self.campo_pedido = QtWidgets.QLineEdit(self.groupBox)
        self.campo_pedido.setGeometry(QtCore.QRect(10, 40, 221, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.campo_pedido.setFont(font)
        self.campo_pedido.setObjectName("campo_pedido")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 20, 81, 16))
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(430, 20, 121, 16))
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(270, 20, 131, 20))
        self.label_3.setObjectName("label_3")
        self.label_17 = QtWidgets.QLabel(self.groupBox)
        self.label_17.setGeometry(QtCore.QRect(360, 80, 101, 16))
        self.label_17.setObjectName("label_17")
        self.campo_lista_status = QtWidgets.QComboBox(self.groupBox)
        self.campo_lista_status.setGeometry(QtCore.QRect(360, 100, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.campo_lista_status.setFont(font)
        self.campo_lista_status.setStyleSheet("")
        self.campo_lista_status.setEditable(False)
        self.campo_lista_status.setObjectName("campo_lista_status")
        self.campo_lista_status.addItem("")
        self.campo_lista_status.setItemText(0, "")
        self.campo_lista_status.addItem("")
        self.campo_lista_status.addItem("")
        self.campo_lista_status.addItem("")
        self.campo_novo_noBd = QtWidgets.QLabel(self.groupBox)
        self.campo_novo_noBd.setGeometry(QtCore.QRect(240, 50, 21, 21))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.campo_novo_noBd.setFont(font)
        self.campo_novo_noBd.setText("")
        self.campo_novo_noBd.setObjectName("campo_novo_noBd")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_5)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 160, 561, 451))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(10, 20, 171, 16))
        self.label_7.setObjectName("label_7")
        self.campo_nome = QtWidgets.QLineEdit(self.groupBox_2)
        self.campo_nome.setGeometry(QtCore.QRect(10, 40, 531, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_nome.setFont(font)
        self.campo_nome.setText("")
        self.campo_nome.setObjectName("campo_nome")
        self.campo_cnpj = QtWidgets.QLineEdit(self.groupBox_2)
        self.campo_cnpj.setGeometry(QtCore.QRect(10, 280, 491, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_cnpj.setFont(font)
        self.campo_cnpj.setObjectName("campo_cnpj")
        self.label_14 = QtWidgets.QLabel(self.groupBox_2)
        self.label_14.setGeometry(QtCore.QRect(10, 260, 171, 16))
        self.label_14.setObjectName("label_14")
        self.campo_oab = QtWidgets.QLineEdit(self.groupBox_2)
        self.campo_oab.setGeometry(QtCore.QRect(330, 220, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_oab.setFont(font)
        self.campo_oab.setStyleSheet("")
        self.campo_oab.setText("")
        self.campo_oab.setObjectName("campo_oab")
        self.label_18 = QtWidgets.QLabel(self.groupBox_2)
        self.label_18.setGeometry(QtCore.QRect(330, 200, 141, 20))
        self.label_18.setObjectName("label_18")
        self.botao_terminar = QtWidgets.QPushButton(self.groupBox_2)
        self.botao_terminar.setGeometry(QtCore.QRect(410, 400, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.botao_terminar.setFont(font)
        self.botao_terminar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_terminar.setStyleSheet("border-radius:10px;\n"
"background-color:rgb(73, 218, 107);\n"
"")
        self.botao_terminar.setObjectName("botao_terminar")
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setGeometry(QtCore.QRect(10, 320, 81, 16))
        self.label_11.setObjectName("label_11")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(10, 140, 81, 16))
        self.label_6.setObjectName("label_6")
        self.campo_digito_rg = QtWidgets.QLineEdit(self.groupBox_2)
        self.campo_digito_rg.setGeometry(QtCore.QRect(330, 100, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.campo_digito_rg.setFont(font)
        self.campo_digito_rg.setText("")
        self.campo_digito_rg.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_digito_rg.setObjectName("campo_digito_rg")
        self.campo_rg = QtWidgets.QLineEdit(self.groupBox_2)
        self.campo_rg.setGeometry(QtCore.QRect(10, 100, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_rg.setFont(font)
        self.campo_rg.setObjectName("campo_rg")
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setGeometry(QtCore.QRect(10, 380, 191, 16))
        self.label_12.setObjectName("label_12")
        self.campo_digito_cpf = QtWidgets.QLineEdit(self.groupBox_2)
        self.campo_digito_cpf.setGeometry(QtCore.QRect(330, 160, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.campo_digito_cpf.setFont(font)
        self.campo_digito_cpf.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_digito_cpf.setObjectName("campo_digito_cpf")
        self.campo_cpf = QtWidgets.QLineEdit(self.groupBox_2)
        self.campo_cpf.setGeometry(QtCore.QRect(10, 160, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_cpf.setFont(font)
        self.campo_cpf.setObjectName("campo_cpf")
        self.campo_digito_ano = QtWidgets.QLineEdit(self.groupBox_2)
        self.campo_digito_ano.setGeometry(QtCore.QRect(220, 400, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.campo_digito_ano.setFont(font)
        self.campo_digito_ano.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_digito_ano.setObjectName("campo_digito_ano")
        self.campo_email = QtWidgets.QLineEdit(self.groupBox_2)
        self.campo_email.setGeometry(QtCore.QRect(10, 340, 531, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_email.setFont(font)
        self.campo_email.setText("")
        self.campo_email.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.campo_email.setObjectName("campo_email")
        self.campo_data_nascimento = QtWidgets.QDateEdit(self.groupBox_2)
        self.campo_data_nascimento.setGeometry(QtCore.QRect(10, 400, 201, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_data_nascimento.setFont(font)
        self.campo_data_nascimento.setStyleSheet("")
        self.campo_data_nascimento.setObjectName("campo_data_nascimento")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(330, 140, 141, 20))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(330, 80, 61, 20))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setGeometry(QtCore.QRect(10, 80, 81, 16))
        self.label_10.setObjectName("label_10")
        self.label_13 = QtWidgets.QLabel(self.groupBox_2)
        self.label_13.setGeometry(QtCore.QRect(220, 380, 61, 16))
        self.label_13.setObjectName("label_13")
        self.botao_consulta_cpf = QtWidgets.QPushButton(self.groupBox_2)
        self.botao_consulta_cpf.setGeometry(QtCore.QRect(510, 160, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_cpf.setFont(font)
        self.botao_consulta_cpf.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_cpf.setObjectName("botao_consulta_cpf")
        self.botao_consulta_cnpj = QtWidgets.QPushButton(self.groupBox_2)
        self.botao_consulta_cnpj.setGeometry(QtCore.QRect(510, 280, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_cnpj.setFont(font)
        self.botao_consulta_cnpj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_cnpj.setObjectName("botao_consulta_cnpj")
        self.campo_cnh = QtWidgets.QLineEdit(self.groupBox_2)
        self.campo_cnh.setGeometry(QtCore.QRect(10, 220, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_cnh.setFont(font)
        self.campo_cnh.setObjectName("campo_cnh")
        self.label_15 = QtWidgets.QLabel(self.groupBox_2)
        self.label_15.setGeometry(QtCore.QRect(10, 200, 61, 20))
        self.label_15.setObjectName("label_15")
        self.botao_consulta_cnh = QtWidgets.QPushButton(self.groupBox_2)
        self.botao_consulta_cnh.setGeometry(QtCore.QRect(290, 220, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_cnh.setFont(font)
        self.botao_consulta_cnh.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_cnh.setObjectName("botao_consulta_cnh")
        self.botao_consulta_rg = QtWidgets.QPushButton(self.groupBox_2)
        self.botao_consulta_rg.setGeometry(QtCore.QRect(510, 100, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_rg.setFont(font)
        self.botao_consulta_rg.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_rg.setObjectName("botao_consulta_rg")
        self.botao_consulta_oab = QtWidgets.QPushButton(self.groupBox_2)
        self.botao_consulta_oab.setGeometry(QtCore.QRect(510, 220, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_oab.setFont(font)
        self.botao_consulta_oab.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_oab.setObjectName("botao_consulta_oab")
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
        self.tableWidget.setGeometry(QtCore.QRect(10, 110, 561, 471))
        self.tableWidget.setMinimumSize(QtCore.QSize(561, 0))
        self.tableWidget.setMaximumSize(QtCore.QSize(561, 16777215))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
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
        self.botao_procurar = QtWidgets.QPushButton(self.tab_6)
        self.botao_procurar.setGeometry(QtCore.QRect(440, 590, 131, 31))
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
        self.label_quantidade_bd.setGeometry(QtCore.QRect(200, 590, 221, 31))
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
        janela.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(janela)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 599, 21))
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
        janela.setTabOrder(self.campo_certificado, self.campo_lista_status)
        janela.setTabOrder(self.campo_lista_status, self.campo_nome)
        janela.setTabOrder(self.campo_nome, self.campo_rg)
        janela.setTabOrder(self.campo_rg, self.campo_cpf)
        janela.setTabOrder(self.campo_cpf, self.campo_cnh)
        janela.setTabOrder(self.campo_cnh, self.campo_oab)
        janela.setTabOrder(self.campo_oab, self.campo_cnpj)
        janela.setTabOrder(self.campo_cnpj, self.campo_email)
        janela.setTabOrder(self.campo_email, self.campo_data_nascimento)
        janela.setTabOrder(self.campo_data_nascimento, self.campo_data_de)
        janela.setTabOrder(self.campo_data_de, self.campo_data_ate)
        janela.setTabOrder(self.campo_data_ate, self.campo_lista_status_2)
        janela.setTabOrder(self.campo_lista_status_2, self.botao_consulta_cpf)
        janela.setTabOrder(self.botao_consulta_cpf, self.botao_consulta_cnpj)
        janela.setTabOrder(self.botao_consulta_cnpj, self.botao_terminar)
        janela.setTabOrder(self.botao_terminar, self.botao_consulta_cnh)
        janela.setTabOrder(self.botao_consulta_cnh, self.botao_consulta_rg)
        janela.setTabOrder(self.botao_consulta_rg, self.botao_consulta_oab)
        janela.setTabOrder(self.botao_consulta_oab, self.botao_consultar)
        janela.setTabOrder(self.botao_consultar, self.botao_procurar)
        janela.setTabOrder(self.botao_procurar, self.campo_digito_rg)
        janela.setTabOrder(self.campo_digito_rg, self.tabWidget)
        janela.setTabOrder(self.tabWidget, self.campo_digito_cpf)
        janela.setTabOrder(self.campo_digito_cpf, self.campo_digito_ano)
        janela.setTabOrder(self.campo_digito_ano, self.tableWidget)

    def retranslateUi(self, janela):
        _translate = QtCore.QCoreApplication.translate
        janela.setWindowTitle(_translate("janela", "MainWindow"))
        self.groupBox.setTitle(_translate("janela", "DADOS AGENDAMENTO"))
        self.label_2.setText(_translate("janela", "🌟 TIPO CERTIFICADO"))
        self.label.setText(_translate("janela", "🌟 PEDIDO"))
        self.label_4.setText(_translate("janela", "🌟 HORA AGENDA"))
        self.label_3.setText(_translate("janela", "🌟 DATA AGENDA"))
        self.label_17.setText(_translate("janela", "🌟 STATUS"))
        self.campo_lista_status.setItemText(1, _translate("janela", "Aguardando"))
        self.campo_lista_status.setItemText(2, _translate("janela", "Aprovado"))
        self.campo_lista_status.setItemText(3, _translate("janela", "Cancelado"))
        self.groupBox_2.setTitle(_translate("janela", "DADOS CLIENTE"))
        self.label_7.setText(_translate("janela", "NOME COMPLETO"))
        self.label_14.setText(_translate("janela", "CNPJ"))
        self.label_18.setText(_translate("janela", "OAB"))
        self.botao_terminar.setText(_translate("janela", "FINALIZAR"))
        self.label_11.setText(_translate("janela", "e-MAIL"))
        self.label_6.setText(_translate("janela", "CPF"))
        self.label_12.setText(_translate("janela", "DATA NASCIMENTO"))
        self.label_8.setText(_translate("janela", "últimos 2 dígitos - CPF"))
        self.label_9.setText(_translate("janela", " dígito - RG"))
        self.label_10.setText(_translate("janela", "RG"))
        self.label_13.setText(_translate("janela", "díg ANO"))
        self.botao_consulta_cpf.setText(_translate("janela", "🔍"))
        self.botao_consulta_cnpj.setText(_translate("janela", "🔍"))
        self.label_15.setText(_translate("janela", "CNH"))
        self.botao_consulta_cnh.setText(_translate("janela", "🔍"))
        self.botao_consulta_rg.setText(_translate("janela", "🔍"))
        self.botao_consulta_oab.setText(_translate("janela", "🔍"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("janela", "Dados"))
        self.groupBox_5.setTitle(_translate("janela", "BUSCA"))
        self.label_19.setText(_translate("janela", "DE:"))
        self.label_20.setText(_translate("janela", "ATÉ:"))
        self.botao_consultar.setText(_translate("janela", "🔍"))
        self.label_21.setText(_translate("janela", "STATUS"))
        self.campo_lista_status_2.setItemText(1, _translate("janela", "Aguardando"))
        self.campo_lista_status_2.setItemText(2, _translate("janela", "Aprovado"))
        self.campo_lista_status_2.setItemText(3, _translate("janela", "Cancelado"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("janela", "PEDIDO"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("janela", "DATA"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("janela", "TIPO"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("janela", "HORA"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("janela", "STATUS"))
        self.botao_procurar.setText(_translate("janela", "EXPORTAR EXCEL"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("janela", "Consulta"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    janela = QtWidgets.QMainWindow()
    ui = Ui_janela()
    ui.setupUi(janela)

    ui.botao_consultar.clicked.connect(preencher_tabela)
    ui.botao_terminar.clicked.connect(gravar_dados)
    ui.botao_procurar.clicked.connect(buscar_dados)
    ui.campo_cpf.editingFinished.connect(formatar_cpf)
    ui.campo_rg.editingFinished.connect(formatar_rg)
    ui.campo_pedido.editingFinished.connect(verificar_se_existe)
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
    

    janela.setWindowTitle("Dados Certificado - Certisign")
    janela.setFixedSize(599, 693)
    janela.show()
    sys.exit(app.exec_())
