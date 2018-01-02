from AgentBackend import AgentBackend
import subprocess
from random import randint
from AgentError import AgentError

adb_error = AgentError("ADB command failed, please detect USB connection.")


class AgentBackendAdb(AgentBackend):
    def __init__(self, android_img_path="/storage/emulated/0/WeJumpAgent.png",
                 local_img_path="./images/WeJumpAgent.png"):
        self.android_img_path = android_img_path
        self.local_img_path = local_img_path

    def fetch_screenshot(self):
        ret0 = self.adb_shell("screencap -p {0}".format(self.android_img_path))
        ret1 = self.shell("adb pull {source} {target}".format(source=self.android_img_path, target=self.local_img_path))
        if ret0 != 0 or ret1 != 0:
            raise adb_error
        return self.local_img_path

    def jump(self, swipe_time):
        x, y = randint(500, 1000), randint(300, 500)
        ret = self.adb_shell("input swipe {x} {y} {x} {y} {time}".format(x=x, y=y, time=swipe_time))
        if ret != 0:
            raise adb_error

    def adb_shell(self, cmd):
        adb_cmd = 'adb shell "{0}"'.format(cmd)
        return self.shell(adb_cmd)

    def shell(self, cmd):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print("-------------------- excuting shell command:")
        print(cmd)
        print()
        print("-------------------- result: ")
        for line in p.stdout.readlines():
            print(line.decode(), end="")
        print()
        ret = p.wait()
        return ret
