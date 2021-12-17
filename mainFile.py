##D# !F:\konda\python -m PyQt5.uic.pyuic -x F:\konda\envs\kub\lib\site-packages\pyqt5_tools\pogoda_prevac.ui -o pogodaApp.py
#!F:\konda\python -m PyQt5.uic.pyuic -x F:\konda\envs\kub\lib\site-packages\pyqt5_tools\wykres.ui -o wykresOkno.py

import requests
from datetime import date, datetime
from PyQt5.QtGui import QPixmap
import matplotlib.pyplot as plt
import multiprocessing as mp
import os, time
from PyQt5 import QtCore, QtGui, QtWidgets

import mySQLite


#global constant
apiID = "7ae9552d9d627023a75e5ea18da1efa0"

#########################

def getForecastFromSite( whatYouNeed = None ):
    response = requests.get( "http://api.openweathermap.org/data/2.5/forecast?lat=35.88&lon=76.51&APPID={}&units=metric".format(apiID) )
    data = response.json()["list"]
    result = []
    resultDate = []
    if whatYouNeed == 'temp':
        for weather in data:
            result.append( weather["main"]["temp"] )
    elif whatYouNeed == 'humidity':
        for weather in data:
            result.append( weather["main"]["humidity"] )
    elif whatYouNeed == 'pressure':
        for weather in data:
            result.append( weather["main"]["pressure"] )
    elif whatYouNeed == 'feels_like':
        for weather in data:
            result.append( weather["main"]["feels_like"] )
    elif whatYouNeed == 'wind':
        for weather in data:
            result.append( weather["wind"]["speed"] )
    elif whatYouNeed == 'main':
        for weather in data:
            result.append( weather["weather"][0]["main"] )
    for weather in data:
        resultDate.append( weather[ "dt_txt" ][5:-6] )
    #print(data[0])
    return result, resultDate

def getDataFromSite():
    try:
        response = requests.get( "http://api.openweathermap.org/data/2.5/weather?lat=35.88&lon=76.51&APPID={}&units=metric".format(apiID) )
    except requests.exceptions.ConnectionError: #no internet error (popular in the wild :P)
        #print(e)
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle( "ConnectionError " )
        msg.setStandardButtons( QtWidgets.QMessageBox.Ok )
        msg.setInformativeText( 'No internet Connection' )
        msg.exec_()
        return
    data = response.json()
    main = data[ "main" ] 
    print( data )
    ret = [ data["weather"][0]["main"], main["temp"],main["feels_like"], main["pressure"], data["wind"]["speed"], main["humidity"] ]
    return ret 



class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(553, 413)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(400, 0, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.spinBoxX = QtWidgets.QSpinBox(Dialog)
        self.spinBoxX.setGeometry(QtCore.QRect(160, 0, 42, 22))
        self.spinBoxX.setMinimum(200)
        self.spinBoxX.setMaximum(1000)
        self.spinBoxX.setSingleStep(50)
        self.spinBoxX.setProperty("value", 400)
        self.spinBoxX.setObjectName("spinBoxX")
        self.wykres = QtWidgets.QLabel(Dialog)
        self.wykres.setGeometry(QtCore.QRect(30, 60, 501, 301))
        self.wykres.setObjectName("wykres")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("WeatherApp", "Powiększ"))
        self.wykres.setText(_translate("Dialog", "TextLabel"))
        #self.label_2.setText(_translate("Dialog", "Wykres pięciodniowy"))
        self.pushButton.clicked.connect( self.render )
        ################
        Dialog.setWindowTitle("Prognoza 5-dniowa")

    def render( self ):
        X = self.spinBoxX.value() 
        #Y = self.spinBoxY.value() 
        self.program.doPlot( self.wykres, X )
        self.wykres.setGeometry( 10, 30, X, int(X*0.75) )


