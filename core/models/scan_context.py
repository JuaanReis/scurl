from time import time

class ScanContext:
    def __init__(self, url):
        self.url = url
        self.start = time()
        self.structure = None
        self.response = None
        self.results = []
        self.results_map = {}
        self.score = None