/*
* Filename
: writer.c
* copyright
: (C) 2006 by zhonghonglie
* Function
: 建立并模拟理发师进程

#define CUTRQUEST 1			//请求理发标识
#define WAITSOFTRESPONSE 2	//请求在沙发等待标识
#define WAITDINGRESPONSE 3	//允许在大厅等待
#define CUTRESPONSE 3   	//允许理发师工作
#define FINISHED 4			//理发完成标识
#define NOPLACE 5			//人满结束标志
#define DONE 6				//记账标志
*/
#include "ipc.h"

void cut(int pid)
{
	printf("%d barber is cutting hair ...\n", pid);
	sleep(1);
}

int main(int argc,char *argv[])
{
	int i,j=0;
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

	//循环请求写
	msg_arg.mid = getpid();
	printf("%d barber sleeping...\n", getpid());
	
	while(1){
		printf("%d barber sleeping...\n", getpid());
		
		//等待允许剪发的消息
		msg_arg.mtype = CUTRESPONSE;
		msgrcv(respond_id, &msg_arg, sizeof(msg_arg), CUTRESPONSE, 0);

		printf("%d receive a customer\n", getpid());
		// 进行理发
		cut(getpid());		

		//请求记账
		msg_arg.mtype = DONE;
		msgsnd(quest_id, &msg_arg, sizeof(msg_arg), 0);

		//服务几位数
		printf("%d had servered one customer\n",getpid());
		sleep(rate);

	}
	
	return EXIT_SUCCESS;
}