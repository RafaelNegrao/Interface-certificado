import datetime
import pandas as pd
import tkinter as tk
import os
import time
import psutil
import requests
import PyPDF2
import fitz
import pyautogui
import sys
import subprocess
import math
import pyperclip
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
from PyQt5 import QtGui, QtWidgets,QtCore,Qt
from PyQt5.QtWidgets import (
QTableWidgetItem,
QTableWidget,
QApplication,
QMessageBox,
QDesktopWidget,
QInputDialog,
QMainWindow,
QFileDialog,
QRadioButton,
QVBoxLayout,
QPushButton,
QDialog, 
QLineEdit,
QScrollArea,
QWidget,
QGridLayout,
QComboBox
)
from PyQt5.QtCore import QDate, QTime,QUrl, Qt,QTimer,QRect,QRegExp,QMimeData, QDateTime
from PyQt5.QtGui import QDesktopServices,QColor,QRegExpValidator,QGuiApplication
from Interface import Ui_janela
from firebase_admin import db
from requests.exceptions import RequestException
from credenciaisBd import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import shutil
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from collections import Counter,defaultdict
import numpy as np
import mplcursors
import calendar  # Para identificar o último dia do mês



ref = db.reference("/")


from acoes_banco_dados import Acoes_banco_de_dados
from funcoes_padrao import Funcoes_padrao
from hideWindow import JanelaOculta



app = QtWidgets.QApplication(sys.argv)
janela = QtWidgets.QMainWindow()
desktop = QDesktopWidget()
ui = Ui_janela()
ui.setupUi(janela)


helper = JanelaOculta(janela,ui)
banco_dados = Acoes_banco_de_dados(ui)
funcoes_app = Funcoes_padrao(ui)
