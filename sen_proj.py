# seudo code:
# IRQ:
#     every number of clk cycles Interrupt
#     set irq global Flag 
#     set data in

# function to output power to oscillators

# main:
#     call setup function
#     while(1):
#         if flag = 1:
#             print(data)
from machine import Pin, Timer
import rp2 
import time

# # SET GLOBAL FLAGS
FLAG = 0
DATA = 0
DataIn_Pin = Pin(0, Pin.IN, Pin.PULL_DOWN)

def main():
    global FLAG
    Setup()
    timer = Timer()
    timer.init(freq=int(12e3), mode=Timer.PERIODIC, callback=DIN_IRQ)
    while True:
        if FLAG == 1:
            print(DATA)
            FLAG = 0

def DIN_IRQ(timer):
    global FLAG
    global DATA
    FLAG = 1
    DATA = DataIn_Pin.value()

def Setup():
    machine.freq(int(96e+6)) # sets clk frequency
    GHz = Pin(7, Pin.OUT) # sets 2.4 GHz start to GP6
    MHz = Pin(8, Pin.OUT) # sets 915 MHz start to GP7
    GHz.high()
    MHz.high()

    

if __name__ == "__main__":
    # execute only if run as a script
    main()