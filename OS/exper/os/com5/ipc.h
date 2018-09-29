/*
* Filename
* copyright
* Function
: ipc.h
: (C) 2006 by zhonghonglie
: 声明 IPC 机制的函数原型和全局变量*/

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/sem.h>
#include <sys/msg.h>
#include <unistd.h>


#define BUFSZ 256
#define MAXVAL 100
#define STRSIZ 4
#define CUTREQUEST 1			//请求理发标识
#define WAITSOFTRESPONSE 2	//请求等待标识
#define WAITDINGRESPONSE 3	//允许在大厅等待
#define CUTRESPONSE 3   	//允许理发师工作
#define FINISHED 4			//理发完成标识
#define NOPLACE 5			//人满结束标志
#define DONE 6				//记账结束标志
#define SLEEP_BARBER 3
#define SOFT_MAX 4
#define DING_MAX 13

typedef union semuns {
	int val;
} Sem_uns;

/* 消息结构体*/
typedef struct msgbuf {
	long mtype;			//定义行为
	int mid;			//定义进度号
} Msg_buf;


key_t buff_key;
int buff_num;
int *buff_ptr;	//存放共享资源的数组，包含账本金额，剩余睡觉理发师，剩余沙发，剩余大厅
int shm_flg;
int quest_flg;
key_t quest_key;
int quest_id;
int respond_flg;
key_t respond_key;
int respond_id;


int get_ipc_id(char *proc_file,key_t key);
char *set_shm(key_t shm_key,int shm_num,int shm_flag);	//设置共享内存
int set_msq(key_t msq_key,int msq_flag);				//设置消息队列
int set_sem(key_t sem_key,int sem_val,int sem_flag);	//设置具有sem_val个信号灯的信号量
int down(int sem_id);
int up(int sem_id);