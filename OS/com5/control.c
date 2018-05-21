/*
* Filename
: control.c
* copyright
: (C) 2018 by Inno Jia
* Function
: 建立并模拟控制者进程

define CUTRQUEST 1			//请求理发标识
#define WAITSOFTRESPONSE 2	//请求在沙发等待标识
#define WAITDINGRESPONSE 3	//允许在大厅等待
#define CUTRESPONSE 3   	//允许理发师工作
#define FINISHED 4			//理发完成标识
#define NOPLACE 5			//人满结束标志
#define DONE 6				//记账结束标志
#define DONE 6				//记账结束标志
#define SLEEP_BARBER 3
#define SOFT_MAX 4
#define DING_MAX 13
*/
#include "ipc.h"
int main(int argc,char *argv[])
{
	
	int i;
	int rate;
	int w_mid;
	int count;
	count = MAXVAL;	// 100
	Msg_buf msg_arg;
	struct msqid_ds msg_inf;

	//建立一个共享内存先写入一串 A 字符模拟要读写的内容
	buff_key = 101;
	buff_num =STRSIZ+1;
	shm_flg = IPC_CREAT | 0644;
	buff_ptr = (int *)set_shm(buff_key,buff_num,shm_flg);
	
	buff_ptr[0] = 0;				//初始账本，金额为０
	buff_ptr[1] = SLEEP_BARBER;		//初始睡觉的理发师３个
	buff_ptr[2] = SOFT_MAX;			// 初始沙发数目４个
	buff_ptr[3] = DING_MAX;			//初始大厅凳子数目　13个
	buff_ptr[4] = '\0';
	
	//建立一条请求消息队列
	quest_flg = IPC_CREAT| 0644;
	quest_key = 201;
	quest_id = set_msq(quest_key,quest_flg);

	//建立一条响应消息队列
	respond_flg = IPC_CREAT|0644;
	respond_key = 202;
	respond_id = set_msq(respond_key,respond_flg);

	//控制进程准备接收和响应读写者的消息
	printf("Wait quest \n");
	while(1){
		
		//当 count 大于 0 时说明没有新的顾客,查询是否有任何新请求
		if(count > 0){
			
			quest_flg = IPC_NOWAIT; //以非阻塞方式接收请求消息
			
			//从消息队列中读取一条消息的系统调用
			if(msgrcv(quest_id,&msg_arg,sizeof(msg_arg),FINISHED,quest_flg) >= 0){
				//有顾客理完头发可以离开
				count++;
				printf("%d customer had his hair cut already and left\n",msg_arg.mid);
				msg_arg.mtype = FINISHED;
				msgsnd(respond_id, &msg_arg, sizeof(msg_arg), respond_flg);

				
			}
			else if(msgrcv(quest_id,&msg_arg,sizeof(msg_arg),DONE,quest_flg)>=0)
			{
				//有理发师记账请求
				w_mid = msg_arg.mid;
				count -= MAXVAL;
				
				//允许理发师记账
				msg_arg.mtype = w_mid;
				msgsnd(respond_id,&msg_arg,sizeof(msg_arg),0);
				printf("%d quest record income ,income now: %d \n",msg_arg.mid, ++buff_ptr[0]);
				buff_ptr[1] ++;
			}
			else if(msgrcv(quest_id,&msg_arg,sizeof(msg_arg),CUTREQUEST,quest_flg) >=0){
				//有顾客到来，请求唤醒理发师
				count --;
				// msg_arg.mtype = msg_arg.mid;
				// msgsnd(respond_id,&msg_arg,sizeof(msg_arg),0);

				if(buff_ptr[1]>0){
					// 有在睡觉的理发师，唤醒
					buff_ptr[1]--;
					msg_arg.mtype = CUTRESPONSE;
					msgsnd(respond_id,&msg_arg, sizeof(msg_arg), 0);

					int residual1, residual0;
					residual0 = SOFT_MAX - buff_ptr[2];	 //沙发等待人数
					residual1 = DING_MAX - buff_ptr[3];  //大厅的等待人数 
					if(buff_ptr[2] > 0)
						if(residual1>=buff_ptr[2])
						{
								printf("%d people will go to the sofa from ding\n", buff_ptr[2]);
								buff_ptr[1] = SOFT_MAX;
								buff_ptr[2] += buff_ptr[2];
						}
						else if(residual1 >0)
						{
							printf("%d people will go to the sofa from ding and ding is empty\n", buff_ptr[2]);
							buff_ptr[2] += residual1;	
						}


				}
				else if(buff_ptr[2] >0)
				{
					// 有剩余沙发,在沙发等待
					buff_ptr[2] --;
					msg_arg.mtype=WAITSOFTRESPONSE;
					msgsnd(respond_id,&msg_arg,sizeof(msg_arg), 0);
				}
				else if(buff_ptr[3] > 0)
				{
					//大厅有剩余位置，在大厅等待
					buff_ptr[3] --;
					msg_arg.mtype = WAITDINGRESPONSE;
					msgsnd(respond_id, &msg_arg, sizeof(msg_arg), 0);
				}
				else
				{
					//无位置可以等待
					msg_arg.mtype = NOPLACE;
					msgsnd(respond_id, &(msg_arg), sizeof(msg_arg), 0);
					//没有座位，顾客离开
					printf("No place to wait and %d customer left\n", msg_arg.mid);
					count++;
				}
				
			}
			
		}
		
		
		//当 count 等于 0 时说明另一个理发师正在记账
		if(count == 0){
			//以阻塞方式接收消息
			msgrcv(quest_id,&msg_arg,sizeof(msg_arg),DONE,0);
			count = MAXVAL;
			printf("%d record finished, income now: %d\n",msg_arg.mid, buff_ptr[0]);

		}
	

	}
	

	return EXIT_SUCCESS;
}
