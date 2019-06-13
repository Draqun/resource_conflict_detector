class Timeframe:
    def __init__(self, number, threads = None):
        self.number = number
        self.threads = [] if threads is None else threads
        for t in self.threads:
            t.add_timeframe(self)

    def add_thread(self, thread):
        thread.add_timeframe(self)
        self.threads.append(thread)

    def __repr__(self):
        return 'Timeframe<'+', '.join("%s: %s" % item for item in vars(self).items())+'>'
