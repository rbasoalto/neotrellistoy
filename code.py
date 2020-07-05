"""NeoTrellis toy for kids


"""
import time
import board
import busio

from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from toy import Toy

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

i2c = board.I2C()

trelli = [
    [NeoTrellis(i2c, False, addr=0x2F),
     NeoTrellis(i2c, False, addr=0x2E), ],
    [NeoTrellis(i2c, False, addr=0x31),
     NeoTrellis(i2c, False, addr=0x30), ],
]
trellis = MultiTrellis(trelli)


class TrellisWrapper(object):
    """Wrapper that implements the basic color iface, for use with Toy"""

    def __init__(self, trellis, brightness=1):
        self.brightness = brightness
        self.trellis = trellis

    def _adjustColor(self, color):
        return (int(c * self.brightness) for c in color)

    def color(self, x, y, color):
        self.trellis.color(x, y, self._adjustColor(color))

    def width(self):
        return 8

    def height(self):
        return 8


trellisWrapper = TrellisWrapper(trellis, 0.5)

toy = Toy(trellisWrapper)


def buttonEvent(x, y, edge):
    toy.onEvent(x, y, edge == NeoTrellis.EDGE_RISING)


for y in range(8):
    for x in range(8):
        trellis.activate_key(x, y, NeoTrellis.EDGE_RISING)
        trellis.activate_key(x, y, NeoTrellis.EDGE_FALLING)
        trellis.set_callback(x, y, buttonEvent)


def tick(cmd=None):
    toy.tick(cmd)
    trellis.sync()
    time.sleep(0.02)


while True:
    print('Toy offline.')
    ble.start_advertising(advertisement)
    while not ble.connected:
        tick()
    print('Connected yay.')
    ble.stop_advertising()
    while ble.connected:
        if uart.in_waiting > 0:
            print('UART has data', end='')
            # there's data
            cmd = uart.readline().decode('ascii').strip()
            print(':', cmd)
            tick(cmd)
        else:
            tick()
