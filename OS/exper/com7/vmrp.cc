/*
* Filename
: vmrp.cc
* copyright
: (C) 2006 by zhonghonglie	
* Function
: 模拟虚拟内存页置换算法的程序
*/
#include "vmrp.h"
using namespace std;

Replace::Replace()
{
	int i;
	//设定总得访问页数,并分配相应的引用页号和淘汰页号记录数组空间
	cout << "Please input page numbers :"<< endl;
	cin >> PageNumber;
	
	ReferencePage = new int[sizeof(int) * PageNumber];
	EliminatePage = new int[sizeof(int) * PageNumber];

	//输入引用页号序列(页面走向),初始化引用页数组
	cout << "Please input reference page string :"<<endl;
	for (i = 0; i < PageNumber; i++)
		cin >> ReferencePage[i];//引用页暂存引用数组
	
	//设定内存实页数(帧数),并分配相应的实页号记录数组空间(页号栈)
	cout << "Please input page frames :"<<endl;
	cin >> FrameNumber;
	PageFrames = new int[sizeof(int) * FrameNumber];

	Framebit = new int[sizeof(int) * FrameNumber];
	
	Referencebit = new int[sizeof(int) * FrameNumber];
	Modifybit = new int[sizeof(int) * FrameNumber];
	count = new int[sizeof(int) * FrameNumber];  
}

Replace::~Replace(){}

void Replace::InitSpace(char * MethodName)
{
	int i;
	cout << endl << MethodName << endl;
	
	FaultNumber=0;
	//引用还未开始,-1 表示无引用页
	for (i = 0; i < PageNumber; i++)
		EliminatePage[i] = -1;
	for(i = 0; i < FrameNumber; i++)
		PageFrames[i] = -1;
	for(i = 0; i<FrameNumber; i++){
		Framebit[i] = 0;  //初始引用位为０，可以进行置换
		Referencebit[i] = 0;	//引用位
		count[i] = 0;     //计数
		Modifybit[i] = 0;       //修改位
	}
	

}

//分析统计选择的算法对于当前输入的页面走向的性能
void Replace::Report(void){
    //报告淘汰页顺序
    cout << endl << "Eliminate page:";
    for(int i=0; EliminatePage[i]!=-1; i++) 
    	cout << EliminatePage[i] << " ";
	
    //报告缺页数和缺页率
    cout << endl << "Number of page faults = " << FaultNumber << endl;
    cout << setw(6) << setprecision(3) ;
    cout << "Rate of page faults = " << 100*(float)FaultNumber/(float)PageNumber <<
                            "%" <<endl;
}

//最近最旧未用置换算法
void Replace::Lru(void)
{
	int i,j,k,l,next;
	InitSpace("LRU");

	//循环装入引用页
	for(k=0,l=0; k < PageNumber; k++){
		next=ReferencePage[k];
		
		//检测引用页当前是否已在实存
		for (i=0; i<FrameNumber; i++){
			if(next == PageFrames[i]){
				//引用页已在实存将其调整到页记录栈顶
				next= PageFrames[i];
				for(j=i;j>0;j--) 
					PageFrames[j] = PageFrames[j-1];
				PageFrames[0]=next;
				break;
			}
		}

		if(PageFrames[0] == next){
			//如果引用页已放栈顶,则为不缺页,报告当前内存页号
			for(j=0; j<FrameNumber; j++)
				if(PageFrames[j]>=0) 
					cout << PageFrames[j] << " ";
			cout << endl;
		continue; //继续装入下一页
		}
		else
			// 如果引用页还未放栈顶,则为缺页,缺页数加 1
			FaultNumber++;
		
		//栈底页号记入淘汰页数组中
		EliminatePage[l] = PageFrames[FrameNumber-1];
		//向下压栈
		for(j=FrameNumber-1;j>0;j--) 
			PageFrames[j]= PageFrames[j-1];
		PageFrames[0]=next; //引用页放栈顶
		//报告当前实存中页号
		for(j=0; j<FrameNumber; j++)
			if(PageFrames[j]>=0) 
				cout << PageFrames[j] << " ";
		//报告当前淘汰的页号
		if(EliminatePage[l]>=0)
			cout << "->" << EliminatePage[l++] << endl;
		else
			cout << endl;
	}
	
	//分析统计选择的算法对于当前引用的页面走向的性能
	Report();
}


