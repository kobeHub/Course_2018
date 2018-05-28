#include <iostream>
#include <mallco.h>

class Queue
{
public:
	Queue(int si);
	~Queue();
	int next();
	void update(int index)
private:
	int * data;
	int size;
	int pointer;
};

Queue::Queue(int si)
{
	size = si;
	data = new int[sizeof(int) * si];
	pointer = 0;

	for(int i=0;i<size;i++)
		data[i] = 1;
}

queue::~Queue()
{
	delete data;
}

int Queue::next()
{	
	int i;
	i = pointer % size;
	pointer ++;
	return data[i];
}

void Queue::update(int index)
{
	if(data[index])
		data[index] = 0;
	else
		data[index] = 1;
}





