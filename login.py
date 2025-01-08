from PyQt5.QtWidgets import (
QApplication,
QMainWindow,
QVBoxLayout,
QPushButton,
QLineEdit,
QWidget,
QLabel,
QHBoxLayout
)
from PyQt5.QtCore import Qt,QTimer
from firebase_admin import db

ref = db.reference("/")


class LoginWindow(QMainWindow):
    def __init__(self, janela, ui):
        super().__init__()
        self.ui = ui
        self.janela = janela

      
        self.fundo_cor = "rgb(40, 42, 54)" 
        self.campo_texto_cor = "rgb(210, 210, 210)"  
        self.campo_fundo_cor = "rgb(30, 30, 30)" 
        self.botao_cor = "rgb(0, 122, 255)"  
        self.cor_login = "rgb(210, 210, 210)"

        self.setWindowTitle("Login")
        self.setFixedSize(300, 300)

      
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

       
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)  

       
        self.label_titulo = QLabel("Login")
        self.label_titulo.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {self.cor_login}; font-family: Calibri;")
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

        
        self.botao_login = QPushButton("Entrar")
        self.botao_login.setStyleSheet(f"font-size: 16px; height: 40px; background-color: {self.botao_cor}; color: {self.campo_texto_cor}; border-radius: 5px; font-family: Calibri;")
        self.botao_login.clicked.connect(self.fazer_login)
        layout.addWidget(self.botao_login)

        
        self.label_mensagem = QLabel("")
        self.label_mensagem.setStyleSheet(f"font-size: 16px; color: {self.campo_texto_cor}; font-family: Calibri;")
        self.label_mensagem.setAlignment(Qt.AlignCenter)
        self.label_mensagem.setFocusPolicy(Qt.NoFocus) 
        self.label_mensagem.hide()  
        layout.addWidget(self.label_mensagem)

        
        self.central_widget.setLayout(layout)

        # Estilizar o fundo da janela
        self.setStyleSheet(f"background-color: {self.fundo_cor}; font-family: Calibri;")


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
            user_ref = ref.child(f"Usuario/{usuario_campo}")
            user_data = user_ref.get()

            # Exibe a mensagem e altera a cor
            self.label_mensagem.show()

            if user_data:
                senha_servidor = user_data.get("Senha")
                if senha_servidor == senha_campo:
                    #QApplication.processEvents() 
                    self.label_mensagem.setText("")
                    self.label_mensagem.setText("✅")
                    self.label_mensagem.setStyleSheet("color: green; font-size: 16px; font-family: Calibri;")

                    QApplication.processEvents() 
                    QTimer.singleShot(0, self.close)

                   
                    self.ui.campo_usuario.setText(f"{usuario_campo}")
                    self.ui.campo_senha_usuario.setText(f"{senha_servidor}")

                    self.janela.show()

                else:
                    self.label_mensagem.setText("")
                    self.label_mensagem.setText("❌ Senha inválida")
                    self.label_mensagem.setStyleSheet("color: red; font-size: 16px; font-family: Calibri;")
                    QApplication.processEvents() 
            else:
                self.label_mensagem.setText("")
                self.label_mensagem.setText("❌ Usuário não encontrado")
                self.label_mensagem.setStyleSheet("color: red; font-size: 16px; font-family: Calibri;")
                QApplication.processEvents() 

        except Exception as e:
            self.label_mensagem.setText("")
            self.label_mensagem.setText("❌ Erro de conexão com o servidor")
            self.label_mensagem.setStyleSheet("color: red; font-size: 16px; font-family: Calibri;")
            print("Erro ao conectar ao Firebase:", e)

