#Questo file mette a disposizione le classi per il controllo della temperatura
#la funzione registrate e' get_controller e restituisce la classe CBeerCocker

from multiprocessing.managers import BaseManager
from controller.draspbeer import CBeerCocker

print 'Comincio a servire'

controller = CBeerCocker()
#controller.
class ClientManager(BaseManager): pass
ClientManager.register('get_controller', callable=lambda: controller)
manager = ClientManager(address=('', 12345), authkey='raspbeer')
server = manager.get_server()
server.serve_forever()