from GameAgent.AgentError import AgentError
from GameAgent.InfoExtractor import InfoExtractor
from GameAgent.InputFetcher import InputFetcher
from GameAgent.CommandMaker import CommandMaker
from typing import List
from time import sleep


class GameAgent(object):
    def __init__(self,
                 sleep_seconds: float,
                 input_fetcher: InputFetcher,
                 extractor_list: List[InfoExtractor],
                 command_maker: CommandMaker,
                 executor):
        self.sleep_seconds = sleep_seconds
        self.input_fetcher = input_fetcher
        self.extractor_list = extractor_list
        self.command_maker = command_maker
        self.executor = executor

    def run(self):
        """
        主循环

        :return: None
        """
        while True:
            sleep(self.sleep_seconds)
            # fetch input
            known_info = self.input_fetcher.fetch_input()
            # extract useful information
            for extractor in self.extractor_list:
                new_info = extractor.extract(known_info)
                known_info = self.__merge_dict(known_info, new_info)
            # analyse known info and make policy
            policy_list = self.command_maker.make_commands(known_info)
            # execute policy
            for command, params in policy_list:
                self.execute_command(command, params)

    def execute_command(self, command: str, params: dict):
        """
        在self.executor内寻找名为command的方法，并以params为参数执行。
        e.g.
        self.execute_command('jump',{'swipe_time':100})
        等价于 self.executor.jump(swipe_time=100)
        要注意的字典params一定要和需要的参数一一对应

        :param command: 方法名
        :param params: 参数字典，和方法需要的参数一一对应
        :return: 执行结果
        """
        cmd_exe = getattr(self.executor, command)
        if not cmd_exe:
            err = 'Method for handling command "{0}" is not implemented.'.format(command)
            raise AgentError(err)
        return cmd_exe(**params)

    def __merge_dict(self, dict1, dict2):
        """
        合并两个字典，注意如果有重复项后一个会覆盖前一个

        :param dict1:
        :param dict2:
        :return:
        """
        return dict(dict1, **dict2)
