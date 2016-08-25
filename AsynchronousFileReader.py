import threading
import Queue


class AsynchronousFileReader(threading.Thread):
    def __init__(self, fd, queue):
        assert isinstance(queue, Queue.Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue

    def run(self):
        for line in iter(self._fd.readline, ''):
            self._queue.put(line)

    def eof(self):
        return not self.is_alive() and self._queue.empty()

# TEST CODE.
"""
import sys
import subprocess
import random
import time

def consume(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout_queue = Queue.Queue()
    stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
    stdout_reader.start()
    stderr_queue = Queue.Queue()
    stderr_reader = AsynchronousFileReader(process.stderr, stderr_queue)
    stderr_reader.start()

    while not stdout_reader.eof() or not stderr_reader.eof():
        while not stdout_queue.empty():
            line = stdout_queue.get()
            print 'Received line on standard output: ' + repr(line)

        while not stderr_queue.empty():
            line = stderr_queue.get()
            print 'Received line on standard error: ' + repr(line)

        time.sleep(.1)

    stdout_reader.join()
    stderr_reader.join()

    process.stdout.close()
    process.stderr.close()


def produce(items=10):
    for i in range(items):
        output = random.choice([sys.stdout, sys.stderr])
        output.write('Line %d on %s\n' % (i, output))
        output.flush()
        time.sleep(random.uniform(.1, 1))


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'produce':
        produce(10)
    else:
        consume(['python', sys.argv[0], 'produce'])
"""

