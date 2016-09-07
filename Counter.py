class Counter(object):
    def __init__(self):
        self.counter = 0

    def __call__(self):
        self.counter += 1
        return 0

# TEST
counter = Counter()
assert callable(counter)