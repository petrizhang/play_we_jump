import subprocess
from GameAgent.AgentError import AgentError
adb_error = AgentError("ADB command failed, please detect USB connection.")
def adb_shell(cmd: str):
    adb_cmd = 'adb shell "{0}"'.format(cmd)
    return shell(adb_cmd)


def shell(cmd: str):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print("-------------------- executing shell command:")
    print(cmd)
    print()
    print("-------------------- result: ")
    for line in p.stdout.readlines():
        print(line.decode(), end="")
    print()
    ret = p.wait()
    return ret
