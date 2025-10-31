from abc import ABC, abstractmethod

class PackageComponent(ABC):
    @abstractmethod
    def install(self):
        pass

    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def display(self, indent=0):
        pass


class Package(PackageComponent):
    def __init__(self, name):
        self.name = name

    def install(self):
        print(f"Установка пакета {self.name}")

    def remove(self):
        print(f"Удаление пакета {self.name}")

    def display(self, indent=0):
        print(" " * indent + f"- {self.name}")


class PackageGroup(PackageComponent):
    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, component: PackageComponent):
        self.children.append(component)

    def remove_component(self, component: PackageComponent):
        self.children.remove(component)

    def install(self):
        print(f"Установка группы {self.name}")
        for child in self.children:
            child.install()

    def remove(self):
        print(f"Удаление группы {self.name}")
        for child in self.children:
            child.remove()

    def display(self, indent=0):
        print(" " * indent + f"[Группа {self.name}]")
        for child in self.children:
            child.display(indent + 2)
