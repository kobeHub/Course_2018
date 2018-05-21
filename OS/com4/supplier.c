/*
*Author: Inno Jia
*Function:
*解决抽烟者问题的ipc,作为供应者的模型，每次仅随机提供三种材料（胶水，纸，烟草）中的两种
而且每次仅提供给一个抽烟者
*/

#include "ipc.h"

int Random(int start, int end)
{
	int dis = end - start;
	return rand() % dis+start;	
}

//提供的物品的种类，0:paper and tobacoo  1:tobacoo and glue 2:glue and paper
enum Item{ paper_toba, toba_glue, glue_paper};


char* map_to(int type) 
{ 
     if(type==0)
     	return "paper and tobacoo";
     else if(type==1)
     	return "tobacoo and glue";
     else if(type==2)
     	return "glue and paper";
     else
     	return "WRONG TYPE!!!!";
} 

int main(int argc, char *argv[])
{
	
	int rate;
	//可在在命令行第一参数指定一个进程睡眠秒数,以调解进程执行速度
	
	if(argv[1] != NULL) 
		rate = atoi(argv[1]);
	else 
		rate = 3; //不指定为 3 秒
	
	//共享内存使用的变量
	buff_key = 1000;//缓冲区任给的键值
	buff_num = 8;//缓冲区任给的长度
	pput_key = 1001;//生产者放产品指针的键值
	pput_num = 1; //指针数
	shm_flg = IPC_CREAT | 0644;//共享内存读写权限

	//获取缓冲区使用的共享内存,buff_ptr 指向缓冲区首地址
	buff_ptr = (char *)set_shm(buff_key,buff_num,shm_flg);
	//获取生产者放产品位置指针 pput_ptr
	pput_ptr = (int *)set_shm(pput_key,pput_num,shm_flg);
	//信号量使用的变量
	prod_key = 1100;//生产者同步信号灯键值
	pmtx_key = 1101;//生产者互斥信号灯键值
	cons_key = 1130;//消费者同步信号灯键值
	cmtx_key = 1131;//消费者互斥信号灯键值
	sem_flg = IPC_CREAT | 0644;
	
	//生产者同步信号灯初值设为缓冲区最大可用量
	sem_val = buff_num;
	//获取生产者同步信号灯,引用标识存 prod_sem
	prod_sem = set_sem(prod_key,sem_val,sem_flg);
	//消费者初始无产品可取,同步信号灯初值设为 0
	sem_val = 0;
	//获取消费者同步信号灯,引用标识存 cons_sem
	cons_sem = set_sem(cons_key,sem_val,sem_flg);
	//生产者互斥信号灯初值为 1
	sem_val = 1;
	//获取生产者互斥信号灯,引用标识存 pmtx_sem
	pmtx_sem = set_sem(pmtx_key,sem_val,sem_flg);
	

	//循环执行模拟生产者不断放产品
	while(1){
		
		//如果缓冲区满则生产者阻塞
		down(prod_sem, NULL);
		//如果另一供应者正在供应,本供应者阻塞
		down(pmtx_sem, NULL);
		
		//将供应者随机供应的产品输出并放入相应位置
		int type;
		type = Random(0, 3);
		buff_ptr[*pput_ptr] = type;
		sleep(rate);
		printf("%d supplier gives: %s to Buffer[%d]\n",getpid(),map_to(buff_ptr[*pput_ptr]),*pput_ptr);

		//存放位置循环下移
		*pput_ptr = (*pput_ptr+1) % buff_num;
		//唤醒阻塞的生产者
		up(pmtx_sem,NULL);
		//唤醒阻塞的消费者
		up(cons_sem, NULL);
	}
	return EXIT_SUCCESS;

}
