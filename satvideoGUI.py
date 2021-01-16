from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import videoMaker
import sys
import os




## Contains all of the widgets for the GUI   
class Window(QMainWindow):
    
    ## All of the button actions are functions
    ## Initializing the window
    def __init__(self):
        super(Window, self).__init__()
        sizeObject = QDesktopWidget().screenGeometry(-1)
        global screenWidth
        screenWidth = sizeObject.width()
        global screenHeight
        screenHeight = sizeObject.height()
        global bw1
        bw1 = int(screenWidth/15)
        global bw2
        bw2 = int(screenWidth/50)
        global bh1
        bh1 = int(screenHeight/15)
        global bh2
        bh2 = int(screenHeight/20)
        self.setGeometry(50, 50, 10 + int(screenWidth/2), 10 + int(screenHeight/2))
        self.setWindowTitle("Satellite Timelapse GUI")
        self.home()



    def makeVideoButton(self, sitename, dates, polygonStuff, satChecks, vidType, rate):
        polygon = []
        for point in polygonStuff:
            print(point)
            long = float(point[0])
            lat = float(point[1])
            polygon.append([long,lat])
        satList = []
        if satChecks[0].isChecked() == True:
            satList.append('S2')
        if satChecks[1].isChecked() == True:
            satList.append('L5')
        if satChecks[2].isChecked() == True:
            satList.append('L7')
        if satChecks[3].isChecked() == True:
            satList.append('L8')
            
        videoMaker.main(polygon, dates, satList, sitename, vidType, rate)
        
    def home(self):

        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QGridLayout()             # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.widget.setLayout(self.vbox)
        
        timelapse = QPushButton('Make Timelapse')
        self.vbox.addWidget(timelapse, 1, 0)

        nameLabel = QLabel('Name')
        name = QLineEdit()
        self.vbox.addWidget(nameLabel, 1,1)
        self.vbox.addWidget(name,2,1)
        
        beginDateLabel = QLabel('Beginning Date (YYYY-MM-DD)')
        beginDate  = QLineEdit()
        self.vbox.addWidget(beginDateLabel,3,1)
        self.vbox.addWidget(beginDate,4,1)

        endDateLabel = QLabel('End Date (YYYY-MM-DD)')
        endDate = QLineEdit()
        self.vbox.addWidget(endDateLabel,3,2)
        self.vbox.addWidget(endDate,4,2)

        longLabel = QLabel('Longitudes')
        latLabel = QLabel('Latitudes')
        self.vbox.addWidget(longLabel,6,1)
        self.vbox.addWidget(latLabel,7,1)

        topLeftLabel = QLabel('Coordinate 1 (decimal degrees)')
        topLeftLong = QLineEdit()
        topLeftLat = QLineEdit()
        self.vbox.addWidget(topLeftLabel, 5, 2)
        self.vbox.addWidget(topLeftLong,6,2)
        self.vbox.addWidget(topLeftLat,7,2)

        topRightLabel = QLabel('Coordinate 2, (decimal degrees)')
        topRightLong = QLineEdit()
        topRightLat = QLineEdit()
        self.vbox.addWidget(topRightLabel, 5, 3)
        self.vbox.addWidget(topRightLong, 6, 3)
        self.vbox.addWidget(topRightLat, 7, 3)

        botLeftLabel = QLabel('Coordinate 3 (decimal degrees)')
        botLeftLong = QLineEdit()
        botLeftLat = QLineEdit()
        self.vbox.addWidget(botLeftLabel, 5, 4)
        self.vbox.addWidget(botLeftLong, 6, 4)
        self.vbox.addWidget(botLeftLat, 7, 4)

        botRightLabel = QLabel('Coordinate 4 (decimal degrees)')
        botRightLong = QLineEdit()
        botRightLat = QLineEdit()
        self.vbox.addWidget(botRightLabel, 5, 5)
        self.vbox.addWidget(botRightLong, 6, 5)
        self.vbox.addWidget(botRightLat, 7, 5)

        vidType = QComboBox()
        types = ['RGB', 'NDVI_NDWI']
        for t in types:
            vidType.addItem(t)
        self.vbox.addWidget(vidType,8,1)

        s2checkLabel = QLabel('Sentinel 2')
        s2check = QCheckBox()
        self.vbox.addWidget(s2checkLabel, 9,1)
        self.vbox.addWidget(s2check,10,1)

        L5checkLabel = QLabel('Landsat 5')
        L5check = QCheckBox()
        self.vbox.addWidget(L5checkLabel, 9,2)
        self.vbox.addWidget(L5check,10,2)

        L7checkLabel = QLabel('Landsat 7')
        L7check = QCheckBox()
        self.vbox.addWidget(L7checkLabel, 9,3)
        self.vbox.addWidget(L7check,10,3)

        L8checkLabel = QLabel('Landsat 8')
        L8check = QCheckBox()
        self.vbox.addWidget(L8checkLabel, 9,4)
        self.vbox.addWidget(L8check,10,4)

        frameRateLabel = QLabel('Frames per second')
        frameRate = QSpinBox()
        frameRate.setMinimum(2)
        frameRate.setMaximum(10)
        frameRate.setValue(4)
        self.vbox.addWidget(frameRateLabel,11,1)
        self.vbox.addWidget(frameRate,12,1)


        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(False)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        polygonStuff = [[topRightLong.text(), topRightLat.text()],
                        [topLeftLong.text(), topLeftLat.text()],
                        [botRightLong.text(), botRightLat.text()],
                        [botLeftLong.text(), botLeftLat.text()],
                        [topRightLong.text(),topRightLat.text()]
                        ]
        
        dates = [beginDate.text(), endDate.text()]
        checkboxes = [s2check, L5check, L7check, L8check]

        ##action
        timelapse.clicked.connect(lambda: self.makeVideoButton(name.text(),
                                                               [beginDate.text(), endDate.text()],
                                                               [[topRightLong.text(), topRightLat.text()],
                                                               [topLeftLong.text(), topLeftLat.text()],
                                                               [botRightLong.text(), botRightLat.text()],
                                                               [botLeftLong.text(), botLeftLat.text()],
                                                               [topRightLong.text(),topRightLat.text()]
                                                               ], checkboxes, str(vidType.currentText()),
                                                               frameRate.value()))
        

                
## Function outside of the class to run the app   
def run():
    app = QApplication(sys.argv)
    GUI = Window()
    GUI.show()
    sys.exit(app.exec_())

## Calling run to run the app
run()
