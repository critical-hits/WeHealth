import threading
def sayHello():
    print "Hello"
    t=threading.Timer(3,sayHello)
    t.start()


def other_func():
    print "Other"

if __name__=="__main__":
    sayHello()
    other_func()