src = thread_func.c
obj = thread_func.o
opt = -g -c
all:	thread_func
thread_func:	$(obj)
		gcc $(obj) -l pthread -o thread_func
thread_func.o:$(src)
		gcc $(opt) $(src)
clean:
		rm tpipe *.o