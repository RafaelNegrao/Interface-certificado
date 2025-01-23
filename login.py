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
import datetime

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
        self.setFixedSize(300, 320)

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
        self.checkbox_lembrar.stateChanged.connect(self.atualizar_json_login)
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
        self.carregar_dados_salvos_login()

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
                        self.salvar_dados_login(usuario_campo, senha_campo)
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
        """Exibe a mensagem de sucesso ao fazer login e verifica o banco de dados local."""
        self.botao_login.hide()
        self.label_mensagem.setText("✅")
        self.label_mensagem.setStyleSheet("font-size: 30px; color: green; font-family: Calibri;")
        self.label_mensagem.setWindowOpacity(0)
        self.label_mensagem.show()

        # Animação da label de sucesso
        self.animacao_label = QPropertyAnimation(self.label_mensagem, b"windowOpacity")
        self.animacao_label.setDuration(300)
        self.animacao_label.setStartValue(0)
        self.animacao_label.setEndValue(1)

        # Conectar o fim da animação para verificar e abrir a próxima janela
        self.animacao_label.finished.connect(self.verificar_banco_e_abrir_proxima_janela)
        self.animacao_label.start()


    def abrir_proxima_janela(self):
        """Carrega os dados do usuário e abre a próxima janela."""
        self.carregar_lista_usuario()

        self.ui.campo_usuario.setCurrentText(self.campo_usuario.text().strip())
        self.ui.campo_senha_usuario.setText(self.campo_senha.text().strip())
        self.close()
        self.janela.show()


    def verificar_banco_e_abrir_proxima_janela(self):
        """Verifica o banco de dados local e sincroniza com o Firebase, se necessário."""
        pasta_dados = os.path.join(os.environ['APPDATA'], 'Dados')
        usuario = self.campo_usuario.text().strip()
        caminho_banco_local = os.path.join(pasta_dados, f"{usuario}.json")
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            # Situação 1: A pasta de dados não existe
            if not os.path.exists(pasta_dados):
                os.makedirs(pasta_dados)  # Cria a pasta
                print("Pasta criada.")
                self.baixar_banco_de_dados_firebase(pasta_dados, data_hora)  # Baixa o banco
                # Atualiza a chave "Ultima Atualizacao" no banco local e Firebase
                self.atualizar_hora_banco_local(pasta_dados, data_hora, usuario, caminho_banco_local)
                self.atualizar_hora_firebase(data_hora)
                print("Banco de dados baixado e arquivo local criado.")

            else:
                # Situação 2: Verificar se é necessário atualizar o banco
                if not self.comparar_ultima_atualizacao(caminho_banco_local):
                    print("Banco de dados desatualizado. Atualizando...")
                    self.baixar_banco_de_dados_firebase(pasta_dados, data_hora)
                    # Atualiza a chave "Ultima Atualizacao" no banco local e Firebase
                    self.atualizar_hora_banco_local(pasta_dados, data_hora, usuario, caminho_banco_local)
                    self.atualizar_hora_firebase(data_hora)
                    print("Banco de dados atualizado com sucesso.")
                else:
                    print("Banco de dados já está sincronizado. Nenhuma ação necessária.")
        except Exception as e:
            print(f"Erro ao verificar ou atualizar o banco de dados: {e}")

        # Após verificar, abrir a próxima janela
        self.abrir_proxima_janela()



    def atualizar_hora_firebase(self,hora_atual):
        self.atualizacao = db.reference(f"Usuario/{self.campo_usuario.text()}/Ultima Atualizacao")
        self.atualizacao.set(hora_atual)


    def atualizar_hora_banco_local(self, pasta_local, hora_data, usuario, caminho_banco):
        try:
            # Verifica se o caminho do arquivo existe
            if not os.path.exists(caminho_banco):
                raise FileNotFoundError(f"O arquivo {caminho_banco} não foi encontrado.")

            # Abrir o arquivo JSON
            with open(caminho_banco, "r", encoding="utf-8") as f:
                dados_banco = json.load(f)  # Carrega o conteúdo do arquivo JSON

            if dados_banco:
                # Adicionar a chave "Ultima Atualizacao" ao conteúdo baixado
                dados_banco["Ultima Atualizacao"] = hora_data

                # Caminho do arquivo local para salvar
                caminho_banco_arquivo = os.path.join(pasta_local, f"{usuario}.json")
                with open(caminho_banco_arquivo, "w", encoding="utf-8") as f:
                    json.dump(dados_banco, f, ensure_ascii=False, indent=4)

                print(f"Banco de dados local {usuario}.json atualizado com sucesso e data/hora registrada.")
            else:
                print("Nenhum dado encontrado para atualizar.")
        except Exception as e:
            print(f"Erro ao atualizar o banco de dados local: {e}")






    def carregar_lista_usuario(self):
        """Carrega a lista de usuários do Firebase e atualiza o campo de usuário."""
        usuarios_ref = db.reference("Usuario")
        usuarios = usuarios_ref.get()
        nomes_usuarios = list(usuarios.keys()) if usuarios else []

        self.ui.campo_usuario.clear()
        for nome in nomes_usuarios:
            self.ui.campo_usuario.addItem(nome)





    def baixar_banco_de_dados_firebase(self, pasta_local,hora_data):
        """Baixa o banco de dados do Firebase e salva localmente."""
        usuario = self.campo_usuario.text().strip()
        ref_banco = db.reference(f"Usuario/{self.campo_usuario.text()}")

        try:
            dados_banco = ref_banco.get()
            if dados_banco:
                caminho_banco_arquivo = os.path.join(pasta_local, f"{usuario}.json")
                with open(caminho_banco_arquivo, 'w', encoding='utf-8') as f:
                    json.dump(dados_banco, f, ensure_ascii=False, indent=4)

                self.atualizar_hora_firebase(hora_data)

                print("Banco de dados baixado com sucesso.")
        except Exception as e:
            print(f"Erro ao baixar banco de dados: {e}")






    def comparar_ultima_atualizacao(self,caminho_banco_local):
        """Compara a última atualização do Firebase com os dados locais armazenados em {usuario}.json."""

        usuario = self.campo_usuario.text().strip()
        ref_atualizacao = db.reference(f"Usuario/{usuario}/Ultima Atualizacao")

        try:
            # Obter a última atualização do Firebase
            atualizacao_bd = ref_atualizacao.get()
            if not atualizacao_bd:
                print("Nenhuma data de atualização encontrada no Firebase.")
                return False

            # Verificar se o banco de dados local existe
            if not os.path.exists(caminho_banco_local):
                print(f"Banco de dados local {caminho_banco_local} não encontrado. Atualização necessária.")
                return False

            # Ler o arquivo local do banco de dados ({usuario}.json)
            with open(caminho_banco_local, "r", encoding="utf-8") as arquivo:
                conteudo_local = json.load(arquivo)
                ultima_atualizacao_local = conteudo_local.get("Ultima Atualizacao")

            # Verificar se a chave "Ultima Atualizacao" existe no arquivo local
            if not ultima_atualizacao_local:
                print("Chave 'Ultima Atualizacao' não encontrada no arquivo local. Atualização necessária.")
                return False

            # Comparar as datas de atualização
            if ultima_atualizacao_local == atualizacao_bd:
                print("As datas de atualização local e do Firebase estão sincronizadas.")
                return True
            else:
                print("As datas de atualização local e do Firebase estão diferentes.")
                return False

        except Exception as e:
            print(f"Erro ao comparar atualizações: {e}")
            return False

    


    def carregar_dados_salvos_login(self):
        """Carrega os dados de login salvos."""
        pasta_dados = os.path.join(os.environ['APPDATA'], 'Dados')
        caminho_login = os.path.join(pasta_dados, "login_data.json")

        # Carrega dados de login, se existirem
        if os.path.exists(caminho_login):
            with open(caminho_login, 'r') as f:
                dados = json.load(f)
                self.campo_usuario.setText(dados.get("usuario", ""))
                self.campo_senha.setText(dados.get("senha", ""))
                self.checkbox_lembrar.setChecked(True)




    def atualizar_json_login(self):
        """Atualiza o JSON quando o checkbox for marcado/desmarcado."""
        pasta_dados = os.path.join(os.environ['APPDATA'], 'Dados')
        caminho = os.path.join(pasta_dados, 'login_data.json')

        if not self.checkbox_lembrar.isChecked():
            if os.path.exists(caminho):
                os.remove(caminho)


    
    def salvar_dados_login(self, usuario, senha):
        """Salva os dados de login no arquivo login_data.json dentro da pasta Dados."""
        pasta_dados = os.path.join(os.environ['APPDATA'], 'Dados')
        if not os.path.exists(pasta_dados):
            os.makedirs(pasta_dados)

        caminho = os.path.join(pasta_dados, 'login_data.json')
        with open(caminho, 'w') as f:
            json.dump({"usuario": usuario, "senha": senha}, f)



    