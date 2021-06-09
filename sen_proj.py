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
# import rp2 
# import time

# # SET GLOBAL FLAGS / CONSTANTS
FLAG = 0
DATA = 0
DIN_PIN = 0
DIN_IRQ_FREQ = 90e3
GHZ_PIN = 7
MHZ_PIN = 8
DATA_STREAM_MAX = 32
DOUBLE_BUF_MAX = 15
DataIn_Pin = Pin(DIN_PIN, Pin.IN, Pin.PULL_DOWN)


def main():
    global FLAG
    Setup()
    timer = Timer()
    # it takes about 10 us to do a read, 
    # fastest interrupt time is 100kHz
    # without doing anything else
    # to provide enough time to do other operations
    # set interrupt frequency to below 90kHz
    timer.init(freq=int(DIN_IRQ_FREQ), mode=Timer.PERIODIC, callback=DIN_IRQ)
    num_bits = 0
    data_stream = ["X"] * DATA_STREAM_MAX
    double_buffer = ["X"] * DOUBLE_BUF_MAX
    buf = 0
    # start = time.time()
    while True:
        if FLAG == 1:
            # print(DATA)
            # print("DATA COMING IN")
            if num_bits < DATA_STREAM_MAX: 
                data_stream[num_bits] = str(DATA)
                num_bits += 1
            else:
                data_stream_str = "".join(data_stream)
                data_string_list = []
                for i in range(0, len(data_stream_str), 8):
                    data_string_list.append(data_stream_str[i:i+8])
                data_string = " ".join(data_string_list)
                # print(data_string)
                double_buffer[buf] = data_string
                # print("double_buff incr")
                buf += 1
                num_bits = 0

            if buf >= DOUBLE_BUF_MAX:
                # print("buffer full")
                # end = time.time()
                buf_out = '\n'.join(double_buffer)
                print(buf_out)
                
                # print(end-start)
                # start = time.time()
                buf = 0

            FLAG = 0

def DIN_IRQ(timer):
    global FLAG
    global DATA
    FLAG = 1
    DATA = DataIn_Pin.value()

def Setup():
    # machine.freq(int(200e+6)) # sets clk frequency
    GHz = Pin(GHZ_PIN, Pin.OUT) # sets 2.4 GHz start to GP6
    MHz = Pin(MHZ_PIN, Pin.OUT) # sets 915 MHz start to GP7
    GHz.high()
    MHz.high()

    

if __name__ == "__main__":
    # execute only if run as a script
    main()