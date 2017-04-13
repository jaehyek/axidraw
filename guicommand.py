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
            fout.close()
            print("Saved...")
            return
        else:
            print("invalid listWidthHeight")

    def On_Click_Pen_Down(self):
        self.ebb.getReady()
        self.ebb.sendPenDown()
        return

    def On_Click_Pen_Up(self):
        self.ebb.getReady()
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

    def On_Click_Set_Origin(self):
        self.ebb.getReset()
        self.setMsgCurrentPosition()
        return

    def On_Click_Set_WidthHeight(self):
        self.listWidthHeight = self.ebb.getStepPosition(False)
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