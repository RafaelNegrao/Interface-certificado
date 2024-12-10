from imports import *

ref = db.reference("/")


class Funcoes_padrao:
    def __init__(self,ui,parent=None):
        self.ui = ui
        self.acoes = Acoes_banco_de_dados(ui)
        self.parent = parent
        self.dicionario = db.reference("/Mensagens").get()

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
                    label.setStyleSheet('color: rgb(113,66,230); background-color: rgb(46, 214, 255); border: 1px solid rgb(68,71,90)')  # Azul
                    label.setText(f"Semana {semana_num} | Meta atingida! - R${certificados_semana} / R${meta_semanal}")
                else:
                    label.setStyleSheet('color: rgb(113,66,230); background-color: transparent; border: 1px solid rgb(68,71,90)')
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
                ui.label_meta_mes.setStyleSheet('color: rgb(113,66,230); background-color: rgb(46, 214, 255); border: 1px solid rgb(68,71,90)')
                ui.label_meta_mes.setText(f"Meta mensal atingida! - R${soma} / R${meta_mensal}")
            else:
                ui.label_meta_mes.setStyleSheet('color: rgb(113,66,230); background-color: transparent; border: 1px solid rgb(68,71,90)')
                ui.label_meta_mes.setText(f"R${soma} / R${meta_mensal}")

        except Exception as e:
            print(f"Erro: {e}")

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
                ui.checkBox_transparecer.setChecked(configs['CHECKBOX TRANSP'])
                ui.campo_porcentagem_transparencia.setValue(configs['VALOR TRANS'])


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
        transparencia = ui.checkBox_transparecer.isChecked()
        valor_transparencia = ui.campo_porcentagem_transparencia.value()
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
            "CHECKBOX TRANSP": transparencia,
            "VALOR TRANS":valor_transparencia
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
        Metas = ref.get()
    
        valor_semanal = Metas['SEMANAL']
        valor_mensal = Metas['MENSAL']
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
                        widget.deleteLater()  # Remover widgets antigos
                QtWidgets.QWidget().setLayout(layout)  # Limpar o layout atual

            if ui.tabWidget.currentIndex() == 2:
                ref = db.reference("/Pedidos")
                Pedidos = ref.get()

                # Inicializando contadores para cada semana
                semanas = [0, 0, 0, 0, 0]

                # Obter a data do campo ui.campo_data_meta
                mes_meta = ui.campo_data_meta.date().month()
                ano_meta = ui.campo_data_meta.date().year()

                # Identificar o último dia do mês dinamicamente
                ultimo_dia = calendar.monthrange(ano_meta, mes_meta)[1]

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

                dias_do_mes = range(1, ultimo_dia + 1)
                categorias_por_dia = {"CPF": defaultdict(int), "CNPJ": defaultdict(int)}
                valores_por_dia = {"CPF": defaultdict(float), "CNPJ": defaultdict(float)}

                for pedido_info in Pedidos:
                    if Pedidos[pedido_info]['STATUS'] == "APROVADO":
                        data_pedido = Pedidos[pedido_info]['DATA']
                        data_formatada = datetime.datetime.strptime(data_pedido, "%Y-%m-%dT%H:%M:%SZ")

                        if data_formatada.month == mes_meta and data_formatada.year == ano_meta:
                            dia = data_formatada.day
                            versao = Pedidos[pedido_info].get('VERSAO', '') 
                            preco = float(Pedidos[pedido_info]['PRECO'].replace(',', '.'))
                            desconto = 1 - (ui.campo_desconto.value() / 100)
                            valor_com_desconto = preco * desconto

                            if "CPF" in versao:
                                categorias_por_dia["CPF"][dia] += 1
                                valores_por_dia["CPF"][dia] += valor_com_desconto
                            elif "CNPJ" in versao:
                                categorias_por_dia["CNPJ"][dia] += 1
                                valores_por_dia["CNPJ"][dia] += valor_com_desconto

                cpf_counts = [categorias_por_dia["CPF"].get(dia, 0) for dia in dias_do_mes]
                cnpj_counts = [categorias_por_dia["CNPJ"].get(dia, 0) for dia in dias_do_mes]
                cpf_totals = [valores_por_dia["CPF"].get(dia, 0) for dia in dias_do_mes]
                cnpj_totals = [valores_por_dia["CNPJ"].get(dia, 0) for dia in dias_do_mes]

                total_counts = [cpf_counts[i] + cnpj_counts[i] for i in range(len(dias_do_mes))]

                # Obter apenas os dias úteis do mês
                dias_uteis = pd.bdate_range(start=f"{ano_meta}-{mes_meta:02d}-01", 
                                            end=f"{ano_meta}-{mes_meta:02d}-{ultimo_dia:02d}").day.tolist()
                                            
                
                media_cumulativa = np.cumsum([total_counts[i - 1] for i in dias_uteis]) / np.arange(1, len(dias_uteis) + 1)
                media_cumulativa_cpf = np.cumsum([cpf_counts[dia - 1] for dia in dias_uteis]) / np.arange(1, len(dias_uteis) + 1)
                media_cumulativa_cnpj = np.cumsum([cnpj_counts[dia - 1] for dia in dias_uteis]) / np.arange(1, len(dias_uteis) + 1)

                soma_maxima = max(total_counts)
                max_y = max(soma_maxima, max(media_cumulativa)) + 2

                fig, ax = plt.subplots(figsize=(14, 8))
                fig.subplots_adjust(left=0.08, right=0.92, top=0.88, bottom=0.12)

                campo_cor_r = 40
                campo_cor_g = 42
                campo_cor_b = 54

                fig.patch.set_facecolor((campo_cor_r/255, campo_cor_g/255, campo_cor_b/255))
                ax.set_facecolor((campo_cor_r/255, campo_cor_g/255, campo_cor_b/255))

                bar_width = 0.6

                ax.bar(dias_do_mes, cnpj_counts, width=bar_width, label="CNPJ", color="orange")
                ax.bar(dias_do_mes, cpf_counts, width=bar_width, bottom=cnpj_counts, label="CPF", color="blue")

                ax.plot(dias_uteis, media_cumulativa, color="red", linestyle="-", linewidth=1, label="Média Acumulada")
                ax.plot(dias_uteis, media_cumulativa_cnpj, color="yellow", linestyle="-", linewidth=1, label="Média Acumulada CNPJ")
                ax.plot(dias_uteis, media_cumulativa_cpf, color="cyan", linestyle="-", linewidth=1, label="Média Acumulada CPF")

                fonte_cor = (150/255, 150/255, 150/255)

                ax.set_xlabel("Dias do Mês", fontsize=7, color=fonte_cor)
                ax.set_ylabel("Quantidade de Pedidos", fontsize=7, color=fonte_cor)
                ax.set_xticks(range(1, ultimo_dia + 1))
                ax.set_ylim(0, max_y)
                ax.set_yticks(range(0, int(max_y) + 1, 1))

                for y in range(0, int(max_y)):
                    ax.axhline(y=y, color="gray", linestyle="-", alpha=0.3, linewidth=0.7)

                leg = ax.legend(fontsize=6, labelcolor=fonte_cor)
                leg.get_frame().set_facecolor((campo_cor_r/255, campo_cor_g/255, campo_cor_b/255))
                leg.get_frame().set_edgecolor((campo_cor_r/255, campo_cor_g/255, campo_cor_b/255))

                ax.tick_params(axis='x', labelsize=6, colors=fonte_cor)
                ax.tick_params(axis='y', labelsize=6, colors=fonte_cor)

                cursor = mplcursors.cursor(ax, hover=True)
                cursor.connect("add", lambda sel: sel.annotation.set_text(
                    f'Dia: {int(sel.target[0])}\n'
                    f'CPF: {cpf_counts[int(sel.target[0]) - 1]}  Valor: R$ {cpf_totals[int(sel.target[0]) - 1]:,.2f}\n'
                    f'CNPJ: {cnpj_counts[int(sel.target[0]) - 1]}  Valor: R$ {cnpj_totals[int(sel.target[0]) - 1]:,.2f}\n'
                    f'TOTAL: R$ {cpf_totals[int(sel.target[0]) - 1] + cnpj_totals[int(sel.target[0]) - 1]:,.2f}'
                ))



                cursor.connect("add", lambda sel: sel.annotation.set_fontsize(7))

                new_layout = QtWidgets.QVBoxLayout()
                new_layout.addWidget(FigureCanvas(fig))
                ui.campo_grafico.setLayout(new_layout)

        except Exception as e:
            print (f'Erro: {e}')




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

            # Tenta criar a pasta no diretório padrão
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

            ui.label_confirmacao_mesclar_pdf.setText("✅")
            #self.mensagem_alerta("Concluído","Os arquivos PDF foram mesclados com sucesso!")
            self.atualizar_documentos_tabela()


        except:
            ui.label_confirmacao_mesclar_pdf.setText("❌")
            pdf_merger.close()
            self.atualizar_documentos_tabela()

            return

    def escolher_conversao(self):

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

            if radio_jpg_to_pdf.isChecked():

                self.converter_jpg_para_pdf()
            elif radio_pdf_to_jpg.isChecked():

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
            'campo_pis',
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
            self.ui.campo_status_bd.setText("❌")
            self.ui.label_confirmacao_salvar.setText("")
            self.ui.campo_status_bd.setToolTip("Pedido desatualizado")

            nome_campo_atual = campo_atual.objectName()
            if nome_campo_atual == "campo_lista_versao_certificado":
                self.buscar_preco_certificado()

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
            ref = db.reference("/Certificados")
            certificados = ref.get()

            ui.campo_lista_versao_certificado.clear()  
            ui.campo_lista_versao_certificado.addItem("")
            ui.campo_lista_versao_certificado.addItems(certificados.keys()) 

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

            item_nome_documento.setForeground(QColor(90, 54, 247))

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
        #verifica se a janela de mensagens está aberta
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

        for i, (chave, valor) in enumerate(self.dicionario.items()):
            titulo = valor.get("titulo")
            if titulo:
                botao = QPushButton()
                botao.setFixedSize(228, 66)
                botao.setStyleSheet("QPushButton { text-align: justify; }")
                linhas = [titulo[j:j+40] for j in range(0, len(titulo), 40)]
                botao.setText('\n'.join(linhas))

                # Conecta o botão à função genérica de tratamento
                botao.clicked.connect(lambda _, c=chave: self.copiar_com_tratamento(c))
                layout.addWidget(botao, i // 2, i % 2)

        widget.setLayout(layout)
        scroll.setWidget(widget)
        self.nova_janela.show()


    def copiar_com_tratamento(self, chave):

        mensagem_firebase = self.dicionario[chave].get("mensagem", "")
        titulo = self.dicionario[chave].get("titulo", "")

        if chave == "clique_btn1":
            mensagem_inicial = self.determinar_hora(datetime.datetime.now().time())
            nome = ui.campo_nome_agente.text()
            mensagem = mensagem_firebase.replace("{{mensagem_inicial}}", mensagem_inicial).replace("{{nome}}", nome)

        elif chave == "clique_btn2":
            certificado = ui.campo_lista_versao_certificado.currentText().lower()
            midia = "CARTÃO" if "cartão" in certificado else "TOKEN" if "token" in certificado else ""
            mensagem = mensagem_firebase.replace("{{midia}}", midia)

        elif chave == "clique_btn11":
            nome = ui.campo_nome.text().split()[0].capitalize() if ui.campo_nome.text() else ""
            rev = ui.campo_cod_rev.text()
            mensagem = mensagem_firebase.replace("{{nome}}", nome).replace("{{cod_rev}}", rev).replace("\\n", "\n")

        elif chave == "clique_btn12":
            pedido = ui.campo_pedido.text()
            mensagem = mensagem_firebase.replace("{{pedido}}", pedido)

        elif chave == "clique_btn18":
            certificado = ui.campo_lista_versao_certificado.currentText()
            cliente = ui.campo_nome.text()
            pedido = ui.campo_pedido.text()
            midia = "TOKEN" if "token" in certificado else "CARTÃO" if "cartão" in certificado else ""
            mensagem = mensagem_firebase.replace("{{cliente}}", cliente).replace("{{pedido}}", pedido).replace("{{midia}}", midia)

        else:
            # Mensagens que não necessitam de tratamento específico
            mensagem = mensagem_firebase

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
'Para prosseguirmos com a validação, preciso que o senhor(a) entre em contato com o suporte pelo contato *4020-9735* para que possam fazer a liberação do pedido.'

        numero = ui.campo_telefone.text()  
        mensagem = mensagem.replace(' ', '%20')  
        url_mensagem = QUrl(f'https://api.whatsapp.com/send?phone={numero}&text={mensagem}')
        QDesktopServices.openUrl(url_mensagem)


    def envio_de_email(self):
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
        

            tipo_mensagem, ok = QInputDialog.getItem(ui.centralwidget, "Envio", "Escolha o conteúdo do E-mail:", ["INICIO DE ATENDIMENTO", "PROBLEMA DE PAGAMENTO","RENOVAÇÃO"], 0, False)
            if not ok:
                return
            
            tamanho_fonte = "17px"
            cor_botao_fundo = "rgb(89, 62, 255)"
            cor_botao_texto = "#FFFFFF"
            tamanho_fonte_footer = "12px"
            primeiro_nome = ui.campo_nome.text().split()[0]

            match tipo_mensagem:
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
                        f"      <p>Esperado que esteja bem.</p>"
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
                        f"      <p>Esperado que esteja bem.</p>"
                        f"      <P>Sou {nome} e sou agente de registro da ACB Digital.</p>"
                        f"      <p>Temos uma validação agendada para o seu certificado digital às <b>{hora}</b> do dia <b>{data}</b>.</p>"
                        f"      <p>No entanto, o pagamento ainda não foi reconhecido em nosso sistema. Para prosseguirmos com a validação, é necessário que o pagamento seja confirmado.</p>"
                        f"      <p>Peço que entre em contato com o suporte pelo telefone 4020-9735 para regularizar a situação.</p>"
                        f"      <p>Agradeço a compreensão.</p>"
                        f"      <p><br>Atenciosamente,<br>{nome}</p>"
                        f"    </div>"
                        f"    <div class='footer'>ACB Digital &copy; 2024. Todos os direitos reservados.</div>"
                        f"  </div>"
                        f"</body>"
                        f"</html>"
                    )
                    
                case 'RENOVAÇÃO':
                    ref_link_venda = db.reference(f"/Certificados/{ui.campo_lista_versao_certificado.currentText()}")
                    certificado = ref_link_venda.get()
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
                        f"      <p>Esperado que esteja bem.</p>"
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


    def envio_em_massa(self):
        try:
            if not banco_dados.mensagem_confirmacao("Confirmação", f"Enviar email de renovação em massa?\n\nDe: {datetime.date.today().strftime('%d/%m/%Y')} \nAté {(datetime.date.today() + datetime.timedelta(days=ui.campo_dias_renovacao.value())).strftime('%d/%m/%Y')}"):

                return

            ui.tableWidget.setRowCount(0)  
            ui.tableWidget.setColumnCount(5) 
            ui.tableWidget.setHorizontalHeaderLabels(["PEDIDO OR","EMAIL", "ENVIADO?", "RETORNO", "PRAZO RESTANTE"]) 
            ui.tableWidget.setColumnWidth(0, 72)
            ui.tableWidget.setColumnWidth(1, 103)
            ui.tableWidget.setColumnWidth(2, 51)
            ui.tableWidget.setColumnWidth(3, 103)
            ui.tableWidget.setColumnWidth(4, 171)  

            pedidos_ref = ref.child("Pedidos").order_by_child("STATUS").equal_to("APROVADO")
            pedidos = pedidos_ref.get()

            ref_link_venda = db.reference(f"/Certificados/")
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
                    # Atualizar campo "EMAIL RENOVACAO" para "SIM"
                    ref.child("Pedidos").child(pedido_info["PEDIDO"]).update({"EMAIL RENOVACAO": "SIM"})

                # Adiciona os dados na QTableWidget
                row_position = ui.tableWidget.rowCount()
                ui.tableWidget.insertRow(row_position)

                pedido_item = QTableWidgetItem(str(pedido_info.get("PEDIDO", "")))
                pedido_item.setTextAlignment(Qt.AlignCenter)
                ui.tableWidget.setItem(row_position, 0, pedido_item)

                # Configura a célula de "EMAIL"
                email_item = QTableWidgetItem(cliente_email)
                email_item.setTextAlignment(Qt.AlignCenter)
                ui.tableWidget.setItem(row_position, 1, email_item)

                # Configura a célula de "ENVIADO?"
                enviado_item = QTableWidgetItem(enviado)
                enviado_item.setTextAlignment(Qt.AlignCenter)
                ui.tableWidget.setItem(row_position, 2, enviado_item)

                # Configura a célula de "MOTIVO"
                motivo_item = QTableWidgetItem(motivo)
                motivo_item.setTextAlignment(Qt.AlignCenter)
                ui.tableWidget.setItem(row_position, 3, motivo_item)

                # Configura a célula de "PRAZO RESTANTE"
                prazo_item = QTableWidgetItem(str(msg_diferenca))  
                prazo_item.setTextAlignment(Qt.AlignCenter)
                ui.tableWidget.setItem(row_position, 4, prazo_item)

                # Atualiza a tela após cada adição
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
                                f"      <p>Esperado que esteja bem.</p>"
                                f"      <p>Sou {nome}, agente de Registro da ACB Digital.</p>"
                                f"      <p>Fizemos a validação para seu certificado digital, modelo"
                                f"      <p><b>{pedido_info['VERSAO']}</b> no dia <b>{data_formatada_validacao}</b>.</p>"
                                f"      <p>Verifiquei que ele está próximo à data <b>vencimento</b> e entendemos a importância do certificado digital para seus negócios.</p>"
                                f"      <p>Para agilizar o processo de renovação, oferecemos a opção de renovar clicando no botão abaixo.</p>"
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
                                f"      <p>Esperado que esteja bem.</p>"
                                f"      <p>Sou {nome}, agente de Registro da ACB Digital.</p>"
                                f"      <p>Fizemos a validação para seu certificado digital, modelo"
                                f"      <p><b>{pedido_info['VERSAO']}</b> no dia <b>{data_formatada_validacao}</b>.</p>"
                                f"      <p>Verifiquei que ele vence <b>Hoje</b> e entendemos a importância do certificado digital para seus negócios.</p>"
                                f"      <p>Para agilizar o processo de renovação, oferecemos a opção de renovar clicando no botão abaixo.</p>"
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
                ui.tableWidget.setColumnWidth(col, 83)



