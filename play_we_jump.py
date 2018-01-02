from GameAgent.GameAgent import GameAgent

from ImageProcessorCV import ImageProcessorCV
from JumpInputFetcher import JumpInputFetcher
from JumpInfoExtractor import JumpInfoExtractor
from JumpCommandMaker import JumpCommandMaker
from JumpExecutor import JumpExecutor


def main():
    sleep_seconds = 1

    input_fetcher = JumpInputFetcher()

    image_processor = ImageProcessorCV()
    info_extractor = JumpInfoExtractor(image_processor)

    command_maker = JumpCommandMaker()

    executor = JumpExecutor()
    agent = GameAgent(sleep_seconds=sleep_seconds,
                      input_fetcher=input_fetcher,
                      extractor_list=[info_extractor],
                      command_maker=command_maker,
                      executor=executor)
    agent.run()


if __name__ == "__main__":
    main()
