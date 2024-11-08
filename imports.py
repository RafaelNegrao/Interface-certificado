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

