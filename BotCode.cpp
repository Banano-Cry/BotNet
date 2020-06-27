#include <winsock2.h> //Crear socket
#include <windows.h> //Ocultar la consola

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

void CreateSocket(SOCKET &socket){
	socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP); //AF_INET: Ipv4 (2); SOCK_STREAM: TCP (1); IPPROTO_TCP: Protocolo TCP (6)
	
}	

void ConnectSocket(SOCKET &socket,sockaddr_in &server){
	if(connect(socket, (sockaddr *) &server, sizeof(server)) == SOCKET_ERROR){
		prtinf("Error al conectar\n");
		closesocket(socket);
		WSACleanup();
		exit(0);
	}
	else{
		printf("Conexion establecida\n");
		getchar();
	}
	closesocket(socket);
	WSACleanup();
	exit(0);
}

int main(){
	WSADATA wsadatal;
	sockaddr_in server;
	SOCKET socket;
	HideCmdWindows();
	StartUseWinsockDll(wsadata);
	createSocket(socket);
	CreateSockAddr_In(server);
	ConnectSocket(socket,server);
return 0;
}
