from GameAgent.InputFetcher import InputFetcher
from adb_utils import *


class JumpInputFetcher(InputFetcher):
    def __init__(self, android_img_path="/storage/emulated/0/WeJumpAgent.png",
                 local_img_path="./images/WeJumpAgent.png"):
        self.android_img_path = android_img_path
        self.local_img_path = local_img_path

    def fetch_input(self, config: dict) -> dict:
        ret0 = adb_shell("screencap -p {0}".format(self.android_img_path))
        ret1 = shell(
            "adb pull {source} {target}".format(source=self.android_img_path, target=self.local_img_path))
        if ret0 != 0 or ret1 != 0:
            raise adb_error
        return {'config': config,
                'img_path': self.local_img_path}
