from GameAgent import GameAgent
from ImageProcessorCV import ImageProcessorCV
from AgentBackendAdb import AgentBackendAdb


def main():
    image_processor = ImageProcessorCV()
    agent_backend = AgentBackendAdb()
    agent = GameAgent(image_processor, agent_backend)
    agent.run()


if __name__ == "__main__":
    main()