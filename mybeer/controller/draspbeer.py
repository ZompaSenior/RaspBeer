# -*- coding: utf-8 -*-

import time
import threading
import platform

localPlatform = platform.platform()

if('arm' in localPlatform): 
    print('Sistema: ARM')
    import RPi.GPIO as GPIO
else:
    print('Sistema: non ARM')
    from RPi_placeholder import GPIO


from ctemperature import CTemperature

class CBeerCocker():
    STATE_NONE = 'none'
    STATE_IDLE = 'idle'
    STATE_INIT = 'init'
    STATE_WAIT = 'wait'
    STATE_COCK = 'cock'
    STATE_BOIL = 'boil'
    STATE_STOP = 'stop'
    
    PIN_MIXER = 17
    PIN_HEATER = 27
    
    SWITCH_TIME = 2.0

    _stateDescriptor = {
        STATE_IDLE: "Idle",
        STATE_INIT: "Initializing",
        STATE_WAIT: "Waiting",
        STATE_COCK: "Cocking",
        STATE_BOIL: "Boiling",
        STATE_STOP: "Stopping",
        }
    """Descrizioni delle fasi di esecuzione."""
    
    _mainThread = None
    _pt100 = None
    _recipe = None
    _state = STATE_IDLE
    _stateForce = STATE_NONE 

    _stopCocking = False
    _stopBoiling = False
    
    _configureIO = False
    _switchTime = 0.0
    
    _mixerState = False
    _heaterState = False

    def __init__(self):
        # Configuro gli io che mi servono se non l'ho già fatto
        if(not CBeerCocker._configureIO):
            # Indico il tipo di indicizzazione uso per i PIN
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            # Configuro i due PIN come uscite
            GPIO.setup(CBeerCocker.PIN_MIXER, GPIO.OUT)
            GPIO.setup(CBeerCocker.PIN_HEATER, GPIO.OUT)
            # Spengo le uscite per sicurezza
            GPIO.output(CBeerCocker.PIN_MIXER, False)
            GPIO.output(CBeerCocker.PIN_HEATER, False)
            CBeerCocker._configureIO = True
        
        # Inizializzo la PT100 se non l'ho già fatto da qualche altra istanza
        if(CBeerCocker._pt100 == None):
            CBeerCocker._pt100 = CTemperature()
    
    def GetState(self):
        return CBeerCocker._state
    
    def SetState(self, inState):
        timeoutCounter = 0
        timeoutCounterMax = 100
        
        # Resetto il processo
        while CBeerCocker._stateForce != CBeerCocker.STATE_NONE:
            time.sleep(0.1)
            timeoutCounter += 1
            if timeoutCounter >= timeoutCounterMax:
                return False
             
        CBeerCocker._stateForce = inState
        return True        
    
    def GetInfo(self):
        r = CBeerCocker
        info_dict = {'temperatura': r._pt100.GetTemperature(), 
        		'mescolatore': r._mixerState, 'resistenza': r._heaterState, 
        		'stato': r._state, 'ricetta_id': 1}
        return info_dict
    
    def SetRecipe(self, inRecipe):
        CBeerCocker._recipe = inRecipe
    
    def GetRecipe(self):
        return CBeerCocker._recipe

    def Start(self):
        if (CBeerCocker._state == CBeerCocker.STATE_IDLE):
            # Lancio il processo
            CBeerCocker._mainThread = threading.Thread(target=self.Main)
            CBeerCocker._mainThread.start()
        else:
            self.SetState(CBeerCocker.STATE_IDLE)
    
    def StartCock(self):
        """Se le condizioni sono ok, fa partire la cottura e restituisce True"""
        if(CBeerCocker._state == CBeerCocker.STATE_WAIT):
            CBeerCocker._state = CBeerCocker.STATE_COCK
            return True
        else:
            return False
    
    def StopCock(self):
        if(CBeerCocker._state == CBeerCocker.STATE_COCK):
            CBeerCocker._stopCocking = True
            return (CBeerCocker.WaitForState(CBeerCocker.STATE_WAIT))
        else:
            return (CBeerCocker._state == CBeerCocker.STATE_WAIT)
    
    def StartBoil(self):
        """Se le condizioni sono ok, fa partire la bollitura e restituisce True"""
        if(CBeerCocker._state == CBeerCocker.STATE_WAIT):
            return self.SetState(CBeerCocker.STATE_BOIL)
        else:
            return False
    
    def StopBoil(self):
        if(CBeerCocker._state == CBeerCocker.STATE_BOIL):
            CBeerCocker._stopBoiling = True
            return (CBeerCocker.WaitForState(CBeerCocker.STATE_WAIT))
        else:
            return False
    
    def Stop(self):
        if (CBeerCocker._state == CBeerCocker.STATE_IDLE):
            # Nulla da fare, e' gia' tutto fermo
            pass
        else:
            self.SetState(CBeerCocker.STATE_STOP)
            return CBeerCocker.WaitForState(CBeerCocker.STATE_IDLE)
    
    @staticmethod
    def WaitForState(inStateToWait, inTimeout = 5.0):
        startTime = time.time()
        while CBeerCocker._state != inStateToWait:
            time.sleep(0.1)
            if ((time.time() - startTime) >= inTimeout):
                break
        return (CBeerCocker._state == inStateToWait)
    
    @staticmethod
    def _ResetSwitchTime():
        """Resetta il tempo dall'ultima communatazione"""
        CBeerCocker._switchTime = time.time() + CBeerCocker.SWITCH_TIME
    
    @staticmethod
    def _SwitchTimeElapsed():
        """Ritorna se è trascorso sufficiente tempo dall'ultima communatazione"""
        return (CBeerCocker._switchTime >= time.time()) 
    
    @staticmethod
    def Main():
        """
Processo principale che gestisce l'automazione di RaspBeer


"""
        r = CBeerCocker
        
        startTime = 0.0
        stepIndex = 0
        
        print("Starting RaspBeer Daemon...")
        continueLoop = True
        while continueLoop:
            # Verifico se qualcuno sta forzando lo stato da fuori
            if r._stateForce != r.STATE_NONE:
                # Setto il nuovo stato
                r._state = r._stateForce
                # Resetto la richiesta
                r._stateForce = r.STATE_NONE
            
            if r._state == r.STATE_IDLE:
                r._state = r.STATE_INIT
                r._ResetSwitchTime()
                
            elif r._state == r.STATE_INIT:
                r._pt100.Start()
                r._state = r.STATE_WAIT
                
            elif r._state == r.STATE_WAIT:
                # Per sicurezza spengio tutto
                r._mixerState = False
                r._heaterState = False
                
            elif r._state == r.STATE_COCK:
                if(startTime == 0.0):
                    print(r._stateDescriptor[r._state])
                    stepIndex = 0
                    # Accendo il miscelatore
                    r._mixerState = True
                    startTime = time.time()
                else:
                    # Verifico di aver eseguito tutti gli step
                    if(stepIndex >= len(r._recipe['cock_step'])):
                        # Spengo la resistenza ed il mescolatore
                        startTime = 0.0
                        r._state = r.STATE_WAIT
                        r._mixerState = False
                        r._heaterState = False
                    else:
                        # print('Step: %d Time: %0.1f (%s, %s)' % (stepIndex, r._recipe['cock_step'][stepIndex]['time'] - (time.time() - startTime), r._mixerState, r._heaterState))
                        if((time.time() - startTime) > r._recipe['cock_step'][stepIndex]['time']):
                            startTime = time.time()
                            stepIndex += 1
                        else:
                            if(r._pt100.GetTemperature() > r._recipe['cock_step'][stepIndex]['temperature']):
                                # Spengo la resistenza
                                r._heaterState = False
                            else:
                                # Accendo la resistenza
                                r._heaterState = True
                
            elif r._state == r.STATE_BOIL:
                # print('Temperature: %0.1f' % (self._pt100.GetTemperature()))
                if(startTime == 0):
                    startTime = time.time()
                    stepIndex = 0
                    print(r._stateDescriptor[r._state])
                else:
                    if(stepIndex >= len(r._recipe['boiling_steps'])):
                        # Spengo la resistenza
                        r._state = CBeerCocker.STATE_WAIT
                    else:
                        # print('Step: %d Time: %0.1f' % (stepIndex, r._recipe['boiling_steps'][stepIndex]['time'] - (time.time() - startTime)))
                        if((time.time() - startTime) > r._recipe['boiling_steps'][stepIndex]['time']):
                            # print(r._recipe['boiling_steps'][stepIndex]['message'])
                            startTime = time.time()
                            stepIndex += 1
                
            elif r._state == r.STATE_STOP:
                r._pt100.Stop()
                continueLoop = False
                r._mixerState = False
                r._heaterState = False
            else:
                print("Error stato non valido '%s'" % (r._state))

            if(r._SwitchTimeElapsed() or (not continueLoop)):
                GPIO.output(r.PIN_MIXER, r._mixerState)
                GPIO.output(r.PIN_HEATER, r._heaterState)
                # print('change DO: %s, %s' % (r._mixerState, r._heaterState))
                r._ResetSwitchTime()
            
            time.sleep(0.1)

        print("Stopping RaspBeer Daemon...")


