/*
* Filename
: psched.c
* copyright
: (C) 2018 by Inno Jia
* Function
: 同步并发的父子进程，使用优先数增减函数，进行随机次数的进程优先级改变
并且输出相应的优先级

:Linux 下的优先级从-20~19一共４０个等级，数字越小则优先级越高，用户程序只可以降低自身优先级
不可以提高优先级，若满足操作则必须在root模式下运行
*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sched.h>
#include <sys/time.h>
#include <sys/resource.h>

int Random(int start, int end){
    int dis = end - start;
    return rand() % dis + start;
}

void sig_int(pid_t pid){

	int pro;
	pro = getpriority(PRIO_PROCESS, pid);
	setpriority(PRIO_PROCESS, pid, pro+1);	
}

void sig_tstp(pid_t pid){
	
	int pro;
	pro = getpriority(PRIO_PROCESS, pid);
	// printf("%d",pro-1);
	setpriority(PRIO_PROCESS, pid, pro-1);
}


int main(int argc, char *argv[])
{
	int status;
	int pid1, pid2; //存放进程号
	struct sched_param p[2]; //设置调度策略时使用的数据结构
	
	pid2 = fork();

	if(pid2 < 0){
		perror("child process not create!");
		exit(EXIT_FAILURE);
	}
	
	if(pid2 > 0){

			pid1 = getpid();
			//取进程优先数放在调度策略数据结构中
			// pid1.sched_priority = (argv[1] != NULL) ? atoi(argv[1]):10;
			setpriority(PRIO_PROCESS,pid1,(argv[1] != NULL) ? atoi(argv[1]):10);
			sched_setscheduler(pid1,(argv[3] != NULL) ? atoi(argv[3]) :SCHED_OTHER,&p[1]);
		

			setpriority(PRIO_PROCESS, pid2 ,10);
			// 父进程设置子进程的调度策略.如果命令行第 3参数指定了父进程策略
			// 值则按指定的数设置,否则都为默认策略
			sched_setscheduler(pid2,(argv[4] != NULL) ? atoi(argv[4]) :SCHED_OTHER,&p[2]);

			printf("I\'m father: pid=%d, priority=%d, policy=%d \n",pid1, getpriority(PRIO_PROCESS,pid1), sched_getscheduler(pid1));
	

	}
	else{	
			
			//报告子进程的信息
			printf("I\'m child: pid = %d priority= %d policy=%d\n",
					getpid(),getpriority(PRIO_PROCESS,pid2),sched_getscheduler(pid2));
	}

	if(pid2 > 0){
		sleep(1);
		while(1){

		int cycle, i;
		cycle = Random(3, 5);
		for(i = 0; i< cycle; i++){
			sig_int(pid1);
			printf("Father call SIGINT:\tpid=%d, priority=%d, policy=%d\n", pid1, getpriority(PRIO_PROCESS,pid1), sched_getscheduler(pid1));
		}
		cycle = Random(3, 5);
		for(i = 0; i< cycle; i++){
			sig_int(pid2);
			printf("Child call SIGINT:\tpid=%d, priority=%d, policy=%d\n", pid2, getpriority(PRIO_PROCESS,pid2), sched_getscheduler(pid2));
		}
		cycle = Random(3, 5);
		for(i = 0; i< cycle; i++){
			sig_tstp(pid1);
			printf("Father call SIGTSTP:\tpid=%d, priority=%d, policy=%d\n", pid1, getpriority(PRIO_PROCESS,pid1), sched_getscheduler(pid1));
		}
		cycle = Random(3, 5);
		for(i = 0; i< cycle; i++){
			sig_tstp(pid2);
			printf("Child call SIGTSTP:\tpid=%d, priority=%d, policy=%d\n", pid2, getpriority(PRIO_PROCESS,pid2), sched_getscheduler(pid2));
		}

		printf("\n\n\n");
		sleep(3);

		}
	}
	
	
	return EXIT_SUCCESS;
}