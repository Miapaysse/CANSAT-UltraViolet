import http.server
import socketserver
import threading
import serial, time
import datetime

PORT = 80
pkt = "0"
uvVolt = "0"
uvRad = "0"
baseline = "0"
presion = "0"
altitud = "0"
temperatura = "0"
uvIndex = "0"

nombrearchivo = 'Datos_CANSAT.txt'

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == "/temperature/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(temperatura).encode("utf-8"))
        elif self.path == "/altitud/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(altitud).encode("utf-8"))
        elif self.path == "/uvvolt/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(uvVolt).encode("utf-8"))
        elif self.path == "/uvrad/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(uvRad).encode("utf-8"))
        elif self.path == "/presion/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(presion).encode("utf-8"))
        elif self.path == "/uvindex/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(uvIndex).encode("utf-8"))
        elif self.path == "/js/highcharts.js":
            self.path = "/js/highcharts.js"
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == "/js/highcharts-more.js":
            self.path = "/js/highcharts-more.js"
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Not Found".encode("utf-8"))


def TCPServer():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.handle_request()
        httpd.serve_forever()

Server = threading.Thread(target= TCPServer)
Server.start()


def getData():
    with serial.Serial("COM6", 115200) as ser:
        while True:
            global pkt
            global uvVolt
            global uvRad
            global baseline
            global presion
            global altitud
            global temperatura
            global uvIndex
            try:
                line = ser.readline().decode('utf-8').strip()
                listaDatos = line.split(',')
                pkt = listaDatos[0]
                uvVolt = listaDatos[1]
                uvRad = listaDatos[2]
                baseline = listaDatos[3]
                presion = listaDatos[4]
                altitud = listaDatos[5]
                temperatura = listaDatos[6]
                uvIndex = float(uvVolt) * 12.49 - 12.49
                if uvIndex < 0:
                    uvIndex = 0
                #print(uvIndex)
            except:
                pass
            
            print(line)
            print(listaDatos)
            texto = line
            texto = str(texto)
            fecha = datetime.datetime.now()
            archivo = open(nombrearchivo,'a')
            archivo.write('[' + str(fecha) + '] ' + texto +'\n')
            archivo.close()

getData()
Server.join()