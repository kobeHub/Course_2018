#include "stdio.h"
#include <stdlib.h>
int Random(int start, int end)
{
	int dis = end - start;
	return rand() % dis+start;	
}

int main(int args, int argv)
{
	int i;
	for(i = 0; i< 5; i++) 
		printf("%d\n", Random(0,2));
}