//先进先出置换算法
void Replace::Fifo(void){
	
	int i,j,k,l,next;
	InitSpace("FIFO");
	
	//循环装入引用页
	for(k=0,j=l=0; k < PageNumber; k++){
		next=ReferencePage[k];
		//如果引用页已在实存中,报告实存页号
		for (i=0; i<FrameNumber; i++) 
			if(next==PageFrames[i]) 
				break;
		
		if (i<FrameNumber){
			for(i=0; i<FrameNumber; i++) 				
				cout << PageFrames[i] << " ";
			cout << endl;
			continue; // 继续引用下一页
		}

		//引用页不在实存中,缺页数加 1
		FaultNumber++;
		EliminatePage[l]= PageFrames[j]; //最先入页号记入淘汰页数组
		PageFrames[j]=next; //引用页号放最先入页号处
		j = (j+1)%FrameNumber; //最先入页号循环下移

		//报告当前实存页号和淘汰页号
		for(i=0; i<FrameNumber; i++)
			if(PageFrames[i]>=0) 
				cout << PageFrames[i] << " ";
		if(EliminatePage[l]>=0)
			cout << "->" << EliminatePage[l++] << endl;
		else
			cout << endl;
	}
	//分析统计选择的算法对于当前引用的页面走向的性能
	Report();
}
// 时钟置换算法
void Replace::Clock(void)
{
	int i,j,m,k,l,next,stop;
	InitSpace("Clock");

	for(k=0,l=0; k < PageNumber; k++){
		next = ReferencePage[k];
		// cout<<"next:"<<next<<endl;

		for(i = 0; i < FrameNumber;i++){
			if(PageFrames[i]==next){
				Framebit[i] = 1;
				break;
			}
		}
		// cout<<"I"<<i<<endl;

		if(i<FrameNumber){
			for(i=0;i<FrameNumber;i++)
				cout<<PageFrames[i]<<" ";
			cout<<endl;
			continue;
		}
		
		// 进行置换操作
		for(m=0; m<2; m++){		//遍历两次
			stop = 0;   //不需要停止，所以是０
			// cout<<"a Here"<<endl;
			for(i=0; i<FrameNumber; i++){
				// cout<<"Here"<<endl;
				if(Framebit[i] == 1)
					// 标志位为１
					Framebit[i] = 0;
				else{
					stop = 1;
					// cout<<"Pos"<<i<<endl;
					break;
				}
			}
			 if(stop)
				 break;
		}

		FaultNumber++;
		if(FaultNumber <= FrameNumber){
			// 说明还有剩余位置可用,不需要置换
			PageFrames[i] = next;
			for(m=0;m<=i;m++)
				Framebit[m] = 1;
			EliminatePage[l++] = next;
		}
		else{
			EliminatePage[l] = PageFrames[i];		//默认的初始状态均为－１可以保证不输出
		    PageFrames[i] = next;
		    Framebit[i] = 1;
		    // j = (j+1)%FrameNumber;
		}

		for(i=0; i<FrameNumber;i++)
			if(PageFrames[i]>0)
				cout<<PageFrames[i]<<" ";
		if(EliminatePage[l]>=0)
			cout<<"->"<<EliminatePage[l++]<<endl;
		else
			cout<<endl;
		
	}
	Report();
}

