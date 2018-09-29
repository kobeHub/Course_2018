#include <pthread.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>
// #include <stdlib.h>
#include <unistd.h>

int value = 0;
void *runner(void *param);/*将要执行的进程*/

int main(int argc, char *argv[])
{
    int pid;
    pthread_t tid;
    pthread_attr_t attr;

    pid = fork();
    if(pid == 0)
    {
    	pthread_attr_init(&attr);
        pthread_create(&tid, &attr, runner, NULL);
        pthread_join(tid, NULL);
        printf("child:value = %d\n", value);
    }
    else if(pid > 0){
    	wait(NULL);
    	printf("parent:value = %d\n", value);
    }
}

void *runner(void *param)
{
	value = 5;
	pthread_exit(0);
}