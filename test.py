# -*- coding: utf-8 -*-
__author__ = 'jaehyek.choi'

"""
purpose :

"""

"""
from __future__ import division
"""

import ebb_motion
import time

dist = 6400

def main():

    ebb = ebb_motion.EBB()
    ebb.sendEnableMotors(1)

    #for i in range(10) :
    #    ebb.sendPenUp( )
    #    ebb.sendPenDown()


    # # ebb.getReset()
    #
    # for i in range(10 ) :
    #     # print( ebb.getStepPosition(False))
    #     ebb.doABMove(dist, 0)
    #     # print( ebb.getStepPosition(False))
    #     ebb.doABMove(0, dist)
    #     # print( ebb.getStepPosition(False))
    #     ebb.doABMove(-dist, 0)
    #     # print( ebb.getStepPosition(False))
    #     ebb.doABMove( 0, -dist)
    #     # print( ebb.getStepPosition(False))


    ebb.sendPenDown()
    ebb.sendDisableMotors()

    del ebb



if __name__ == "__main__":
    main()