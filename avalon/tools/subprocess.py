import threading

from subprocess import PIPE, Popen, CalledProcessError


class Command(object):

    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
        self.result = None

    def run(self):

        def target():
            self.process = Popen(self.cmd, stdout=PIPE, stderr=PIPE,
                                 shell=True, universal_newlines=True)
            self.result = self.process.communicate()

        thread = threading.Thread(target=target)
        thread.start()

        thread.join()
        if thread.is_alive():
            self.process.terminate()
            thread.join()

        if self.process.returncode != 0:
            raise CalledProcessError(self.process.returncode, self.cmd)

        return self.result
