from abc import ABC, abstractmethod
from components import *

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class InstallCommand(Command):
    def __init__(self, package: PackageComponent):
        self.package = package

    def execute(self):
        self.package.install()


class RemoveCommand(Command):
    def __init__(self, package: PackageComponent):
        self.package = package

    def execute(self):
        self.package.remove()


class UpdateCommand(Command):
    def __init__(self, package: PackageComponent):
        self.package = package

    def execute(self):
        print(f"Обновление {self.package.name}")
        self.package.remove()
        self.package.install()


class DisplayCommand(Command):
    def __init__(self, package: PackageComponent):
        self.package = package

    def execute(self):
        print("Текущая структура пакетов:")
        self.package.display()
