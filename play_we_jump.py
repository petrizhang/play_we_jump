from WeJumpAgent import WeJumpAgent
from ImageProcessorCV import ImageProcessorCV
from AgentBackendAdb import AgentBackendAdb


def main():
    image_processor = ImageProcessorCV()
    agent_backend = AgentBackendAdb()
    agent = WeJumpAgent(image_processor, agent_backend)
    agent.run()


if __name__ == "__main__":
    main()
