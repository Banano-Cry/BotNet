#include <winsock2.h> //Crear socket
#include <windows.h> //Ocultar la consola
#include <stdio.h>
#include <ws2tcpip.h>

#pragma comment(lib, "Ws2_32.lib")

void HideCmdWindowsWithoutFlash(){
	HWND hide = FindWindowA("ConsoleWindowClass",NULL); //check
	AllocConsole(); //check
	ShowWindow(hide,SW_SHOWNORMAL);
}

void HideCmdWindows(){ //Hace un pestañeo
	HWND hWnd = GetConsoleWindow();
	ShowWindow(hWnd, SW_SHOWNORMAL); //SW_SHOWNORMAL = 1; SW_HIDE  = 0
}

void StartUseWinsockDll(WSADATA wsadata){
	WORD wVersion = MAKEWORD(2,2);
	WSAStartup(wVersion, &wsadata);
}

void CreateSockAddr_In(sockaddr_in &server){
	server.sin_family = AF_INET; //AF_INET: ipV4
	server.sin_addr.s_addr = inet_addr("192.168.0.7"); //Direccion IP
	server.sin_port = htons(8080); //Puerto
}

void CreateSocket(SOCKET &socketS){
	socketS = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP); //AF_INET: Ipv4 (2); SOCK_STREAM: TCP (1); IPPROTO_TCP: Protocolo TCP (6)
	
}	

void ConnectSocket(SOCKET &socketS,sockaddr_in &server){
	if(connect(socketS, (sockaddr *) &server, sizeof(server)) == SOCKET_ERROR){
		printf("Error al conectar\n");
	}
	else{
		printf("Conexion establecida\n");
		char Received[1024] = "";
		int Result = recv(socketS,Received,1024,0);
		printf("Received: %s",Received);
		printf("Longitud: %d",Result);
		getchar();
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
	StartUseWinsockDll(wsadata);
	CreateSocket(socketS);
	CreateSockAddr_In(server);
	ConnectSocket(socketS,server);
return 0;
}
