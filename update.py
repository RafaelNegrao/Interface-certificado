import os
import requests
import sys
import shutil
from PyQt5.QtWidgets import QMessageBox, QProgressDialog


class Atualizar:
    def __init__(self, parent=None):
        self.parent = parent
        self.versao = "1.0.16" 


    def verificar_atualizacao(self):
        GITHUB_API_URL = "https://api.github.com/repos/RafaelNegrao/Interface-certificado/releases/latest"
        try:
            response = requests.get(GITHUB_API_URL)
            response.raise_for_status()
            dados_release = response.json()

            ultima_versao = dados_release["tag_name"]
            assets = dados_release.get("assets", [])

            if self.comparar_versoes(self.versao, ultima_versao):
                if assets:
                    download_url = assets[0]["browser_download_url"]
                    self.mostrar_janela_confirmacao(ultima_versao, download_url)
                else:
                    QMessageBox.information(self.parent, "Atualização", "Nova versão disponível, mas sem arquivos para baixar.")
                    sys.exit(0)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self.parent, "Erro de Rede", f"Falha ao verificar atualizações:\n{str(e)}")


    def mostrar_janela_confirmacao(self, ultima_versao, download_url):
        msg_box = QMessageBox(self.parent)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Atualização disponível")
        msg_box.setText(f"Nova versão disponível: {ultima_versao}.\nVersão atual: {self.versao}.\n")

        # Define apenas um botão "Atualizar"
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg_box.button(QMessageBox.Ok).setText("Atualizar")

        # Exibe a mensagem e aguarda a resposta
        resposta = msg_box.exec_()

        if resposta == QMessageBox.Ok:
            self.baixar_arquivo(download_url, ultima_versao)
        else:
            sys.exit(0)


    @staticmethod
    def atualizar(novo_arquivo):
        try:
            executavel_atual = os.path.join(os.getcwd(), "Auxiliar.exe")
            if os.path.exists(executavel_atual):
                os.remove(executavel_atual)
            shutil.move(novo_arquivo, executavel_atual)
            print("Atualização concluída com sucesso!")
        except Exception as e:
            print(f"Ocorreu um erro ao atualizar: {str(e)}")


    def baixar_arquivo(self, download_url, nova_versao):
        try:
            nome_arquivo = f"Auxiliar-{nova_versao}.exe"
            caminho_arquivo = os.path.join(os.getcwd(), nome_arquivo)

            response = requests.get(download_url, stream=True)
            response.raise_for_status()

            total_tamanho = int(response.headers.get('content-length', 0))
            download_size = 0

            progress_dialog = QProgressDialog("Baixando atualização...", "Cancelar", 0, 100, self.parent)
            progress_dialog.setWindowTitle("Progresso do Download")
            progress_dialog.setModal(True)
            progress_dialog.setValue(0)

            with open(caminho_arquivo, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        download_size += len(chunk)
                        progress = (download_size / total_tamanho) * 100
                        progress_dialog.setValue(int(progress))

                        if progress_dialog.wasCanceled():
                            QMessageBox.information(self.parent, "Download Cancelado", "O download foi cancelado.")
                            sys.exit(0)

            self.iniciar_atualizador(caminho_arquivo)
            

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self.parent, "Erro de Download", f"Ocorreu um erro durante o download:\n{str(e)}")
        except Exception as e:
            QMessageBox.critical(self.parent, "Erro Inesperado", f"Ocorreu um erro inesperado:\n{str(e)}")


    def iniciar_atualizador(self, novo_arquivo):
        try:
            caminho_antigo = os.path.join(os.getcwd(), "Auxiliar.exe")
            caminho_novo = os.path.abspath(novo_arquivo)
            script_bat = os.path.abspath("atualizar.bat")

            if not os.path.exists(caminho_novo):
                raise FileNotFoundError(f"O arquivo {caminho_novo} não foi encontrado.")

            conteudo_bat = f"""
                @echo off
                chcp 65001 >nul
                title Atualizando o Programa
                echo Aguarde...

                :check_auxiliar_running
                tasklist /fi "imagename eq Auxiliar.exe" | find /i "Auxiliar.exe" >nul
                if not errorlevel 1 (
                    echo Aguardando o encerramento...
                    timeout /t 1 >nul
                    goto check_auxiliar_running
                )

                echo Encerrando o processo...
                taskkill /im "Auxiliar.exe" /f >nul 2>&1

                :check_delete_old
                echo Deletando arquivos temporarios...
                del "{caminho_antigo}" >nul 2>&1
                if exist "{caminho_antigo}" (
                    echo Nao foi possivel deletar o arquivo antigo. Tentando novamente...
                    timeout /t 1 >nul
                    goto check_delete_old
                )

                echo Arquivo antigo deletado com sucesso.

                :apply_update
                echo Aplicando atualizacao...
                ren "{caminho_novo}" "Auxiliar.exe"
                if not exist "{os.path.join(os.getcwd(), 'Auxiliar.exe')}" (
                    echo A atualizacao falhou. Tentando novamente...
                    timeout /t 1 >nul
                    goto apply_update
                )

                echo Atualizacao aplicada com sucesso.

                :check_firebase_connection
                echo Testando conexao com o Firebase...
                ping -n 1 firebase.google.com >nul
                if errorlevel 1 (
                    echo Falha na conexao com o Firebase. Tentando novamente...
                    timeout /t 2 >nul
                    goto check_firebase_connection
                )

                echo Conexao bem sucedida.

                :start_program
                echo Iniciando o programa...
                start "" "{os.path.join(os.getcwd(), 'Auxiliar.exe')}""

                :cleanup
                echo Limpando arquivos temporarios...
                del "%~f0" >nul 2>&1
                if exist "%~f0" (
                    echo Nao foi possivel limpar o script temporario. Tentando novamente...
                    timeout /t 1 >nul
                    goto cleanup
                )

                echo Atualizacao concluida com sucesso!
                """


            with open(script_bat, "w") as f:
                f.write(conteudo_bat)

            os.system(f'start /b cmd /c "{script_bat}"')
            
            sys.exit(0)
        except Exception as e:
            QMessageBox.critical(self.parent, "Erro ao Iniciar Atualizador", f"Falha ao iniciar o atualizador:\n{str(e)}")


    @staticmethod
    def comparar_versoes(versao_atual, nova_versao):
        return tuple(map(int, versao_atual.split("."))) < tuple(map(int, nova_versao.split(".")))
