class Singleton(object):
    def __init__(self, singleton_class):
        self.singleton_class = singleton_class
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.singleton_class(*args, **kwargs)
        return self.instance
