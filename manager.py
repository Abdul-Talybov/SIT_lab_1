from commands import *

class PackageManager:
    def __init__(self):
        self.history = []

    def execute_command(self, command: Command):
        self.history.append(command)
        command.execute()
