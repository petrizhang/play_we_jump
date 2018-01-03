from GameAgent.GameAgent import GameAgent

from ImageProcessorCV import ImageProcessorCV
from JumpInputFetcher import JumpInputFetcher
from JumpInfoExtractor import JumpInfoExtractor
from JumpCommandMaker import JumpCommandMaker
from JumpExecutor import JumpExecutor

import matplotlib.pyplot as plt


def main():
    config = {
        'show_img': True,
        'sleep_seconds': 0.6
    }

    input_fetcher = JumpInputFetcher()

    image_processor = ImageProcessorCV()
    info_extractor = JumpInfoExtractor(image_processor)

    command_maker = JumpCommandMaker()

    executor = JumpExecutor()

    agent = GameAgent(config=config,
                      input_fetcher=input_fetcher,
                      extractor_list=[info_extractor],
                      command_maker=command_maker,
                      executor=executor)

    plt.ion()
    agent.run()


if __name__ == "__main__":
    main()
