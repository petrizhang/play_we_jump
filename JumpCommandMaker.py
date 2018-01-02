from typing import List
from GameAgent.CommandMaker import CommandMaker
from GameAgent.CommandMaker import Command


class JumpCommandMaker(CommandMaker):
    def __init__(self, coefficient=1.393):
        self.coefficient = coefficient

    def make_commands(self, known_info: dict) -> List[Command]:
        distance = known_info['distance']
        drawing_img = known_info['drawing_img']
        edge_img = known_info['edge_img']

        swipe_time = int(round(distance * self.coefficient))

        return [('show', {'drawing_img': drawing_img, 'edge_img': edge_img}),
                ('jump', {'swipe_time': swipe_time}),
                ('sleep', {'seconds': swipe_time / 1000})]
