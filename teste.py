import os
import psutil

def fechar_arquivo_se_aberto(caminho_arquivo):
    # Verifica se o arquivo está aberto por algum processo
    for processo in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            open_files = processo.info.get('open_files')
            if open_files:
                for file_info in open_files:
                    if caminho_arquivo == file_info.path:
                        print(f'O arquivo {caminho_arquivo} está aberto pelo processo {processo.info["pid"]} ({processo.info["name"]}).')
                        
                        # Força o fechamento do processo
                        psutil.Process(processo.info['pid']).terminate()
                        print(f'O processo foi encerrado.')

        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            continue

def listar_arquivos_em_pasta(pasta):
    try:
        # Lista todos os itens na pasta (arquivos e subpastas)
        itens = os.listdir(pasta)

        # Filtra apenas os arquivos
        arquivos = [item for item in itens if os.path.isfile(os.path.join(pasta, item))]

        return arquivos

    except Exception as e:
        print(f'Erro ao listar arquivos em {pasta}: {e}')
        return None

# Exemplo de uso
pasta_exemplo = "C:\\Users\\Rafael\\Desktop\\5"
arquivos_na_pasta = listar_arquivos_em_pasta(pasta_exemplo)

if arquivos_na_pasta is not None:
    for arquivo in arquivos_na_pasta:
        caminho_completo = os.path.join(pasta_exemplo, arquivo)
        fechar_arquivo_se_aberto(caminho_completo)