def Parti():
    xx = CBeerCocker()
    
    print(xx.Start())
    

def Ferma():
    yy = CBeerCocker()
    
    print(yy.Stop())
    

if __name__ == "__main__":
    Parti()
    
    zz = CBeerCocker()
    
    recipe = {
            'cock_step': [
                          {'time': 30.0, 'temperature': 40.0},
                          ],
            'boiling_steps': [],
            }
    
    zz.SetRecipe(recipe)
    
    while zz.GetState() != CBeerCocker.STATE_WAIT:
        print(zz.GetInfo())
        time.sleep(1)
    
    zz.StartCock()
    
    while zz.GetState() != CBeerCocker.STATE_WAIT:
        print(zz.GetInfo())
        time.sleep(1)
        
    Ferma()
    
    
if __name__ == "__main__" and False:
    recipe = {
            'cock_step': [
                          {'time': 1.0, 'temperature': 40.0},
                          {'time': 2.0, 'temperature': 40.0},
                          {'time': 3.0, 'temperature': 40.0},
                          ],
            'boiling_steps': [
                          {'time': 3.0, 'message': "Metti questo"},
                          {'time': 2.0, 'message': "Metti quello"},
                          {'time': 1.0, 'message': "Metti quell'altro"},
                          ],
            }
    
    beer = CBeerCocker()
    beer.SetRecipe(recipe)
    beer.Start()

    while beer.GetState() != CBeerCocker.STATE_WAIT:
        time.sleep(1)
    
    beer.StartCock()
    
    while beer.GetState() != CBeerCocker.STATE_WAIT:
        time.sleep(1)
    
    beer.StartBoil()
    
    while beer.GetState() != CBeerCocker.STATE_WAIT:
        time.sleep(1)
    
    beer.Stop()
        

        
