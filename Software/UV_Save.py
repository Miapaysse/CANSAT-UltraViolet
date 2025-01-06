''' Rssi y SNR LoRa punto a punto
paquete de datos desde puerto Serial
generados desde dispositivo LoRa
modelo Heltec Lora 32 v.2
Girni 2020-10-07 propuesta: edelros@espol.edu.ec
'''
import numpy as np
import matplotlib.pyplot as plt
import serial, time
import datetime

# INGRESO
# Puerto de captura de datos USB-Serial
puerto = 'com6'
baudios = 115200

# Archivo para el registro de cada evento rx,tx
nombrearchivo = 'DatosUV.txt'


# inicializa archivo.txt a vacio
archivo = open(nombrearchivo,'w')
archivo.close()  # Cierra el archivo

# Abre puerto Serial
arduino = serial.Serial(puerto, baudios)
time.sleep(0.3)

# limpia buffer de datos anteriores
time.sleep(1.5)
print('\nEstado del puerto: ',arduino.isOpen())
print('Nombre del dispositivo conectado: ', arduino.name)
print('Dump de la configuración:\n ',arduino)
print('\n###############################################\n')

# Lectura de datos
while True:
    #esperar hasta recibir un paquete
    while (arduino.inWaiting()==0):
        pass 

    # leer linea desde puerto serial
    linea = arduino.readline().decode('utf-8').strip()
    # binario a texto, elimina /r/n
    texto = linea
    texto = str(texto)
    fecha = datetime.datetime.now()
    # identificar la trama como rx, tx
    archivo = open(nombrearchivo,'a')
    archivo.write('[' + str(fecha) + '] ' + texto +'\n')
    archivo.close()

    
        

# Cerrar el puerto serial.
serial.Serial.close