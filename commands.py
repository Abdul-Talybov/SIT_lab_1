from abc import ABC, abstractmethod
from manager import PackageManager

class Command(ABC):
    @abstractmethod
    def execute(self): pass
    @abstractmethod
    def undo(self): pass

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
        self.old_version = None
    def execute(self):
        name, _ = self.manager._split(self.spec)
        if name in self.manager.installed:
            self.old_version = self.manager.installed[name]
        self.manager.update(self.spec)
    def undo(self):
        if self.old_version:
            name, _ = self.manager._split(self.spec)
            self.manager.install(f"{name}=={self.old_version}")
        else:
            print("[UNDO] Нет предыдущей версии")

class ListCommand(Command):
    def __init__(self, manager: PackageManager):
        self.manager = manager
    def execute(self):
        self.manager.list_installed()
    def undo(self): pass

class UndoCommand(Command):
    def __init__(self, manager: PackageManager):
        self.manager = manager
    def execute(self):
        self.manager.undo_last()
    def undo(self):
        print("[UNDO] Отмена undo не поддерживается")