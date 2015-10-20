#UTF-8
import time
import threading
import random

class CTemperature():
    STATE_IDLE = 'idle'
    STATE_INIT = 'init'
    STATE_READ = 'read'
    STATE_STOP = 'stop'

    _stateDescriptor = {
        STATE_IDLE: "Idle",
        STATE_INIT: "Initializing",
        STATE_READ: "reading",
        STATE_STOP: "Stopping",
        }
    """Descrizioni delle fasi di secuzione."""

    def __init__(self):
        self._state = CTemperature.STATE_IDLE
        self._mainThread = None
        self._stop = False
        self._temperature = 0.0

    def GetState(self):
        return self._state

    def GetTemperature(self):
        return self._temperature

    def Start(self):
        self._stop = False
        
        if (self._state == CTemperature.STATE_IDLE):
            # Lancia il processo di lettura
            self._mainThread = threading.Thread(target=self.Main)
            self._mainThread.start()
        else:
            # Invio ai vari processi un comando per reinizializzarsi
            pass

    def Stop(self):
        if (self._state == CTemperature.STATE_IDLE):
            # Nulla da fare, e' gia' tutto fermo
            pass
        else:
            startTime = time.clock()
            self._stop = True
            while self._state != CTemperature.STATE_STOP:
                time.sleep(0.1)
                if ((time.clock() - startTime) > 5.0):
                    break

    def Main(self):
        """
Processo per la lettura della temperatura


"""
        print("Starting Temperature Daemon...")
        continueLoop = True
        while continueLoop:
            print(self._stateDescriptor[self._state])
            
            if self._state == CTemperature.STATE_IDLE:
                self._state = CTemperature.STATE_INIT
                
            elif self._state == CTemperature.STATE_INIT:
                self._state = CTemperature.STATE_READ
                
            elif self._state == CTemperature.STATE_READ:
                if self._stop:
                    self._state = CTemperature.STATE_STOP
                else:
                    self._temperature = random.random() * 100.0
                
            elif self._state == CTemperature.STATE_STOP:
                continueLoop = False
            else:
                print("Error stato non valido '%s'" % (self._state))
            
            time.sleep(1)

        print("Stopping Temperature Daemon...")


if __name__ == "__main__":
    PT100 = CTemperature()
    PT100.Start()

    for i in range(100):
        if(PT100.GetState() == CTemperature.STATE_READ):
            print('Temperature: %0.1f' % (PT100.GetTemperature()))
        time.sleep(0.1)
        
    PT100.Stop()

