from typing import List
from GameAgent.CommandMaker import CommandMaker
from GameAgent.CommandMaker import Command


class JumpCommandMaker(CommandMaker):
    def __init__(self, coefficient=1.393):
        self.coefficient = coefficient

    def make_commands(self, known_info: dict) -> List[Command]:
        distance = known_info['distance']
        swipe_time = int(round(distance * self.coefficient))

        return [('jump', {'swipe_time': swipe_time}),
                ('sleep', {'seconds': swipe_time / 1000})]