class Ui_WeatherApp(object):
    def setupUi(self, WeatherApp):
        WeatherApp.setObjectName("WeatherApp")
        WeatherApp.resize(793, 400)
        WeatherApp.setMinimumSize(QtCore.QSize(350, 400))
        self.centralwidget = QtWidgets.QWidget(WeatherApp)
        self.centralwidget.setObjectName("centralwidget")
        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setGeometry(QtCore.QRect(110, 270, 161, 51))
        self.refreshButton.setObjectName("refreshButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(56, 30, 131, 20))
        self.label.setObjectName("label")
        self.dateRefresh = QtWidgets.QLineEdit(self.centralwidget)
        self.dateRefresh.setGeometry(QtCore.QRect(200, 30, 113, 20))
        self.dateRefresh.setObjectName("dateRefresh")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(60, 70, 261, 170))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.formLayout = QtWidgets.QFormLayout(self.frame)
        self.formLayout.setObjectName("formLayout")
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.weatherLine = QtWidgets.QLineEdit(self.frame)
        self.weatherLine.setObjectName("weatherLine")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.weatherLine)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.temperatureLine = QtWidgets.QLineEdit(self.frame)
        self.temperatureLine.setObjectName("temperatureLine")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.temperatureLine)
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.tempFeelsLine = QtWidgets.QLineEdit(self.frame)
        self.tempFeelsLine.setObjectName("tempFeelsLine")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.tempFeelsLine)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.pessureLine = QtWidgets.QLineEdit(self.frame)
        self.pessureLine.setObjectName("pessureLine")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.pessureLine)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.windSpeedLine = QtWidgets.QLineEdit(self.frame)
        self.windSpeedLine.setObjectName("windSpeedLine")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.windSpeedLine)
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.humidityLine = QtWidgets.QLineEdit(self.frame)
        self.humidityLine.setObjectName("humidityLine")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.humidityLine)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(60, 100, 160, 20))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.wykresLabel = QtWidgets.QLabel(self.centralwidget)
        self.wykresLabel.setGeometry(QtCore.QRect(390, 80, 311, 241))
        self.wykresLabel.setText("")
        self.wykresLabel.setObjectName("wykresLabel")
        self.radioTemp = QtWidgets.QRadioButton(self.centralwidget)
        self.radioTemp.setGeometry(QtCore.QRect(360, 0, 101, 20))
        self.radioTemp.setChecked(True)
        self.radioTemp.setObjectName("radioTemp")
        self.radioPress = QtWidgets.QRadioButton(self.centralwidget)
        self.radioPress.setGeometry(QtCore.QRect(470, 0, 81, 20))
        self.radioPress.setObjectName("radioPress")
        self.radioSpeed = QtWidgets.QRadioButton(self.centralwidget)
        self.radioSpeed.setGeometry(QtCore.QRect(550, 0, 121, 20))
        self.radioSpeed.setObjectName("radioSpeed")
        self.radioHuminity = QtWidgets.QRadioButton(self.centralwidget)
        self.radioHuminity.setGeometry(QtCore.QRect(670, 0, 95, 20))
        self.radioHuminity.setObjectName("radioHuminity")
        self.zoomButton = QtWidgets.QPushButton(self.centralwidget)
        self.zoomButton.setGeometry(QtCore.QRect(470, 30, 161, 31))
        self.zoomButton.setCheckable(True)
        self.zoomButton.setChecked(False)
        self.zoomButton.setObjectName("zoomButton")
        WeatherApp.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(WeatherApp)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 793, 26))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuWy_wietl_historyczne_dane = QtWidgets.QMenu(self.menuMenu)
        self.menuWy_wietl_historyczne_dane.setObjectName("menuWy_wietl_historyczne_dane")
        self.menuWsp_rz_dne_2 = QtWidgets.QMenu(self.menuMenu)
        self.menuWsp_rz_dne_2.setObjectName("menuWsp_rz_dne_2")
        WeatherApp.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(WeatherApp)
        self.statusbar.setObjectName("statusbar")
        WeatherApp.setStatusBar(self.statusbar)
        self.actionMinumum = QtWidgets.QAction(WeatherApp)
        self.actionMinumum.setObjectName("actionMinumum")
        self.actionMaksimum = QtWidgets.QAction(WeatherApp)
        self.actionMaksimum.setObjectName("actionMaksimum")
        self.actionSrednia = QtWidgets.QAction(WeatherApp)
        self.actionSrednia.setObjectName("actionSrednia")
        self.action35_88 = QtWidgets.QAction(WeatherApp)
        self.action35_88.setObjectName("action35_88")
        self.action36 = QtWidgets.QAction(WeatherApp)
        self.action36.setObjectName("action36")
        self.Xcoord = QtWidgets.QAction(WeatherApp)
        self.Xcoord.setObjectName("Xcoord")
        self.Ycoord = QtWidgets.QAction(WeatherApp)
        self.Ycoord.setObjectName("Ycoord")
        self.actionExit = QtWidgets.QAction(WeatherApp)
        self.actionExit.setObjectName("actionExit")
        self.actionPomoc = QtWidgets.QAction(WeatherApp)
        self.actionPomoc.setObjectName("actionPomoc")
        self.menuWy_wietl_historyczne_dane.addAction(self.actionMinumum)
        self.menuWy_wietl_historyczne_dane.addAction(self.actionMaksimum)
        self.menuWy_wietl_historyczne_dane.addAction(self.actionSrednia)
        self.menuWsp_rz_dne_2.addAction(self.Xcoord)
        self.menuWsp_rz_dne_2.addAction(self.Ycoord)
        self.menuMenu.addAction(self.menuWy_wietl_historyczne_dane.menuAction())
        self.menuMenu.addAction(self.menuWsp_rz_dne_2.menuAction())
        self.menuMenu.addAction(self.actionPomoc)
        self.menuMenu.addAction(self.actionExit)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(WeatherApp)
        QtCore.QMetaObject.connectSlotsByName(WeatherApp)

    def retranslateUi(self, WeatherApp):
        _translate = QtCore.QCoreApplication.translate
        WeatherApp.setWindowTitle(_translate("WeatherApp", "MainWindow"))
        self.refreshButton.setText(_translate("WeatherApp", "ODŚWIEŻ"))
        self.label.setText(_translate("WeatherApp", "Ostatni raz odświeżono: "))
        self.dateRefresh.setText(_translate("WeatherApp", "1.1.2020, 21.37"))
        self.label_9.setText(_translate("WeatherApp", "Pogoda"))
        self.weatherLine.setText(_translate("WeatherApp", "Pochmurnie"))
        self.label_2.setText(_translate("WeatherApp", "Temperatura"))
        self.temperatureLine.setText(_translate("WeatherApp", "2 st. C."))
        self.label_8.setText(_translate("WeatherApp", "Temp. odczuwalna"))
        self.tempFeelsLine.setText(_translate("WeatherApp", "2 st. C."))
        self.label_3.setText(_translate("WeatherApp", "Ciśnienie"))
        self.pessureLine.setText(_translate("WeatherApp", "1013,25 hPa"))
        self.label_4.setText(_translate("WeatherApp", "Prędkość wiatru"))
        self.windSpeedLine.setText(_translate("WeatherApp", "8 m/s"))
        self.label_6.setText(_translate("WeatherApp", "Wilgotność powietrza"))
        self.humidityLine.setText(_translate("WeatherApp", "68%"))
        self.radioTemp.setText(_translate("WeatherApp", "Temperatura"))
        self.radioPress.setText(_translate("WeatherApp", "Ciśnienie"))
        self.radioSpeed.setText(_translate("WeatherApp", "Prędkość wiatru"))
        self.radioHuminity.setText(_translate("WeatherApp", "Wilgotność"))
        self.zoomButton.setText(_translate("WeatherApp", "Powiększ"))
        self.menuMenu.setTitle(_translate("WeatherApp", "Menu"))
        self.menuWy_wietl_historyczne_dane.setTitle(_translate("WeatherApp", "Wyświetl historyczą temperaturę"))
        self.menuWsp_rz_dne_2.setTitle(_translate("WeatherApp", "Współrzędne"))
        self.actionMinumum.setText(_translate("WeatherApp", "Minumum"))
        self.actionMaksimum.setText(_translate("WeatherApp", "Maksimum"))
        self.actionSrednia.setText(_translate("WeatherApp", "Średnia"))
        self.action35_88.setText(_translate("WeatherApp", "35.88"))
        self.action36.setText(_translate("WeatherApp", "76.51"))
        self.Xcoord.setText(_translate("WeatherApp", "X:35.88"))
        self.Ycoord.setText(_translate("WeatherApp", "Y:76.51"))
        self.actionExit.setText(_translate("WeatherApp", "Wyjście"))
        self.actionPomoc.setText(_translate("WeatherApp", "Pomoc"))



        ##################
        self.init( WeatherApp )

    def refreshAll( self ):
        Now = datetime.now().strftime("%Y-%m-%d %H:%M")
        data = getDataFromSite()
        if data:
            self.dateRefresh.setText( Now )
            self.weatherLine.setText( data[0] )
            self.temperatureLine.setText( str( data[1] ) + "st. C" )
            self.tempFeelsLine.setText( str( data[2] ) + "st. C" )
            self.pessureLine.setText( str( data[3] ) + "hPa")
            self.windSpeedLine.setText( str( data[4] ) + "m/s")
            self.humidityLine.setText( str( data[5] ) + "%" )
            dataToSave = [ Now, data[0], data[1], data[2], data[3], data[4], data[5]]
            self.DB.pushWeather( dataToSave )

            self.doPlot()

    def doPlot( self, labelPlot = None, resize = 400 ):
        if self.radioTemp.isChecked():
            forecastWeather = getForecastFromSite("temp")
        elif self.radioPress.isChecked():
            forecastWeather = getForecastFromSite("pressure")
        elif self.radioSpeed.isChecked():
            forecastWeather = getForecastFromSite("wind")
        elif self.radioHuminity.isChecked():
            forecastWeather = getForecastFromSite("humidity")
        #elif self.radioFeels.isChecked():
            #forecastWeather = getForecastFromSite("feels_like")
        if labelPlot == None:
            labelPlot = self.wykresLabel

        plik = 'wykres.png'
        output_values, input_values = forecastWeather
        plt.plot(input_values, output_values)
        plt.savefig(plik)

        wykres_png = QPixmap(plik)
        pixmap_resized = wykres_png.scaled( resize, int( resize * 3/4. ))

        #os.remove(plik)
        plt.clf()

        labelPlot.setPixmap(pixmap_resized)
        labelPlot.resize( resize, int( resize * 3/4. ) )     

    def getMinimumFromDB( self ):
        sql = self.DB.getMinimum()[ 0 ]
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle( "Minimum " )
        msg.setStandardButtons( QtWidgets.QMessageBox.Ok )
        msg.setInformativeText( 'Minimalna zarejestrowana temperatura to: ' + str( sql[0] ) + "C" )
        msg.exec_()

    def getMaximumFromDB( self ):
        sql = self.DB.getMaximum()[ 0 ]
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle( "Maksimum " )
        msg.setStandardButtons( QtWidgets.QMessageBox.Ok )
        msg.setInformativeText( 'Maksymalna zarejestrowana temperatura to: ' + str( sql[0] ) + "C" )
        msg.exec_()

    def getAvgFromDB( self ):
        sql = self.DB.getAvg()[ 0 ]
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle( "Średnia " )
        msg.setStandardButtons( QtWidgets.QMessageBox.Ok )
        msg.setInformativeText( 'Średnia zarejestrowana temperatura to: ' + str( round( sql[0], 2 ) ) + "C" )
        msg.exec_()

    def init(self, WeatherApp):
        self.WeatherApp = WeatherApp
        self.WeatherApp.setWindowTitle( 'Aktualna Pogoda' )
        self.refreshButton.clicked.connect( self.refreshAll )
        #WeatherApp.setFixedSize(800, 413)
        self.apiID = "7ae9552d9d627023a75e5ea18da1efa0" #zaszyte moje ID
        self.DB = mySQLite.database( "weather_data_base" ) #zaszyta prywatna nazwa bazy
        self.actionMinumum.triggered.connect( self.getMinimumFromDB )
        self.actionMaksimum.triggered.connect( self.getMaximumFromDB )
        self.actionSrednia.triggered.connect( self.getAvgFromDB )
        self.zoomButton.clicked.connect( self.zoomPlot )
        self.timer = QtCore.QTimer( WeatherApp )
        self.timer.timeout.connect( self.refreshAll )
        minutesRefresh = 5 #interval refresh
        self.timer.start(1000 * 60 * minutesRefresh)
        self.bigPlot = Ui_Dialog()
        self.Dialog = QtWidgets.QDialog()
        self.bigPlot.setupUi( self.Dialog )
        self.bigPlot.program = self
        self.actionExit.triggered.connect( self.leave )
        self.actionPomoc.triggered.connect( self.help )
        self.refreshAll()

    def leave( self ):
        sys.exit()

    def zoomPlot( self ):
        print('rendering1')
        self.bigPlot.render()
        self.Dialog.show()

    def help( self ):

        helpStr = """Dane są automatycznie pobierane co 5 minut. Przycisk 'Odśwież' pozwala ręcznie zaktualizować dane. \
Na wykresie może znajdować się tylko jeden typ danych (wymienionych nad wykresem) na raz. Po zmianie typu danych należy zaktualizować wykres przyciskiem 'Odśwież'.
W rozwijanym menu można podejrzeć współrzędne punktu pobierania danych meteorologicznych, oraz sprawdzić zapisane przez program odczyty tymperatury.
"""
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle( "Pomoc " )
        msg.setStandardButtons( QtWidgets.QMessageBox.Ok )
        msg.setInformativeText( helpStr )
        msg.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WeatherApp = QtWidgets.QMainWindow()
    ui = Ui_WeatherApp()
    ui.setupUi(WeatherApp)
    WeatherApp.show()
    exitApp = app.exec_()
    sys.exit()