void Replace::Eclock (void)
{
	int i,j,k,l,next;
	InitSpace("Eclock");

	for(k=0,j=l=0; k< PageNumber;k++){
		next = ReferencePage[k];

		//检测当前页是否在实存 
		for(i = 0 ;i<FrameNumber; i++)
			if(next == PageFrames[i]){
				Referencebit[i] = 1;
				count[i] ++;

			    // 如果引用两次，就把修改位设置为１
		        if(count[i]%2==0)
			        Modifybit[i] = 0;
		        else
			        Modifybit[i] = 1;
			    break;
			}

		if(i<FrameNumber){
			for(i=0;i<FrameNumber;i++)
				cout<<PageFrames[i]<<" ";
			cout<<endl;
			continue;
		}

		if(Referencebit[j] == 1)
			Referencebit[j] = 0;
        if(Modifybit[j] == 1)
        	Modifybit[j] == 0;

        int min = 10*Referencebit[j]+Modifybit[j];
        int index = j;
        for(i=0; i<FrameNumber;i++){
        	if(10*Referencebit[i]+Modifybit[i]<min){
        		min = 10*Referencebit[i]+Modifybit[i];
        		index = i;
        	}
        }

        EliminatePage[l] = PageFrames[index];
        PageFrames[index] = next;
        Referencebit[index] = 0;
        Modifybit[index] = 0;
        count[index] = 0;
        FaultNumber++;
        j = (j+1)%FrameNumber;


        for(i=0;i<FrameNumber;i++)
        	if(PageFrames[i]>=0)
        		cout<<PageFrames[i]<<" ";
        if(EliminatePage[l]>=0)
        	cout<<"->"<<EliminatePage[l++]<<endl;
        else
        	cout<<endl;
	}

	Report();
}


void Replace::Lfu(void)
{
    int i,j,k,l,next;
    InitSpace("Lfu");

    for(k=0,j=l=0; k<PageNumber;k++){
    	next = ReferencePage[k];

    	for(i=0; i<FrameNumber;i++)
    		if(next == PageFrames[i]){
    			count[i]++;
    			break;
    		}

        if(i<FrameNumber){
        	for(i=0;i<FrameNumber;i++)
        		cout<<PageFrames[i]<<" ";
        	cout<<endl;
        	continue;
        }

        FaultNumber++;
        int min = count[0];
        int index = 0;
        for(i=0; i<FrameNumber;i++){
        	if(count[i]<min){
        		min = count[i];
        		index = i;
        	}
        }

        EliminatePage[l] = PageFrames[index];
        PageFrames[index] = next;

        count[index] = 1;

        for(i=0;i<FrameNumber;i++)
        	if(PageFrames[i]>=0)
        		cout<<PageFrames[i]<<" ";
        if(EliminatePage[l]>=0)
        	cout<<"->"<<EliminatePage[l++]<<endl;
        else
        	cout<<endl;
    }
    Report();
}
void Replace::Mfu(void){

	int i,j,k,l,next;
    InitSpace("Mfu");

    for(i=0;i<FrameNumber;i++)
    	count[i] = 1;

    for(k=0,j=l=0; k<PageNumber;k++){
    	next = ReferencePage[k];

    	for(i=0; i<FrameNumber;i++)
    		if(next == PageFrames[i]){
    			count[i]++;
    			break;
    		}

        if(i<FrameNumber){
        	for(i=0;i<FrameNumber;i++)
        		cout<<PageFrames[i]<<" ";
        	cout<<endl;
        	continue;
        }

        FaultNumber++;
        int max = count[0];
        int index = 0;
        for(i=0; i<FrameNumber;i++){
        	if(count[i]>max){
        		max = count[i];
        		index = i;
        	}
        }

        EliminatePage[l] = PageFrames[index];
        PageFrames[index] = next;

        count[index] = 0;

        for(i=0;i<FrameNumber;i++)
        	if(PageFrames[i]>=0)
        		cout<<PageFrames[i]<<" ";
        if(EliminatePage[l]>=0)
        	cout<<"->"<<EliminatePage[l++]<<endl;
        else
        	cout<<endl;
    }
    Report();
}
 

int main(int argc,char *argv[]){
	
	Replace * vmpr = new Replace();
	vmpr->Lru();
	vmpr->Fifo();
	vmpr->Clock();
	vmpr->Eclock();
	vmpr->Lfu();
	vmpr->Mfu();
	return 0;
}