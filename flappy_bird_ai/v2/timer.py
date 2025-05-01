from flappy_bird_ai.v2.node import Node


class Timer(Node):
    def __init__(self, trigger, callback):
        self.trigger = trigger
        self.callback = callback
        self.running = False
        self.time = 0

        super().__init__()

    def process(self, delta: float):
        if self.running:
            self.time += delta

            if self.time >= self.trigger:
                self.running = False
                self.callback()

    def start(self):
        self.running = True
        self.time = 0

    def stop(self):
        self.running = False