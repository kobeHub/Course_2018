/**
Author:Inno Jia
@ www.innohub.top
**/
#include "pctrl.h"


char *args[] = {"/bin/ls","-l",NULL};
int status;
int status1;

void child_ls()
{
		
			int i;
			for(i=0; args[i] != NULL; i++) 
				printf("%s ",args[i]);
			printf("\n");
			//装入并执行新的程序
		    // execve(args[0],args,NULL);
		    status = system("/bin/ls -l");
			
		
}

void child_ps()
{
		
		
			printf("ps -l\n");
			//装入并执行新的程序
		    // execve(args[0],args,NULL);
		    status1 = system("ps -l");
			// sleep(3);
		
}
int main(int argc, char *argv[])
{
	
	
	while(1)
	{
	int pid1;
	int pid2;
	//存放子进程号
	
	//signal(SIGINT,(sighandler_t)sigcat); 注册一个本进程处理键盘中断的函数
	pid1=fork() ; //建立子进程
	
	if(pid1<0) // 建立子进程失败?
	{
		printf("Create Process fail!\n");
		exit(EXIT_FAILURE);
	}
	if(pid1 == 0) // 子进程执行代码段
	{
		//报告父子进程进程号
		printf("I am Child process %d\nMy father is %d\n",getpid(),getppid());
		printf("%d child will Running: \n",getpid()); //
		printf("The ls command!\n");
	    sleep(1);
		child_ls();
		
		exit(0);

	}
	else
	{	
		printf("\nI am Parent process %d\n",getpid());
		
		pid2 = fork();
		if(pid2 <0)
		{
			printf("Child Process Failed!\n");
		}
		if(pid2==0)
		{
			printf("I am Child process %d\nMy father is %d\n",getpid(),getppid());
			printf("%d child will Running: \n",getpid()); //
			printf("The ps command!\n");

			child_ps();
			
			exit(0);
		}
		if(pid2 > 0)//父进程执行代码段
		{
		
			
			waitpid(pid2,&status1,0);
			waitpid(pid1, &status,0);
			
			kill(pid2, SIGINT);
			printf("ps process over:%d\n", pid1);
			kill(pid1, SIGINT);
			printf("ls process over:%d\n", pid1);
		}
	 }
	
	sleep(3);
	}
		
	return EXIT_SUCCESS;
}
