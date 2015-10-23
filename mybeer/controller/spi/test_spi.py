# test della comunicazione spi

import spidev
import time
spi = spidev.SpiDev()
spi.open(0,0)
while True:
    resp = spi.xfer2([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07])
    print(resp)
    time.sleep(1)