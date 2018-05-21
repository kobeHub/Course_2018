/*
*
*
Filename
copyright
* Function
: dp.h
: (C) 2006 by zhonghonglie
: 声明 IPC 机制的函数原型和哲学家管程类
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



/*信号灯控制用的共同体*/
typedef union semuns {
	int val;
} Sem_uns;

//哲学家的 3 个状态(思考、饥俄、就餐)
enum State {thinking,hungry,eating};

//哲学家管程中使用的信号量
class Sema{
	public :
		Sema(int id);
		~Sema();
		// 控制信号量加减
		int down();
		int up();
	private:
		int sem_id;
};

// 哲学家管程中使用的锁
class Lock{
public:
	Lock(Sema * lock);
	~Lock();
	void close_lock();
	void open_lock();
private:
	Sema *sema;  //所使用的信号量
};

// 哲学家管程中使用的条件变量
class Condition{
public:
	Condition(char *st[], Sema *sm);
	~Condition();

	void Wait(Lock *lock, int i);  //条件变量阻塞操作
	void Signal(int i);  //条件变量唤醒操作
private:
	Sema *sema;
	char **state;
};

// 哲学家管程定义
class dp{

public:
	dp(int rate);
	~dp();
	void pickup(int i);		//捡起筷子
	void putdown(int i);   //放下

	// 建立或获取ipc信号量的函数说明
	int get_ipc_id(char *proc_file, key_t key);
	int set_sem(key_t sem_key, int sem_val, int sem_flag);

	// 创建共享内存,存放哲学家状态
	char *set_shm(key_t shm_key, int shm_num, int shm_flag);

private:
	int rate;
	Lock *lock;				//控制互斥
	char *state[5];			//存放５个哲学家状态
	Condition *self[5]; 	//控制哲学家的条件变量
};