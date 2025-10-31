from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class PackageComponent(ABC):
    @abstractmethod
    def install(self) -> None:
        pass

    @abstractmethod
    def remove(self) -> None:
        pass

    @abstractmethod
    def display(self, indent: int = 0) -> None:
        pass


class Package(PackageComponent):
    def __init__(self, name: str) -> None:
        self.name: str = name

    def install(self) -> None:
        print(f"Установка пакета {self.name}")

    def remove(self) -> None:
        print(f"Удаление пакета {self.name}")

    def display(self, indent: int = 0) -> None:
        print(" " * indent + f"- {self.name}")


class PackageGroup(PackageComponent):
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.children: List[PackageComponent] = []

    def add(self, component: PackageComponent) -> None:
        self.children.append(component)

    def remove_component(self, component: PackageComponent) -> None:
        self.children.remove(component)

    def install(self) -> None:
        print(f"Установка группы {self.name}")
        for child in self.children:
            child.install()

    def remove(self) -> None:
        print(f"Удаление группы {self.name}")
        for child in self.children:
            child.remove()

    def display(self, indent: int = 0) -> None:
        print(" " * indent + f"[Группа {self.name}]")
        for child in self.children:
            child.display(indent + 2)
