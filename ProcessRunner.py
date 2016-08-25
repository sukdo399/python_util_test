import subprocess


class ProcessRunner():
    def __init__(self):
        pass

    def Run(self, cmd):
        args = cmd.split(" ")
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            # returns None while subprocess is running
            # it's block...
            ret_code = p.poll()
            line = p.stdout.readline().rstrip()
            yield line
            if ret_code is not None:
                break

    def Stop(self):
        pass

# TEST CODE.
'''
pr = ProcessRunner()
cmd = "python ../test/test.py"

for line in pr.Run(cmd):
    print(line)
'''

