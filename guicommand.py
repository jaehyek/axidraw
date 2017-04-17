# -*- coding: utf-8 -*-
__author__ = 'jaehyek.choi'

#test.py
try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 2
import pygubu
import ebb_motion
import time

"""
pip install pygubu 을 하고, 
C:\Python34\Scripts\pygubu-designer.exe 을 실행하여  gui을 생성한다.
"""

class Application:
    def __init__(self, master):

        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('AxiDraw.ui')

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('mainwindow', master)
        self.MsgPosition = builder.get_object('ID_MSG_POSITION', master)

        self.ebb = ebb_motion.EBB()
        self.ebb.sendEnableMotors(1)
        self.listpos = self.ebb.getStepPosition(False)
        self.listWidthHeight = [0,0]

        # define the distance of movement
        self.dist = 500
        self.config_penup = 16000
        self.config_pendown = 12000
        self.config_penrate = 750

        # read config file and set .
        try:
            fconf = open("Axidraw.conf")
            for line in fconf:
                key, values = line.strip().split("=")
                if len(key) == 0:
                    continue
                listvalues = values.split(",")
                if len(listvalues) >= 2 :
                    self.__dict__[key.strip()] = [int(aa) for aa in values.split(",")]
                else:
                    self.__dict__[key.strip()] = int(listvalues[0])
        except:
            pass

        self.configPenUpDown()
        self.builder.tkvariables['PenConfigup'].set(self.config_penup)
        self.builder.tkvariables['PenConfigdown'].set(self.config_pendown)

        self.builder.tkvariables['msg_WidthHeight'].set("(" + ",".join([str(aa) for aa in self.listWidthHeight ] ) + ")")



        #4. Connect callbacks
        callbacks = {
            'On_Click_Close':self.On_Click_Close,
            'On_Click_Save':self.On_Click_Save,
            'On_Click_Pen_Down':self.On_Click_Pen_Down,
            'On_Click_Pen_Up':self.On_Click_Pen_Up,

            'On_Click_BackLeft':self.On_Click_BackLeft,
            'On_Click_Back':self.On_Click_Back,
            'On_Click_BackRight':self.On_Click_BackRight,
            'On_Click_Left':self.On_Click_Left,

            'On_Click_Right':self.On_Click_Right,
            'On_Click_ForeLeft':self.On_Click_ForeLeft,
            'On_Click_Forward':self.On_Click_Forward,
            'On_Click_ForeRight':self.On_Click_ForeRight,

            'On_Click_Move_Origin': self.On_Click_Move_Origin,
            'On_Click_Move_Width': self.On_Click_Move_Width,
            'On_Click_Move_WidthHeight': self.On_Click_Move_WidthHeight,
            'On_Click_Move_Height': self.On_Click_Move_Height,

            'On_Click_Dist_20': self.On_Click_Dist_20,
            'On_Click_Dist_100': self.On_Click_Dist_100,
            'On_Click_Dist_500': self.On_Click_Dist_500,
            'On_Click_Dist_1000': self.On_Click_Dist_1000,

            'On_Click_Set_Origin': self.On_Click_Set_Origin,
            'On_Click_Set_WidthHeight': self.On_Click_Set_WidthHeight,
            'On_Click_Click': self.On_Click_Click


        }
        builder.connect_callbacks(callbacks)
        self.setMsgCurrentPosition()

    def configPenUpDown(self):
        self.ebb.configServo(4, self.config_pendown)
        self.ebb.configServo(5, self.config_penup)
        self.ebb.configServo(11, self.config_penrate)
        self.ebb.configServo(12, self.config_penrate)


    def setMsgCurrentPosition(self):
        self.listpos = self.ebb.getStepPosition(False)
        self.MsgPosition.config(text=",".join([str(aa) for aa in self.listpos]))


    def On_Click_Close(self):
        print("closing....")
        exit()

    def On_Click_Save(self):
        #self.listphoneRes = [int(aa) for aa in self.builder.tkvariables['strWidthHeight'].get().split(",") ]
        if len(self.listWidthHeight) == 2 :
            fout = open("Axidraw.conf", "w")
            fout.write("listAxiRes=" + ",".join([str(aa) for aa in self.listWidthHeight]) + "\n")
            fout.write("config_penup=%s\n" % self.config_penup)
            fout.write("config_pendown=%s\n" % self.config_pendown)
            fout.close()
            print("Saved...")
            return
        else:
            print("invalid listWidthHeight")

    def On_Click_Pen_Down(self):
        self.ebb.getReady()
        config_penup = self.builder.tkvariables['PenConfigup'].get()
        config_pendown = self.builder.tkvariables['PenConfigdown'].get()
        if config_penup != self.config_penup or config_pendown != self.config_pendown :
            self.config_penup = config_penup
            self.config_pendown = config_pendown
            self.configPenUpDown()
        self.ebb.sendPenDown()
        return

    def On_Click_Pen_Up(self):
        self.ebb.getReady()
        config_penup = self.builder.tkvariables['PenConfigup'].get()
        config_pendown = self.builder.tkvariables['PenConfigdown'].get()
        if config_penup != self.config_penup or config_pendown != self.config_pendown :
            self.config_penup = config_penup
            self.config_pendown = config_pendown
            self.configPenUpDown()

        self.ebb.sendPenUp()
        return

    def On_Click_BackLeft(self):
        self.ebb.doABMove(-self.dist, -self.dist)
        self.setMsgCurrentPosition()
        return

    def On_Click_Back(self):
        self.ebb.doABMove(0, -self.dist)
        self.setMsgCurrentPosition()
        return

    def On_Click_BackRight(self):
        self.ebb.doABMove(self.dist, -self.dist)
        self.setMsgCurrentPosition()
        return

    def On_Click_Left(self):
        self.ebb.doABMove(-self.dist, 0)
        self.setMsgCurrentPosition()
        return

    def On_Click_Right(self):
        self.ebb.doABMove(self.dist, 0 )
        self.setMsgCurrentPosition()
        return

    def On_Click_ForeLeft(self):
        self.ebb.doABMove(-self.dist, self.dist)
        self.setMsgCurrentPosition()
        return

    def On_Click_Forward(self):
        self.ebb.doABMove(0, self.dist)
        self.setMsgCurrentPosition()
        return

    def On_Click_ForeRight(self):
        self.ebb.doABMove(self.dist, self.dist)
        self.setMsgCurrentPosition()
        return

    def On_Click_Dist_20(self):
        self.dist = 20
        return

    def On_Click_Dist_100(self):
        self.dist = 100
        return

    def On_Click_Dist_500(self):
        self.dist = 500
        return

    def On_Click_Dist_1000(self):
        self.dist = 1000
        return

    def MoveABSCoordinate(self, x, y):
        relatedX = x - self.listpos[0]
        relatedY = y - self.listpos[1]
        self.ebb.doABMove(relatedX, relatedY)
        self.setMsgCurrentPosition()

    def On_Click_Move_Origin(self):
        self.MoveABSCoordinate(0,0)

    def On_Click_Move_Width(self):
        self.MoveABSCoordinate(self.listWidthHeight[0], 0)

    def On_Click_Move_WidthHeight(self):
        self.MoveABSCoordinate(self.listWidthHeight[0], self.listWidthHeight[1])

    def On_Click_Move_Height(self):
        self.MoveABSCoordinate(0, self.listWidthHeight[1])

    def On_Click_Set_Origin(self):
        self.ebb.getReset()
        self.config_penup = self.builder.tkvariables['PenConfigup'].get()
        self.config_pendown = self.builder.tkvariables['PenConfigdown'].get()
        self.configPenUpDown()
        self.setMsgCurrentPosition()
        return

    def On_Click_Set_WidthHeight(self):
        self.listWidthHeight = self.ebb.getStepPosition(False)
        self.builder.tkvariables['msg_WidthHeight'].set( ",".join([str(aa) for aa in self.listWidthHeight]) )
        return

    def On_Click_Click(self):
        self.On_Click_Pen_Up()
        self.On_Click_Pen_Down()
        time.sleep(0.2)
        self.On_Click_Pen_Up()





if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()