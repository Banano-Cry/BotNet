#include <stdio.h>

int main(){
	int contador = 0;
	char hola[20] = "Buenas tardes";
	for(int i = 0; i < (*(&hola + 1)) - hola; ++i){
		if(hola[i] == ' ')
			printf("Espacio %d",contador);
		contador++;
		if(hola[i] == 0)
			break;
	}
	printf("%d",contador);
return 0;
}
