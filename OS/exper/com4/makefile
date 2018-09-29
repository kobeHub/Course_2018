hdrs = ipc.h
opts = -g -c
sm_src = smoker.c ipc.c
sm_obj = smoker.o ipc.o
su_src = supplier.c ipc.c
su_obj = supplier.o ipc.o
all:	supplier smoker
smoker:		$(sm_obj)
			gcc $(sm_obj) -o smoker
smoker.o:	$(sm_src) $(hdrs)
			gcc $(opts) $(sm_src)
supplier: 	$(su_obj)
			gcc $(su_obj) -o supplier
supplier.o: $(su_src) $(hdrs)
			gcc $(opts) $(su_src)
clean:
			rm *.o 
			