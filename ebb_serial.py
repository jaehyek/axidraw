# ebb_serial.py
# Serial connection utilities for EiBotBoard
# https://github.com/evil-mad/plotink
# 
# Intended to provide some common interfaces that can be used by 
# EggBot, WaterColorBot, AxiDraw, and similar machines.
#
# Version 0.5, Dated March 7, 2017.
#
# Thanks to Shel Michaels for bug fixes and helpful suggestions. 
#
# The MIT License (MIT)
# 
# Copyright (c) 2017 Evil Mad Scientist Laboratories
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import print_function

# 다음을 실행하기 전에  >pip install pyserial 을 수행할 것.
import serial

def version():
    return "0.5"    # Version number for this document

def findPort():    
    #Find a single EiBotBoard connected to a USB port.
    try:
        from serial.tools.list_ports import comports
    except ImportError:
        comports = None        
        return None
    if comports:
        comPortsList = list(comports())
        EBBport = None
        for port in comPortsList:
            if port[1].startswith("EiBotBoard"):
                EBBport = port[0]     #Success; EBB found by name match.
                break    #stop searching-- we are done.
        if EBBport is None:
            for port in comPortsList:
                if port[2].startswith("USB VID:PID=04D8:FD92"):
                    EBBport = port[0] #Success; EBB found by VID/PID match.
                    break    #stop searching-- we are done.                
        return EBBport

def testPort( comPort ):
    '''
    Return a SerialPort object
    for the first port with an EBB (EiBotBoard; EggBot controller board).
    YOU are responsible for closing this serial port!
    '''        
    if comPort is not None:
        try:
            serialPort = serial.Serial( comPort, timeout=1.0 ) # 1 second timeout!
            serialPort.write( 'v\r'.encode('ascii') )
            strVersion = serialPort.readline()            
            if strVersion and strVersion.startswith( "EBB".encode('ascii') ):
                return serialPort
                            
            serialPort.write( 'v\r'.encode('ascii') ) 
            strVersion = serialPort.readline()
            if strVersion and strVersion.startswith( "EBB".encode('ascii') ):
                return serialPort                    
            serialPort.close()
        except serial.SerialException:
            pass
        return None
    else:
        return None

def openPort():
    foundPort = findPort()
    serialPort = testPort( foundPort )
    if serialPort:
        return serialPort
    return None

def closePort(comPort):
    if comPort is not None:
        try:
            comPort.close()
        except serial.SerialException:
            pass

def query( comPort, cmd ):
    if (comPort is not None) and (cmd is not None):
        try:
            # comPort.flush()
            comPort.write( cmd.encode('ascii')  )
            return comPort.readline().decode('ascii').strip()
        except:
            print( "Error reading serial data." )
        return None
    else:
        return None

def command( comPort, cmd ):
    if (comPort is not None) and (cmd is not None):
        try:
            comPort.write( cmd.encode('ascii') )
            nRetryCount = 0
            response = ""
            while ( len(response) == 0 ) and ( nRetryCount < 100 ):
                response = comPort.readline().decode('ascii').strip()
                if response.startswith("OK"):
                    return
                else:
                    # print (response)
                    pass
                # get new response to replace null response if necessary
                nRetryCount += 1
                response = ""

            if ( response != '' ):
                print( 'Error: Unexpected response from EBB.')
                print( '   Command: ' + cmd.strip() )
                print( '   Response: ' + str( response.strip() ) )
            else:
                print( 'EBB Serial Timeout after command: ' + cmd )

        except:
            print( 'Failed after command: ' + cmd )        
            pass 

def bootload( comPort ):
    # Enter bootloader mode. Do not try to read back data.
    if (comPort is not None):
        try:
            comPort.write( 'BL\r'.encode('ascii') )
        except:
            print( 'Failed while trying to enter bootloader.' )
            pass 
