import thread


finished = False

class Mutex(object):
    want = [False, False]
    turn = 0
    resource = 0

    def __init__(self, resource):
        self.resouce = resource

    def do_in_critical_section(self, func, pid):
        self.want[pid] = True
        self.turn = 1 - pid;

        while (self.want[1 - pid] and self.turn == 1 - pid):
            pass  # wait

        # critical section
        self.resource = func(self.resource)

        # end of critical section
        self.want[pid] = False;


def incr(a):
    a += 1
    return a


def f(mutex):
    global finished

    for i in xrange(10000):
        mutex.do_in_critical_section(incr, 1)

    finished = True


if __name__ == '__main__':
    mutex = Mutex(0)  # Create mutex with initial value of resource

    thread.start_new_thread(f, (mutex,))

    for i in xrange(10000):
        mutex.do_in_critical_section(incr, 0)

    while not finished:
        pass

    print mutex.resource
