from abc import ABC, abstractmethod
from manager import PackageManager

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    @abstractmethod
    def undo(self):
        pass

class InstallCommand(Command):
    def __init__(self, manager: PackageManager, spec: str):
        self.manager = manager
        self.spec = spec
    def execute(self):
        self.manager.install(self.spec)
    def undo(self):
        self.manager.remove(self.spec)

class RemoveCommand(Command):
    def __init__(self, manager: PackageManager, spec: str):
        self.manager = manager
        self.spec = spec
    def execute(self):
        self.manager.remove(self.spec)
    def undo(self):
        self.manager.install(self.spec)

class UpdateCommand(Command):
    def __init__(self, manager: PackageManager, spec: str):
        self.manager = manager
        self.spec = spec
    def execute(self):
        self.manager.update(self.spec)
    def undo(self):
        print("[UNDO] Отмена обновления не поддерживается")

class ListCommand(Command):
    def __init__(self, manager: PackageManager):
        self.manager = manager
    def execute(self):
        self.manager.list_installed()
    def undo(self):
        pass