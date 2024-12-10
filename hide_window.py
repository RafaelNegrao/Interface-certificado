from imports import *

class JanelaOculta:
    def __init__(self, parent,ui):
        self.parent = parent
        self.ui = ui
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_window_size)
        self.animation_step = 5  # Ajustei para diminuir a animação
        self.animation_duration = 2  # Duração da animação em milissegundos
        self.animation_target_width = 0
        self.animation_target_height = 0
        self.janela = Funcoes_padrao(ui)
        

    def enterEvent(self, event):
        self.animate_window_resize(769, 705)
        self.janela.atualizar_documentos_tabela()
        self.parent.setWindowOpacity(1.0)  

    def leaveEvent(self, event):
        self.janela.atualizar_documentos_tabela()


        if not self.ui.campo_verifica_tela_cheia.text() == "SIM":

            cursor_pos = QtGui.QCursor.pos()
            window_pos = self.parent.mapToGlobal(QtCore.QPoint(0, 0))
            window_rect = QRect(window_pos, self.parent.size())

            mouse_dentro_da_janela = window_rect.contains(cursor_pos)

            if not mouse_dentro_da_janela:

                if int(self.ui.campo_status_videook.text()) == 0 and int(self.ui.campo_status_verificacao.text()) == 0:
                    self.animate_window_resize(108, 53)
                else:
                    self.animate_window_resize(151, 53)
        else:
            cursor_pos = QtGui.QCursor.pos()
            window_pos = self.parent.mapToGlobal(QtCore.QPoint(0, 0))
            window_rect = QRect(window_pos, self.parent.size())
            transparencia = self.ui.campo_porcentagem_transparencia.value() / 100
            mouse_dentro_da_janela = window_rect.contains(cursor_pos)

            if not mouse_dentro_da_janela:
                if self.ui.checkBox_transparecer.isChecked(): 
                    self.parent.setWindowOpacity(transparencia)  
                else:
                    self.parent.setWindowOpacity(1.0)  
            else:
                self.parent.setWindowOpacity(1.0)  

        
    def mousePressEvent(self, event):
        self.animate_window_resize(769,705)#469

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

