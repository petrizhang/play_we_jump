class AgentError(Exception):
    def __init__(self, *args, **kwargs):
        super(AgentError, self).__init__(*args, **kwargs)
