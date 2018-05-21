/*
*
*FileName:train.h
*copyright (C) Inno Jia
*实现火车调度问题的函数以及管程类
*/
#include "train.h"
using namespace std;


Sema::Sema(int id)
{
	sem_id = id;
}

Sema::~Sema(){ }

int Sema::down()
{
	struct sembuf buf;
	buf.sem_op = -1;
	buf.sem_num = 0;
	buf.sem_flg = SEM_UNDO;

	if((semop(sem_id,&buf,1)) <0) {
		perror("down error ");
		exit(EXIT_FAILURE);
	}
	return EXIT_SUCCESS;
}

int Sema::up()
{
	Sem_uns arg;
	struct sembuf buf;
	buf.sem_op = 1;
	buf.sem_num = 0;
	buf.sem_flg = SEM_UNDO;

	if((semop(sem_id,&buf,1)) <0) {
		perror("up error ");
		exit(EXIT_FAILURE);
	}
	return EXIT_SUCCESS;
}


/*
* 用于哲学家管程的互斥执行
*/
Lock::Lock(Sema * s)
{
	sema = s;
}
Lock::~Lock(){ }
//上锁
void Lock::close_lock()
{
	sema->down();
}
//开锁
void Lock::open_lock()
{
	sema->up();
}


Direction::Direction(char *di)
{
	dir = di;
}

Direction::~Direction(){}

bool train::allow_change()
{
	if(gone_[0] == right_num)
		return true;
	else
		return false;
}

train::train(int ra, int nu)
{	
	int ipc_flg = IPC_CREAT | 0644;
	int shm_key = 220;
	int shm_num = 1;
	int sem_key = 120;
	// int sem_val = 0;
	int sem_id;
	Sema *sema;
	rate = ra;
	num = train_num;  //需要的火车数量
	
	// gone = (int*) malloc(sizeof(int)*num);
	
	// 同一时刻仅允许一个方向的火车,作为互斥信号灯
	if((sem_id = set_sem(sem_key, 0, ipc_flg)) < 0)
	{
		perror("Semaphor create error");
		exit(EXIT_FAILURE);
	}

	if((gone_ = (int *)set_shm(shm_key,shm_num,ipc_flg)) <0)
	{
		perror("Share memory create error");
		exit(EXIT_FAILURE);
	}
	gone_[0] = 0;

	sema = new Sema(sem_id);
	lock = new Lock(sema);
	now = right_;

	// 赋予所有火车初始方向
	for(int i=0;i<num; i++)
	{
		int di = Random(0, 2);
		if(di){
			state[i] = right_;
			right_num++;
		}
		else
			state[i] = left_;
		gone[i] = 0;    
	}
}

train::~train(){}

int train::get_ipc_id(char *proc_file,key_t key)
{
	#define BUFSZ 256
	FILE *pf;
	int i,j;
	char line[BUFSZ],colum[BUFSZ];

	if((pf = fopen(proc_file,"r")) == NULL){
		perror("Proc file not open");
		exit(EXIT_FAILURE);
	}

	fgets(line, BUFSZ,pf);
	while(!feof(pf)){
		i = j = 0;
		fgets(line, BUFSZ,pf);
		while(line[i] == ' ') 
			i++;
		while(line[i] !=' ') 
			colum[j++] = line[i++];
		colum[j] = '\0';
		if(atoi(colum) != key) 
			continue;
		
		j=0;
		while(line[i] == ' ') 
			i++;
		while(line[i] !=' ') 
			colum[j++] = line[i++];
		colum[j] = '\0';
		i = atoi(colum);
		fclose(pf);
		return i;
	}
	fclose(pf);

	return -1;
}

int train::set_sem(key_t sem_key,int sem_val,int sem_flg)
{
	int sem_id;
	Sem_uns sem_arg;
	
	//测试由 sem_key 标识的信号量是否已经建立
	if((sem_id=get_ipc_id("/proc/sysvipc/sem",sem_key)) < 0 )
	{
		//semget 新建一个信号灯,其标号返回到 sem_id
		if((sem_id = semget(sem_key,1,sem_flg)) < 0){
			perror("semaphore create error");
			exit(EXIT_FAILURE);
		}
	}

	//设置信号量的初值
	sem_arg.val = sem_val;
	if(semctl(sem_id,0,SETVAL,sem_arg) < 0){
		perror("semaphore set error");
		exit(EXIT_FAILURE);
	}
	
	return sem_id;
}

char * get_type(int i)
{
	if(i)
		return "right";
	else
		return "left";
}

void train::run(int i)
{
	if(state[i] == now)
	{
		cout<<getpid()<<" train can go to "<<get_type(state[i])<<endl;
		
		sleep(rate);
		// lock->open_lock();
		gone_[0]++;
		gone[i] = 1;
		// lock -> close_lock();
		cout<<getpid()<<" train arrival ~"<<endl;
		
	}
	else
	{	
		cout<<getpid()<<" trian is waiting..."<<"dir->"<<get_type(state[i])<<endl;
		
		
		
		if(allow_change())
		{
			lock->close_lock();
			now = direction(state[i]);
			
			lock->open_lock();
		}

	}
	

}

char * train::set_shm(key_t shm_key,int shm_num,int shm_flg)
{
	int i,shm_id;
	char * shm_buf;

	//测试由 shm_key 标识的共享内存区是否已经建立
	if((shm_id=get_ipc_id("/proc/sysvipc/shm",shm_key))<0){
		//shmget 新建 一个长度为 shm_num 字节的共享内存
		if((shm_id= shmget(shm_key,shm_num,shm_flg)) <0){
			perror("shareMemory set error");
			exit(EXIT_FAILURE);
		}
		
		//shmat 将由 shm_id 标识的共享内存附加给指针 shm_buf
		if((shm_buf=(char *)shmat(shm_id,0,0)) < (char *)0){
			perror("get shareMemory error");
			exit(EXIT_FAILURE);
		}

		for(i=0; i<shm_num; i++) shm_buf[i] = 0; //初始为 0
	}

	//共享内存区已经建立,将由 shm_id 标识的共享内存附加给指针 shm_buf
	if((shm_buf = (char *)shmat(shm_id,0,0)) < (char *)0) {
		perror("get shareMemory error");
		exit(EXIT_FAILURE);
	}
	
	return shm_buf;
}


int main(int argc,char *argv[])
{

	cout<<"Enter the total trains number:"<<endl;
	cin>>train_num;

	if (argv[1]!= NULL)
		g_rate = atoi(argv[1]);
	else
		g_rate = 3;

	train *test;  //管程对象指针
	int pid[train_num];
	test = new train(g_rate, train_num);

	for (int i=  0;i<train_num; i++)
	{
		pid[i] = fork();
		if(pid[i]<0){ 
			perror("p1 create error"); 
			exit(EXIT_FAILURE);
		}
		else if(pid[i]==0){
			while(1)
			{
				//利用管程模拟第一个哲学家就餐的过程
				test->run(i);
				sleep(2);
				if(gone[i] == 1)
					break;
			}
			
			exit(0);
		}	
		sleep(1);
		
	}

}