from PyQt5.QtCore import QPropertyAnimation,QRect

class AlteracoesInterface:
    def __init__(self, ui):
        self.ui = ui

    # Funções relacionadas ao status do banco de dados
    def apagar_label_status_bd(self):
        self.ui.campo_status_bd.setText("")
        AlteracoesInterface.animar_label_pular(self,self.ui.campo_status_bd)
    
    def label_status_bd_atualizado(self):
        self.ui.campo_status_bd.setText("✅")
        self.ui.campo_status_bd.setToolTip("Pedido atualizado")
        AlteracoesInterface.animar_label_pular(self,self.ui.campo_status_bd)

    def label_status_bd_desatualizado(self):
        self.ui.campo_status_bd.setText("❌")
        self.ui.campo_status_bd.setToolTip("Pedido desatualizado")


    # Funções relacionadas à captura de tela
    def confirmar_label_captura_tela(self):
        self.ui.label_confirmacao_tirar_print.setText("✅")
        AlteracoesInterface.animar_label_pular(self, self.ui.label_confirmacao_tirar_print)

    def negar_label_captura_tela(self):
        self.ui.label_confirmacao_tirar_print.setText("❌")
        AlteracoesInterface.animar_label_pular(self, self.ui.label_confirmacao_tirar_print)

    def zerar_label_captura_tela(self):
        self.ui.label_confirmacao_tirar_print.setText("")
        AlteracoesInterface.animar_label_pular(self, self.ui.label_confirmacao_tirar_print)


    # Funções relacionadas ao PDF
    def confirmar_label_converter_pdf(self):
        self.ui.label_confirmacao_converter_pdf.setText("✅")
        AlteracoesInterface.animar_label_pular(self, self.ui.label_confirmacao_converter_pdf)

    def zerar_label_converter_pdf(self):
        self.ui.label_confirmacao_converter_pdf.setText("")
        AlteracoesInterface.animar_label_pular(self, self.ui.label_confirmacao_converter_pdf)

    def negar_label_converter_pdf(self):
        self.ui.label_confirmacao_converter_pdf.setText("❌")
        AlteracoesInterface.animar_label_pular(self, self.ui.label_confirmacao_converter_pdf)


    # Funções mesclar PDF
    def confirmar_label_mesclar_pdf(self):
        self.ui.label_confirmacao_mesclar_pdf.setText("✅")
        AlteracoesInterface.animar_label_pular(self,self.ui.label_confirmacao_mesclar_pdf)

    def zerar_label_mesclar_pdf(self):
        self.ui.label_confirmacao_mesclar_pdf.setText("")
        AlteracoesInterface.animar_label_pular(self,self.ui.label_confirmacao_mesclar_pdf)

    def negar_label_mesclar_pdf(self):
        self.ui.label_confirmacao_mesclar_pdf.setText("❌")
        AlteracoesInterface.animar_label_pular(self,self.ui.label_confirmacao_mesclar_pdf)


    # Funções relacionadas à criação de pasta
    def confirmar_label_criar_pasta(self):
        self.ui.label_confirmacao_criar_pasta.setText("✅")
        AlteracoesInterface.animar_label_pular(self, self.ui.label_confirmacao_criar_pasta)

    def zerar_label_criar_pasta(self):
        self.ui.label_confirmacao_criar_pasta.setText("")
        AlteracoesInterface.animar_label_pular(self, self.ui.label_confirmacao_criar_pasta)

    def negar_label_criar_pasta(self):
        self.ui.label_confirmacao_criar_pasta.setText("❌")
        AlteracoesInterface.animar_label_pular(self, self.ui.label_confirmacao_criar_pasta)

    def lixeira_label_criar_pasta(self):
        self.ui.label_confirmacao_criar_pasta.setText("🗑️")
        AlteracoesInterface.animar_label_pular(self, self.ui.label_confirmacao_criar_pasta)


    # Funções relacionadas ao salvamento
    def confirmar_label_salvar(self):
        self.ui.label_confirmacao_salvar.setText("✅")
        AlteracoesInterface.animar_label_pular(self,self.ui.label_confirmacao_salvar)

    def zerar_label_salvar(self):
        self.ui.label_confirmacao_salvar.setText("")
        AlteracoesInterface.animar_label_pular(self,self.ui.label_confirmacao_salvar)

    def negar_label_salvar(self):
        self.ui.label_confirmacao_salvar.setText("❌")
        AlteracoesInterface.animar_label_pular(self,self.ui.label_confirmacao_salvar)


    # Funções relacionadas à exclusão
    def confirmar_label_excluir(self):
        self.ui.label_confirmacao_excluir.setText("⬇️")
        AlteracoesInterface.animar_label_pular(self, self.ui.label_confirmacao_excluir)

    def zerar_label_excluir(self):
        self.ui.label_confirmacao_excluir.setText("")
        AlteracoesInterface.animar_label_pular( self,self.ui.label_confirmacao_excluir)


    def animar_label_pular(self, label):

        if not hasattr(self, "animations"):
            self.animations = {}

        if label in self.animations and self.animations[label]["animation"].state() == QPropertyAnimation.Running:
            self.animations[label]["animation"].stop()
            label.setGeometry(self.animations[label]["start_geometry"])

        start_geometry = label.geometry()

        anim = QPropertyAnimation(label, b"geometry")
        anim.setDuration(500)

        end_geometry = QRect(
            start_geometry.x(),
            start_geometry.y() - 5,
            start_geometry.width(),
            start_geometry.height()
        )

        anim.setKeyValueAt(0.0, start_geometry)
        anim.setKeyValueAt(0.25, end_geometry)
        anim.setKeyValueAt(0.5, start_geometry)
        anim.setKeyValueAt(0.75, end_geometry)
        anim.setKeyValueAt(1.0, start_geometry)


        anim.finished.connect(lambda: label.setGeometry(start_geometry))

        self.animations[label] = {"animation": anim, "start_geometry": start_geometry}

        # Iniciar a animação
        anim.start()
