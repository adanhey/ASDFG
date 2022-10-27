import threading
import time


def ifff (x,y):
    for i in range(x,y):
        print(i)
        time.sleep(1)
thread1 = threading.Thread(name='t1',target= ifff,args=(1,10))
thread2 = threading.Thread(name='t2',target= ifff,args=(11,20))
thread1.start()   #启动线程1
thread2.start()   #启动线程2