from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QWidget,
    QLabel,
    QHBoxLayout,
    QCheckBox,
    QSpacerItem, 
    QSizePolicy
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from firebase_admin import db
from update import Atualizar
import os
import json

ref = db.reference("/")


class LoginWindow(QMainWindow):
    def __init__(self, janela, ui):
        super().__init__()

        atualizar = Atualizar()
        versao = atualizar.versao

        self.ui = ui
        self.janela = janela

        self.fundo_cor = "rgb(40, 42, 54)"
        self.campo_texto_cor = "rgb(255, 255, 255)"
        self.campo_fundo_cor = "rgb(30, 30, 30)"
        self.botao_cor = "rgb(0, 102, 215)"
        self.botao_cor_hover = "rgb(0, 122, 255)"
        self.cor_login = "rgb(210, 210, 210)"

        self.setWindowTitle("Login")
        self.setFixedSize(350, 320)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)  # Ajustando o espaçamento entre os widgets

        self.label_titulo = QLabel("Login")
        self.label_titulo.setStyleSheet(f"font-size: 26px; font-weight: bold; color: {self.cor_login}; font-family: Calibri;")
        self.label_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_titulo)

        self.campo_usuario = QLineEdit()
        self.campo_usuario.setPlaceholderText("Usuário")
        self.campo_usuario.setStyleSheet(f"font-size: 18px; height: 35px; border-radius: 5px; padding: 5px; background-color: {self.campo_fundo_cor}; color: {self.campo_texto_cor}; border: 1px solid {self.campo_texto_cor}; font-family: Calibri;")
        self.campo_usuario.setFocusPolicy(Qt.StrongFocus)
        layout.addWidget(self.campo_usuario)

        senha_layout = QHBoxLayout()
        senha_layout.setContentsMargins(0, 0, 0, 0)
        self.campo_senha = QLineEdit()
        self.campo_senha.setPlaceholderText("Senha")
        self.campo_senha.setEchoMode(QLineEdit.Password)
        self.campo_senha.setStyleSheet(f"font-size: 18px; height: 35px; border-radius: 5px; padding: 5px; background-color: {self.campo_fundo_cor}; color: {self.campo_texto_cor}; border: 1px solid {self.campo_texto_cor}; font-family: Calibri;")
        self.campo_senha.setFocusPolicy(Qt.StrongFocus)
        senha_layout.addWidget(self.campo_senha)

        self.botao_olho = QPushButton("👁️")
        self.botao_olho.setStyleSheet(f"font-size: 25px; height: 40px; background-color: transparent; color: {self.campo_texto_cor}; border: none; padding: 0; font-family: Calibri;")
        self.botao_olho.setFixedSize(35, 35)
        self.botao_olho.clicked.connect(self.toggle_senha_visivel)
        senha_layout.addWidget(self.botao_olho)

        layout.addLayout(senha_layout)

        # Adicionando o checkbox "Lembrar-me"
        self.checkbox_lembrar = QCheckBox("Lembrar-me")
        self.checkbox_lembrar.setStyleSheet(f"color: gray; font-size: 14px; font-family: Calibri;")
        self.checkbox_lembrar.stateChanged.connect(self.atualizar_json)
        layout.addWidget(self.checkbox_lembrar)

        spacer_item = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer_item)

        self.botao_login = QPushButton("Entrar")
        self.botao_login.setStyleSheet(f"""
            QPushButton {{
                font-size: 20px;
                height: 40px;
                width: 200px;
                background-color: {self.botao_cor};
                color: {self.campo_texto_cor};
                border-radius: 5px;
                font-family: Calibri;
            }}
            QPushButton:hover {{
                background-color: {self.botao_cor_hover};
            }}
        """)
        self.botao_login.clicked.connect(self.fazer_login)
        layout.addWidget(self.botao_login)

        self.label_mensagem = QLabel("✅")
        self.label_mensagem.setStyleSheet(f"font-size: 20px; color: green; font-family: Calibri;")
        self.label_mensagem.setAlignment(Qt.AlignCenter)
        self.label_mensagem.hide()
        layout.addWidget(self.label_mensagem)

        # Adicionando a label da versão
        self.label_versao = QLabel(f"Versão: {versao}")
        self.label_versao.setStyleSheet(f"font-size: 14px; color: gray; font-family: Calibri;")
        self.label_versao.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_versao)

        self.central_widget.setLayout(layout)
        self.setStyleSheet(f"background-color: {self.fundo_cor}; font-family: Calibri;")

        # Tentar carregar dados salvos
        self.carregar_dados_salvos()

    def toggle_senha_visivel(self):
        if self.campo_senha.echoMode() == QLineEdit.Password:
            self.campo_senha.setEchoMode(QLineEdit.Normal)
            self.botao_olho.setText("❌")
        else:
            self.campo_senha.setEchoMode(QLineEdit.Password)
            self.botao_olho.setText("👁️")


    def fazer_login(self):
        usuario_campo = self.campo_usuario.text().strip()
        senha_campo = self.campo_senha.text().strip()

        try:
            # Verifica se os campos estão vazios
            if not usuario_campo and not senha_campo:
                self.campo_usuario.clear()
                self.campo_senha.clear()
                self.exibir_erro(self.campo_usuario, "Usuário incorreto")
                self.exibir_erro(self.campo_senha, "Senha incorreta")
                return

            if not usuario_campo:
                self.campo_usuario.clear()
                self.exibir_erro(self.campo_usuario, "Usuário incorreto")
                self.exibir_erro(self.campo_senha, "")
                return

            if not senha_campo:
                self.campo_senha.clear()
                self.exibir_erro(self.campo_senha, "Senha incorreta")
                self.exibir_erro(self.campo_usuario, "")
                return

            # Verifica se o usuário existe no banco de dados
            user_ref = ref.child(f"Usuario/{usuario_campo}")
            user_data = user_ref.get()

            if not user_data:
                # Usuário não encontrado
                self.campo_usuario.clear()  # Zera o valor do campo
                self.campo_senha.clear()  # Zera o valor do campo
                self.exibir_erro(self.campo_usuario, "Usuário incorreto")
                self.exibir_erro(self.campo_senha, "Senha incorreta")
            else:
                # Verifica se a senha está correta
                senha_servidor = user_data.get("Senha")
                if senha_servidor == senha_campo:
                    # Login bem-sucedido
                    self.iniciar_animacao_sucesso()
                    if self.checkbox_lembrar.isChecked():
                        self.salvar_dados(usuario_campo, senha_campo)
                else:
                    # Senha incorreta
                    self.campo_senha.clear()  # Zera o valor do campo
                    self.exibir_erro(self.campo_senha, "Senha incorreta")
                    self.exibir_erro(self.campo_usuario, "")  # Limpa o erro do campo usuário

        except Exception as e:
            # Caso ocorra um erro na conexão
            self.exibir_erro(self.campo_usuario, "Erro de conexão")
            self.exibir_erro(self.campo_senha, "")
            print("Erro ao conectar ao Firebase:", e)

        # Reseta estilo quando o usuário clica no campo novamente
        self.campo_usuario.textChanged.connect(lambda: self.resetar_estilo(self.campo_usuario, "Usuário"))
        self.campo_senha.textChanged.connect(lambda: self.resetar_estilo(self.campo_senha, "Senha"))

    def exibir_erro(self, campo, mensagem):
        """Exibe o erro no campo de entrada: borda vermelha e placeholder com a mensagem de erro."""
        if mensagem:
            campo.setStyleSheet(f"""
                QLineEdit {{
                    font-size: 18px;
                    height: 35px;
                    border-radius: 5px;
                    padding: 5px;
                    background-color: {self.campo_fundo_cor};
                    color: {self.campo_texto_cor};
                    border: 1px solid red;
                    font-family: Calibri;
                }}
            """)
            campo.setPlaceholderText(mensagem)
            campo.clear()  # Zera o valor do campo para exibir o placeholder
        else:
            self.resetar_estilo(campo, "Usuário" if campo == self.campo_usuario else "Senha")

    def resetar_estilo(self, campo, placeholder):
        """Restaura o estilo normal do campo."""
        campo.setStyleSheet(f"""
            QLineEdit {{
                font-size: 18px;
                height: 35px;
                border-radius: 5px;
                padding: 5px;
                background-color: {self.campo_fundo_cor};
                color: {self.campo_texto_cor};
                border: 1px solid {self.campo_texto_cor};
                font-family: Calibri;
            }}
        """)
        campo.setPlaceholderText(placeholder)


    def iniciar_animacao_sucesso(self):
        botao_geometry = self.botao_login.geometry()

        self.animacao_botao = QPropertyAnimation(self.botao_login, b"geometry")
        self.animacao_botao.setDuration(200)
        self.animacao_botao.setStartValue(botao_geometry)
        self.animacao_botao.setEndValue(
            QRect(
                botao_geometry.center().x(),
                botao_geometry.y(),
                0,
                botao_geometry.height(),
            )
        )

        self.animacao_botao.finished.connect(self.mostrar_label_sucesso)
        self.animacao_botao.start()

    def mostrar_label_sucesso(self):
        self.botao_login.hide()
        self.label_mensagem.setText("✅")
        self.label_mensagem.setStyleSheet("font-size: 30px; color: green; font-family: Calibri;")
        self.label_mensagem.setWindowOpacity(0)
        self.label_mensagem.show()

        self.animacao_label = QPropertyAnimation(self.label_mensagem, b"windowOpacity")
        self.animacao_label.setDuration(300)
        self.animacao_label.setStartValue(0)
        self.animacao_label.setEndValue(1)
        self.animacao_label.finished.connect(self.abrir_proxima_janela)
        self.animacao_label.start()

    def abrir_proxima_janela(self):
        """Fecha a janela de login e abre a próxima janela."""
        self.ui.campo_usuario.setText(self.campo_usuario.text().strip())
        self.ui.campo_senha_usuario.setText(self.campo_senha.text().strip())
        self.close()
        self.janela.show()

    def salvar_dados(self, usuario, senha):
        dados = {"usuario": usuario, "senha": senha}
        caminho = os.path.join(os.environ['APPDATA'], 'login_data.json')
        with open(caminho, 'w') as f:
            json.dump(dados, f)

    def carregar_dados_salvos(self):
        caminho = os.path.join(os.environ['APPDATA'], 'login_data.json')
        if os.path.exists(caminho):
            with open(caminho, 'r') as f:
                dados = json.load(f)
                self.campo_usuario.setText(dados.get("usuario", ""))
                self.campo_senha.setText(dados.get("senha", ""))
                self.checkbox_lembrar.setChecked(True)

    def atualizar_json(self):
        """Atualiza o JSON quando o checkbox for marcado/desmarcado."""
        caminho = os.path.join(os.environ['APPDATA'], 'login_data.json')
        if not self.checkbox_lembrar.isChecked():
            if os.path.exists(caminho):
                os.remove(caminho)
        else:
            pass