#include "train.h"
using namespace std;

int main(int argc,char *argv[])
{

	cout<<"Enter the total trains number:"<<endl;
	cin>>train_num;

	g_rate = (argc > 1) ? atoi(argv[1]) : 3;
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
			//利用管程模拟第一个哲学家就餐的过程
			test->run(i);
			exit(0);
		}	
		sleep(1);
	}

}