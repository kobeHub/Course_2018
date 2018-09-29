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
#define STRSIZ 8
#define WRITERQUEST 1	//写请求标识
#define READERQUEST 2	//读请求标识
#define FINISHED 3		//读写完成标识
 

typedef union semuns {
	int val;
} Sem_uns;

/* 消息结构体*/
typedef struct msgbuf {
	long mtype;
	int mid;
	int prority;	//定义读者优先级，数值越大，优先级越高
} Msg_buf;


key_t buff_key;
int buff_num;
char *buff_ptr;
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