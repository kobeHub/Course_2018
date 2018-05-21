/*
* Filename
: reader.c
* copyright
: (C) 2018 Inno Jia
* Function
: 建立并模拟顾客进程
define CUTRQUEST 1			//请求理发标识
#define WAITSOFTRESPONSE 2	//请求在沙发等待标识
#define WAITDINGRESPONSE 3	//允许在大厅等待
#define CUTRESPONSE 3   	//允许理发师工作
#define FINISHED 4			//理发完成标识
#define NOPLACE 5			//人满结束标志
#define DONE 6				//记账结束标志
*/
#include "ipc.h"

void under_cut(int pid)
{
	printf("%d is under cutting..\n", pid);
	sleep(1);
}

int main(int argc,char *argv[])
{
	int i;
	int rate;
	Msg_buf msg_arg;

	//可在在命令行第一参数指定一个进程睡眠秒数,以调解进程执行速度
	if(argv[1] != NULL) 
		rate = atoi(argv[1]);
	else rate = 3;

	//附加一个要读内容的共享内存
	buff_key = 101;
	buff_num = STRSIZ+1;
	shm_flg = IPC_CREAT | 0644;
	buff_ptr = (int *)set_shm(buff_key,buff_num,shm_flg);

	//联系一个请求消息队列
	quest_flg = IPC_CREAT| 0644;
	quest_key = 201;
	quest_id = set_msq(quest_key,quest_flg);

	//联系一个响应消息队列
	respond_flg = IPC_CREAT| 0644;
	respond_key = 202;
	respond_id = set_msq(respond_key,respond_flg);

	///循环请求读/
	// msg_arg.mid = getpid();
	while(1){
		sleep(rate);
		//发请求理发消息
		msg_arg.mtype = CUTREQUEST;
		msgsnd(quest_id,&msg_arg,sizeof(msg_arg),quest_flg); 		//以阻塞方式发送一条系统消息　最后参数为０
		printf("%d customer quest cutting hair\n",msg_arg.mid);

		//等待允许消息
		if(msgrcv(respond_id, &msg_arg, sizeof(msg_arg), CUTRESPONSE, IPC_NOWAIT)>=0)
		{ 
			//有理发师处于空闲，可以直接唤醒理发
			under_cut(getpid());
		}
		else if(msgrcv(respond_id, &msg_arg, sizeof(msg_arg), WAITSOFTRESPONSE, IPC_NOWAIT)>=0)
		{
			printf(" %d customer is waiting is the sofa \n", getpid());
		}
		else if (msgrcv(respond_id, &msg_arg, sizeof(msg_arg), WAITDINGRESPONSE, IPC_NOWAIT)>=0)
		{
			printf("I\'m  waiting in the ding room\n");
		}
		else if(msgrcv(respond_id, &msg_arg, sizeof(msg_arg), NOPLACE, IPC_NOWAIT)>=0)
		{
			printf("There are too many people, I have to leave now\n");
			break;
		}

		//发读理发完成标志
		msg_arg.mtype = FINISHED;
		msgsnd(quest_id,&msg_arg,sizeof(msg_arg),0);

		if(msgrcv(respond_id, &msg_arg, sizeof(msg_arg), FINISHED,0) >= 0)
		{
			// 接收到退出信号
			printf("I\'m finishied. leave now ...\n");
			break;
			
		}

	}

	return EXIT_SUCCESS;
}