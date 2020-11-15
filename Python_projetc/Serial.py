#coding: utf-8
import sys
import glob
import serial
import time
import threading

class Serial_Handle():
    def __init__(self):
        super(Serial_Handle,self).__init__()
        self.s=serial.Serial
        self.COM_Port=""
    
    def serial_init(self):
        try:
            self.s=serial.Serial(self.COM_Port)
            self.s.timeout=5
            self.s.write_timeout=5
            self.s.baudrate=115200
            
            return True
        except:
            return False
        
    def serial_close(self):
        try:
            self.s.close()
            time.sleep(2)       # DELAY
            return True
        except:
            return False
    
    def read_from_serial(self):
        answer=""
        try:
            answer=self.s.readline().decode('utf-8').rstrip("\n\r")
            #print(answer)       # DEBUG
        except:
            print("Mensagem nao veio codificada em ASCII")
        return answer
    
    
    
