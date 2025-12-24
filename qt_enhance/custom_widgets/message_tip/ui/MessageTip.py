# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MessageTip.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QWidget)
import image_rc

class Ui_MessageTip(object):
    def setupUi(self, MessageTip):
        if not MessageTip.objectName():
            MessageTip.setObjectName(u"MessageTip")
        MessageTip.resize(291, 62)
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font.setPointSize(10)
        MessageTip.setFont(font)
        self.horizontalLayout = QHBoxLayout(MessageTip)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(MessageTip)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"background-color: rgb(170, 255, 127);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/png/images/ok.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(50, 0))
        self.label.setMaximumSize(QSize(400, 16777215))
        self.label.setFont(font)
        self.label.setStyleSheet(u"color: rgb(0, 170, 0);\n"
"color: rgb(0, 116, 0);")
        self.label.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.label)


        self.horizontalLayout.addWidget(self.frame)


        self.retranslateUi(MessageTip)

        QMetaObject.connectSlotsByName(MessageTip)
    # setupUi

    def retranslateUi(self, MessageTip):
        MessageTip.setWindowTitle(QCoreApplication.translate("MessageTip", u"Form", None))
        self.pushButton.setText("")
        self.label.setText(QCoreApplication.translate("MessageTip", u"TextLabel", None))
    # retranslateUi

