class InfoExtractor(object):
    def extract(self, known_info: dict) -> dict:
        raise NotImplementedError
