import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
import numpy as np

x = 0
y = 1

pkt = []
pkt.append([0])
pkt.append([0])

uvVolt = []
uvVolt.append([0.0])
uvVolt.append([0.0])

uv = []
uv.append([0.0])
uv.append([0.0])

p = []
p.append([0.0])
p.append([0.0])

a = []
a.append([0.0])
a.append([0.0])

t = []
t.append([0.0])
t.append([0.0])

def getData():
    with serial.Serial("COM6", 115200) as ser:
        while True:
            line = ser.readline().decode('utf-8')
            try:
                indicador1 = line.find(',')
                #pkt[y].append(float(line[:indicador1]))
                indicador2 = line.find(',', indicador1+1)
                uvVolt[y].append(float(line[indicador1+1:indicador2]))
                indicador3 = line.find(',', indicador2+1)
                uv[y].append(float(line[indicador2+1:indicador3]))
                if len(uv[y] > 60):
                    uv[y].pop(0)
                print("uv Index = " + str(line[indicador3+1:]))
            except:
                pass
            indicador1 = line.find(',')
            indicador2 = line.find(',', indicador1+1)
            indicador3 = line.find(',', indicador2+1)
            print("uv Index = " + str(line[indicador3+1:]))
            

dataGet = threading.Thread(target= getData)
dataGet.start()

def update_line(num, hl, data):
    dx = np.array(range(len(data[y])))
    dy = np.array(data[y])
    hl.set_data(dx, dy)
    return hl,

fig = plt.figure(figsize=(10,8))
plt.ylim(0, 700)
plt.xlim(0,60)
hl, = plt.plot(uv[x], uv[y])

line_ani = animation.FuncAnimation(fig, update_line, fargs=(hl, uv), interval = 50, blit = False, cache_frame_data=False)
plt.show()
dataGet.join()

'''def readserial(comport, baudrate):

    ser = serial.Serial(comport, baudrate, timeout=0.1)         # 1/timeout is the frequency at which the port is read

    while True:
        line = ser.readline().decode('ascii').strip()
        if line:
            try:
                indicador1 = line.find(',')
                pkt[y].append(int(line[:indicador1]))
                indicador2 = line.find(',', indicador1+1)
                uvVolt[y].append(float(line[indicador1+1:indicador2]))
                indicador3 = line.find(',', indicador2+1)
                uv[y].append(float(line[indicador2+1:indicador3]))
            except:
                pass
            indicador1 = line.find(',')
            indicador2 = line.find(',', indicador1+1)
            indicador3 = line.find(',', indicador2+1)
            print("uv Index = " + str(line[indicador3+1:]))
            print(line)
            print(float(line[indicador2+1:indicador3]))
            uv[y].append(float(line[indicador2+1:indicador3]))
            print(uv[y])

readserial('COM6', 115200)'''