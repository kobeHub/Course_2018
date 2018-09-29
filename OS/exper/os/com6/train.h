/*
*
*FileName:train.h
*copyright (C) Inno Jia
*声明火车调度问题的函数原型以及管程类
*/
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/msg.h>
#include <wait.h>
#include <sys/sem.h>

int Random(int start, int end)
{
	int dis = end - start;
	return rand() % dis+start;	
}

typedef union semus {
	int val;
}Sem_uns;

enum direction{left_, right_};

class Sema{
public:
	Sema(int id);
	~Sema();
	int down();
	int up();

private:
	int sem_id;
};

class Lock{
public:
	Lock(Sema * lock);
	~Lock();
	void close_lock();
	void open_lock();

private:
	Sema * sema;
};

class Direction{
public:
	Direction(char *di);
	~Direction();
private:
	// Sema *sema;
	char *dir;
};

class train{
public:
	train(int rate, int nu);
	~train();

	// 建立或获取ipc信号量的函数说明
	int get_ipc_id(char *proc_file, key_t key);
	int set_sem(key_t sem_key, int sem_val, int sem_flag);

	// 创建共享内存,存放哲学家状态
	char *set_shm(key_t shm_key, int shm_num, int shm_flag);

	//火车等待或者启动
	void run(int i);

	bool allow_change();

private:
	int rate;
	int num;
	Lock *lock;      //作为控制方向的互斥锁  
	int state[50];   //存放每一辆火车的方向
	
	direction now;   //存放当前火车前进方向
};



int g_rate;
int train_num;   //需要建立的火车进程的数量
int *gone_;	//所有火车均未到站
int right_num = 0;
int gone[50];