class Acoes_banco_de_dados:
    def __init__(self,ui):
        self.ui = ui
        self.ref = db.reference("/Pedidos")
    
    def salvar_pedido(self):
        # Analisa se os campos do pedido estão preenchidos
        try:
            pasta_cliente = ui.caminho_pasta.text()
            if not self.analise_de_campos():
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
                        if not self.mensagem_confirmacao("Confirmação", f"Salvar pedido como {banco_dados.alteracao_status()}?"):
                            return
                        # Fiz essa alteração pra manter apenas as chaves que tenham algum valor 
                        # Caso queira retornar, é só mudar para update
                        novo_pedido_ref.set(self.dicionario_banco_de_dados())
                        self.ui.campo_status_bd.setText("")
                        self.ui.campo_status_bd.setToolTip("")
                        self.forcar_fechamento_de_arquivo_e_deletar_pasta(pasta_cliente)
                        self.apagar_campos_pedido(0)
                        ui.label_confirmacao_salvar.setText("✅")
                        self.contar_verificacao()
                        funcoes_app.ajuste_largura_col()

                    #Pedido existente + gravado temporariamente
                    # Fiz essa alteração pra manter apenas as chaves que tenham algum valor 
                    # Caso queira retornar, é só mudar 
                    case 'TEMPORARIO':
                        novo_pedido_ref.set(self.dicionario_banco_de_dados())
                        self.ui.campo_status_bd.setText("✅")
                        ui.label_confirmacao_salvar.setText("✅")
                        self.ui.campo_status_bd.setToolTip("Pedido Atualizado")
                        self.contar_verificacao()
                        funcoes_app.ajuste_largura_col()
                        
            #NOVO PEDIDO
            else:
                condic = self.verificar_status()
                match condic:
                    #Pedido existente + gravado Definitivo
                    case 'DEFINITIVO':
                        if not self.mensagem_confirmacao("Confirmação", f"Salvar pedido como {banco_dados.alteracao_status()}?"):
                            return
                        
                        novo_pedido_ref.set(self.dicionario_banco_de_dados())
                        self.ui.campo_status_bd.setText("")
                        self.ui.campo_status_bd.setToolTip("")
                        self.forcar_fechamento_de_arquivo_e_deletar_pasta(ui.caminho_pasta.text())
                        self.apagar_campos_pedido(0)
                        ui.label_confirmacao_salvar.setText("✅")
                        self.contar_verificacao()
                        funcoes_app.ajuste_largura_col()

                    #Pedido existente + gravado temporariamente
                    case 'TEMPORARIO':

                        novo_pedido_ref.set(self.dicionario_banco_de_dados())
                        self.ui.campo_status_bd.setText("✅")
                        ui.label_confirmacao_salvar.setText("✅")
                        self.ui.campo_status_bd.setToolTip("Pedido Atualizado")
                        self.contar_verificacao()
                        funcoes_app.ajuste_largura_col()
                        
        except Exception as e:
            print(e)
                
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
            ui.label_confirmacao_salvar.setText("❌")
            return False
        return True

    def apagar_campos_pedido(self,origem):
        if origem == 1:
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
        ui.label_confirmacao_salvar.setText("")
        ui.campo_comentario.setStyleSheet("border-radius:7px;border: 1px solid rgb(68,71,90);background-color:rgb(40,42, 54);color:orange")
         
    def dicionario_banco_de_dados(self):
        duracoes_certificado = {
            "12": datetime.timedelta(days=365),
            "18": datetime.timedelta(days=540),
            "24": datetime.timedelta(days=720),
            "36": datetime.timedelta(days=1080)
        }
        
        data_validacao = datetime.datetime.strptime(ui.campo_data_agendamento.date().toString("yyyy-MM-dd"), "%Y-%m-%d")
        certificado_duracao = duracoes_certificado.get(ui.campo_lista_versao_certificado.currentText(), datetime.timedelta(days=0))
        duracao_certificado = data_validacao + certificado_duracao

        renova = "SIM" if ui.campo_email_enviado.text() == "SIM" else "NAO"

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
            "DATA": self.data_para_iso(QDateTime(ui.campo_data_agendamento.date())),
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
            "VALIDO ATE": "",
            "EMAIL RENOVACAO": renova
        }

        # Limpa dos dados se o status for "DEFINITIVO"
        if self.verificar_status() == "DEFINITIVO":
            campos_para_limpar = ["PASTA", "MUNICIPIO", "CODIGO DE SEG CNH", "RG", "CPF", "CNH", "MAE", "CNPJ", "NASCIMENTO", "RAZAO SOCIAL", "ORGAO RG", "PIS", "OAB"]
            novos_dados.update({campo: None for campo in campos_para_limpar})
            novos_dados["VALIDO ATE"] = duracao_certificado.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Filtrar chaves não vazias
        dados_filtrados = {chave: valor for chave, valor in novos_dados.items() if valor not in [None, ""]}

        return dados_filtrados

    def forcar_fechamento_de_arquivo_e_deletar_pasta(self,folder_path):
        for _ in range(3):  # Tenta fehar por 3 vezes
            try:
                shutil.rmtree(folder_path)
                return "Pasta excluída com sucesso"
                
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
        #CORRIGIDO ------------------------------------------------
        try:
            num_pedido = ui.campo_pedido.text()

            if num_pedido == "":
                return

            self.ref = db.reference("/Pedidos")

            pedido_ref = self.ref.child(num_pedido)
            pedido_data = pedido_ref.get()

            if pedido_data:

                self.preencher_dados(pedido_data)
               
            else:  
               return 'Pedido nao existe'

        except Exception as e:
            pass

    def pegar_valor_tabela(self):
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
            (ui.campo_email_enviado, "EMAIL RENOVACAO")
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

            ui.campo_status_bd.setText('✅')
            
            ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed) 
            for i in range(ui.tableWidget.columnCount()): 
                ui.tableWidget.horizontalHeader().resizeSection(i, 83)

            
        except Exception as e:
            print(f"Erro ao atualizar o status: {e}")

        # Atualizar o campo de confirmação de pasta
        try:
            if ui.caminho_pasta.text():
                ui.label_confirmacao_criar_pasta.setText("✅")
        except Exception as e:
            print(f"Erro ao atualizar confirmação de pasta: {e}")

    def contar_verificacao(self):
        # Consulta no Firebase para pedidos com status "VERIFICAÇÃO"
        pedidos_verificacao = ref.child("Pedidos").order_by_child("STATUS").equal_to("VERIFICAÇÃO").get()
        
        # Consulta no Firebase para pedidos com status "VIDEO REALIZADA"
        pedidos_videook = ref.child("Pedidos").order_by_child("STATUS").equal_to("VIDEO REALIZADA").get()

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
        
        try:
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
                            ui.barra_progresso_consulta.setValue(y)
                            QApplication.processEvents()

                ui.barra_progresso_consulta.setValue(total_pedidos)  
                self.contar_verificacao()

                total_venda = valor_cnpj + valor_cpf
                ui.campo_relatorio.setPlainText(f'''(+)e-CNPJ [{j}]........R$ {valor_cnpj:.2f}
(+)e-CPF [{f}].........R$ {valor_cpf:.2f}
(=)Total [{j+f}].........R$ {total_venda:.2f}
(-){ui.campo_desconto.text()}%...............R$ {total_venda * (float(ui.campo_desconto.text()) / 100):.2f}
----------------------------------
(=)Total Esperado....R$ {total_venda * (1 - float(ui.campo_desconto.text()) / 100):.2f}
Vendas..........{venda}
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
        except:
            pass
 
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

            item_nome_documento.setForeground(QColor(90, 54, 247))

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
            ui.rb_digitacao.setStyleSheet("border:none;color:rgb(113,66,230);")  
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
        
        ui.rb_digitacao.setStyleSheet("border:none; color:rgb(170,170,170);")  
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
        self.animate_window_resize(530, 730)
        self.janela.atualizar_documentos_tabela()
        self.parent.setWindowOpacity(1.0)  

    def leaveEvent(self, event):
        self.janela.atualizar_documentos_tabela()


        if not ui.campo_verifica_tela_cheia.text() == "SIM":

            cursor_pos = QtGui.QCursor.pos()
            window_pos = self.parent.mapToGlobal(QtCore.QPoint(0, 0))
            window_rect = QRect(window_pos, self.parent.size())

            mouse_dentro_da_janela = window_rect.contains(cursor_pos)

            if not mouse_dentro_da_janela:

                if int(ui.campo_status_videook.text()) == 0 and int(ui.campo_status_verificacao.text()) == 0:
                    self.animate_window_resize(108, 53)
                else:
                    self.animate_window_resize(151, 53)
        else:
            cursor_pos = QtGui.QCursor.pos()
            window_pos = self.parent.mapToGlobal(QtCore.QPoint(0, 0))
            window_rect = QRect(window_pos, self.parent.size())
            transparencia = ui.campo_porcentagem_transparencia.value() / 100
            mouse_dentro_da_janela = window_rect.contains(cursor_pos)

            if not mouse_dentro_da_janela:
                if ui.checkBox_transparecer.isChecked(): 
                    self.parent.setWindowOpacity(transparencia)  
                else:
                    self.parent.setWindowOpacity(1.0)  
            else:
                self.parent.setWindowOpacity(1.0)  

        
    def mousePressEvent(self, event):
        self.animate_window_resize(530,730)#469

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
ui.campo_funcional.textChanged.connect(lambda:funcoes_app.valor_alterado(ui.campo_funcional))
ui.rb_aprovado.toggled.connect(lambda:funcoes_app.valor_alterado(ui.rb_aprovado))
ui.rb_cancelado.toggled.connect(lambda:funcoes_app.valor_alterado(ui.rb_cancelado))
ui.rb_digitacao.toggled.connect(lambda:funcoes_app.valor_alterado(ui.rb_digitacao))
ui.rb_verificacao.toggled.connect(lambda:funcoes_app.valor_alterado(ui.rb_verificacao))
ui.rb_videook.toggled.connect(lambda:funcoes_app.valor_alterado(ui.rb_videook))

#Campos botões
ui.botao_excluir_dados_tabela.clicked.connect(lambda:funcoes_app.limpar_tabela())
ui.botao_duplicar_pedido.clicked.connect(lambda:funcoes_app.duplicar_pedido())
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
ui.botao_consulta_funcional.clicked.connect((lambda:funcoes_app.procurar_funcional()))
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
ui.campo_funcional.mousePressEvent = lambda event: funcoes_app.copiar_campo("campo_funcional")
ui.campo_preco_certificado.setReadOnly(False)
#ui.campo_cnpj_razao_social.setReadOnly(True)
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
ui.campo_dias_renovacao.setToolTip("Define o intervalo de dias para o envio de emails de renovação. Por exemplo, se definir 15 , serão considerados os próximos 15 dias a partir de hoje.")


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
janela.setFixedSize(151, 53)           
janela.show()


sys.exit(app.exec_())