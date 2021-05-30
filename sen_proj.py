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
    # timer.init(freq=int(12e6), mode=Timer.PERIODIC, callback=DIN_IRQ)
    # timer.init(freq=int(12e3), mode=Timer.PERIODIC, callback=DIN_IRQ)
    # timer.init(freq=int(48e3), mode=Timer.PERIODIC, callback=DIN_IRQ)
    timer.init(freq=int(100e3), mode=Timer.PERIODIC, callback=DIN_IRQ)
    DATA_STREAM_MAX = 32
    DOUBLE_BUF_MAX = 15
    num_bits = 0
    data_stream = ["X"] * DATA_STREAM_MAX
    double_buffer = ["X"] * DOUBLE_BUF_MAX
    buf = 0
    while True:
        if FLAG == 1:
            # print(DATA)
            if num_bits < DATA_STREAM_MAX: 
                data_stream[num_bits] = str(DATA)
                num_bits += 1
            else:
                data_stream_str = "".join(data_stream)
                # data_string = "%s %s %s %s" %(data_stream_str[0:4], data_stream_str[4:8], data_stream_str[8:12], data_stream_str[12:16])
                data_string = "%s %s %s %s" %(data_stream_str[0:8], data_stream_str[8:16], data_stream_str[16:24], data_stream_str[24:32])
                # print(data_string)
                double_buffer[buf] = data_string
                # print("double_buff incr")
                buf += 1
                num_bits = 0

            if buf >= DOUBLE_BUF_MAX:
                # print("buffer full")
                buf_out = '\n'.join(double_buffer)
                print(buf_out)
                buf = 0

            FLAG = 0

def DIN_IRQ(timer):
    global FLAG
    global DATA
    FLAG = 1
    DATA = DataIn_Pin.value()

def Setup():
    # machine.freq(int(200e+6)) # sets clk frequency
    GHz = Pin(7, Pin.OUT) # sets 2.4 GHz start to GP6
    MHz = Pin(8, Pin.OUT) # sets 915 MHz start to GP7
    GHz.high()
    MHz.high()

    

if __name__ == "__main__":
    # execute only if run as a script
    main()