from typing import List
from GameAgent.CommandMaker import CommandMaker
from GameAgent.CommandMaker import Command


class JumpCommandMaker(CommandMaker):
    def __init__(self, coefficient=1.615):
        self.coefficient = coefficient

    def make_commands(self, known_info: dict) -> List[Command]:
        xdistance = known_info['xdistance']
        drawing_img = known_info['drawing_img']
        edge_img = known_info['edge_img']

        swipe_time = int(xdistance * self.coefficient)
        config = known_info.get('config', {})
        if config.get('show_img'):
            commands = [('show', {'drawing_img': drawing_img, 'edge_img': edge_img}),
                        ('jump', {'swipe_time': swipe_time}),
                        ('sleep', {'seconds': swipe_time / 1000})]
        else:
            commands = [('jump', {'swipe_time': swipe_time}),
                        ('sleep', {'seconds': swipe_time / 1000})]
        return commands
