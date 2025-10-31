from __future__ import annotations
from abc import ABC, abstractmethod
from components import *


class Command(ABC):

    @abstractmethod
    def execute(self) -> None:
        pass


class InstallCommand(Command):

    def __init__(self, package: PackageComponent) -> None:
        self.package: PackageComponent = package

    def execute(self) -> None:
        self.package.install()


class RemoveCommand(Command):

    def __init__(self, package: PackageComponent) -> None:
        self.package: PackageComponent = package

    def execute(self) -> None:
        self.package.remove()


class UpdateCommand(Command):

    def __init__(self, package: PackageComponent) -> None:
        self.package: PackageComponent = package

    def execute(self) -> None:
        print(f"Обновление {self.package.name}")
        self.package.remove()
        self.package.install()


class DisplayCommand(Command):

    def __init__(self, package: PackageComponent) -> None:
        self.package: PackageComponent = package

    def execute(self) -> None:
        print("Текущая структура пакетов:")
        self.package.display()
