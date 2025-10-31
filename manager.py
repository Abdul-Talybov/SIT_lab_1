from __future__ import annotations
from typing import List
from commands import *


class PackageManager:

    def __init__(self) -> None:
        # История выполненных команд
        self.history: List[Command] = []

    def execute_command(self, command: Command) -> None:
        self.history.append(command)
        command.execute()
