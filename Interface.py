
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_janela(object):
    def setupUi(self, janela):
        janela.setObjectName("janela")
        janela.resize(604, 708)
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
        janela.setFocusPolicy(QtCore.Qt.StrongFocus)
        janela.setAutoFillBackground(False)
        janela.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(janela)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(-4, 50, 648, 789))
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tabWidget.setMaximumSize(QtCore.QSize(16777202, 16777215))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet("\n"
"QTabWidget::pane {\n"
"    background-color: rgb(40, 45, 50); /* Cor do painel */\n"
"    font-size: 30px; /* Tamanho da fonte */\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"     background-color: rgb(40, 45, 50); /* Cor das abas selecionadas */\n"
"     color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background-color: rgb(60,62, 84); /* Cor das abas selecionadas */\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QHeader{\n"
"     background-color: rgb(40, 45, 50)\n"
"}\n"
"\n"
"/* Estiliza o conteúdo das abas */\n"
"QWidget {\n"
"    background-color: rgb(60, 62,84); /* Cor do conteúdo */\n"
"    color: rgb(255, 255, 255);\n"
"    border: none;\n"
"}\n"
"QTabBar::tab:Hover {\n"
"    background-color: rgb(60, 62, 84); /* Cor das abas selecionadas */\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.label = QtWidgets.QLabel(self.tab_5)
        self.label.setGeometry(QtCore.QRect(16, 6, 49, 10))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label.setObjectName("label")
        self.campo_data_agendamento = QtWidgets.QDateEdit(self.tab_5)
        self.campo_data_agendamento.setGeometry(QtCore.QRect(168, 20, 93, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_data_agendamento.setFont(font)
        self.campo_data_agendamento.setStyleSheet("QDateEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QDateEdit:disabled, QDateEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"\n"
"QDateEdit::up-button {\n"
"    width: 0;\n"
"    height: 0;\n"
"    border: none;\n"
"}\n"
"\n"
"QDateEdit::down-button {\n"
"    width: 0;\n"
"    height: 0;\n"
"    border: none;\n"
"}\n"
"")
        self.campo_data_agendamento.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_data_agendamento.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.campo_data_agendamento.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.campo_data_agendamento.setMaximumDate(QtCore.QDate(9999, 12, 26))
        self.campo_data_agendamento.setObjectName("campo_data_agendamento")
        self.campo_pedido = QtWidgets.QLineEdit(self.tab_5)
        self.campo_pedido.setGeometry(QtCore.QRect(16, 20, 133, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.campo_pedido.setFont(font)
        self.campo_pedido.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_pedido.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_pedido.setText("")
        self.campo_pedido.setObjectName("campo_pedido")
        self.campo_hora_agendamento = QtWidgets.QTimeEdit(self.tab_5)
        self.campo_hora_agendamento.setGeometry(QtCore.QRect(280, 20, 68, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_hora_agendamento.setFont(font)
        self.campo_hora_agendamento.setStyleSheet("QTimeEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QTimeEdit:disabled, QTimeEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}")
        self.campo_hora_agendamento.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_hora_agendamento.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.campo_hora_agendamento.setObjectName("campo_hora_agendamento")
        self.label_4 = QtWidgets.QLabel(self.tab_5)
        self.label_4.setGeometry(QtCore.QRect(280, 6, 49, 10))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(self.tab_5)
        self.label_3.setGeometry(QtCore.QRect(168, 6, 41, 10))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_3.setObjectName("label_3")
        self.campo_lista_venda = QtWidgets.QComboBox(self.tab_5)
        self.campo_lista_venda.setGeometry(QtCore.QRect(179, 116, 64, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_lista_venda.setFont(font)
        self.campo_lista_venda.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.campo_lista_venda.setToolTip("")
        self.campo_lista_venda.setStatusTip("")
        self.campo_lista_venda.setStyleSheet("QComboBox {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QComboBox:disabled, QComboBox:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: none;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    width: 0;\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.campo_lista_venda.setInputMethodHints(QtCore.Qt.ImhNone)
        self.campo_lista_venda.setEditable(False)
        self.campo_lista_venda.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.campo_lista_venda.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.campo_lista_venda.setIconSize(QtCore.QSize(0, 0))
        self.campo_lista_venda.setDuplicatesEnabled(False)
        self.campo_lista_venda.setFrame(True)
        self.campo_lista_venda.setObjectName("campo_lista_venda")
        self.campo_lista_venda.addItem("")
        self.campo_lista_venda.addItem("")
        self.label_22 = QtWidgets.QLabel(self.tab_5)
        self.label_22.setGeometry(QtCore.QRect(182, 104, 57, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_22.setFont(font)
        self.label_22.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.tab_5)
        self.label_23.setGeometry(QtCore.QRect(16, 102, 77, 10))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_23.setFont(font)
        self.label_23.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_23.setObjectName("label_23")
        self.campo_lista_modalidade = QtWidgets.QComboBox(self.tab_5)
        self.campo_lista_modalidade.setGeometry(QtCore.QRect(15, 116, 149, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_lista_modalidade.setFont(font)
        self.campo_lista_modalidade.setStyleSheet("QComboBox {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QComboBox:disabled, QComboBox:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: none;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    width: 0;\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.campo_lista_modalidade.setEditable(False)
        self.campo_lista_modalidade.setObjectName("campo_lista_modalidade")
        self.campo_lista_modalidade.addItem("")
        self.campo_lista_modalidade.setItemText(0, "")
        self.campo_lista_modalidade.addItem("")
        self.campo_lista_modalidade.addItem("")
        self.botao_pasta_cliente = QtWidgets.QPushButton(self.tab_5)
        self.botao_pasta_cliente.setGeometry(QtCore.QRect(122, 14, 30, 30))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_pasta_cliente.setFont(font)
        self.botao_pasta_cliente.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_pasta_cliente.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_pasta_cliente.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.botao_pasta_cliente.setStyleSheet("border-radius:7px;\n"
"background-color:transparent")
        self.botao_pasta_cliente.setObjectName("botao_pasta_cliente")
        self.label_confirmacao_criar_pasta = QtWidgets.QLabel(self.tab_5)
        self.label_confirmacao_criar_pasta.setGeometry(QtCore.QRect(138, 14, 17, 17))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_confirmacao_criar_pasta.setFont(font)
        self.label_confirmacao_criar_pasta.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
        self.label_confirmacao_criar_pasta.setText("")
        self.label_confirmacao_criar_pasta.setObjectName("label_confirmacao_criar_pasta")
        self.campo_lista_versao_certificado = QtWidgets.QComboBox(self.tab_5)
        self.campo_lista_versao_certificado.setGeometry(QtCore.QRect(16, 68, 421, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_lista_versao_certificado.setFont(font)
        self.campo_lista_versao_certificado.setStyleSheet("QComboBox {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QComboBox:disabled, QComboBox:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: none;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    width: 0;\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.campo_lista_versao_certificado.setEditable(False)
        self.campo_lista_versao_certificado.setObjectName("campo_lista_versao_certificado")
        self.label_40 = QtWidgets.QLabel(self.tab_5)
        self.label_40.setGeometry(QtCore.QRect(16, 54, 80, 10))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_40.setFont(font)
        self.label_40.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_40.setObjectName("label_40")
        self.campo_preco_certificado = QtWidgets.QLineEdit(self.tab_5)
        self.campo_preco_certificado.setEnabled(True)
        self.campo_preco_certificado.setGeometry(QtCore.QRect(360, 116, 77, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_preco_certificado.setFont(font)
        self.campo_preco_certificado.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_preco_certificado.setToolTipDuration(999999999)
        self.campo_preco_certificado.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_preco_certificado.setText("")
        self.campo_preco_certificado.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_preco_certificado.setObjectName("campo_preco_certificado")
        self.label_13 = QtWidgets.QLabel(self.tab_5)
        self.label_13.setGeometry(QtCore.QRect(360, 106, 53, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_13.setObjectName("label_13")
        self.groupBox_status = QtWidgets.QGroupBox(self.tab_5)
        self.groupBox_status.setGeometry(QtCore.QRect(448, 17, 146, 127))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.groupBox_status.setFont(font)
        self.groupBox_status.setStyleSheet("border-radius:7px;\n"
"border: 1px solid rgb(120,120,120);\n"
"background-color:rgb(60, 62, 84);")
        self.groupBox_status.setTitle("")
        self.groupBox_status.setObjectName("groupBox_status")
        self.rb_digitacao = QtWidgets.QRadioButton(self.groupBox_status)
        self.rb_digitacao.setGeometry(QtCore.QRect(12, 10, 93, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.rb_digitacao.setFont(font)
        self.rb_digitacao.setFocusPolicy(QtCore.Qt.NoFocus)
        self.rb_digitacao.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.rb_digitacao.setStyleSheet("border: solid rgb(0, 0, 253);\n"
"color:rgb(255,255,255)")
        self.rb_digitacao.setChecked(True)
        self.rb_digitacao.setObjectName("rb_digitacao")
        self.rb_videook = QtWidgets.QRadioButton(self.groupBox_status)
        self.rb_videook.setGeometry(QtCore.QRect(12, 33, 124, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.rb_videook.setFont(font)
        self.rb_videook.setFocusPolicy(QtCore.Qt.NoFocus)
        self.rb_videook.setStyleSheet("border: solid rgb(0, 0, 253)")
        self.rb_videook.setObjectName("rb_videook")
        self.rb_verificacao = QtWidgets.QRadioButton(self.groupBox_status)
        self.rb_verificacao.setGeometry(QtCore.QRect(12, 56, 106, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.rb_verificacao.setFont(font)
        self.rb_verificacao.setFocusPolicy(QtCore.Qt.NoFocus)
        self.rb_verificacao.setStyleSheet("border: solid rgb(0, 0, 253)")
        self.rb_verificacao.setObjectName("rb_verificacao")
        self.rb_aprovado = QtWidgets.QRadioButton(self.groupBox_status)
        self.rb_aprovado.setGeometry(QtCore.QRect(12, 79, 92, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.rb_aprovado.setFont(font)
        self.rb_aprovado.setFocusPolicy(QtCore.Qt.NoFocus)
        self.rb_aprovado.setStyleSheet("border: solid rgb(0, 0, 253)")
        self.rb_aprovado.setObjectName("rb_aprovado")
        self.rb_cancelado = QtWidgets.QRadioButton(self.groupBox_status)
        self.rb_cancelado.setGeometry(QtCore.QRect(12, 102, 96, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.rb_cancelado.setFont(font)
        self.rb_cancelado.setFocusPolicy(QtCore.Qt.NoFocus)
        self.rb_cancelado.setStyleSheet("border: solid rgb(0, 0, 253)")
        self.rb_cancelado.setObjectName("rb_cancelado")
        self.campo_preco_certificado_cheio = QtWidgets.QLineEdit(self.tab_5)
        self.campo_preco_certificado_cheio.setEnabled(True)
        self.campo_preco_certificado_cheio.setGeometry(QtCore.QRect(258, 116, 79, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_preco_certificado_cheio.setFont(font)
        self.campo_preco_certificado_cheio.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_preco_certificado_cheio.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_preco_certificado_cheio.setText("")
        self.campo_preco_certificado_cheio.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_preco_certificado_cheio.setObjectName("campo_preco_certificado_cheio")
        self.label_17 = QtWidgets.QLabel(self.tab_5)
        self.label_17.setGeometry(QtCore.QRect(264, 106, 53, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_17.setObjectName("label_17")
        self.botao_link_venda = QtWidgets.QPushButton(self.tab_5)
        self.botao_link_venda.setGeometry(QtCore.QRect(410, 66, 23, 23))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_link_venda.setFont(font)
        self.botao_link_venda.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_link_venda.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_link_venda.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.botao_link_venda.setStyleSheet("border-radius:7px;\n"
";background-color: transparent")
        self.botao_link_venda.setObjectName("botao_link_venda")
        self.label_31 = QtWidgets.QLabel(self.tab_5)
        self.label_31.setGeometry(QtCore.QRect(456, 13, 35, 8))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_31.setFont(font)
        self.label_31.setStyleSheet("background-color:rgb(60,62, 84);color:rgb(150,150,150)")
        self.label_31.setObjectName("label_31")
        self.botao_salvar = QtWidgets.QPushButton(self.tab_5)
        self.botao_salvar.setGeometry(QtCore.QRect(365, 16, 32, 32))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_salvar.setFont(font)
        self.botao_salvar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_salvar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_salvar.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.botao_salvar.setStyleSheet("border-radius:7px;\n"
"")
        self.botao_salvar.setIconSize(QtCore.QSize(16, 16))
        self.botao_salvar.setObjectName("botao_salvar")
        self.botao_excluir_dados = QtWidgets.QPushButton(self.tab_5)
        self.botao_excluir_dados.setGeometry(QtCore.QRect(403, 16, 32, 32))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_excluir_dados.setFont(font)
        self.botao_excluir_dados.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_excluir_dados.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_excluir_dados.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.botao_excluir_dados.setStyleSheet("border-radius:7px;\n"
"")
        self.botao_excluir_dados.setObjectName("botao_excluir_dados")
        self.label_confirmacao_salvar = QtWidgets.QLabel(self.tab_5)
        self.label_confirmacao_salvar.setGeometry(QtCore.QRect(379, 10, 17, 17))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_confirmacao_salvar.setFont(font)
        self.label_confirmacao_salvar.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
        self.label_confirmacao_salvar.setText("")
        self.label_confirmacao_salvar.setObjectName("label_confirmacao_salvar")
        self.campo_email_enviado = QtWidgets.QLineEdit(self.tab_5)
        self.campo_email_enviado.setGeometry(QtCore.QRect(628, 599, 133, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_email_enviado.setFont(font)
        self.campo_email_enviado.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_email_enviado.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(40, 42, 54);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(68, 71, 90);\n"
"}\n"
"")
        self.campo_email_enviado.setText("")
        self.campo_email_enviado.setObjectName("campo_email_enviado")
        self.label_confirmacao_excluir = QtWidgets.QLabel(self.tab_5)
        self.label_confirmacao_excluir.setGeometry(QtCore.QRect(416, 10, 17, 17))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_confirmacao_excluir.setFont(font)
        self.label_confirmacao_excluir.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
        self.label_confirmacao_excluir.setText("")
        self.label_confirmacao_excluir.setObjectName("label_confirmacao_excluir")
        self.alerta_midia = QtWidgets.QPushButton(self.tab_5)
        self.alerta_midia.setGeometry(QtCore.QRect(384, 64, 26, 26))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.alerta_midia.setFont(font)
        self.alerta_midia.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.alerta_midia.setFocusPolicy(QtCore.Qt.NoFocus)
        self.alerta_midia.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.alerta_midia.setStyleSheet("border-radius:7px;\n"
";background-color: transparent")
        self.alerta_midia.setText("")
        self.alerta_midia.setObjectName("alerta_midia")
        self.botao_agrupar_PDF_pasta_cliente = QtWidgets.QPushButton(self.tab_5)
        self.botao_agrupar_PDF_pasta_cliente.setGeometry(QtCore.QRect(567, 216, 29, 28))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.botao_agrupar_PDF_pasta_cliente.setFont(font)
        self.botao_agrupar_PDF_pasta_cliente.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_agrupar_PDF_pasta_cliente.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_agrupar_PDF_pasta_cliente.setStyleSheet("border-radius:10px;\n"
"background-color:transparent")
        self.botao_agrupar_PDF_pasta_cliente.setFlat(True)
        self.botao_agrupar_PDF_pasta_cliente.setObjectName("botao_agrupar_PDF_pasta_cliente")
        self.botao_converter_todas_imagens_em_pdf = QtWidgets.QPushButton(self.tab_5)
        self.botao_converter_todas_imagens_em_pdf.setGeometry(QtCore.QRect(565, 186, 30, 32))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.botao_converter_todas_imagens_em_pdf.setFont(font)
        self.botao_converter_todas_imagens_em_pdf.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_converter_todas_imagens_em_pdf.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_converter_todas_imagens_em_pdf.setStyleSheet("border-radius:10px;background-color:transparent")
        self.botao_converter_todas_imagens_em_pdf.setAutoDefault(False)
        self.botao_converter_todas_imagens_em_pdf.setDefault(False)
        self.botao_converter_todas_imagens_em_pdf.setFlat(True)
        self.botao_converter_todas_imagens_em_pdf.setObjectName("botao_converter_todas_imagens_em_pdf")
        self.label_12 = QtWidgets.QLabel(self.tab_5)
        self.label_12.setGeometry(QtCore.QRect(346, 178, 61, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_12.setObjectName("label_12")
        self.label_49 = QtWidgets.QLabel(self.tab_5)
        self.label_49.setGeometry(QtCore.QRect(300, 408, 45, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_49.setFont(font)
        self.label_49.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_49.setObjectName("label_49")
        self.label_44 = QtWidgets.QLabel(self.tab_5)
        self.label_44.setGeometry(QtCore.QRect(448, 176, 101, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_44.setFont(font)
        self.label_44.setStyleSheet("background-color:rgb(60, 62, 84);\n"
"color:rgb(170,170,170)")
        self.label_44.setAlignment(QtCore.Qt.AlignCenter)
        self.label_44.setObjectName("label_44")
        self.campo_cnh = QtWidgets.QLineEdit(self.tab_5)
        self.campo_cnh.setGeometry(QtCore.QRect(18, 358, 117, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_cnh.setFont(font)
        self.campo_cnh.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_cnh.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_cnh.setText("")
        self.campo_cnh.setObjectName("campo_cnh")
        self.label_15 = QtWidgets.QLabel(self.tab_5)
        self.label_15.setGeometry(QtCore.QRect(17, 348, 25, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.tab_5)
        self.label_16.setGeometry(QtCore.QRect(16, 406, 80, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_16.setObjectName("label_16")
        self.label_11 = QtWidgets.QLabel(self.tab_5)
        self.label_11.setGeometry(QtCore.QRect(17, 236, 37, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_11.setObjectName("label_11")
        self.botao_telefone = QtWidgets.QPushButton(self.tab_5)
        self.botao_telefone.setGeometry(QtCore.QRect(418, 244, 25, 25))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_telefone.setFont(font)
        self.botao_telefone.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_telefone.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_telefone.setStyleSheet("border-radius:10px;background-color:transparent")
        self.botao_telefone.setObjectName("botao_telefone")
        self.botao_consulta_pis = QtWidgets.QPushButton(self.tab_5)
        self.botao_consulta_pis.setGeometry(QtCore.QRect(418, 418, 21, 25))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_pis.setFont(font)
        self.botao_consulta_pis.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_pis.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_consulta_pis.setStyleSheet("border-radius:10px;background-color:transparent")
        self.botao_consulta_pis.setObjectName("botao_consulta_pis")
        self.label_10 = QtWidgets.QLabel(self.tab_5)
        self.label_10.setGeometry(QtCore.QRect(186, 292, 21, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_10.setObjectName("label_10")
        self.label_18 = QtWidgets.QLabel(self.tab_5)
        self.label_18.setGeometry(QtCore.QRect(146, 348, 65, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_18.setFont(font)
        self.label_18.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_18.setObjectName("label_18")
        self.campo_nome_mae = QtWidgets.QLineEdit(self.tab_5)
        self.campo_nome_mae.setGeometry(QtCore.QRect(144, 358, 294, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_nome_mae.setFont(font)
        self.campo_nome_mae.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_nome_mae.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_nome_mae.setText("")
        self.campo_nome_mae.setObjectName("campo_nome_mae")
        self.botao_consulta_cpf = QtWidgets.QPushButton(self.tab_5)
        self.botao_consulta_cpf.setGeometry(QtCore.QRect(152, 302, 21, 25))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_cpf.setFont(font)
        self.botao_consulta_cpf.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_cpf.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_consulta_cpf.setStyleSheet("border-radius:10px;background-color:transparent")
        self.botao_consulta_cpf.setObjectName("botao_consulta_cpf")
        self.label_27 = QtWidgets.QLabel(self.tab_5)
        self.label_27.setGeometry(QtCore.QRect(450, 406, 61, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_27.setFont(font)
        self.label_27.setStyleSheet("background-color:rgb(60, 62, 84);\n"
"color:rgb(170,170,170)")
        self.label_27.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_27.setObjectName("label_27")
        self.label_24 = QtWidgets.QLabel(self.tab_5)
        self.label_24.setGeometry(QtCore.QRect(17, 178, 77, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_24.setFont(font)
        self.label_24.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_24.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_24.setObjectName("label_24")
        self.botao_consulta_rg = QtWidgets.QPushButton(self.tab_5)
        self.botao_consulta_rg.setGeometry(QtCore.QRect(286, 302, 17, 25))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_rg.setFont(font)
        self.botao_consulta_rg.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_rg.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_consulta_rg.setStyleSheet("border-radius:10px;background-color:transparent")
        self.botao_consulta_rg.setObjectName("botao_consulta_rg")
        self.campo_comentario = QtWidgets.QTextEdit(self.tab_5)
        self.campo_comentario.setGeometry(QtCore.QRect(448, 416, 148, 204))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.campo_comentario.setFont(font)
        self.campo_comentario.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_comentario.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.campo_comentario.setStyleSheet("border-radius:7px;\n"
"border: 1px solid rgb(120,120,120);\n"
"background-color:rgb(60,62, 84);\n"
"color:orange")
        self.campo_comentario.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.campo_comentario.setObjectName("campo_comentario")
        self.label_6 = QtWidgets.QLabel(self.tab_5)
        self.label_6.setGeometry(QtCore.QRect(17, 292, 25, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_6.setObjectName("label_6")
        self.tabela_documentos = QtWidgets.QTableWidget(self.tab_5)
        self.tabela_documentos.setGeometry(QtCore.QRect(449, 186, 148, 206))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(8)
        self.tabela_documentos.setFont(font)
        self.tabela_documentos.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.tabela_documentos.setStyleSheet("border-radius:7px;\n"
"border: 1px solid rgb(120,120,120);\n"
"background-color:rgb(60,62, 84);")
        self.tabela_documentos.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tabela_documentos.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tabela_documentos.setColumnCount(1)
        self.tabela_documentos.setObjectName("tabela_documentos")
        self.tabela_documentos.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tabela_documentos.setHorizontalHeaderItem(0, item)
        self.tabela_documentos.horizontalHeader().setVisible(False)
        self.tabela_documentos.horizontalHeader().setCascadingSectionResizes(False)
        self.tabela_documentos.horizontalHeader().setDefaultSectionSize(240)
        self.tabela_documentos.horizontalHeader().setHighlightSections(True)
        self.tabela_documentos.horizontalHeader().setSortIndicatorShown(False)
        self.tabela_documentos.horizontalHeader().setStretchLastSection(True)
        self.tabela_documentos.verticalHeader().setVisible(False)
        self.tabela_documentos.verticalHeader().setDefaultSectionSize(12)
        self.tabela_documentos.verticalHeader().setHighlightSections(False)
        self.tabela_documentos.verticalHeader().setMinimumSectionSize(20)
        self.campo_data_nascimento = QtWidgets.QDateEdit(self.tab_5)
        self.campo_data_nascimento.setGeometry(QtCore.QRect(346, 188, 91, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_data_nascimento.setFont(font)
        self.campo_data_nascimento.setStyleSheet("QDateEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QDateEdit:disabled, QDateEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"\n"
"QDateEdit::up-button {\n"
"    width: 0;\n"
"    height: 0;\n"
"    border: none;\n"
"}\n"
"\n"
"QDateEdit::down-button {\n"
"    width: 0;\n"
"    height: 0;\n"
"    border: none;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"")
        self.campo_data_nascimento.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_data_nascimento.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.campo_data_nascimento.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToPreviousValue)
        self.campo_data_nascimento.setProperty("showGroupSeparator", False)
        self.campo_data_nascimento.setCalendarPopup(False)
        self.campo_data_nascimento.setObjectName("campo_data_nascimento")
        self.label_48 = QtWidgets.QLabel(self.tab_5)
        self.label_48.setGeometry(QtCore.QRect(318, 292, 57, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_48.setFont(font)
        self.label_48.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_48.setObjectName("label_48")
        self.botao_enviar_email = QtWidgets.QPushButton(self.tab_5)
        self.botao_enviar_email.setGeometry(QtCore.QRect(282, 244, 25, 25))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_enviar_email.setFont(font)
        self.botao_enviar_email.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_enviar_email.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_enviar_email.setStyleSheet("border-radius:10px;background-color:transparent")
        self.botao_enviar_email.setObjectName("botao_enviar_email")
        self.campo_rg = QtWidgets.QLineEdit(self.tab_5)
        self.campo_rg.setGeometry(QtCore.QRect(185, 302, 119, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_rg.setFont(font)
        self.campo_rg.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_rg.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_rg.setText("")
        self.campo_rg.setPlaceholderText("")
        self.campo_rg.setObjectName("campo_rg")
        self.campo_telefone = QtWidgets.QLineEdit(self.tab_5)
        self.campo_telefone.setGeometry(QtCore.QRect(317, 246, 121, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_telefone.setFont(font)
        self.campo_telefone.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_telefone.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_telefone.setText("")
        self.campo_telefone.setObjectName("campo_telefone")
        self.botao_consulta_funcional = QtWidgets.QPushButton(self.tab_5)
        self.botao_consulta_funcional.setGeometry(QtCore.QRect(270, 418, 17, 25))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_funcional.setFont(font)
        self.botao_consulta_funcional.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_funcional.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_consulta_funcional.setStyleSheet("border-radius:10px;background-color:transparent")
        self.botao_consulta_funcional.setObjectName("botao_consulta_funcional")
        self.campo_nome = QtWidgets.QLineEdit(self.tab_5)
        self.campo_nome.setGeometry(QtCore.QRect(16, 188, 316, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_nome.setFont(font)
        self.campo_nome.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_nome.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_nome.setText("")
        self.campo_nome.setPlaceholderText("")
        self.campo_nome.setObjectName("campo_nome")
        self.campo_funcional = QtWidgets.QLineEdit(self.tab_5)
        self.campo_funcional.setGeometry(QtCore.QRect(146, 418, 142, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_funcional.setFont(font)
        self.campo_funcional.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_funcional.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_funcional.setText("")
        self.campo_funcional.setPlaceholderText("")
        self.campo_funcional.setObjectName("campo_funcional")
        self.label_50 = QtWidgets.QLabel(self.tab_5)
        self.label_50.setGeometry(QtCore.QRect(146, 408, 55, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_50.setFont(font)
        self.label_50.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_50.setObjectName("label_50")
        self.campo_seguranca_cnh = QtWidgets.QLineEdit(self.tab_5)
        self.campo_seguranca_cnh.setGeometry(QtCore.QRect(17, 418, 119, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_seguranca_cnh.setFont(font)
        self.campo_seguranca_cnh.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_seguranca_cnh.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_seguranca_cnh.setObjectName("campo_seguranca_cnh")
        self.campo_email = QtWidgets.QLineEdit(self.tab_5)
        self.campo_email.setGeometry(QtCore.QRect(15, 246, 289, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_email.setFont(font)
        self.campo_email.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_email.setText("")
        self.campo_email.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.campo_email.setPlaceholderText("")
        self.campo_email.setObjectName("campo_email")
        self.botao_consulta_cnh = QtWidgets.QPushButton(self.tab_5)
        self.botao_consulta_cnh.setGeometry(QtCore.QRect(116, 358, 21, 25))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_cnh.setFont(font)
        self.botao_consulta_cnh.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_cnh.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_consulta_cnh.setStyleSheet("border-radius:10px;background-color:transparent")
        self.botao_consulta_cnh.setObjectName("botao_consulta_cnh")
        self.campo_cpf = QtWidgets.QLineEdit(self.tab_5)
        self.campo_cpf.setGeometry(QtCore.QRect(15, 302, 156, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_cpf.setFont(font)
        self.campo_cpf.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_cpf.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_cpf.setText("")
        self.campo_cpf.setPlaceholderText("")
        self.campo_cpf.setObjectName("campo_cpf")
        self.label_46 = QtWidgets.QLabel(self.tab_5)
        self.label_46.setGeometry(QtCore.QRect(318, 236, 49, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_46.setFont(font)
        self.label_46.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_46.setObjectName("label_46")
        self.campo_pis = QtWidgets.QLineEdit(self.tab_5)
        self.campo_pis.setGeometry(QtCore.QRect(299, 418, 138, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_pis.setFont(font)
        self.campo_pis.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_pis.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_pis.setText("")
        self.campo_pis.setObjectName("campo_pis")
        self.campo_rg_orgao = QtWidgets.QLineEdit(self.tab_5)
        self.campo_rg_orgao.setGeometry(QtCore.QRect(318, 302, 119, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_rg_orgao.setFont(font)
        self.campo_rg_orgao.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_rg_orgao.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_rg_orgao.setText("")
        self.campo_rg_orgao.setPlaceholderText("")
        self.campo_rg_orgao.setObjectName("campo_rg_orgao")
        self.campo_cnpj_municipio = QtWidgets.QLineEdit(self.tab_5)
        self.campo_cnpj_municipio.setEnabled(True)
        self.campo_cnpj_municipio.setGeometry(QtCore.QRect(16, 594, 421, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_cnpj_municipio.setFont(font)
        self.campo_cnpj_municipio.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.campo_cnpj_municipio.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_cnpj_municipio.setText("")
        self.campo_cnpj_municipio.setPlaceholderText("")
        self.campo_cnpj_municipio.setObjectName("campo_cnpj_municipio")
        self.campo_cnpj = QtWidgets.QLineEdit(self.tab_5)
        self.campo_cnpj.setGeometry(QtCore.QRect(15, 490, 314, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_cnpj.setFont(font)
        self.campo_cnpj.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_cnpj.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_cnpj.setText("")
        self.campo_cnpj.setPlaceholderText("")
        self.campo_cnpj.setObjectName("campo_cnpj")
        self.label_25 = QtWidgets.QLabel(self.tab_5)
        self.label_25.setGeometry(QtCore.QRect(16, 584, 77, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_25.setFont(font)
        self.label_25.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_25.setObjectName("label_25")
        self.botao_consulta_cnpj = QtWidgets.QPushButton(self.tab_5)
        self.botao_consulta_cnpj.setGeometry(QtCore.QRect(290, 488, 17, 25))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consulta_cnpj.setFont(font)
        self.botao_consulta_cnpj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consulta_cnpj.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_consulta_cnpj.setStyleSheet("border-radius:10px;background-color:transparent")
        self.botao_consulta_cnpj.setObjectName("botao_consulta_cnpj")
        self.campo_cnpj_razao_social = QtWidgets.QLineEdit(self.tab_5)
        self.campo_cnpj_razao_social.setGeometry(QtCore.QRect(16, 543, 421, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_cnpj_razao_social.setFont(font)
        self.campo_cnpj_razao_social.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_cnpj_razao_social.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_cnpj_razao_social.setText("")
        self.campo_cnpj_razao_social.setPlaceholderText("")
        self.campo_cnpj_razao_social.setObjectName("campo_cnpj_razao_social")
        self.botao_junta = QtWidgets.QPushButton(self.tab_5)
        self.botao_junta.setGeometry(QtCore.QRect(418, 490, 17, 25))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.botao_junta.setFont(font)
        self.botao_junta.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_junta.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_junta.setStyleSheet("border-radius:10px;background-color:transparent")
        self.botao_junta.setObjectName("botao_junta")
        self.label_47 = QtWidgets.QLabel(self.tab_5)
        self.label_47.setGeometry(QtCore.QRect(16, 534, 105, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_47.setFont(font)
        self.label_47.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_47.setObjectName("label_47")
        self.campo_lista_junta_comercial = QtWidgets.QComboBox(self.tab_5)
        self.campo_lista_junta_comercial.setGeometry(QtCore.QRect(346, 490, 91, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_lista_junta_comercial.setFont(font)
        self.campo_lista_junta_comercial.setStyleSheet("QComboBox {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QComboBox:disabled, QComboBox:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: none;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    width: 0;\n"
"}")
        self.campo_lista_junta_comercial.setEditable(False)
        self.campo_lista_junta_comercial.setObjectName("campo_lista_junta_comercial")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.setItemText(0, "")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.campo_lista_junta_comercial.addItem("")
        self.botao_dados_cnpj = QtWidgets.QPushButton(self.tab_5)
        self.botao_dados_cnpj.setGeometry(QtCore.QRect(308, 488, 21, 25))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_dados_cnpj.setFont(font)
        self.botao_dados_cnpj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_dados_cnpj.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_dados_cnpj.setStyleSheet("border-radius:10px;background-color:transparent")
        self.botao_dados_cnpj.setObjectName("botao_dados_cnpj")
        self.label_14 = QtWidgets.QLabel(self.tab_5)
        self.label_14.setGeometry(QtCore.QRect(17, 480, 29, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_14.setFont(font)
        self.label_14.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_14.setObjectName("label_14")
        self.label_28 = QtWidgets.QLabel(self.tab_5)
        self.label_28.setGeometry(QtCore.QRect(346, 480, 41, 7))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_28.setFont(font)
        self.label_28.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_28.setObjectName("label_28")
        self.label_38 = QtWidgets.QLabel(self.tab_5)
        self.label_38.setGeometry(QtCore.QRect(13, 154, 585, 13))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_38.setFont(font)
        self.label_38.setStyleSheet("background-color:rgb(40, 45, 50);\n"
"")
        self.label_38.setObjectName("label_38")
        self.label_39 = QtWidgets.QLabel(self.tab_5)
        self.label_39.setGeometry(QtCore.QRect(13, 456, 426, 13))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_39.setFont(font)
        self.label_39.setStyleSheet("background-color:rgb(40, 45, 50);\n"
"")
        self.label_39.setObjectName("label_39")
        self.campo_funcional.raise_()
        self.campo_cnh.raise_()
        self.campo_cnpj_razao_social.raise_()
        self.label_47.raise_()
        self.campo_lista_junta_comercial.raise_()
        self.campo_pis.raise_()
        self.campo_rg.raise_()
        self.label_16.raise_()
        self.campo_telefone.raise_()
        self.campo_cpf.raise_()
        self.tabela_documentos.raise_()
        self.campo_data_agendamento.raise_()
        self.campo_pedido.raise_()
        self.campo_hora_agendamento.raise_()
        self.label_4.raise_()
        self.label_3.raise_()
        self.campo_lista_venda.raise_()
        self.label_22.raise_()
        self.campo_lista_modalidade.raise_()
        self.label.raise_()
        self.label_23.raise_()
        self.botao_pasta_cliente.raise_()
        self.label_confirmacao_criar_pasta.raise_()
        self.campo_lista_versao_certificado.raise_()
        self.label_40.raise_()
        self.campo_preco_certificado.raise_()
        self.label_13.raise_()
        self.groupBox_status.raise_()
        self.campo_preco_certificado_cheio.raise_()
        self.label_17.raise_()
        self.botao_link_venda.raise_()
        self.botao_salvar.raise_()
        self.botao_excluir_dados.raise_()
        self.label_confirmacao_salvar.raise_()
        self.label_31.raise_()
        self.campo_email_enviado.raise_()
        self.label_confirmacao_excluir.raise_()
        self.alerta_midia.raise_()
        self.botao_agrupar_PDF_pasta_cliente.raise_()
        self.botao_converter_todas_imagens_em_pdf.raise_()
        self.label_12.raise_()
        self.label_49.raise_()
        self.label_44.raise_()
        self.label_15.raise_()
        self.label_11.raise_()
        self.botao_telefone.raise_()
        self.botao_consulta_pis.raise_()
        self.label_10.raise_()
        self.label_18.raise_()
        self.campo_nome_mae.raise_()
        self.botao_consulta_cpf.raise_()
        self.label_27.raise_()
        self.label_24.raise_()
        self.botao_consulta_rg.raise_()
        self.campo_comentario.raise_()
        self.label_6.raise_()
        self.campo_data_nascimento.raise_()
        self.label_48.raise_()
        self.botao_consulta_funcional.raise_()
        self.campo_nome.raise_()
        self.label_50.raise_()
        self.campo_seguranca_cnh.raise_()
        self.campo_email.raise_()
        self.botao_consulta_cnh.raise_()
        self.label_46.raise_()
        self.campo_rg_orgao.raise_()
        self.campo_cnpj_municipio.raise_()
        self.campo_cnpj.raise_()
        self.label_25.raise_()
        self.botao_consulta_cnpj.raise_()
        self.botao_junta.raise_()
        self.botao_dados_cnpj.raise_()
        self.label_14.raise_()
        self.label_28.raise_()
        self.botao_enviar_email.raise_()
        self.label_38.raise_()
        self.label_39.raise_()
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.botao_procurar = QtWidgets.QPushButton(self.tab_6)
        self.botao_procurar.setGeometry(QtCore.QRect(528, 594, 62, 29))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.botao_procurar.setFont(font)
        self.botao_procurar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_procurar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_procurar.setStyleSheet("border-radius:4px;\n"
"background-color:rgb(73, 218, 107);\n"
"color:rgb(255,255,255);\n"
"")
        self.botao_procurar.setObjectName("botao_procurar")
        self.label_quantidade_bd = QtWidgets.QLabel(self.tab_6)
        self.label_quantidade_bd.setGeometry(QtCore.QRect(172, 596, 226, 25))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_quantidade_bd.setFont(font)
        self.label_quantidade_bd.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_quantidade_bd.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_quantidade_bd.setStyleSheet("color:rgb(220,220,220);")
        self.label_quantidade_bd.setText("")
        self.label_quantidade_bd.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_quantidade_bd.setObjectName("label_quantidade_bd")
        self.botao_consultar = QtWidgets.QPushButton(self.tab_6)
        self.botao_consultar.setGeometry(QtCore.QRect(165, 144, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_consultar.setFont(font)
        self.botao_consultar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_consultar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_consultar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.botao_consultar.setStyleSheet("border-radius:7px;\n"
"background-color:transparent")
        self.botao_consultar.setObjectName("botao_consultar")
        self.campo_data_ate = QtWidgets.QDateEdit(self.tab_6)
        self.campo_data_ate.setGeometry(QtCore.QRect(18, 82, 140, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_data_ate.setFont(font)
        self.campo_data_ate.setStyleSheet("QDateEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QDateEdit:disabled, QDateEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"\n"
"QDateEdit::up-button {\n"
"    width: 0;\n"
"    height: 0;\n"
"    border: none;\n"
"}\n"
"\n"
"QDateEdit::down-button {\n"
"    width: 0;\n"
"    height: 0;\n"
"    border: none;\n"
"}\n"
"")
        self.campo_data_ate.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.campo_data_ate.setObjectName("campo_data_ate")
        self.campo_lista_status_2 = QtWidgets.QComboBox(self.tab_6)
        self.campo_lista_status_2.setGeometry(QtCore.QRect(18, 146, 140, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_lista_status_2.setFont(font)
        self.campo_lista_status_2.setStyleSheet("QComboBox {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QComboBox:disabled, QComboBox:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: none;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    width: 0;\n"
"}\n"
"\n"
"\n"
"")
        self.campo_lista_status_2.setEditable(False)
        self.campo_lista_status_2.setObjectName("campo_lista_status_2")
        self.campo_lista_status_2.addItem("")
        self.campo_lista_status_2.addItem("")
        self.campo_lista_status_2.addItem("")
        self.campo_lista_status_2.addItem("")
        self.campo_lista_status_2.addItem("")
        self.campo_lista_status_2.addItem("")
        self.label_19 = QtWidgets.QLabel(self.tab_6)
        self.label_19.setGeometry(QtCore.QRect(14, 8, 21, 9))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_19.setFont(font)
        self.label_19.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_19.setObjectName("label_19")
        self.barra_progresso_consulta = QtWidgets.QProgressBar(self.tab_6)
        self.barra_progresso_consulta.setGeometry(QtCore.QRect(18, 174, 140, 3))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(1)
        font.setBold(False)
        font.setWeight(50)
        self.barra_progresso_consulta.setFont(font)
        self.barra_progresso_consulta.setStyleSheet("")
        self.barra_progresso_consulta.setProperty("value", 0)
        self.barra_progresso_consulta.setAlignment(QtCore.Qt.AlignCenter)
        self.barra_progresso_consulta.setFormat("")
        self.barra_progresso_consulta.setObjectName("barra_progresso_consulta")
        self.label_21 = QtWidgets.QLabel(self.tab_6)
        self.label_21.setGeometry(QtCore.QRect(14, 138, 45, 9))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_21.setFont(font)
        self.label_21.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_21.setObjectName("label_21")
        self.campo_data_de = QtWidgets.QDateEdit(self.tab_6)
        self.campo_data_de.setGeometry(QtCore.QRect(18, 16, 140, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_data_de.setFont(font)
        self.campo_data_de.setStyleSheet("QDateEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QDateEdit:disabled, QDateEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"\n"
"QDateEdit::up-button {\n"
"    width: 0;\n"
"    height: 0;\n"
"    border: none;\n"
"}\n"
"\n"
"QDateEdit::down-button {\n"
"    width: 0;\n"
"    height: 0;\n"
"    border: none;\n"
"}\n"
"")
        self.campo_data_de.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.campo_data_de.setObjectName("campo_data_de")
        self.label_20 = QtWidgets.QLabel(self.tab_6)
        self.label_20.setGeometry(QtCore.QRect(14, 74, 25, 9))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_20.setFont(font)
        self.label_20.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_20.setObjectName("label_20")
        self.label_msg_copiado = QtWidgets.QLabel(self.tab_6)
        self.label_msg_copiado.setGeometry(QtCore.QRect(18, 594, 29, 25))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_msg_copiado.setFont(font)
        self.label_msg_copiado.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_msg_copiado.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_msg_copiado.setStyleSheet("color:rgb(90,54,247);")
        self.label_msg_copiado.setText("")
        self.label_msg_copiado.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_msg_copiado.setObjectName("label_msg_copiado")
        self.botao_hoje = QtWidgets.QPushButton(self.tab_6)
        self.botao_hoje.setGeometry(QtCore.QRect(165, 82, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_hoje.setFont(font)
        self.botao_hoje.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_hoje.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_hoje.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.botao_hoje.setStyleSheet("border-radius:7px;\n"
"background-color:transparent")
        self.botao_hoje.setObjectName("botao_hoje")
        self.campo_relatorio = QtWidgets.QTextEdit(self.tab_6)
        self.campo_relatorio.setGeometry(QtCore.QRect(242, 16, 349, 163))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_relatorio.setFont(font)
        self.campo_relatorio.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_relatorio.setStyleSheet("border-radius:7px;\n"
"border: 1px solid rgb(120,120,120);\n"
"background-color:rgb(60,62, 84);")
        self.campo_relatorio.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.campo_relatorio.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.campo_relatorio.setObjectName("campo_relatorio")
        self.label_26 = QtWidgets.QLabel(self.tab_6)
        self.label_26.setGeometry(QtCore.QRect(254, 10, 57, 9))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_26.setFont(font)
        self.label_26.setStyleSheet("background-color:rgb(60, 62, 84);\n"
"color:rgb(170,170,170)")
        self.label_26.setObjectName("label_26")
        self.botao_envio_massa = QtWidgets.QPushButton(self.tab_6)
        self.botao_envio_massa.setGeometry(QtCore.QRect(404, 594, 117, 29))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.botao_envio_massa.setFont(font)
        self.botao_envio_massa.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_envio_massa.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_envio_massa.setStyleSheet("border-radius:4px;\n"
"background-color:rgb(120, 0, 190);\n"
"color:rgb(205,205,205);\n"
"")
        self.botao_envio_massa.setObjectName("botao_envio_massa")
        self.botao_excluir_dados_tabela = QtWidgets.QPushButton(self.tab_6)
        self.botao_excluir_dados_tabela.setGeometry(QtCore.QRect(200, 144, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_excluir_dados_tabela.setFont(font)
        self.botao_excluir_dados_tabela.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_excluir_dados_tabela.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_excluir_dados_tabela.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.botao_excluir_dados_tabela.setStyleSheet("border-radius:7px;\n"
"background-color:transparent")
        self.botao_excluir_dados_tabela.setObjectName("botao_excluir_dados_tabela")
        self.tableWidget = QtWidgets.QTableWidget(self.tab_6)
        self.tableWidget.setGeometry(QtCore.QRect(18, 192, 574, 394))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(8)
        self.tableWidget.setFont(font)
        self.tableWidget.setStyleSheet("/* Adicionar borda ao redor de todo o QTableWidget */\n"
"QTableWidget {\n"
"    border: 1px solid rgb(100, 100, 100); /* Borda ao redor da tabela */\n"
"}\n"
"\n"
"/* Adicionar borda ao redor do header */\n"
"\n"
"\n"
"/* Estilo para cada seção do header */\n"
"QHeaderView::section {\n"
"    border: 1px solid rgb(100, 100, 100); /* Borda ao redor de cada célula do cabeçalho */\n"
"    background-color: transparent; /* Fundo transparente */\n"
"    padding: 1px; /* Ajuste de espaçamento */\n"
"}\n"
"")
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
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
        self.tableWidget.horizontalHeader().setDefaultSectionSize(96)
        self.tableWidget.verticalHeader().setVisible(False)
        self.botao_procurar.raise_()
        self.label_quantidade_bd.raise_()
        self.botao_consultar.raise_()
        self.campo_data_ate.raise_()
        self.campo_lista_status_2.raise_()
        self.label_21.raise_()
        self.campo_data_de.raise_()
        self.label_20.raise_()
        self.label_msg_copiado.raise_()
        self.botao_hoje.raise_()
        self.label_19.raise_()
        self.campo_relatorio.raise_()
        self.label_26.raise_()
        self.botao_envio_massa.raise_()
        self.botao_excluir_dados_tabela.raise_()
        self.tableWidget.raise_()
        self.barra_progresso_consulta.raise_()
        self.tabWidget.addTab(self.tab_6, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tab_2)
        self.tabWidget_2.setGeometry(QtCore.QRect(16, 69, 580, 563))
        self.tabWidget_2.setStyleSheet("QTabBar::tab:selected {\n"
"    background-color: rgb(70,72, 84); /* Cor das abas selecionadas */\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QTabBar::tab:Hover {\n"
"    background-color: rgb(80, 82, 84); /* Cor das abas selecionadas */\n"
"}")
        self.tabWidget_2.setUsesScrollButtons(False)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.barra_meta_semana_2 = QtWidgets.QProgressBar(self.tab_3)
        self.barra_meta_semana_2.setGeometry(QtCore.QRect(16, 162, 547, 40))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        self.barra_meta_semana_2.setFont(font)
        self.barra_meta_semana_2.setStyleSheet("color:rgb(113,66,230)")
        self.barra_meta_semana_2.setProperty("value", 0)
        self.barra_meta_semana_2.setAlignment(QtCore.Qt.AlignCenter)
        self.barra_meta_semana_2.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.barra_meta_semana_2.setFormat("")
        self.barra_meta_semana_2.setObjectName("barra_meta_semana_2")
        self.barra_meta_mensal = QtWidgets.QProgressBar(self.tab_3)
        self.barra_meta_mensal.setGeometry(QtCore.QRect(16, 440, 547, 40))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        self.barra_meta_mensal.setFont(font)
        self.barra_meta_mensal.setStyleSheet("color:rgb(113,66,230)")
        self.barra_meta_mensal.setMaximum(300)
        self.barra_meta_mensal.setProperty("value", 0)
        self.barra_meta_mensal.setAlignment(QtCore.Qt.AlignCenter)
        self.barra_meta_mensal.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.barra_meta_mensal.setFormat("")
        self.barra_meta_mensal.setObjectName("barra_meta_mensal")
        self.barra_meta_semana_5 = QtWidgets.QProgressBar(self.tab_3)
        self.barra_meta_semana_5.setGeometry(QtCore.QRect(16, 370, 547, 40))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        self.barra_meta_semana_5.setFont(font)
        self.barra_meta_semana_5.setStyleSheet("color:rgb(113,66,230)")
        self.barra_meta_semana_5.setProperty("value", 0)
        self.barra_meta_semana_5.setAlignment(QtCore.Qt.AlignCenter)
        self.barra_meta_semana_5.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.barra_meta_semana_5.setFormat("")
        self.barra_meta_semana_5.setObjectName("barra_meta_semana_5")
        self.label_meta3 = QtWidgets.QLabel(self.tab_3)
        self.label_meta3.setGeometry(QtCore.QRect(16, 232, 547, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_meta3.setFont(font)
        self.label_meta3.setStyleSheet("color:rgb(113,66,230);border: 1px solid rgb(68,71,90)")
        self.label_meta3.setText("")
        self.label_meta3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_meta3.setObjectName("label_meta3")
        self.label_meta_mes = QtWidgets.QLabel(self.tab_3)
        self.label_meta_mes.setGeometry(QtCore.QRect(16, 440, 547, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_meta_mes.setFont(font)
        self.label_meta_mes.setStyleSheet("color:rgb(113,66,230);border: 1px solid rgb(68,71,90)")
        self.label_meta_mes.setText("")
        self.label_meta_mes.setAlignment(QtCore.Qt.AlignCenter)
        self.label_meta_mes.setObjectName("label_meta_mes")
        self.label_meta4 = QtWidgets.QLabel(self.tab_3)
        self.label_meta4.setGeometry(QtCore.QRect(16, 302, 547, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_meta4.setFont(font)
        self.label_meta4.setStyleSheet("color:rgb(113,66,230);border: 1px solid rgb(68,71,90)")
        self.label_meta4.setText("")
        self.label_meta4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_meta4.setObjectName("label_meta4")
        self.barra_meta_semana_1 = QtWidgets.QProgressBar(self.tab_3)
        self.barra_meta_semana_1.setGeometry(QtCore.QRect(16, 92, 547, 40))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        self.barra_meta_semana_1.setFont(font)
        self.barra_meta_semana_1.setStyleSheet("color:rgb(113,66,230)")
        self.barra_meta_semana_1.setProperty("value", 0)
        self.barra_meta_semana_1.setAlignment(QtCore.Qt.AlignCenter)
        self.barra_meta_semana_1.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.barra_meta_semana_1.setFormat("")
        self.barra_meta_semana_1.setObjectName("barra_meta_semana_1")
        self.label_meta2 = QtWidgets.QLabel(self.tab_3)
        self.label_meta2.setGeometry(QtCore.QRect(16, 162, 547, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_meta2.setFont(font)
        self.label_meta2.setStyleSheet("color:rgb(113,66,230);border: 1px solid rgb(68,71,90)")
        self.label_meta2.setText("")
        self.label_meta2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_meta2.setObjectName("label_meta2")
        self.label_meta5 = QtWidgets.QLabel(self.tab_3)
        self.label_meta5.setGeometry(QtCore.QRect(16, 370, 547, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_meta5.setFont(font)
        self.label_meta5.setStyleSheet("color:rgb(113,66,230);border: 1px solid rgb(68,71,90)")
        self.label_meta5.setText("")
        self.label_meta5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_meta5.setObjectName("label_meta5")
        self.barra_meta_semana_4 = QtWidgets.QProgressBar(self.tab_3)
        self.barra_meta_semana_4.setGeometry(QtCore.QRect(16, 302, 547, 40))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        self.barra_meta_semana_4.setFont(font)
        self.barra_meta_semana_4.setStyleSheet("color:rgb(113,66,230)")
        self.barra_meta_semana_4.setProperty("value", 0)
        self.barra_meta_semana_4.setAlignment(QtCore.Qt.AlignCenter)
        self.barra_meta_semana_4.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.barra_meta_semana_4.setFormat("")
        self.barra_meta_semana_4.setObjectName("barra_meta_semana_4")
        self.label_meta1 = QtWidgets.QLabel(self.tab_3)
        self.label_meta1.setGeometry(QtCore.QRect(16, 92, 547, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_meta1.setFont(font)
        self.label_meta1.setStyleSheet("color:rgb(113,66,230);border: 1px solid rgb(68,71,90)")
        self.label_meta1.setText("")
        self.label_meta1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_meta1.setObjectName("label_meta1")
        self.barra_meta_semana_3 = QtWidgets.QProgressBar(self.tab_3)
        self.barra_meta_semana_3.setGeometry(QtCore.QRect(16, 232, 547, 40))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        self.barra_meta_semana_3.setFont(font)
        self.barra_meta_semana_3.setStyleSheet("color:rgb(113,66,230)")
        self.barra_meta_semana_3.setProperty("value", 0)
        self.barra_meta_semana_3.setAlignment(QtCore.Qt.AlignCenter)
        self.barra_meta_semana_3.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.barra_meta_semana_3.setFormat("")
        self.barra_meta_semana_3.setObjectName("barra_meta_semana_3")
        self.label_71 = QtWidgets.QLabel(self.tab_3)
        self.label_71.setGeometry(QtCore.QRect(216, 18, 75, 9))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_71.setFont(font)
        self.label_71.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_71.setObjectName("label_71")
        self.campo_meta_semanal = QtWidgets.QSpinBox(self.tab_3)
        self.campo_meta_semanal.setGeometry(QtCore.QRect(101, 30, 90, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_meta_semanal.setFont(font)
        self.campo_meta_semanal.setStyleSheet("QSpinBox {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QSpinBox:disabled, QSpinBox:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_meta_semanal.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.campo_meta_semanal.setMinimum(1)
        self.campo_meta_semanal.setMaximum(100000)
        self.campo_meta_semanal.setObjectName("campo_meta_semanal")
        self.label_70 = QtWidgets.QLabel(self.tab_3)
        self.label_70.setGeometry(QtCore.QRect(98, 18, 85, 9))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_70.setFont(font)
        self.label_70.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_70.setObjectName("label_70")
        self.campo_meta_mes = QtWidgets.QSpinBox(self.tab_3)
        self.campo_meta_mes.setGeometry(QtCore.QRect(219, 30, 90, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_meta_mes.setFont(font)
        self.campo_meta_mes.setStyleSheet("QSpinBox {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QSpinBox:disabled, QSpinBox:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_meta_mes.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.campo_meta_mes.setMinimum(1)
        self.campo_meta_mes.setMaximum(1000000)
        self.campo_meta_mes.setObjectName("campo_meta_mes")
        self.botao_atualizar_meta = QtWidgets.QPushButton(self.tab_3)
        self.botao_atualizar_meta.setGeometry(QtCore.QRect(352, 30, 106, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.botao_atualizar_meta.setFont(font)
        self.botao_atualizar_meta.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_atualizar_meta.setStyleSheet("border-radius:10px;\n"
"background-color:rgb(73, 218, 107);\n"
"color:rgb(255,255,255);\n"
"")
        self.botao_atualizar_meta.setObjectName("botao_atualizar_meta")
        self.barra_meta_semana_4.raise_()
        self.barra_meta_semana_3.raise_()
        self.barra_meta_semana_2.raise_()
        self.barra_meta_mensal.raise_()
        self.barra_meta_semana_5.raise_()
        self.label_meta3.raise_()
        self.label_meta_mes.raise_()
        self.label_meta4.raise_()
        self.barra_meta_semana_1.raise_()
        self.label_meta2.raise_()
        self.label_meta5.raise_()
        self.label_meta1.raise_()
        self.campo_meta_semanal.raise_()
        self.label_70.raise_()
        self.campo_meta_mes.raise_()
        self.botao_atualizar_meta.raise_()
        self.label_71.raise_()
        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.campo_grafico = QtWidgets.QWidget(self.tab_7)
        self.campo_grafico.setGeometry(QtCore.QRect(-18, -32, 641, 551))
        self.campo_grafico.setObjectName("campo_grafico")
        self.campo_comentario_4 = QtWidgets.QTextEdit(self.tab_7)
        self.campo_comentario_4.setEnabled(False)
        self.campo_comentario_4.setGeometry(QtCore.QRect(12, 491, 560, 42))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.campo_comentario_4.setFont(font)
        self.campo_comentario_4.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_comentario_4.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.campo_comentario_4.setStyleSheet("border-radius:7px;\n"
"\n"
"background-color:rgb(60,62, 84);\n"
"color:rgb(230,230,230)")
        self.campo_comentario_4.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.campo_comentario_4.setObjectName("campo_comentario_4")
        self.tabWidget_2.addTab(self.tab_7, "")
        self.tab_11 = QtWidgets.QWidget()
        self.tab_11.setObjectName("tab_11")
        self.campo_grafico_valores = QtWidgets.QWidget(self.tab_11)
        self.campo_grafico_valores.setGeometry(QtCore.QRect(-18, -32, 641, 551))
        self.campo_grafico_valores.setObjectName("campo_grafico_valores")
        self.campo_comentario_5 = QtWidgets.QTextEdit(self.tab_11)
        self.campo_comentario_5.setEnabled(False)
        self.campo_comentario_5.setGeometry(QtCore.QRect(20, 493, 546, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.campo_comentario_5.setFont(font)
        self.campo_comentario_5.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_comentario_5.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.campo_comentario_5.setStyleSheet("border-radius:7px;\n"
"\n"
"background-color:rgb(60,62, 84);\n"
"color:rgb(230,230,230)")
        self.campo_comentario_5.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.campo_comentario_5.setObjectName("campo_comentario_5")
        self.tabWidget_2.addTab(self.tab_11, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.campo_grafico_horario = QtWidgets.QWidget(self.tab_4)
        self.campo_grafico_horario.setGeometry(QtCore.QRect(-44, -26, 690, 545))
        self.campo_grafico_horario.setObjectName("campo_grafico_horario")
        self.campo_comentario_3 = QtWidgets.QTextEdit(self.tab_4)
        self.campo_comentario_3.setEnabled(False)
        self.campo_comentario_3.setGeometry(QtCore.QRect(4, 490, 578, 44))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.campo_comentario_3.setFont(font)
        self.campo_comentario_3.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_comentario_3.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.campo_comentario_3.setStyleSheet("border-radius:7px;\n"
"\n"
"background-color:rgb(60,62, 84);\n"
"color:rgb(230,230,230)")
        self.campo_comentario_3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.campo_comentario_3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.campo_comentario_3.setObjectName("campo_comentario_3")
        self.tabWidget_2.addTab(self.tab_4, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.campo_grafico_tipo_certificado = QtWidgets.QWidget(self.tab_8)
        self.campo_grafico_tipo_certificado.setGeometry(QtCore.QRect(-14, -10, 618, 569))
        self.campo_grafico_tipo_certificado.setObjectName("campo_grafico_tipo_certificado")
        self.tabWidget_2.addTab(self.tab_8, "")
        self.tab_9 = QtWidgets.QWidget()
        self.tab_9.setObjectName("tab_9")
        self.campo_grafico_indice_aprovacao = QtWidgets.QWidget(self.tab_9)
        self.campo_grafico_indice_aprovacao.setGeometry(QtCore.QRect(-34, -94, 644, 581))
        self.campo_grafico_indice_aprovacao.setObjectName("campo_grafico_indice_aprovacao")
        self.label_73 = QtWidgets.QLabel(self.tab_9)
        self.label_73.setGeometry(QtCore.QRect(144, 28, 287, 33))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_73.setFont(font)
        self.label_73.setStyleSheet("background-color:transparent;\n"
"color:rgb(230,230,230)")
        self.label_73.setAlignment(QtCore.Qt.AlignCenter)
        self.label_73.setObjectName("label_73")
        self.campo_comentario_2 = QtWidgets.QTextEdit(self.tab_9)
        self.campo_comentario_2.setEnabled(False)
        self.campo_comentario_2.setGeometry(QtCore.QRect(25, 409, 537, 119))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.campo_comentario_2.setFont(font)
        self.campo_comentario_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_comentario_2.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.campo_comentario_2.setStyleSheet("border-radius:7px;\n"
"\n"
"background-color:rgb(60,62, 84);\n"
"color:rgb(230,230,230)")
        self.campo_comentario_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.campo_comentario_2.setObjectName("campo_comentario_2")
        self.tabWidget_2.addTab(self.tab_9, "")
        self.tab_10 = QtWidgets.QWidget()
        self.tab_10.setObjectName("tab_10")
        self.campo_grafico_uf = QtWidgets.QWidget(self.tab_10)
        self.campo_grafico_uf.setGeometry(QtCore.QRect(-40, -16, 644, 581))
        self.campo_grafico_uf.setObjectName("campo_grafico_uf")
        self.tabWidget_2.addTab(self.tab_10, "")
        self.tab_14 = QtWidgets.QWidget()
        self.tab_14.setObjectName("tab_14")
        self.campo_grafico_quantidade_anual = QtWidgets.QWidget(self.tab_14)
        self.campo_grafico_quantidade_anual.setGeometry(QtCore.QRect(0, 2, 580, 512))
        self.campo_grafico_quantidade_anual.setObjectName("campo_grafico_quantidade_anual")
        self.campo_comentario_7 = QtWidgets.QTextEdit(self.tab_14)
        self.campo_comentario_7.setEnabled(False)
        self.campo_comentario_7.setGeometry(QtCore.QRect(-1, 504, 582, 37))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.campo_comentario_7.setFont(font)
        self.campo_comentario_7.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_comentario_7.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.campo_comentario_7.setStyleSheet("border-radius:7px;\n"
"\n"
"background-color:rgb(60,62, 84);\n"
"color:rgb(230,230,230)")
        self.campo_comentario_7.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.campo_comentario_7.setObjectName("campo_comentario_7")
        self.tabWidget_2.addTab(self.tab_14, "")
        self.tab_12 = QtWidgets.QWidget()
        self.tab_12.setObjectName("tab_12")
        self.campo_grafico_clientes_recorrentes = QtWidgets.QWidget(self.tab_12)
        self.campo_grafico_clientes_recorrentes.setGeometry(QtCore.QRect(0, -14, 595, 529))
        self.campo_grafico_clientes_recorrentes.setObjectName("campo_grafico_clientes_recorrentes")
        self.campo_comentario_6 = QtWidgets.QTextEdit(self.tab_12)
        self.campo_comentario_6.setEnabled(False)
        self.campo_comentario_6.setGeometry(QtCore.QRect(1, 506, 560, 42))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.campo_comentario_6.setFont(font)
        self.campo_comentario_6.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_comentario_6.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.campo_comentario_6.setStyleSheet("border-radius:7px;\n"
"\n"
"background-color:rgb(60,62, 84);\n"
"color:rgb(230,230,230)")
        self.campo_comentario_6.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.campo_comentario_6.setObjectName("campo_comentario_6")
        self.tabWidget_2.addTab(self.tab_12, "")
        self.campo_data_meta = QtWidgets.QDateEdit(self.tab_2)
        self.campo_data_meta.setEnabled(True)
        self.campo_data_meta.setGeometry(QtCore.QRect(237, 25, 103, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.campo_data_meta.setFont(font)
        self.campo_data_meta.setStyleSheet("QDateEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QDateEdit:disabled, QDateEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"\n"
"QDateEdit::up-button {\n"
"    width: 0;\n"
"    height: 0;\n"
"    border: none;\n"
"}\n"
"\n"
"QDateEdit::down-button {\n"
"    width: 0;\n"
"    height: 0;\n"
"    border: none;\n"
"}\n"
"")
        self.campo_data_meta.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_data_meta.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.campo_data_meta.setObjectName("campo_data_meta")
        self.label_36 = QtWidgets.QLabel(self.tab_2)
        self.label_36.setGeometry(QtCore.QRect(242, 14, 100, 8))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_36.setFont(font)
        self.label_36.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_36.setObjectName("label_36")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label_56 = QtWidgets.QLabel(self.tab)
        self.label_56.setGeometry(QtCore.QRect(58, 224, 79, 10))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_56.setFont(font)
        self.label_56.setStyleSheet("\n"
"color:rgb(220,220,220)")
        self.label_56.setObjectName("label_56")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_3.setGeometry(QtCore.QRect(48, 228, 509, 64))
        self.groupBox_3.setStyleSheet("QGroupBox{\n"
"border-radius:7px;\n"
"border: 1px solid rgb(120,120,120);\n"
"background-color:rgb(60, 62, 84);}")
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.botao_altera_pasta_principal = QtWidgets.QPushButton(self.groupBox_3)
        self.botao_altera_pasta_principal.setGeometry(QtCore.QRect(452, 14, 33, 30))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_altera_pasta_principal.setFont(font)
        self.botao_altera_pasta_principal.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_altera_pasta_principal.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_altera_pasta_principal.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.botao_altera_pasta_principal.setStyleSheet("border-radius:7px;\n"
"background-color:transparent")
        self.botao_altera_pasta_principal.setObjectName("botao_altera_pasta_principal")
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setGeometry(QtCore.QRect(19, 16, 137, 10))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_7.setObjectName("label_7")
        self.caminho_pasta_principal = QtWidgets.QLineEdit(self.groupBox_3)
        self.caminho_pasta_principal.setEnabled(True)
        self.caminho_pasta_principal.setGeometry(QtCore.QRect(19, 25, 463, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.caminho_pasta_principal.setFont(font)
        self.caminho_pasta_principal.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.caminho_pasta_principal.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.caminho_pasta_principal.setText("")
        self.caminho_pasta_principal.setObjectName("caminho_pasta_principal")
        self.caminho_pasta_principal.raise_()
        self.botao_altera_pasta_principal.raise_()
        self.label_7.raise_()
        self.label_32 = QtWidgets.QLabel(self.tab)
        self.label_32.setGeometry(QtCore.QRect(58, 310, 99, 10))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_32.setFont(font)
        self.label_32.setStyleSheet("\n"
"color:rgb(220,220,220)")
        self.label_32.setObjectName("label_32")
        self.groupBox_6 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_6.setGeometry(QtCore.QRect(48, 314, 509, 173))
        self.groupBox_6.setStyleSheet("QGroupBox{\n"
"border-radius:7px;\n"
"border: 1px solid rgb(120,120,120);\n"
"background-color:rgb(60, 62, 84);}")
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.label_8 = QtWidgets.QLabel(self.groupBox_6)
        self.label_8.setGeometry(QtCore.QRect(20, 17, 157, 10))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_8.setObjectName("label_8")
        self.caminho_pasta = QtWidgets.QLineEdit(self.groupBox_6)
        self.caminho_pasta.setEnabled(True)
        self.caminho_pasta.setGeometry(QtCore.QRect(20, 28, 467, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.caminho_pasta.setFont(font)
        self.caminho_pasta.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.caminho_pasta.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.caminho_pasta.setText("")
        self.caminho_pasta.setObjectName("caminho_pasta")
        self.campo_lista_tipo_criar_pasta = QtWidgets.QComboBox(self.groupBox_6)
        self.campo_lista_tipo_criar_pasta.setGeometry(QtCore.QRect(18, 76, 157, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_lista_tipo_criar_pasta.setFont(font)
        self.campo_lista_tipo_criar_pasta.setStyleSheet("QComboBox {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QComboBox:disabled, QComboBox:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: none;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    width: 0;\n"
"}\n"
"")
        self.campo_lista_tipo_criar_pasta.setEditable(False)
        self.campo_lista_tipo_criar_pasta.setObjectName("campo_lista_tipo_criar_pasta")
        self.campo_lista_tipo_criar_pasta.addItem("")
        self.campo_lista_tipo_criar_pasta.addItem("")
        self.campo_lista_tipo_criar_pasta.addItem("")
        self.label_42 = QtWidgets.QLabel(self.groupBox_6)
        self.label_42.setGeometry(QtCore.QRect(19, 67, 69, 10))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_42.setFont(font)
        self.label_42.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_42.setObjectName("label_42")
        self.campo_telefone_sac_cliente = QtWidgets.QLineEdit(self.groupBox_6)
        self.campo_telefone_sac_cliente.setEnabled(True)
        self.campo_telefone_sac_cliente.setGeometry(QtCore.QRect(207, 77, 200, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_telefone_sac_cliente.setFont(font)
        self.campo_telefone_sac_cliente.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_telefone_sac_cliente.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_telefone_sac_cliente.setText("")
        self.campo_telefone_sac_cliente.setObjectName("campo_telefone_sac_cliente")
        self.label_54 = QtWidgets.QLabel(self.groupBox_6)
        self.label_54.setGeometry(QtCore.QRect(208, 68, 69, 10))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_54.setFont(font)
        self.label_54.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_54.setObjectName("label_54")
        self.campo_dias_renovacao = QtWidgets.QSpinBox(self.groupBox_6)
        self.campo_dias_renovacao.setGeometry(QtCore.QRect(19, 131, 72, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_dias_renovacao.setFont(font)
        self.campo_dias_renovacao.setStyleSheet("QSpinBox {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QSpinBox:disabled, QSpinBox:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_dias_renovacao.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.campo_dias_renovacao.setMinimum(0)
        self.campo_dias_renovacao.setMaximum(255)
        self.campo_dias_renovacao.setObjectName("campo_dias_renovacao")
        self.campo_verifica_tela_cheia = QtWidgets.QLineEdit(self.groupBox_6)
        self.campo_verifica_tela_cheia.setEnabled(True)
        self.campo_verifica_tela_cheia.setGeometry(QtCore.QRect(428, 78, 58, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_verifica_tela_cheia.setFont(font)
        self.campo_verifica_tela_cheia.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_verifica_tela_cheia.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_verifica_tela_cheia.setText("")
        self.campo_verifica_tela_cheia.setObjectName("campo_verifica_tela_cheia")
        self.label_41 = QtWidgets.QLabel(self.groupBox_6)
        self.label_41.setGeometry(QtCore.QRect(19, 122, 100, 10))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_41.setFont(font)
        self.label_41.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_41.setObjectName("label_41")
        self.label_9 = QtWidgets.QLabel(self.groupBox_6)
        self.label_9.setGeometry(QtCore.QRect(428, 69, 61, 10))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_9.setObjectName("label_9")
        self.campo_porcentagem_transparencia = QtWidgets.QSpinBox(self.groupBox_6)
        self.campo_porcentagem_transparencia.setGeometry(QtCore.QRect(138, 128, 86, 28))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.campo_porcentagem_transparencia.setFont(font)
        self.campo_porcentagem_transparencia.setStyleSheet("QSpinBox {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QSpinBox:disabled, QSpinBox:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_porcentagem_transparencia.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.campo_porcentagem_transparencia.setMinimum(10)
        self.campo_porcentagem_transparencia.setMaximum(100)
        self.campo_porcentagem_transparencia.setObjectName("campo_porcentagem_transparencia")
        self.checkBox_transparecer = QtWidgets.QCheckBox(self.groupBox_6)
        self.checkBox_transparecer.setGeometry(QtCore.QRect(206, 134, 19, 17))
        self.checkBox_transparecer.setText("")
        self.checkBox_transparecer.setObjectName("checkBox_transparecer")
        self.label_58 = QtWidgets.QLabel(self.groupBox_6)
        self.label_58.setGeometry(QtCore.QRect(136, 122, 100, 10))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_58.setFont(font)
        self.label_58.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_58.setObjectName("label_58")
        self.label_61 = QtWidgets.QLabel(self.groupBox_6)
        self.label_61.setGeometry(QtCore.QRect(289, 123, 90, 10))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_61.setFont(font)
        self.label_61.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_61.setObjectName("label_61")
        self.campo_telefone_alo_parceiro = QtWidgets.QLineEdit(self.groupBox_6)
        self.campo_telefone_alo_parceiro.setEnabled(True)
        self.campo_telefone_alo_parceiro.setGeometry(QtCore.QRect(288, 132, 198, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_telefone_alo_parceiro.setFont(font)
        self.campo_telefone_alo_parceiro.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_telefone_alo_parceiro.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_telefone_alo_parceiro.setText("")
        self.campo_telefone_alo_parceiro.setObjectName("campo_telefone_alo_parceiro")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(58, 14, 39, 10))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("\n"
"color:rgb(220,220,220)")
        self.label_2.setObjectName("label_2")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(48, 18, 509, 62))
        self.groupBox.setStyleSheet("QGroupBox{\n"
"border-radius:7px;\n"
"border: 1px solid rgb(120,120,120);\n"
"background-color:rgb(60, 62, 84);}")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.botao_ocultar_senha_usuario = QtWidgets.QPushButton(self.groupBox)
        self.botao_ocultar_senha_usuario.setGeometry(QtCore.QRect(464, 20, 25, 21))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_ocultar_senha_usuario.setFont(font)
        self.botao_ocultar_senha_usuario.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_ocultar_senha_usuario.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.botao_ocultar_senha_usuario.setStyleSheet("border-radius:7px;\n"
"background-color:transparent")
        self.botao_ocultar_senha_usuario.setObjectName("botao_ocultar_senha_usuario")
        self.campo_senha_usuario = QtWidgets.QLineEdit(self.groupBox)
        self.campo_senha_usuario.setEnabled(True)
        self.campo_senha_usuario.setGeometry(QtCore.QRect(262, 22, 226, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_senha_usuario.setFont(font)
        self.campo_senha_usuario.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_senha_usuario.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_senha_usuario.setText("")
        self.campo_senha_usuario.setObjectName("campo_senha_usuario")
        self.label_35 = QtWidgets.QLabel(self.groupBox)
        self.label_35.setGeometry(QtCore.QRect(20, 14, 49, 10))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_35.setFont(font)
        self.label_35.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_35.setObjectName("label_35")
        self.label_43 = QtWidgets.QLabel(self.groupBox)
        self.label_43.setGeometry(QtCore.QRect(262, 14, 49, 10))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_43.setFont(font)
        self.label_43.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_43.setObjectName("label_43")
        self.campo_usuario = QtWidgets.QComboBox(self.groupBox)
        self.campo_usuario.setGeometry(QtCore.QRect(20, 20, 228, 26))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_usuario.setFont(font)
        self.campo_usuario.setStyleSheet("QComboBox {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QComboBox:disabled, QComboBox:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: none;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    width: 0;\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.campo_usuario.setEditable(False)
        self.campo_usuario.setObjectName("campo_usuario")
        self.campo_senha_usuario.raise_()
        self.botao_ocultar_senha_usuario.raise_()
        self.label_43.raise_()
        self.campo_usuario.raise_()
        self.label_35.raise_()
        self.label_57 = QtWidgets.QLabel(self.tab)
        self.label_57.setGeometry(QtCore.QRect(58, 94, 75, 10))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_57.setFont(font)
        self.label_57.setStyleSheet("\n"
"color:rgb(220,220,220)")
        self.label_57.setObjectName("label_57")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setGeometry(QtCore.QRect(48, 98, 509, 110))
        self.groupBox_2.setStyleSheet("QGroupBox{\n"
"border-radius:7px;\n"
"border: 1px solid rgb(120,120,120);\n"
"background-color:rgb(60, 62, 84);}")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_30 = QtWidgets.QLabel(self.groupBox_2)
        self.label_30.setGeometry(QtCore.QRect(16, 16, 49, 10))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_30.setFont(font)
        self.label_30.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_30.setObjectName("label_30")
        self.campo_nome_agente = QtWidgets.QLineEdit(self.groupBox_2)
        self.campo_nome_agente.setEnabled(True)
        self.campo_nome_agente.setGeometry(QtCore.QRect(16, 24, 236, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_nome_agente.setFont(font)
        self.campo_nome_agente.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_nome_agente.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_nome_agente.setText("")
        self.campo_nome_agente.setObjectName("campo_nome_agente")
        self.label_33 = QtWidgets.QLabel(self.groupBox_2)
        self.label_33.setGeometry(QtCore.QRect(13, 59, 41, 10))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_33.setFont(font)
        self.label_33.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_33.setObjectName("label_33")
        self.campo_email_empresa = QtWidgets.QLineEdit(self.groupBox_2)
        self.campo_email_empresa.setEnabled(True)
        self.campo_email_empresa.setGeometry(QtCore.QRect(13, 68, 239, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_email_empresa.setFont(font)
        self.campo_email_empresa.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_email_empresa.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_email_empresa.setText("")
        self.campo_email_empresa.setObjectName("campo_email_empresa")
        self.botao_ocultar_senha = QtWidgets.QPushButton(self.groupBox_2)
        self.botao_ocultar_senha.setGeometry(QtCore.QRect(462, 64, 25, 21))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_ocultar_senha.setFont(font)
        self.botao_ocultar_senha.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_ocultar_senha.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.botao_ocultar_senha.setStyleSheet("border-radius:7px;\n"
"background-color:transparent")
        self.botao_ocultar_senha.setObjectName("botao_ocultar_senha")
        self.label_34 = QtWidgets.QLabel(self.groupBox_2)
        self.label_34.setGeometry(QtCore.QRect(282, 58, 69, 10))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_34.setFont(font)
        self.label_34.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_34.setObjectName("label_34")
        self.campo_senha_email = QtWidgets.QLineEdit(self.groupBox_2)
        self.campo_senha_email.setEnabled(True)
        self.campo_senha_email.setGeometry(QtCore.QRect(282, 67, 206, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_senha_email.setFont(font)
        self.campo_senha_email.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_senha_email.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_senha_email.setText("")
        self.campo_senha_email.setObjectName("campo_senha_email")
        self.label_29 = QtWidgets.QLabel(self.groupBox_2)
        self.label_29.setGeometry(QtCore.QRect(284, 14, 49, 10))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_29.setFont(font)
        self.label_29.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_29.setObjectName("label_29")
        self.campo_cod_rev = QtWidgets.QLineEdit(self.groupBox_2)
        self.campo_cod_rev.setEnabled(True)
        self.campo_cod_rev.setGeometry(QtCore.QRect(284, 24, 100, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_cod_rev.setFont(font)
        self.campo_cod_rev.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_cod_rev.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QLineEdit:disabled, QLineEdit:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_cod_rev.setText("")
        self.campo_cod_rev.setObjectName("campo_cod_rev")
        self.campo_senha_email.raise_()
        self.label_30.raise_()
        self.campo_nome_agente.raise_()
        self.label_33.raise_()
        self.campo_email_empresa.raise_()
        self.botao_ocultar_senha.raise_()
        self.label_34.raise_()
        self.label_29.raise_()
        self.campo_cod_rev.raise_()
        self.label_55 = QtWidgets.QLabel(self.tab)
        self.label_55.setGeometry(QtCore.QRect(58, 504, 54, 10))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_55.setFont(font)
        self.label_55.setStyleSheet("\n"
"color:rgb(220,220,220)")
        self.label_55.setObjectName("label_55")
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_4.setGeometry(QtCore.QRect(49, 510, 509, 67))
        self.groupBox_4.setStyleSheet("QGroupBox{\n"
"border-radius:7px;\n"
"border: 1px solid rgb(120,120,120);\n"
"background-color:rgb(60, 62, 84);}")
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_53 = QtWidgets.QLabel(self.groupBox_4)
        self.label_53.setGeometry(QtCore.QRect(194, 15, 100, 10))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_53.setFont(font)
        self.label_53.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_53.setObjectName("label_53")
        self.label_45 = QtWidgets.QLabel(self.groupBox_4)
        self.label_45.setGeometry(QtCore.QRect(18, 15, 100, 10))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_45.setFont(font)
        self.label_45.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_45.setObjectName("label_45")
        self.label_51 = QtWidgets.QLabel(self.groupBox_4)
        self.label_51.setGeometry(QtCore.QRect(294, 15, 100, 10))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_51.setFont(font)
        self.label_51.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_51.setObjectName("label_51")
        self.campo_imposto_validacao = QtWidgets.QSpinBox(self.groupBox_4)
        self.campo_imposto_validacao.setGeometry(QtCore.QRect(294, 24, 81, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_imposto_validacao.setFont(font)
        self.campo_imposto_validacao.setStyleSheet("QSpinBox {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QSpinBox:disabled, QSpinBox:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_imposto_validacao.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.campo_imposto_validacao.setMinimum(1)
        self.campo_imposto_validacao.setMaximum(100)
        self.campo_imposto_validacao.setProperty("value", 1)
        self.campo_imposto_validacao.setObjectName("campo_imposto_validacao")
        self.campo_desconto = QtWidgets.QSpinBox(self.groupBox_4)
        self.campo_desconto.setGeometry(QtCore.QRect(194, 24, 83, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_desconto.setFont(font)
        self.campo_desconto.setStyleSheet("QSpinBox {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QSpinBox:disabled, QSpinBox:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_desconto.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.campo_desconto.setMinimum(1)
        self.campo_desconto.setMaximum(100)
        self.campo_desconto.setProperty("value", 1)
        self.campo_desconto.setObjectName("campo_desconto")
        self.campo_porcentagem_validacao = QtWidgets.QSpinBox(self.groupBox_4)
        self.campo_porcentagem_validacao.setGeometry(QtCore.QRect(18, 24, 68, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_porcentagem_validacao.setFont(font)
        self.campo_porcentagem_validacao.setStyleSheet("QSpinBox {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QSpinBox:disabled, QSpinBox:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_porcentagem_validacao.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.campo_porcentagem_validacao.setMinimum(1)
        self.campo_porcentagem_validacao.setMaximum(100)
        self.campo_porcentagem_validacao.setProperty("value", 1)
        self.campo_porcentagem_validacao.setObjectName("campo_porcentagem_validacao")
        self.label_52 = QtWidgets.QLabel(self.groupBox_4)
        self.label_52.setGeometry(QtCore.QRect(394, 15, 100, 10))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_52.setFont(font)
        self.label_52.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_52.setObjectName("label_52")
        self.campo_desconto_validacao = QtWidgets.QDoubleSpinBox(self.groupBox_4)
        self.campo_desconto_validacao.setGeometry(QtCore.QRect(394, 24, 100, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_desconto_validacao.setFont(font)
        self.campo_desconto_validacao.setStyleSheet("QDoubleSpinBox {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QDoubleSpinBox:disabled, QDoubleSpinBox:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_desconto_validacao.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.campo_desconto_validacao.setMinimum(1.0)
        self.campo_desconto_validacao.setMaximum(50.0)
        self.campo_desconto_validacao.setSingleStep(0.1)
        self.campo_desconto_validacao.setProperty("value", 1.0)
        self.campo_desconto_validacao.setObjectName("campo_desconto_validacao")
        self.label_59 = QtWidgets.QLabel(self.groupBox_4)
        self.label_59.setGeometry(QtCore.QRect(104, 15, 72, 10))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_59.setFont(font)
        self.label_59.setStyleSheet("background-color:transparent;\n"
"color:rgb(170,170,170)")
        self.label_59.setObjectName("label_59")
        self.campo_porcentagem_venda = QtWidgets.QSpinBox(self.groupBox_4)
        self.campo_porcentagem_venda.setGeometry(QtCore.QRect(104, 24, 70, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.campo_porcentagem_venda.setFont(font)
        self.campo_porcentagem_venda.setStyleSheet("QSpinBox {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(90, 54, 247);\n"
"    border-radius: 0;\n"
"    background-color: rgb(60, 62, 84);\n"
"}\n"
"\n"
"QSpinBox:disabled, QSpinBox:!focus {\n"
"    border-bottom: 1px solid rgb(120, 120, 120);\n"
"}\n"
"")
        self.campo_porcentagem_venda.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.campo_porcentagem_venda.setMinimum(1)
        self.campo_porcentagem_venda.setMaximum(100)
        self.campo_porcentagem_venda.setProperty("value", 1)
        self.campo_porcentagem_venda.setObjectName("campo_porcentagem_venda")
        self.botao_atualizar_configuracoes = QtWidgets.QPushButton(self.tab)
        self.botao_atualizar_configuracoes.setGeometry(QtCore.QRect(520, 585, 43, 42))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(22)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_atualizar_configuracoes.setFont(font)
        self.botao_atualizar_configuracoes.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_atualizar_configuracoes.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_atualizar_configuracoes.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.botao_atualizar_configuracoes.setStyleSheet("border-radius:7px;\n"
"")
        self.botao_atualizar_configuracoes.setIconSize(QtCore.QSize(16, 16))
        self.botao_atualizar_configuracoes.setObjectName("botao_atualizar_configuracoes")
        self.label_novo_usuario = QtWidgets.QLabel(self.tab)
        self.label_novo_usuario.setGeometry(QtCore.QRect(484, 584, 23, 22))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)
        self.label_novo_usuario.setFont(font)
        self.label_novo_usuario.setStyleSheet("background-color:transparent")
        self.label_novo_usuario.setObjectName("label_novo_usuario")
        self.botao_criar_usuario = QtWidgets.QPushButton(self.tab)
        self.botao_criar_usuario.setGeometry(QtCore.QRect(461, 585, 45, 40))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(24)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_criar_usuario.setFont(font)
        self.botao_criar_usuario.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_criar_usuario.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_criar_usuario.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.botao_criar_usuario.setStyleSheet("border-radius:7px;")
        self.botao_criar_usuario.setObjectName("botao_criar_usuario")
        self.botao_criar_usuario.raise_()
        self.groupBox_3.raise_()
        self.groupBox_6.raise_()
        self.groupBox.raise_()
        self.groupBox_2.raise_()
        self.groupBox_4.raise_()
        self.botao_atualizar_configuracoes.raise_()
        self.label_novo_usuario.raise_()
        self.label_2.raise_()
        self.label_57.raise_()
        self.label_55.raise_()
        self.label_56.raise_()
        self.label_32.raise_()
        self.tabWidget.addTab(self.tab, "")
        self.botao_print_direto_na_pasta = QtWidgets.QPushButton(self.centralwidget)
        self.botao_print_direto_na_pasta.setGeometry(QtCore.QRect(436, -5, 46, 56))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(24)
        self.botao_print_direto_na_pasta.setFont(font)
        self.botao_print_direto_na_pasta.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_print_direto_na_pasta.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_print_direto_na_pasta.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.botao_print_direto_na_pasta.setStyleSheet("border-radius:10px;")
        self.botao_print_direto_na_pasta.setFlat(True)
        self.botao_print_direto_na_pasta.setObjectName("botao_print_direto_na_pasta")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(-92, -8, 700, 59))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color:rgb(40, 45, 50);\n"
"")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.botao_tela_cheia = QtWidgets.QPushButton(self.centralwidget)
        self.botao_tela_cheia.setGeometry(QtCore.QRect(8, 1, 46, 46))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(20)
        self.botao_tela_cheia.setFont(font)
        self.botao_tela_cheia.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_tela_cheia.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_tela_cheia.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.botao_tela_cheia.setStyleSheet("border-radius:10px;")
        self.botao_tela_cheia.setFlat(True)
        self.botao_tela_cheia.setObjectName("botao_tela_cheia")
        self.botao_agrupar_PDF = QtWidgets.QPushButton(self.centralwidget)
        self.botao_agrupar_PDF.setGeometry(QtCore.QRect(546, 3, 46, 43))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.botao_agrupar_PDF.setFont(font)
        self.botao_agrupar_PDF.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_agrupar_PDF.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_agrupar_PDF.setStyleSheet("border-radius:10px;")
        self.botao_agrupar_PDF.setFlat(True)
        self.botao_agrupar_PDF.setObjectName("botao_agrupar_PDF")
        self.botao_converter = QtWidgets.QPushButton(self.centralwidget)
        self.botao_converter.setGeometry(QtCore.QRect(490, 7, 49, 41))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(22)
        font.setBold(False)
        font.setWeight(50)
        self.botao_converter.setFont(font)
        self.botao_converter.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_converter.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_converter.setStyleSheet("border-radius:10px;")
        self.botao_converter.setAutoDefault(False)
        self.botao_converter.setDefault(False)
        self.botao_converter.setFlat(True)
        self.botao_converter.setObjectName("botao_converter")
        self.campo_status_bd = QtWidgets.QLabel(self.centralwidget)
        self.campo_status_bd.setGeometry(QtCore.QRect(80, 1, 26, 26))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.campo_status_bd.setFont(font)
        self.campo_status_bd.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.campo_status_bd.setText("")
        self.campo_status_bd.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_status_bd.setObjectName("campo_status_bd")
        self.label_confirmacao_tirar_print = QtWidgets.QLabel(self.centralwidget)
        self.label_confirmacao_tirar_print.setGeometry(QtCore.QRect(464, 9, 16, 16))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(9)
        self.label_confirmacao_tirar_print.setFont(font)
        self.label_confirmacao_tirar_print.setText("")
        self.label_confirmacao_tirar_print.setObjectName("label_confirmacao_tirar_print")
        self.label_confirmacao_criar_link_video = QtWidgets.QLabel(self.centralwidget)
        self.label_confirmacao_criar_link_video.setGeometry(QtCore.QRect(746, 11, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_confirmacao_criar_link_video.setFont(font)
        self.label_confirmacao_criar_link_video.setText("")
        self.label_confirmacao_criar_link_video.setObjectName("label_confirmacao_criar_link_video")
        self.label_confirmacao_converter_pdf = QtWidgets.QLabel(self.centralwidget)
        self.label_confirmacao_converter_pdf.setGeometry(QtCore.QRect(514, 7, 16, 16))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(9)
        self.label_confirmacao_converter_pdf.setFont(font)
        self.label_confirmacao_converter_pdf.setText("")
        self.label_confirmacao_converter_pdf.setObjectName("label_confirmacao_converter_pdf")
        self.label_confirmacao_mesclar_pdf = QtWidgets.QLabel(self.centralwidget)
        self.label_confirmacao_mesclar_pdf.setGeometry(QtCore.QRect(572, 7, 16, 16))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(9)
        self.label_confirmacao_mesclar_pdf.setFont(font)
        self.label_confirmacao_mesclar_pdf.setText("")
        self.label_confirmacao_mesclar_pdf.setObjectName("label_confirmacao_mesclar_pdf")
        self.campo_status_bd_2 = QtWidgets.QLabel(self.centralwidget)
        self.campo_status_bd_2.setGeometry(QtCore.QRect(58, 2, 41, 45))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.campo_status_bd_2.setFont(font)
        self.campo_status_bd_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.campo_status_bd_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.campo_status_bd_2.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_status_bd_2.setObjectName("campo_status_bd_2")
        self.botao_menagem = QtWidgets.QPushButton(self.centralwidget)
        self.botao_menagem.setGeometry(QtCore.QRect(382, 4, 46, 43))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(24)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.botao_menagem.setFont(font)
        self.botao_menagem.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_menagem.setFocusPolicy(QtCore.Qt.NoFocus)
        self.botao_menagem.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.botao_menagem.setStyleSheet("border-radius:10px;")
        self.botao_menagem.setObjectName("botao_menagem")
        self.campo_status_bd_3 = QtWidgets.QLabel(self.centralwidget)
        self.campo_status_bd_3.setGeometry(QtCore.QRect(96, 5, 45, 37))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.campo_status_bd_3.setFont(font)
        self.campo_status_bd_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.campo_status_bd_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.campo_status_bd_3.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_status_bd_3.setObjectName("campo_status_bd_3")
        self.campo_status_verificacao = QtWidgets.QLabel(self.centralwidget)
        self.campo_status_verificacao.setGeometry(QtCore.QRect(128, 9, 33, 17))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.campo_status_verificacao.setFont(font)
        self.campo_status_verificacao.setToolTipDuration(999999999)
        self.campo_status_verificacao.setStyleSheet("color: orange")
        self.campo_status_verificacao.setText("")
        self.campo_status_verificacao.setObjectName("campo_status_verificacao")
        self.campo_status_videook = QtWidgets.QLabel(self.centralwidget)
        self.campo_status_videook.setGeometry(QtCore.QRect(128, 24, 33, 21))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.campo_status_videook.setFont(font)
        self.campo_status_videook.setToolTipDuration(999999999)
        self.campo_status_videook.setStyleSheet("color: rgb(18,191,255)")
        self.campo_status_videook.setText("")
        self.campo_status_videook.setObjectName("campo_status_videook")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(905, 21, 69, 206))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.campo_certificados_semana_1 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.campo_certificados_semana_1.setFont(font)
        self.campo_certificados_semana_1.setText("")
        self.campo_certificados_semana_1.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_certificados_semana_1.setObjectName("campo_certificados_semana_1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.campo_certificados_semana_1)
        self.campo_certificados_semana_2 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.campo_certificados_semana_2.setFont(font)
        self.campo_certificados_semana_2.setText("")
        self.campo_certificados_semana_2.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_certificados_semana_2.setObjectName("campo_certificados_semana_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.campo_certificados_semana_2)
        self.campo_certificados_semana_3 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.campo_certificados_semana_3.setFont(font)
        self.campo_certificados_semana_3.setText("")
        self.campo_certificados_semana_3.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_certificados_semana_3.setObjectName("campo_certificados_semana_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.campo_certificados_semana_3)
        self.campo_certificados_semana_4 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.campo_certificados_semana_4.setFont(font)
        self.campo_certificados_semana_4.setText("")
        self.campo_certificados_semana_4.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_certificados_semana_4.setObjectName("campo_certificados_semana_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.campo_certificados_semana_4)
        self.campo_certificados_semana_5 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.campo_certificados_semana_5.setFont(font)
        self.campo_certificados_semana_5.setText("")
        self.campo_certificados_semana_5.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_certificados_semana_5.setObjectName("campo_certificados_semana_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.campo_certificados_semana_5)
        self.campo_certificados_mes = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.campo_certificados_mes.setFont(font)
        self.campo_certificados_mes.setText("")
        self.campo_certificados_mes.setAlignment(QtCore.Qt.AlignCenter)
        self.campo_certificados_mes.setObjectName("campo_certificados_mes")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.campo_certificados_mes)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(986, 28, 100, 373))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.campo_m7 = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_m7.setFont(font)
        self.campo_m7.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_m7.setText("")
        self.campo_m7.setPlaceholderText("")
        self.campo_m7.setObjectName("campo_m7")
        self.gridLayout.addWidget(self.campo_m7, 6, 0, 1, 1)
        self.campo_m13 = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_m13.setFont(font)
        self.campo_m13.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_m13.setText("")
        self.campo_m13.setPlaceholderText("")
        self.campo_m13.setObjectName("campo_m13")
        self.gridLayout.addWidget(self.campo_m13, 12, 0, 1, 1)
        self.campo_m12 = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_m12.setFont(font)
        self.campo_m12.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_m12.setText("")
        self.campo_m12.setPlaceholderText("")
        self.campo_m12.setObjectName("campo_m12")
        self.gridLayout.addWidget(self.campo_m12, 11, 0, 1, 1)
        self.campo_m3 = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_m3.setFont(font)
        self.campo_m3.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_m3.setText("")
        self.campo_m3.setPlaceholderText("")
        self.campo_m3.setObjectName("campo_m3")
        self.gridLayout.addWidget(self.campo_m3, 2, 0, 1, 1)
        self.campo_m11 = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_m11.setFont(font)
        self.campo_m11.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_m11.setText("")
        self.campo_m11.setPlaceholderText("")
        self.campo_m11.setObjectName("campo_m11")
        self.gridLayout.addWidget(self.campo_m11, 10, 0, 1, 1)
        self.campo_m5 = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_m5.setFont(font)
        self.campo_m5.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_m5.setText("")
        self.campo_m5.setPlaceholderText("")
        self.campo_m5.setObjectName("campo_m5")
        self.gridLayout.addWidget(self.campo_m5, 4, 0, 1, 1)
        self.campo_m9 = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_m9.setFont(font)
        self.campo_m9.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_m9.setText("")
        self.campo_m9.setPlaceholderText("")
        self.campo_m9.setObjectName("campo_m9")
        self.gridLayout.addWidget(self.campo_m9, 8, 0, 1, 1)
        self.campo_m8 = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_m8.setFont(font)
        self.campo_m8.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_m8.setText("")
        self.campo_m8.setPlaceholderText("")
        self.campo_m8.setObjectName("campo_m8")
        self.gridLayout.addWidget(self.campo_m8, 7, 0, 1, 1)
        self.campo_m10 = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_m10.setFont(font)
        self.campo_m10.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_m10.setText("")
        self.campo_m10.setPlaceholderText("")
        self.campo_m10.setObjectName("campo_m10")
        self.gridLayout.addWidget(self.campo_m10, 9, 0, 1, 1)
        self.campo_m1 = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_m1.setFont(font)
        self.campo_m1.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_m1.setText("")
        self.campo_m1.setPlaceholderText("")
        self.campo_m1.setObjectName("campo_m1")
        self.gridLayout.addWidget(self.campo_m1, 0, 0, 1, 1)
        self.campo_m4 = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_m4.setFont(font)
        self.campo_m4.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_m4.setText("")
        self.campo_m4.setPlaceholderText("")
        self.campo_m4.setObjectName("campo_m4")
        self.gridLayout.addWidget(self.campo_m4, 3, 0, 1, 1)
        self.campo_m2 = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_m2.setFont(font)
        self.campo_m2.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_m2.setText("")
        self.campo_m2.setPlaceholderText("")
        self.campo_m2.setObjectName("campo_m2")
        self.gridLayout.addWidget(self.campo_m2, 1, 0, 1, 1)
        self.campo_m6 = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.campo_m6.setFont(font)
        self.campo_m6.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.campo_m6.setText("")
        self.campo_m6.setPlaceholderText("")
        self.campo_m6.setObjectName("campo_m6")
        self.gridLayout.addWidget(self.campo_m6, 5, 0, 1, 1)
        self.label_versao = QtWidgets.QLabel(self.centralwidget)
        self.label_versao.setGeometry(QtCore.QRect(508, 56, 84, 16))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_versao.setFont(font)
        self.label_versao.setStyleSheet("background-color:transparent;color:rgb(200,200,200)")
        self.label_versao.setText("")
        self.label_versao.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_versao.setObjectName("label_versao")
        self.label_60 = QtWidgets.QLabel(self.centralwidget)
        self.label_60.setGeometry(QtCore.QRect(350, 50, 419, 23))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(False)
        font.setWeight(50)
        self.label_60.setFont(font)
        self.label_60.setStyleSheet("background-color:rgb(40, 45, 50);\n"
"")
        self.label_60.setText("")
        self.label_60.setObjectName("label_60")
        self.label_5.raise_()
        self.tabWidget.raise_()
        self.label_confirmacao_criar_link_video.raise_()
        self.campo_status_bd_2.raise_()
        self.botao_converter.raise_()
        self.botao_menagem.raise_()
        self.botao_tela_cheia.raise_()
        self.botao_print_direto_na_pasta.raise_()
        self.campo_status_bd.raise_()
        self.label_confirmacao_converter_pdf.raise_()
        self.label_confirmacao_tirar_print.raise_()
        self.botao_agrupar_PDF.raise_()
        self.label_confirmacao_mesclar_pdf.raise_()
        self.campo_status_bd_3.raise_()
        self.campo_status_verificacao.raise_()
        self.campo_status_videook.raise_()
        self.layoutWidget.raise_()
        self.layoutWidget.raise_()
        self.label_60.raise_()
        self.label_versao.raise_()
        janela.setCentralWidget(self.centralwidget)

        self.retranslateUi(janela)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(janela)
        janela.setTabOrder(self.campo_pedido, self.campo_data_agendamento)
        janela.setTabOrder(self.campo_data_agendamento, self.campo_hora_agendamento)
        janela.setTabOrder(self.campo_hora_agendamento, self.campo_lista_versao_certificado)
        janela.setTabOrder(self.campo_lista_versao_certificado, self.campo_lista_modalidade)
        janela.setTabOrder(self.campo_lista_modalidade, self.campo_lista_venda)
        janela.setTabOrder(self.campo_lista_venda, self.campo_preco_certificado_cheio)
        janela.setTabOrder(self.campo_preco_certificado_cheio, self.campo_preco_certificado)
        janela.setTabOrder(self.campo_preco_certificado, self.campo_nome)
        janela.setTabOrder(self.campo_nome, self.campo_data_nascimento)
        janela.setTabOrder(self.campo_data_nascimento, self.campo_email)
        janela.setTabOrder(self.campo_email, self.campo_telefone)
        janela.setTabOrder(self.campo_telefone, self.campo_cpf)
        janela.setTabOrder(self.campo_cpf, self.campo_rg)
        janela.setTabOrder(self.campo_rg, self.campo_rg_orgao)
        janela.setTabOrder(self.campo_rg_orgao, self.campo_cnh)
        janela.setTabOrder(self.campo_cnh, self.campo_nome_mae)
        janela.setTabOrder(self.campo_nome_mae, self.campo_seguranca_cnh)
        janela.setTabOrder(self.campo_seguranca_cnh, self.campo_funcional)
        janela.setTabOrder(self.campo_funcional, self.campo_pis)
        janela.setTabOrder(self.campo_pis, self.campo_cnpj)
        janela.setTabOrder(self.campo_cnpj, self.campo_lista_junta_comercial)
        janela.setTabOrder(self.campo_lista_junta_comercial, self.campo_cnpj_razao_social)
        janela.setTabOrder(self.campo_cnpj_razao_social, self.campo_cnpj_municipio)
        janela.setTabOrder(self.campo_cnpj_municipio, self.campo_data_de)
        janela.setTabOrder(self.campo_data_de, self.campo_data_ate)
        janela.setTabOrder(self.campo_data_ate, self.campo_lista_status_2)
        janela.setTabOrder(self.campo_lista_status_2, self.campo_data_meta)
        janela.setTabOrder(self.campo_data_meta, self.tableWidget)
        janela.setTabOrder(self.tableWidget, self.campo_m5)
        janela.setTabOrder(self.campo_m5, self.campo_m3)
        janela.setTabOrder(self.campo_m3, self.campo_m7)
        janela.setTabOrder(self.campo_m7, self.campo_certificados_mes)
        janela.setTabOrder(self.campo_certificados_mes, self.campo_certificados_semana_4)
        janela.setTabOrder(self.campo_certificados_semana_4, self.campo_m2)
        janela.setTabOrder(self.campo_m2, self.campo_m9)
        janela.setTabOrder(self.campo_m9, self.campo_m4)
        janela.setTabOrder(self.campo_m4, self.campo_certificados_semana_2)
        janela.setTabOrder(self.campo_certificados_semana_2, self.campo_certificados_semana_5)
        janela.setTabOrder(self.campo_certificados_semana_5, self.campo_m1)
        janela.setTabOrder(self.campo_m1, self.campo_certificados_semana_3)
        janela.setTabOrder(self.campo_certificados_semana_3, self.campo_m6)
        janela.setTabOrder(self.campo_m6, self.tabela_documentos)
        janela.setTabOrder(self.tabela_documentos, self.campo_m11)
        janela.setTabOrder(self.campo_m11, self.campo_m13)
        janela.setTabOrder(self.campo_m13, self.campo_m12)
        janela.setTabOrder(self.campo_m12, self.campo_relatorio)
        janela.setTabOrder(self.campo_relatorio, self.campo_m10)
        janela.setTabOrder(self.campo_m10, self.tabWidget)
        janela.setTabOrder(self.tabWidget, self.campo_m8)
        janela.setTabOrder(self.campo_m8, self.tabWidget_2)
        janela.setTabOrder(self.tabWidget_2, self.botao_atualizar_meta)
        janela.setTabOrder(self.botao_atualizar_meta, self.campo_comentario)
        janela.setTabOrder(self.campo_comentario, self.campo_meta_semanal)
        janela.setTabOrder(self.campo_meta_semanal, self.campo_meta_mes)
        janela.setTabOrder(self.campo_meta_mes, self.campo_certificados_semana_1)
        janela.setTabOrder(self.campo_certificados_semana_1, self.campo_email_enviado)

    def retranslateUi(self, janela):
        _translate = QtCore.QCoreApplication.translate
        janela.setWindowTitle(_translate("janela", "MainWindow"))
        self.label.setText(_translate("janela", "⭐ PEDIDO"))
        self.label_4.setText(_translate("janela", "⭐ HORA"))
        self.label_3.setText(_translate("janela", "⭐ DATA"))
        self.campo_lista_venda.setItemText(0, _translate("janela", "NAO"))
        self.campo_lista_venda.setItemText(1, _translate("janela", "SIM"))
        self.label_22.setText(_translate("janela", "VENDA?"))
        self.label_23.setText(_translate("janela", "⭐ ATENDIMENTO"))
        self.campo_lista_modalidade.setItemText(1, _translate("janela", "VIDEO"))
        self.campo_lista_modalidade.setItemText(2, _translate("janela", "PRESENCIAL"))
        self.botao_pasta_cliente.setText(_translate("janela", "📁"))
        self.label_40.setText(_translate("janela", "⭐ CERTIFICADO"))
        self.label_13.setText(_translate("janela", "COMISSÃO"))
        self.rb_digitacao.setText(_translate("janela", "DIGITAÇÃO"))
        self.rb_videook.setText(_translate("janela", "VIDEO REALIZADA"))
        self.rb_verificacao.setText(_translate("janela", "VERIFICAÇÃO"))
        self.rb_aprovado.setText(_translate("janela", "APROVADO"))
        self.rb_cancelado.setText(_translate("janela", "CANCELADO"))
        self.label_17.setText(_translate("janela", "PREÇO"))
        self.botao_link_venda.setText(_translate("janela", "🛒"))
        self.label_31.setText(_translate("janela", " STATUS"))
        self.botao_salvar.setText(_translate("janela", "💾"))
        self.botao_excluir_dados.setText(_translate("janela", "🗑️"))
        self.botao_agrupar_PDF_pasta_cliente.setText(_translate("janela", "🗃️"))
        self.botao_converter_todas_imagens_em_pdf.setToolTip(_translate("janela", "Converte as imagens da pasta do cliente para PDF"))
        self.botao_converter_todas_imagens_em_pdf.setText(_translate("janela", "🔄️"))
        self.label_12.setText(_translate("janela", "NASCIMENTO"))
        self.label_49.setText(_translate("janela", "PIS/CEI"))
        self.label_44.setText(_translate("janela", "DOCUMENTOS NA PASTA"))
        self.label_15.setText(_translate("janela", "CNH"))
        self.label_16.setText(_translate("janela", "CÓD SEG - CNH"))
        self.label_11.setText(_translate("janela", "E-MAIL"))
        self.botao_telefone.setText(_translate("janela", "📞"))
        self.botao_consulta_pis.setText(_translate("janela", "🔍"))
        self.label_10.setText(_translate("janela", "RG"))
        self.label_18.setText(_translate("janela", "NOME DA MÃE"))
        self.botao_consulta_cpf.setText(_translate("janela", "🔍︎"))
        self.label_27.setText(_translate("janela", "  OBSERVAÇÕES"))
        self.label_24.setText(_translate("janela", "NOME"))
        self.botao_consulta_rg.setText(_translate("janela", "🔍"))
        self.campo_comentario.setHtml(_translate("janela", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Calibri\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Consolas\';\"><br /></p></body></html>"))
        self.label_6.setText(_translate("janela", "CPF"))
        item = self.tabela_documentos.horizontalHeaderItem(0)
        item.setText(_translate("janela", "docs"))
        self.label_48.setText(_translate("janela", "ORGÃO RG"))
        self.botao_enviar_email.setText(_translate("janela", "📧"))
        self.botao_consulta_funcional.setText(_translate("janela", "🔍"))
        self.label_50.setText(_translate("janela", "FUNCIONAL"))
        self.botao_consulta_cnh.setText(_translate("janela", "🔍"))
        self.label_46.setText(_translate("janela", "TELEFONE"))
        self.label_25.setText(_translate("janela", "MUNICÍPIO CNPJ"))
        self.botao_consulta_cnpj.setText(_translate("janela", "🔍"))
        self.botao_junta.setText(_translate("janela", "🔍"))
        self.label_47.setText(_translate("janela", "RAZÃO SOCIAL - CNPJ"))
        self.campo_lista_junta_comercial.setItemText(1, _translate("janela", "SP"))
        self.campo_lista_junta_comercial.setItemText(2, _translate("janela", "AC"))
        self.campo_lista_junta_comercial.setItemText(3, _translate("janela", "AL"))
        self.campo_lista_junta_comercial.setItemText(4, _translate("janela", "AM"))
        self.campo_lista_junta_comercial.setItemText(5, _translate("janela", "AP"))
        self.campo_lista_junta_comercial.setItemText(6, _translate("janela", "BA"))
        self.campo_lista_junta_comercial.setItemText(7, _translate("janela", "CE"))
        self.campo_lista_junta_comercial.setItemText(8, _translate("janela", "DF"))
        self.campo_lista_junta_comercial.setItemText(9, _translate("janela", "ES"))
        self.campo_lista_junta_comercial.setItemText(10, _translate("janela", "GO"))
        self.campo_lista_junta_comercial.setItemText(11, _translate("janela", "MA"))
        self.campo_lista_junta_comercial.setItemText(12, _translate("janela", "MG"))
        self.campo_lista_junta_comercial.setItemText(13, _translate("janela", "MS"))
        self.campo_lista_junta_comercial.setItemText(14, _translate("janela", "MT"))
        self.campo_lista_junta_comercial.setItemText(15, _translate("janela", "PA"))
        self.campo_lista_junta_comercial.setItemText(16, _translate("janela", "PB"))
        self.campo_lista_junta_comercial.setItemText(17, _translate("janela", "PE"))
        self.campo_lista_junta_comercial.setItemText(18, _translate("janela", "PI"))
        self.campo_lista_junta_comercial.setItemText(19, _translate("janela", "PR"))
        self.campo_lista_junta_comercial.setItemText(20, _translate("janela", "RJ"))
        self.campo_lista_junta_comercial.setItemText(21, _translate("janela", "RN"))
        self.campo_lista_junta_comercial.setItemText(22, _translate("janela", "RO"))
        self.campo_lista_junta_comercial.setItemText(23, _translate("janela", "RR"))
        self.campo_lista_junta_comercial.setItemText(24, _translate("janela", "RS"))
        self.campo_lista_junta_comercial.setItemText(25, _translate("janela", "SC"))
        self.campo_lista_junta_comercial.setItemText(26, _translate("janela", "SE"))
        self.campo_lista_junta_comercial.setItemText(27, _translate("janela", "TO"))
        self.botao_dados_cnpj.setText(_translate("janela", "📋"))
        self.label_14.setText(_translate("janela", "CNPJ"))
        self.label_28.setText(_translate("janela", "JUNTA"))
        self.label_38.setText(_translate("janela", " Dados Pessoais"))
        self.label_39.setText(_translate("janela", " Dados Empresa"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("janela", "Dados Pedido"))
        self.botao_procurar.setText(_translate("janela", " EXCEL"))
        self.botao_consultar.setText(_translate("janela", "🔍"))
        self.campo_lista_status_2.setItemText(0, _translate("janela", "TODAS"))
        self.campo_lista_status_2.setItemText(1, _translate("janela", "DIGITAÇÃO"))
        self.campo_lista_status_2.setItemText(2, _translate("janela", "VIDEO REALIZADA"))
        self.campo_lista_status_2.setItemText(3, _translate("janela", "VERIFICAÇÃO"))
        self.campo_lista_status_2.setItemText(4, _translate("janela", "APROVADO"))
        self.campo_lista_status_2.setItemText(5, _translate("janela", "CANCELADO"))
        self.label_19.setText(_translate("janela", " DE:"))
        self.label_21.setText(_translate("janela", " STATUS"))
        self.label_20.setText(_translate("janela", " ATÉ:"))
        self.botao_hoje.setText(_translate("janela", "📅"))
        self.label_26.setText(_translate("janela", " RELATÓRIO"))
        self.botao_envio_massa.setText(_translate("janela", "RENOVAÇÃO"))
        self.botao_excluir_dados_tabela.setText(_translate("janela", "🗑️"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("janela", "STATUS"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("janela", "PEDIDO"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("janela", "DATA"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("janela", "HORA"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("janela", "NOME"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("janela", "VERSAO"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("janela", "Consulta"))
        self.label_71.setText(_translate("janela", " META MÊS"))
        self.label_70.setText(_translate("janela", " META SEMANA"))
        self.botao_atualizar_meta.setText(_translate("janela", "SALVAR META"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), _translate("janela", "Metas"))
        self.campo_comentario_4.setHtml(_translate("janela", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Calibri\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Este gráfico mostra a quantidade de certificados APROVADOS e vendas realizadas na data referência. A média é (quantidade acumulada /quantidade de dias trabalhados)</p></body></html>"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_7), _translate("janela", "Quant Mês"))
        self.campo_comentario_5.setHtml(_translate("janela", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Calibri\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Este gráfico mostra os valores de certificados APROVADOS e vendas realizadas na data referência.  A média é (valor acumulado /quantidade de dias trabalhados)</p></body></html>"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_11), _translate("janela", "Valores"))
        self.campo_comentario_3.setHtml(_translate("janela", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Calibri\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">O gráfico exibe a quantidade de certificados APROVADOS em intervalos de hora durante o mês de referência. O objetivo é identificar os horários com maior pico de aprovação no período analisado</p></body></html>"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate("janela", "Horários"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_8), _translate("janela", "Estat"))
        self.label_73.setText(_translate("janela", "INDICE DE APROVAÇÃO"))
        self.campo_comentario_2.setHtml(_translate("janela", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Calibri\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Descrição do gráfico</span>:<br />Este gráfico exibe a porcentagem de pedidos que foram aprovados pelo agente, considerando todos os pedidos recebidos, tanto por vídeo conferência quanto presencial. A taxa de aprovação indica a probabilidade de sucesso na validação do pedido.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">O que isso significa</span>:<br />Por exemplo, se a taxa de aprovação for de 80%, isso significa que o cliente tem 80% de chance de seu pedido ser aprovado.</p></body></html>"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_9), _translate("janela", "Indíce"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_10), _translate("janela", "  UF "))
        self.campo_comentario_7.setHtml(_translate("janela", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Calibri\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Este gráfico apresenta a quantidade de certificados <span style=\" font-weight:600;\">APROVADOS</span> ao longo dos últimos 24 meses, exibindo a distribuição mensal dos valores aprovados</p></body></html>"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_14), _translate("janela", "Quant Anual"))
        self.campo_comentario_6.setHtml(_translate("janela", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Calibri\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Gráfico que apresenta a quantidade de pedidos <span style=\" font-weight:600;\">APROVADOS</span> agrupados por <span style=\" font-weight:600;\">CPF</span>, considerando todos os registros no banco de dados.</p></body></html>"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_12), _translate("janela", "Cli Recorrentes"))
        self.campo_data_meta.setDisplayFormat(_translate("janela", "MM/yyyy"))
        self.label_36.setText(_translate("janela", "DATA REFERÊNCIA"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("janela", "Indicadores"))
        self.label_56.setText(_translate("janela", "  PASTA PRINCIPAL"))
        self.botao_altera_pasta_principal.setText(_translate("janela", "📂"))
        self.label_7.setText(_translate("janela", "DIRETÓRIO PASTA PRINCIPAL"))
        self.label_32.setText(_translate("janela", "  CONFIGURAÇÕES APP"))
        self.label_8.setText(_translate("janela", "DIRETÓRIO PASTA CLIENTE ATUAL"))
        self.campo_lista_tipo_criar_pasta.setItemText(0, _translate("janela", "PEDIDO"))
        self.campo_lista_tipo_criar_pasta.setItemText(1, _translate("janela", "NOME"))
        self.campo_lista_tipo_criar_pasta.setItemText(2, _translate("janela", "PEDIDO-NOME"))
        self.label_42.setText(_translate("janela", "MODO  PASTA"))
        self.label_54.setText(_translate("janela", "SAC CLIENTE"))
        self.label_41.setText(_translate("janela", "DIAS RENOVAÇÃO"))
        self.label_9.setText(_translate("janela", "TELA CHEIA"))
        self.label_58.setText(_translate("janela", "TRANSP JANELA"))
        self.label_61.setText(_translate("janela", "ALÔ PARCEIRO"))
        self.label_2.setText(_translate("janela", "  LOGIN"))
        self.botao_ocultar_senha_usuario.setText(_translate("janela", "👁️"))
        self.label_35.setText(_translate("janela", "USUÁRIO"))
        self.label_43.setText(_translate("janela", "SENHA"))
        self.label_57.setText(_translate("janela", "  DADOS AGENTE"))
        self.label_30.setText(_translate("janela", "AGENTE"))
        self.label_33.setText(_translate("janela", "E-MAIL"))
        self.botao_ocultar_senha.setText(_translate("janela", "👁️"))
        self.label_34.setText(_translate("janela", "SENHA EMAIL"))
        self.label_29.setText(_translate("janela", "COD REV"))
        self.label_55.setText(_translate("janela", "  CONTÁBIL"))
        self.label_53.setText(_translate("janela", "DESC DO TOTAL (%)"))
        self.label_45.setText(_translate("janela", "(%) VALIDAÇÃO"))
        self.label_51.setText(_translate("janela", "IMP DE RENDA (%)"))
        self.label_52.setText(_translate("janela", "DESC. POR VALIDAÇÃO"))
        self.label_59.setText(_translate("janela", " (%) VENDA"))
        self.botao_atualizar_configuracoes.setText(_translate("janela", "💾"))
        self.label_novo_usuario.setText(_translate("janela", "➕"))
        self.botao_criar_usuario.setText(_translate("janela", "🙍"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("janela", "Configurações"))
        self.botao_print_direto_na_pasta.setText(_translate("janela", "📸"))
        self.botao_tela_cheia.setText(_translate("janela", "🔓"))
        self.botao_agrupar_PDF.setText(_translate("janela", "🗃️"))
        self.botao_converter.setText(_translate("janela", "🔄️"))
        self.campo_status_bd_2.setText(_translate("janela", "🖥️"))
        self.botao_menagem.setText(_translate("janela", "💬"))
        self.campo_status_bd_3.setText(_translate("janela", "🚦"))

