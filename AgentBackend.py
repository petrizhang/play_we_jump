class AgentBackend(object):
    def fetch_screenshot(self):
        raise NotImplementedError

    def jump(self, swipe_time):
        raise NotImplementedError
