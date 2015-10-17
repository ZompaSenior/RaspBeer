#UTF-8
import time
import threading

from ctemperature import CTemperature

class CBeerCocker():
    STATE_IDLE = 'idle'
    STATE_INIT = 'init'
    STATE_WAIT = 'wait'
    STATE_COCK = 'cock'
    STATE_BOIL = 'boil'
    STATE_STOP = 'stop'

    _stateDescriptor = {
        STATE_IDLE: "Idle",
        STATE_INIT: "Initializing",
        STATE_WAIT: "Waiting",
        STATE_COCK: "Cocking",
        STATE_BOIL: "Boiling",
        STATE_STOP: "Stopping",
        }
    """Descrizioni delle fasi di secuzione."""
    
    _mainThread = None
    _pt100 = None
    _recipe = None
    _state = STATE_IDLE

    _stopCocking = False
    _stopBoiling = False

    def __init__(self):
        if(CBeerCocker._pt100 == None):
            CBeerCocker._pt100 = CTemperature()
    
    def GetState(self):
    	print 'ciccia'
        return CBeerCocker._state
        
	def GetInfo(self):
		info_dict = {'temperatura':0, 'resistenza':'', 'mescolatore':'', 'stato':'', 'ricetta_id':0}
		return info_dict
    
    def SetRecipe(self, inRecipe):
        CBeerCocker._recipe = inRecipe
    
    def GetRecipe(self):
        return CBeerCocker._recipe

    def Start(self):
        if (CBeerCocker._state == CBeerCocker.STATE_IDLE):
            # Lancio i vari processi
            CBeerCocker._mainThread = threading.Thread(target=self.Main)
            CBeerCocker._mainThread.start()
        else:
            # Invio ai vari processi un comando per reinizializzarsi
            pass
    
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
            return False
    
    def StartBoil(self):
        """Se le condizioni sono ok, fa partire la bollitura e restituisce True"""
        if(CBeerCocker._state == CBeerCocker.STATE_WAIT):
            CBeerCocker._state = CBeerCocker.STATE_BOIL
            return True
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
            CBeerCocker._state = CBeerCocker.STATE_BOIL
    
    @staticmethod
    def WaitForState(inStateToWait, inTimeout = 5.0):
        startTime = time.time()
        while CBeerCocker._state != inStateToWait:
            time.sleep(0.1)
            if ((time.time() - startTime) >= inTimeout):
                break
        return (CBeerCocker._state == inStateToWait)
    
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
            # print(self._stateDescriptor[self._state])
            
            if r._state == r.STATE_IDLE:
                r._state = r.STATE_INIT
                
            elif r._state == r.STATE_INIT:
                r._pt100.Start()
                r._state = r.STATE_WAIT
                
            elif r._state == r.STATE_WAIT:
                # print('Temperature: %0.1f' % (self._pt100.GetTemperature()))
                # Spengo il miscelatore
                pass
                
            elif r._state == r.STATE_COCK:
                # print('Temperature: %0.1f' % (self._pt100.GetTemperature()))
                # Accendo il miscelatore
                if(startTime == 0.0):
                    startTime = time.time()
                    stepIndex = 0
                    print(r._stateDescriptor[r._state])
                else:
                    if(stepIndex >= len(r._recipe['cock_step'])):
                        # Spengo la resistenza
                        startTime = 0.0
                        r._state = CBeerCocker.STATE_WAIT
                    else:
                        print('Step: %d Time: %0.1f' % (stepIndex, r._recipe['cock_step'][stepIndex]['time'] - (time.time() - startTime)))
                        if((time.time() - startTime) > r._recipe['cock_step'][stepIndex]['time']):
                            startTime = time.time()
                            stepIndex += 1
                        else:
                            if(r._pt100.GetTemperature() > r._recipe['cock_step'][stepIndex]['temperature']):
                                # Spengo la resistenza
                                pass
                            else:
                                # Accendo la resistenza
                                pass
                
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
                        print('Step: %d Time: %0.1f' % (stepIndex, r._recipe['boiling_steps'][stepIndex]['time'] - (time.time() - startTime)))
                        if((time.time() - startTime) > r._recipe['boiling_steps'][stepIndex]['time']):
                            print(r._recipe['boiling_steps'][stepIndex]['message'])
                            startTime = time.time()
                            stepIndex += 1
                
            elif r._state == r.STATE_STOP:
                r._pt100.Stop()
                continueLoop = False
            else:
                print("Error stato non valido '%s'" % (r._state))
            
            time.sleep(0.1)

        print("Stopping RaspBeer Daemon...")


def Prova():
    xx = CBeerCocker()
    
    xx.Start()
    

def Provetta():
    yy = CBeerCocker()
    
    yy.Stop()
    

if __name__ == "__main__":
    Prova()
    
    zz = CBeerCocker()
    
    recipe = {
            'cock_step': [
                          {'time': 3.0, 'temperature': 40.0},
                          ],
            'boiling_steps': [],
            }
    
    zz.SetRecipe(recipe)
    
    while zz.GetState() != CBeerCocker.STATE_WAIT:
        time.sleep(1)
    
    zz.StartCock()
    
    while zz.GetState() != CBeerCocker.STATE_WAIT:
        time.sleep(1)
        
    Provetta()
    
    
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
        

        
