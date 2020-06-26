#include <windows.h>

void HideCmdWindows(){
	HWND hWnd = getConsoleWindow();
	ShowWindow(hWnd, SW_SHOWNORMAL); //SW_SHOWNORMAL = 1; SW_HIDE  = 0
}

int main(){
	HideCmdWindows();




return 0;
}
