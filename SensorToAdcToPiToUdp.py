import smbus
import time
from socket import *

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

BROADCAST_TO_PORT = 22392

# check your PCF8591 address by type in 'sudo i2cdetect -y -1' in terminal.

def setup(Addr):
    global address
    address = Addr


def read(chn):  # channel
    if chn == 0:
        bus.write_byte(address, 0x40)
    if chn == 1:
        bus.write_byte(address, 0x41)
    if chn == 2:
        bus.write_byte(address, 0x02)
    if chn == 3:
        bus.write_byte(address, 0x03)
    if chn == 4:
        bus.write_byte(address, 0x44)
    if chn == 5:
        bus.write_byte(address, 0x45)
    if chn == 6:
        bus.write_byte(address, 0x46)
    if chn == 7:
        bus.write_byte(address, 0x47)
    if chn == 8:
        bus.write_byte(address, 0x47)
    return bus.read_byte(address)


if __name__ == "__main__":
    setup(0x48)
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    udpSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    while True:
        val = read(1)
        print("Raw value from ADC: ", val)

        if val == 0:  # Avoid div by zero
            val = 1

        resSensor = 20000*(5.00-(val*5.00/1024.0))/(val*5.00/1024.0) # Measured resistance of sensor
        resOriginal = 200000 # Resistance of sensor in normal air (no alcohol)

        ratio = resSensor/resOriginal

        print("Res. ratio: ", ratio)

        mgPerL = (5233*pow(5233,(8/17)))/(100000*pow(10,(15/17))*pow(ratio,(25/17)))
        airGPerL = 1.29

        print("mg/L: ", mgPerL)

        bAC = mgPerL / airGPerL

        print("BAC permille: ", bAC)

        udpSocket.sendto(bytes(str(bAC), "UTF-8"), ('<broadcast>', BROADCAST_TO_PORT))

        time.sleep(1.0)