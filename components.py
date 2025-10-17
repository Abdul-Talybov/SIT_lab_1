from abc import ABC, abstractmethod
from typing import List, Optional
from manager import PackageManager

class PackageComponent(ABC):
    @abstractmethod
    def name(self) -> str: ...
    @abstractmethod
    def install(self, manager: PackageManager) -> None: ...
    @abstractmethod
    def remove(self, manager: PackageManager) -> None: ...
    @abstractmethod
    def dependencies(self): ...

class PackageLeaf(PackageComponent):
    def __init__(self, pkg_spec: str, deps: Optional[List[str]] = None):
        self.pkg_spec = pkg_spec
        self._deps = deps or []

    def name(self):
        return self.pkg_spec.split("==")[0]

    def version(self):
        return self.pkg_spec.split("==")[1] if "==" in self.pkg_spec else None

    def dependencies(self):
        return self._deps

    def install(self, manager: PackageManager):
        manager.install(self.pkg_spec)

    def remove(self, manager: PackageManager):
        manager.remove(self.pkg_spec)

class PackageGroup(PackageComponent):
    def __init__(self, name: str):
        self.group_name = name
        self.children: List[PackageComponent] = []

    def add(self, comp: PackageComponent):
        self.children.append(comp)

    def name(self):
        return self.group_name

    def dependencies(self):
        deps = []
        for c in self.children:
            deps.extend(c.dependencies())
        return deps

    def install(self, manager: PackageManager):
        for c in self.children:
            c.install(manager)

    def remove(self, manager: PackageManager):
        for c in reversed(self.children):
            c.remove(manager)