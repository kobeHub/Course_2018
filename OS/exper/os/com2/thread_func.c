/*
* 
: (C) by Inno Jia
: 利用管道实现在在线程间进行函数运算
*/
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <pthread.h>

void task1(int *); //函数fx执行函数原型
void task2(int *); //函数fy 执行函数原型
void task3(int *);

int f(int a);
int g(int b);
int x, y;

int pipe1[2],pipe2[2], pipe3[2], pipe4[2];
pthread_t thrd1,thrd2, thrd3;


int main(int argc,char *arg[])
{
	int ret;
	int num1,num2, num3;
	

	printf("Enter the value of x and y:\n");
	scanf("%d,%d", &x, &y);

	
	//使用 pipe()系统调用建立3个无名管道。建立不成功程序退出,执行终止
	if(pipe(pipe1) < 0){
		perror("pipe1 not create");
		exit(EXIT_FAILURE);
	}
	if(pipe(pipe2) < 0){
		perror("pipe2 not create");
		exit(EXIT_FAILURE);
	}
	if(pipe(pipe3) < 0){
		perror("pipe3 not create");
		exit(EXIT_FAILURE);
	}
	if(pipe(pipe4) < 0){
		perror("pipe4 not create");
		exit(EXIT_FAILURE);
	}

	// 将x,y分别写入管道１，３的１端，以便于在其他线程中使用
	write(pipe1[1],&x,sizeof(int));
	write(pipe2[1],&y,sizeof(int));
	close(pipe1[1]);
	close(pipe2[1]);
	//使用 pthread_create 系统调用建立两个线程。建立不成功程序退出,执行终止
	num1 = 1 ;
	ret = pthread_create(&thrd1,NULL,(void *) task1,(void *) &num1);
	if(ret){
		perror("pthread_create: f(x)");
		exit(EXIT_FAILURE);
	}

	num2 = 2 ;
	ret = pthread_create(&thrd2,NULL,(void *) task2,(void *) &num2);
	if(ret){
		perror("pthread_create: f(y)");
		exit(EXIT_FAILURE);
	}

	num3 = 3;
	ret = pthread_create(&thrd3, NULL,(void *) task3, (void *) &num3);
	if(ret){
		perror("pthread_create: f(x, y)");
		exit(EXIT_FAILURE);
	}



	//挂起当前线程切换到 thrd2 线程
	pthread_join(thrd1,NULL);
	// /挂起当前线程切换到 thrd1 线程
	pthread_join(thrd2,NULL);
	pthread_join(thrd3, NULL);
	exit(EXIT_SUCCESS);	
}


//线程 1 执行函数,它首先向管道写,然后从管道读
void task1(int *num)
{
	
	//每次循环向管道 13的 1 端写入变量 X 的值,并从
	//管道 1的 0 端读一整数写入 ｆｘ 
	read(pipe1[0], &x, sizeof(int));
	printf("thread %d read the valueof x: %d\n", *num, x);
	x = f(x);
	// printf("%d\n", x);
	write(pipe3[1],&x,sizeof(int));
	//读写完成后,关闭管道
	close(pipe1[0]);
	close(pipe3[1]);
}


//线程 2 执行函数,它首先从管道读,然后向管道写
void task2(int * num)
{
	
	//每次循环从管道 2 的 0 端读一个整数放入变量 X 中,
	//管道４的１端写入g(y)
	read(pipe2[0],&y,sizeof(int));
	printf("thread %d read the value of y: %d\n", *num, y);
	y = g(y);
	write(pipe4[1],&y,sizeof(int));
	// printf("%d\n", y);

	close(pipe2[0]);
	close(pipe4[1]);
}

void task3(int * num){
	//分别从管道３, ４的０端读取fx fy的值
	int f_x, f_y;
	read(pipe3[0],&f_x,sizeof(int));
	printf("thread %d read the value of f(x): %d\n", *num, f_x);

	read(pipe4[0],&f_y,sizeof(int));
	printf("thread %d read the value of f(y): %d\n", *num, f_y);

	printf("thread %d read the value of f(x, y):%d\n", *num, f_x+f_y);


}

int f(int a){
	if(a < 1){
		printf("Error input!\n" );
		exit(EXIT_FAILURE);
	}
	if(a == 1)
		return 1;
	else
		return f(a-1)*a;
}

int g(int b){
	/**if(b < 0){
		printf("Error input!\n" );
		exit(EXIT_FAILURE);
	}*/
	
	if(b==2 || b == 1)
		return 1;
	else
		return g(b-1)+g(b-2);


}