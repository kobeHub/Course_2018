head = pctrl.h
srcs = pctrl.c
objs = pctrl.o
opts = -g -c
all: pctrl
pctrl:	$(objs)
		gcc $(objs) -o pctl
pctrl.o:	$(srcs) $(head)
		gcc $(opts) $(srcs)
clean:
		rm pctl *.o
