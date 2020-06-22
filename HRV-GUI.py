# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lol.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QPalette, QDoubleValidator
from PyQt5.QtWidgets import QApplication, QWidget, QPlainTextEdit
import pyqtgraph as pg
import scipy.io
from scipy.signal import butter, lfilter
import numpy as np
from pyhrv.hrv import hrv
from biosppy.signals.ecg import ecg
import pyhrv.tools as tools
import matplotlib.pyplot as plt
from scipy import signal
from openpyxl import Workbook
import os

global name, data, pre, flag_obelezi, results, rpeaks, nni, sample_rate, folder

data = None
flag_obelezi=0

def notch_filter(data, f0, fs):
    Q=50.0
    b, a = signal.iirnotch(f0, Q, fs)
    y = lfilter(b, a, data)
    return y

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1130, 1004)
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #self.graphicsView = pg.PlotWidget(self.centralwidget)
        #self.graphicsView.setGeometry(QtCore.QRect(90, 10, 1021, 321))
        #self.graphicsView.setObjectName("graphicsView")
        self.view_tab = QtWidgets.QTabWidget(self.centralwidget)
        self.view_tab.setGeometry(QtCore.QRect(90, 10, 1021, 321))
        self.view_tab.setObjectName("view_tab")
        self.signal_tab = QtWidgets.QWidget()
        self.signal_tab.setObjectName("signal_tab")
        self.view_signal = pg.PlotWidget(self.signal_tab)
        self.view_signal.setGeometry(QtCore.QRect(0, 0, 1011, 291))
        self.view_signal.setObjectName("view_signal")
        self.view_tab.addTab(self.signal_tab, "")
        self.tachogram_tab = QtWidgets.QWidget()
        self.tachogram_tab.setObjectName("tachogram_tab")
        self.tachogram_view = pg.PlotWidget(self.tachogram_tab)
        self.tachogram_view.setGeometry(QtCore.QRect(0, 0, 1011, 291))
        self.tachogram_view.setObjectName("tachogram_view")
        self.view_tab.addTab(self.tachogram_tab, "")
        
        self.load = QtWidgets.QPushButton(self.centralwidget)
        self.load.setGeometry(QtCore.QRect(10, 10, 71, 321))
        self.load.setObjectName("load")
        self.filter_box = QtWidgets.QGroupBox(self.centralwidget)
        self.filter_box.setGeometry(QtCore.QRect(10, 340, 221, 161))
        self.filter_box.setObjectName("filter_box")
        self.filter = QtWidgets.QPushButton(self.filter_box)
        self.filter.setGeometry(QtCore.QRect(60, 120, 111, 31))
        self.filter.setObjectName("filter")
        self.label_2 = QtWidgets.QLabel(self.filter_box)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 71, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.filter_box)
        self.label_3.setGeometry(QtCore.QRect(20, 50, 71, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.filter_box)
        self.label_4.setGeometry(QtCore.QRect(20, 80, 71, 21))
        self.label_4.setObjectName("label_4")
        self.sample_rate = QtWidgets.QLineEdit(self.filter_box)
        self.sample_rate.setGeometry(QtCore.QRect(100, 20, 113, 22))
        self.sample_rate.setValidator(QDoubleValidator())
        self.sample_rate.setObjectName("sample_rate")
        self.lowcut = QtWidgets.QLineEdit(self.filter_box)
        self.lowcut.setGeometry(QtCore.QRect(100, 50, 113, 22))
        self.lowcut.setValidator(QDoubleValidator())
        self.lowcut.setObjectName("lowcut")
        self.highcut = QtWidgets.QLineEdit(self.filter_box)
        self.highcut.setGeometry(QtCore.QRect(100, 80, 113, 22))
        self.highcut.setValidator(QDoubleValidator())
        self.highcut.setObjectName("highcut")
        self.cutter_box = QtWidgets.QGroupBox(self.centralwidget)
        self.cutter_box.setGeometry(QtCore.QRect(10, 580, 221, 161))
        self.cutter_box.setObjectName("cutter_box")
        self.select = QtWidgets.QPushButton(self.cutter_box)
        self.select.setGeometry(QtCore.QRect(10, 40, 101, 41))
        self.select.setObjectName("select")
        self.select.setEnabled(False)
        self.cut = QtWidgets.QPushButton(self.cutter_box)
        self.cut.setGeometry(QtCore.QRect(110, 40, 101, 41))
        self.cut.setObjectName("cut")
        self.cut.setEnabled(False)
        self.undo = QtWidgets.QPushButton(self.cutter_box)
        self.undo.setGeometry(QtCore.QRect(10, 100, 101, 41))
        self.undo.setObjectName("undo")
        self.undo.setEnabled(False)
        self.redo = QtWidgets.QPushButton(self.cutter_box)
        self.redo.setGeometry(QtCore.QRect(110, 100, 101, 41))
        self.redo.setObjectName("redo")
        self.redo.setEnabled(False)
        self.results_box = QtWidgets.QGroupBox(self.centralwidget)
        self.results_box.setGeometry(QtCore.QRect(240, 480, 871, 471))
        self.results_box.setObjectName("results_box")
        self.results_tab = QtWidgets.QTabWidget(self.results_box)
        self.results_tab.setGeometry(QtCore.QRect(0, 20, 871, 471))
        self.results_tab.setObjectName("results_tab")
        self.time = QtWidgets.QWidget()
        self.time.setObjectName("time")
        self.time_results = QtWidgets.QTabWidget(self.time)
        self.time_results.setGeometry(QtCore.QRect(0, 0, 871, 421))
        self.time_results.setObjectName("time_results")
        self.nni_hist = QtWidgets.QWidget()
        self.nni_hist.setObjectName("nni_hist")
        self.nni_hist_label = QtWidgets.QLabel(self.nni_hist)
        self.nni_hist_label.setGeometry(QtCore.QRect(0, 0, 861, 391))
        self.nni_hist_label.setObjectName("nni_hist_label")
        self.time_results.addTab(self.nni_hist, "")
        self.time_param = QtWidgets.QWidget()
        self.time_param.setObjectName("time_param")
        self.time_results.addTab(self.time_param, "")
        self.results_tab.addTab(self.time, "")
        self.frequency = QtWidgets.QWidget()
        self.frequency.setObjectName("frequency")
        self.freq_results = QtWidgets.QTabWidget(self.frequency)
        self.freq_results.setGeometry(QtCore.QRect(0, 0, 871, 421))
        self.freq_results.setObjectName("freq_results")
        self.welch = QtWidgets.QWidget()
        self.welch.setObjectName("welch")
        self.welch_label = QtWidgets.QLabel(self.welch)
        self.welch_label.setGeometry(QtCore.QRect(0, 0, 861, 391))
        self.welch_label.setObjectName("welch_label")
        self.freq_results.addTab(self.welch, "")
        self.psd_ls = QtWidgets.QWidget()
        self.psd_ls.setObjectName("psd_ls")
        self.psd_ls_label = QtWidgets.QLabel(self.psd_ls)
        self.psd_ls_label.setGeometry(QtCore.QRect(0, 0, 861, 391))
        self.psd_ls_label.setObjectName("psd_ls_label")
        self.freq_results.addTab(self.psd_ls, "")
        self.psd_autoregressive = QtWidgets.QWidget()
        self.psd_autoregressive.setObjectName("psd_autoregressive")
        self.psd_autoregressive_label = QtWidgets.QLabel(self.psd_autoregressive)
        self.psd_autoregressive_label.setGeometry(QtCore.QRect(0, 0, 861, 391))
        self.psd_autoregressive_label.setObjectName("psd_autoregressive_label")
        self.freq_results.addTab(self.psd_autoregressive, "")
        self.freq_param = QtWidgets.QWidget()
        self.freq_param.setObjectName("freq_param")
        self.freq_results.addTab(self.freq_param, "")
        self.results_tab.addTab(self.frequency, "")
        self.nonlinear = QtWidgets.QWidget()
        self.nonlinear.setObjectName("nonlinear")
        self.nonlinear_results = QtWidgets.QTabWidget(self.nonlinear)
        self.nonlinear_results.setGeometry(QtCore.QRect(0, 0, 871, 421))
        self.nonlinear_results.setObjectName("nonlinear_results")
        self.poincare = QtWidgets.QWidget()
        self.poincare.setObjectName("poincare")
        self.poincare_label = QtWidgets.QLabel(self.poincare)
        self.poincare_label.setGeometry(QtCore.QRect(0, 0, 861, 391))
        self.poincare_label.setObjectName("poincare_label")
        self.nonlinear_results.addTab(self.poincare, "")
        self.dfa = QtWidgets.QWidget()
        self.dfa.setObjectName("dfa")
        self.dfa_label = QtWidgets.QLabel(self.dfa)
        self.dfa_label.setGeometry(QtCore.QRect(0, 0, 861, 391))
        self.dfa_label.setObjectName("dfa_label")
        self.nonlinear_results.addTab(self.dfa, "")
        self.nonlin_param = QtWidgets.QWidget()
        self.nonlin_param.setObjectName("nonlin_param")
        self.nonlinear_results.addTab(self.nonlin_param, "")
        self.results_tab.addTab(self.nonlinear, "")
        self.export_2 = QtWidgets.QPushButton(self.centralwidget)
        self.export_2.setGeometry(QtCore.QRect(10, 890, 221, 41))
        self.export_2.setObjectName("export_2")
        self.builtin_box = QtWidgets.QGroupBox(self.centralwidget)
        self.builtin_box.setGeometry(QtCore.QRect(10, 500, 221, 80))
        self.builtin_box.setObjectName("builtin_box")
        self.filter_builtin = QtWidgets.QPushButton(self.builtin_box)
        self.filter_builtin.setGeometry(QtCore.QRect(60, 30, 111, 31))
        self.filter_builtin.setObjectName("radio_notch")
        self.rpeaks_view = pg.PlotWidget(self.centralwidget)
        self.rpeaks_view.setGeometry(QtCore.QRect(240, 350, 871, 121))
        self.rpeaks_view.setObjectName("label_5")
        self.calculateresults_box = QtWidgets.QGroupBox(self.centralwidget)
        self.calculateresults_box.setGeometry(QtCore.QRect(10, 740, 221, 141))
        self.calculateresults_box.setObjectName("calculateresults_box")
        self.calculate = QtWidgets.QPushButton(self.calculateresults_box)
        self.calculate.setGeometry(QtCore.QRect(50, 100, 111, 31))
        self.calculate.setObjectName("calculate")
        self.radio_group = QtWidgets.QGroupBox(self.calculateresults_box)
        self.radio_group.setGeometry(QtCore.QRect(10, 20, 201, 71))
        self.radio_group.setTitle("")
        self.radio_group.setObjectName("radio_group")
        self.results_whole = QtWidgets.QRadioButton(self.radio_group)
        self.results_whole.setGeometry(QtCore.QRect(20, 10, 161, 20))
        self.results_whole.setObjectName("results_whole")
        self.results_whole.setChecked(True)
        self.results_part = QtWidgets.QRadioButton(self.radio_group)
        self.results_part.setGeometry(QtCore.QRect(20, 40, 161, 20))
        self.results_part.setObjectName("results_part")

        self.time_txt = QPlainTextEdit(self.time_param)
        self.time_txt.setGeometry(QtCore.QRect(10, 10, 841, 371))
        self.time_txt.setObjectName("textBrowser")
        self.time_txt.setReadOnly(True)

        self.freq_txt = QPlainTextEdit(self.freq_param)
        self.freq_txt.setGeometry(QtCore.QRect(10, 10, 841, 371))
        self.freq_txt.setObjectName("textBrowser")
        self.time_txt.setReadOnly(False)

        self.nonlin_txt = QPlainTextEdit(self.nonlin_param)
        self.nonlin_txt.setGeometry(QtCore.QRect(10, 10, 841, 371))
        self.nonlin_txt.setObjectName("textBrowser")
        self.time_txt.setReadOnly(False)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1130, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1124, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setSizeGripEnabled(False)
        MainWindow.setStatusBar(self.statusbar)
        self.lr = pg.LinearRegionItem([50000, 80000])

        self.retranslateUi(MainWindow)
        self.results_tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.filter_builtin.clicked.connect(self.builtinFilter)
        self.load.clicked.connect(self.file_open)
        self.select.clicked.connect(self.selectf)
        self.cut.clicked.connect(self.cutf)

        self.undo.clicked.connect(self.undof)
        self.redo.clicked.connect(self.redof)

        self.filter.clicked.connect(self.filter_signal)
        self.sample_rate.editingFinished.connect(self.getSampleRate)

        self.calculate.clicked.connect(self.getResults)
        self.results_part.toggled.connect(lambda:self.selectPartResults())
        self.results_whole.toggled.connect(lambda:self.selectPartResults())

        self.export_2.clicked.connect(self.exportResults)

    def exportResults(self):
        global results, name
        s=folder + '/' + name + '_export.xlsx'
        wb=Workbook()
        sheet1=wb.active
        sheet1.append(['ID', 'Mean HR', 'Min HR', 'Max HR', 'Std. Dev. HR', 'Mean NN', 'Min NN', 'Max NN', 'Mean NN diff.', 'Min NN diff.', 'Max NN diff.', 'SDNN', 'SDNN Index', 'SDANN', 'RMMSD', 'SDSD', 'NN50', 'pNN50', 'NN20', 'pNN20', 'Triangular Index', 'TINN', 'Geometrical param. N', 'Geometrical param. M', 'Weltch\'s peaks (VLF, LF, HLF) [Hz]', 'Weltch\'s Absolute powers (VLF, LF, HLF) [ms^2]', 'Weltch\'s Relative powers (VLF, LF, HLF) [%]', 'Weltch\'s Logaritmic powers (VLF, LF, HLF) [-]', 'Weltch\'s Total power [ms^2]', 'Weltch\'s LF/HF ratio [-]', 'PSD - LS peaks (VLF, LF, HLF) [Hz]', 'PSD - LS Absolute powers (VLF, LF, HLF) [ms^2]', 'PSD - LS Relative powers (VLF, LF, HLF) [%]', 'PSD - LS Logaritmic powers (VLF, LF, HLF) [-]', 'PSD - LS Total power [ms^2]', 'PSD - LS LF/HF ratio [-]', 'PSD - AR peaks (VLF, LF, HLF) [Hz]', 'PSD - AR Absolute powers (VLF, LF, HLF) [ms^2]', 'PSD - AR Relative powers (VLF, LF, HLF) [%]', 'PSD - AR Logaritmic powers (VLF, LF, HLF) [-]', 'PSD - AR Total power [ms^2]', 'PSD - AR LF/HF ratio [-]', 'Poincaré SD1 [ms]', 'Poincaré SD2 [ms]', 'Poincaré SD2/SD1 [-]', 'Area S [ms]', 'Sample Entropy', 'DFA alpha1 [ms]', 'DFA alpha2[ms]'])
        sheet1.append([str(name), results['hr_mean'], results['hr_min'], results['hr_max'], results['hr_std'], results['nni_mean'], results['nni_min'], results['nni_max'], results['nni_diff_mean'], results['nni_diff_min'], results['nni_diff_max'], results['sdnn'], results['sdnn_index'], results['sdann'], results['rmssd'], results['sdsd'], results['nn50'], results['pnn50'], results['nn20'], results['pnn20'], results['tri_index'], results['tinn'], results['tinn_n'], results['tinn_m'], str(results['fft_peak']), str(results['fft_abs']), str(results['fft_rel']), str(results['fft_log']), results['fft_total'], results['fft_ratio'], str(results['lomb_peak']), str(results['lomb_abs']), str(results['lomb_rel']), str(results['lomb_log']), results['lomb_total'], results['lomb_ratio'], str(results['ar_peak']), str(results['ar_abs']), str(results['ar_rel']), str(results['ar_log']), results['ar_total'], results['ar_ratio'], results['sd1'], results['sd2'], results['sd_ratio'], results['ellipse_area'], results['sampen'], results['dfa_alpha1'], results['dfa_alpha2']])
        wb.save(s)

    def nonlin_domain_txt(self):
        global results, folder
        s=str(folder + '/nonlinear_domain.txt')
        file = open(s,"w")
        file.write("============================================ \n")
        file.write("             NONLINEAR ANALYSIS\n")
        file.write("============================================ \n")
        file.write("Poincaré Plot\n")
        file.write("SD1:				%f [ms]\n" % results['sd1'])
        file.write("SD2:				%f [ms]\n" % results['sd2'])
        file.write("SD2/SD1:				%f [-]\n" % results['sd_ratio'])
        file.write("Area S:				%f [ms]\n" % results['ellipse_area'])
        file.write("Sample Entropy:			%f\n" % results['sampen'])
        file.write("DFA alpha1:				%f [ms]\n" % results['dfa_alpha1'])
        file.write("DFA alpha2:				%f [ms]\n" % results['dfa_alpha2'])

        file.close()
        
    def freq_domain_txt(self):
        global results, folder
        s=str(folder + '/frequency_domain.txt')
        file = open(s,"w")

        file.write("============================================ \n")
        file.write("        FREQUENCY DOMAIN PARAMETERS\n")
        file.write("============================================ \n")

        file.write("\nWELCH'S METHOD \n \n")
        file.write("Peak Frequencies:\n")
        file.write("VLF:				%f [Hz]\n" % results['fft_peak'][0])
        file.write("LF :				%f [Hz]\n" % results['fft_peak'][1])
        file.write("HLF:				%f [Hz]\n" % results['fft_peak'][2])

        file.write("Absolute Powers:\n")
        file.write("VLF:				%f [ms^2]\n" % results['fft_abs'][0])
        file.write("LF :				%f [ms^2]\n" % results['fft_abs'][1])
        file.write("HLF:				%f [ms^2]\n" % results['fft_abs'][2])

        file.write("Relative Powers:\n")
        file.write("VLF:				%f [%%]\n" % results['fft_rel'][0])
        file.write("LF :				%f [%%]\n" % results['fft_rel'][1])
        file.write("HLF:				%f [%%]\n" % results['fft_rel'][2])

        file.write("Logarithmic Powers:\n")
        file.write("VLF:				%f [-]\n" % results['fft_log'][0])
        file.write("LF :				%f [-]\n" % results['fft_log'][1])
        file.write("HLF:				%f [-]\n" % results['fft_log'][2])
        file.write("Total Power:			%f [ms^2]\n" % results['fft_total'])
        file.write("LF/HF ratio:			%f [-]\n" % results['fft_ratio'])

        file.write("\nPSD - LOMB-SCARGLE \n \n")
        file.write("Peak Frequencies:\n")
        file.write("VLF:				%f [Hz]\n" % results['lomb_peak'][0])
        file.write("LF :				%f [Hz]\n" % results['lomb_peak'][1])
        file.write("HLF:				%f [Hz]\n" % results['lomb_peak'][2])

        file.write("Absolute Powers:\n")
        file.write("VLF:				%f [ms^2]\n" % results['lomb_abs'][0])
        file.write("LF :				%f [ms^2]\n" % results['lomb_abs'][1])
        file.write("HLF:				%f [ms^2]\n" % results['lomb_abs'][2])

        file.write("Relative Powers:\n")
        file.write("VLF:				%f [%%]\n" % results['lomb_rel'][0])
        file.write("LF :				%f [%%]\n" % results['lomb_rel'][1])
        file.write("HLF:				%f [%%]\n" % results['lomb_rel'][2])

        file.write("Logarithmic Powers:\n")
        file.write("VLF:				%f [-]\n" % results['lomb_log'][0])
        file.write("LF :				%f [-]\n" % results['lomb_log'][1])
        file.write("HLF:				%f [-]\n" % results['lomb_log'][2])
        file.write("Total Power:			%f [ms^2]\n" % results['lomb_total'])
        file.write("LF/HF ratio:			%f [-]\n" % results['lomb_ratio'])

        file.write("\nPSD - AUTOREGRESSIVE \n \n")
        file.write("Peak Frequencies:\n")
        file.write("VLF:				%f [Hz]\n" % results['ar_peak'][0])
        file.write("LF :				%f [Hz]\n" % results['ar_peak'][1])
        file.write("HLF:				%f [Hz]\n" % results['ar_peak'][2])

        file.write("Absolute Powers:\n")
        file.write("VLF:				%f [ms^2]\n" % results['ar_abs'][0])
        file.write("LF :				%f [ms^2]\n" % results['ar_abs'][1])
        file.write("HLF:				%f [ms^2]\n" % results['ar_abs'][2])

        file.write("Relative Powers:\n")
        file.write("VLF:				%f [%%]\n" % results['ar_rel'][0])
        file.write("LF :				%f [%%]\n" % results['ar_rel'][1])
        file.write("HLF:				%f [%%]\n" % results['ar_rel'][2])

        file.write("Logarithmic Powers:\n")
        file.write("VLF:				%f [-]\n" % results['ar_log'][0])
        file.write("LF :				%f [-]\n" % results['ar_log'][1])
        file.write("HLF:				%f [-]\n" % results['ar_log'][2])
        file.write("Total Power:			%f [ms^2]\n" % results['ar_total'])
        file.write("LF/HF ratio:			%f [-]\n" % results['ar_ratio'])

        file.close()
        
    def time_domain_txt(self):
        global results, folder
        s=str(folder + '/time_domain.txt')
        file = open(s,"w")
        
        file.write("============================================ \n")
        file.write("         TIME DOMAIN Results \n")
        file.write("============================================\n")
        
        file.write('HR Results\n')
        file.write('Mean HR:				%f [bpm]\n' % results['hr_mean'])
        file.write('Min HR:				%f [bpm]\n' % results['hr_min'])
        file.write('Max HR:				%f [bpm]\n' % results['hr_max'])
        file.write('Std. Dev. HR:			%f [bpm]\n' % results['hr_std'])

        file.write('NN Results\n')
        file.write('Mean NN:				%f [ms]\n' % results['nni_mean'])
        file.write('Min NN:				%f [ms]\n' % results['nni_min'])
        file.write('Max NN:				%f [ms]\n' % results['nni_max'])

        file.write('NN diff. Results\n')

        file.write('Mean NN diff:			%f [ms]\n' % results['nni_diff_mean'])
        file.write('Min NN diff:			%f [ms]\n' % results['nni_diff_min'])
        file.write('Max NN diff:			%f [ms]\n' % results['nni_diff_max'])

        file.write('SDNN:				%f [ms]\n' % results['sdnn'])
        file.write('SDNN Index:				%f [ms]\n' % results['sdnn_index'])
        file.write('SDANN:				%f [ms]\n' % results['sdann'])
        file.write('RMMSD:				%f [ms]\n' % results['rmssd'])
        file.write('SDSD:				%f [ms]\n' % results['sdsd'])
        file.write('NN50:				%i [-]\n' % results['nn50'])
        file.write('pNN50: 				%f [%%]\n' % results['pnn50'])
        file.write('NN20:				%i [-]\n' % results['nn20'])
        file.write('pNN20: 				%f [%%]\n' % results['pnn20'])

        file.write('=== Geometrical Parameters\n')
        file.write('Triangular Index:			%f [-]\n' % results['tri_index'])
        file.write('TINN:				%f [ms]\n' % results['tinn'])
        file.write('N:  				%f [ms]\n' % results['tinn_n'])
        file.write('M:	          			%f [ms]\n' % results['tinn_m'])

        file.close()

    def getSampleRate(self):
        global sample_rate
        sample_rate=float(self.sample_rate.text())

    def builtinFilter(self):
        global data, sample_rate, rpeaks, pre
        if data is None:
            self.showMsg('No data to filter')
        else:
            filt, rpeaks=ecg(signal=data, sampling_rate=float(sample_rate), show=False)[1:3]
            pre=data
            data=filt
            self.undo.setEnabled(True)
            self.redo.setEnabled(False)
            
            self.update()

    def plotPeaks(self, signal, peaks):
        global sample_rate
        self.rpeaks_view.clear()
        t=tools.time_vector(signal=signal, sampling_rate=sample_rate)
        self.rpeaks_view.plot(t, signal, pen=pg.mkPen('r'))
        p=np.array([])
        for x in peaks:
            p=np.append(p, signal[x])
        r=t[peaks]
        scatter=pg.ScatterPlotItem(pen=pg.mkPen(width=5, color='g'), symbol='d', size=1)
        scatter.setData(r, p)
        self.rpeaks_view.addItem(scatter)
        self.rpeaks_view.setLimits(xMin=0, xMax=t[-1])
        self.rpeaks_view.setXRange(5, 10)
        self.rpeaks_view.setMouseEnabled(x=True, y=False)
        self.rpeaks_view.setLabel('bottom', text='Time [s]')

    def showPlots(self):
        global folder
        #Time Domain plots
        s=str(folder + '/nni_histogram.jpg')
        results['nni_histogram'].savefig(s)
        nni_histogram = QImage(s)
        self.nni_hist_label.setPixmap(QPixmap.fromImage(nni_histogram).scaled(861, 391, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation))
        self.nni_hist_label.setAlignment(QtCore.Qt.AlignCenter)

        #Frequency Domain plots
        s=str(folder + '/fft_plot.jpg')
        results['fft_plot'].savefig(s)
        fft_plot = QImage(s)
        self.welch_label.setPixmap(QPixmap.fromImage(fft_plot).scaled(861, 391, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation))
        self.welch_label.setAlignment(QtCore.Qt.AlignCenter)

        s=str(folder + '/lomb_plot.jpg')
        results['lomb_plot'].savefig(s)
        lomb_plot = QImage(s)
        self.psd_ls_label.setPixmap(QPixmap.fromImage(lomb_plot).scaled(861, 391, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation))
        self.psd_ls_label.setAlignment(QtCore.Qt.AlignCenter)

        s=str(folder + '/ar_plot.jpg')
        results['ar_plot'].savefig(s)
        ar_plot = QImage(s)
        self.psd_autoregressive_label.setPixmap(QPixmap.fromImage(ar_plot).scaled(861, 391, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation))
        self.psd_autoregressive_label.setAlignment(QtCore.Qt.AlignCenter)

        #Nonlinear plots
        s=str(folder + '/poincare_plot.jpg')
        results['poincare_plot'].savefig(s)
        poincare_plot = QImage(s)
        self.poincare_label.setPixmap(QPixmap.fromImage(poincare_plot).scaled(861, 391, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation))
        self.poincare_label.setAlignment(QtCore.Qt.AlignCenter)

        s=str(folder + '/dfa_plot.jpg')
        results['dfa_plot'].savefig(s)
        dfa_plot = QImage(s)
        self.dfa_label.setPixmap(QPixmap.fromImage(dfa_plot).scaled(861, 391, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation))
        self.dfa_label.setAlignment(QtCore.Qt.AlignCenter)

        for key in results.keys():
            print(key, results[key])

    def selectPartResults(self):

        if self.view_tab.currentIndex()==0:
            plot=self.view_signal
        else:
            plot=self.tachogram_view

        if self.results_part.isChecked():
            
            geom=plot.getPlotItem().getViewBox().viewRange()
            a=geom[0][0]+(geom[0][1]-geom[0][0])*0.2
            b=geom[0][1]-(geom[0][1]-geom[0][0])*0.2
            self.lr.setRegion([int(a), int(b)])
            plot.addItem(self.lr)
        elif self.results_whole.isChecked():
            plot.removeItem(self.lr)
            
    def getResults(self):
        global data, results, rpeaks, sample_rate
        if self.results_whole.isChecked():
            filt, rpeaks=ecg(signal=data, sampling_rate=sample_rate, show=False)[1:3]
            self.plotPeaks(data, rpeaks)
            rpeaks=rpeaks/sample_rate
            nni=tools.nn_intervals(rpeaks=rpeaks)
            results=hrv(nni=nni, rpeaks=rpeaks, sampling_rate=sample_rate, interval=[0, int(len(data)/sample_rate)], show=False)
            self.showPlots()

            self.time_domain_txt()
            s=str(folder + '/time_domain.txt')
            text=open(s).read()
            self.time_txt.setPlainText(text)

            self.freq_domain_txt()
            s=str(folder + '/frequency_domain.txt')
            text=open(s).read()
            self.freq_txt.setPlainText(text)

            self.nonlin_domain_txt()
            s=str(folder + '/nonlinear_domain.txt')
            text=open(s).read()
            self.nonlin_txt.setPlainText(text)
            
        elif self.results_part.isChecked():
            limits = self.lr.getRegion()
            x=int(limits[0]*sample_rate)
            y=int(limits[1]*sample_rate)
            if x<0:
                signal_t=data[0:y]
            elif y>len(data):
                signal_t=data[x:]
            else:    
                signal_t=data[x:y]

            filt, rpeaks=ecg(signal=signal_t, sampling_rate=sample_rate, show=False)[1:3]
            self.plotPeaks(signal_t, rpeaks)
            rpeaks=rpeaks/sample_rate
            nni=tools.nn_intervals(rpeaks=rpeaks)
            results=hrv(nni=nni, rpeaks=rpeaks, sampling_rate=sample_rate, interval=[0, int(len(signal_t)/sample_rate)], show=False)
            self.showPlots()
        else:
            self.showMsg('Please select if you want HRV parameters for whole signal or for selected part')

    def showMsg(self, message):
        msgBox=QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setWindowTitle('Warning')
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()

    def filter_signal(self):
        global data, rpeaks
        sample_rate=self.sample_rate.text()
        lowcut=self.lowcut.text()
        highcut=self.highcut.text()
        if data is None:
            self.showMsg('No data to filter')
        elif sample_rate=='' or lowcut=='' or highcut=='':
            self.showMsg('Enter all parameters for filter')
        else:
            a=butter_bandpass_filter(data, float(lowcut), float(highcut), float(sample_rate))
            data=a
            #filt, rpeaks=ecg(signal=data, sampling_rate=float(sample_rate), show=False)[1:3]
            #data=filt
            self.update()
            self.undo.setEnabled(True)
            self.redo.setEnabled(False)
       

    def undof(self):
        global pre, data
        temp=data
        data=pre
        pre=temp
        self.redo.setEnabled(True)
        self.undo.setEnabled(False)
        self.update()
        
    def redof(self):
        global pre, data
        temp=data
        data=pre
        pre=temp
        self.redo.setEnabled(False)
        self.undo.setEnabled(True)
        self.update()

    def selectf(self):
        
        global flag_obelezi

        if self.view_tab.currentIndex()==0:
            plot=self.view_signal
        else:
            plot=self.tachogram_view
            
        geom=plot.getPlotItem().getViewBox().viewRange()
        a=geom[0][0]+(geom[0][1]-geom[0][0])*0.2
        b=geom[0][1]-(geom[0][1]-geom[0][0])*0.2
        self.lr.setRegion([int(a), int(b)])
        if flag_obelezi==0:
            plot.addItem(self.lr)
            self.cut.setDisabled(False)
            flag_obelezi=1
        else:
            flag_obelezi=0
            plot.removeItem(self.lr)
            self.cut.setDisabled(True)
            

    def cutf(self):
        global flag_obelezi, rpeaks, sample_rate, pre, data

        if self.view_tab.currentIndex()==0:
            plot=self.view_signal
        else:
            plot=self.tachogram_view
            
        self.redo.setEnabled(False)
        self.undo.setEnabled(True)
        limits = self.lr.getRegion()
        pre=data
        x=int(limits[0]*sample_rate)
        y=int(limits[1]*sample_rate)
        if x<0:
            data=pre[y:]
        elif y>len(data):
            data=pre[0:x]
        else:    
            a=pre[0:x]
            b=pre[y:]
            data=np.concatenate((a,b))
        plot.removeItem(self.lr)
        flag_obelezi=0
        filt, rpeaks=ecg(signal=data, sampling_rate=sample_rate, show=False)[1:3]
        self.update()
        self.cut.setEnabled(False)
        self.select.setDisabled(False)

    def file_open(self):
        global name, data, pre, folder
        if self.sample_rate.text()=='':
            self.showMsg('Please enter sampling rate first')
        else:
            name, _ =QtWidgets.QFileDialog.getOpenFileName(None, "Open File", "", "Mat Files (*.mat)")
            if name!='':
                di=name
                mat= scipy.io.loadmat(name)
                a=mat['ALLEEG']
                b=a['data']
                c=b[0,0]
                data=c[19]
                pre=data
                sample_rate=float(self.sample_rate.text())
                name=name.split(".")[0]
                name=name.split("/")[-1]
                s=di.split("/")
                del s[-1]
                folder=("/").join(s) + '/' + name + '_results'
                if os.path.exists(folder)==False:
                    os.mkdir(folder)
                
                
                self.update()
                self.undo.setEnabled(False)
                self.redo.setEnabled(False)
                self.rpeaks_view.clear()
                self.nni_hist_label.clear()
                self.welch_label.clear()
                self.psd_ls_label.clear()
                self.psd_autoregressive_label.clear()
                self.poincare_label.clear()
                self.dfa_label.clear()
                self.time_txt.clear()
                self.freq_txt.clear()
                self.nonlin_txt.clear()
                self.select.setDisabled(False)

    def update(self):
        global data, rpeaks, nni, sample_rate
        t=tools.time_vector(signal=data, sampling_rate=sample_rate)

        self.view_signal.clear()
        self.view_signal.plot(t, data, pen=pg.mkPen('r'))
        self.view_signal.setLimits(xMin=0, xMax=t[-1])
        self.view_signal.setMouseEnabled(x=True, y=False)
        self.view_signal.setLabel('bottom', text='Time [s]')
        
        filt, rpeaks=ecg(signal=data, sampling_rate=sample_rate, show=False)[1:3]
        rpeaks=rpeaks/sample_rate
        nni=tools.nn_intervals(rpeaks=rpeaks)
        
        t = np.cumsum(nni) / 1000.

        self.tachogram_view.clear()
        self.tachogram_view.plot(t, nni, pen=pg.mkPen('r'))
        self.tachogram_view.setLimits(xMin=0, xMax=t[-1])
        self.tachogram_view.setMouseEnabled(x=True, y=False)
        self.tachogram_view.setLabel('bottom', text='Time [s]')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HRV"))
        self.load.setText(_translate("MainWindow", "Load"))
        self.filter_box.setTitle(_translate("MainWindow", "Bandpass Filter"))
        self.filter.setText(_translate("MainWindow", "Filter"))
        self.label_2.setText(_translate("MainWindow", "Sample rate"))
        self.label_3.setText(_translate("MainWindow", "Low Cut"))
        self.label_4.setText(_translate("MainWindow", "High Cut"))
        self.cutter_box.setTitle(_translate("MainWindow", "Cut signal"))
        self.select.setText(_translate("MainWindow", "Select"))
        self.cut.setText(_translate("MainWindow", "Cut"))
        self.undo.setText(_translate("MainWindow", "Undo"))
        self.redo.setText(_translate("MainWindow", "Redo"))
        self.results_box.setTitle(_translate("MainWindow", "Results"))
        self.time_results.setTabText(self.time_results.indexOf(self.nni_hist), _translate("MainWindow", "NNI Histogram"))
        self.time_results.setTabText(self.time_results.indexOf(self.time_param), _translate("MainWindow", "Parameters"))
        self.results_tab.setTabText(self.results_tab.indexOf(self.time), _translate("MainWindow", "Time Domain"))
        self.freq_results.setTabText(self.freq_results.indexOf(self.welch), _translate("MainWindow", "Welch\'s Method"))
        self.freq_results.setTabText(self.freq_results.indexOf(self.psd_ls), _translate("MainWindow", "PSD - Lomb-Scargle"))
        self.freq_results.setTabText(self.freq_results.indexOf(self.psd_autoregressive), _translate("MainWindow", "PSD - Autoregressive"))
        self.freq_results.setTabText(self.freq_results.indexOf(self.freq_param), _translate("MainWindow", "Parameters"))
        self.results_tab.setTabText(self.results_tab.indexOf(self.frequency), _translate("MainWindow", "Frequency Domain"))
        self.nonlinear_results.setTabText(self.nonlinear_results.indexOf(self.poincare), _translate("MainWindow", "Poincare"))
        self.nonlinear_results.setTabText(self.nonlinear_results.indexOf(self.dfa), _translate("MainWindow", "Detrended Fluctuation Analysis"))
        self.nonlinear_results.setTabText(self.nonlinear_results.indexOf(self.nonlin_param), _translate("MainWindow", "Parameters"))
        self.results_tab.setTabText(self.results_tab.indexOf(self.nonlinear), _translate("MainWindow", "Nonlinear"))
        self.calculate.setText(_translate("MainWindow", "Calculate results"))
        self.export_2.setText(_translate("MainWindow", "Export"))
        self.builtin_box.setTitle(_translate("MainWindow", "Built-in filter"))
        self.filter_builtin.setText(_translate("MainWindow", "Filter"))
        self.calculateresults_box.setTitle(_translate("MainWindow", "Calculate results"))
        self.calculate.setText(_translate("MainWindow", "Calculate results"))
        self.results_whole.setText(_translate("MainWindow", "for whole signal"))
        self.results_part.setText(_translate("MainWindow", "for selected part"))
        self.view_tab.setTabText(self.view_tab.indexOf(self.signal_tab), _translate("MainWindow", "Signal"))
        self.view_tab.setTabText(self.view_tab.indexOf(self.tachogram_tab), _translate("MainWindow", "Tachogram"))
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

