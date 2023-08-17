class Actor:
    def __init__(self, name):
        self.name = name

    def perform_as(self, task):
        task.perform_as(self)
    