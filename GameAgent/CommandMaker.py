from typing import List, Tuple

Command = Tuple[str, dict]


class CommandMaker(object):
    def make_commands(self, known_info: dict) -> List[Command]:
        raise NotImplementedError
