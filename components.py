from abc import ABC, abstractmethod
from typing import List, Optional


class PackageComponent(ABC):

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def install(self, manager):
        pass

    @abstractmethod
    def remove(self, manager):
        pass

    @abstractmethod
    def dependencies(self) -> List[str]:
        pass

    @abstractmethod
    def version(self) -> Optional[str]:
        pass

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

    def install(self, manager):
        manager._install_component(self)

    def remove(self, manager):
        name = self.name()
        if name in manager.installed:
            del manager.installed[name]
            if name in manager.components:
                del manager.components[name]
            print(f"[OK] Удалён {name} из компонентов")

class PackageGroup(PackageComponent):
    def __init__(self, name: str):
        self.group_name = name
        self.children: List[PackageComponent] = []

    def add(self, comp: PackageComponent):
        self.children.append(comp)

    def name(self):
        return self.group_name

    def version(self):
        return None

    def dependencies(self):
        deps = []
        for c in self.children:
            deps.extend(c.dependencies())
        return deps

    def install(self, manager):
        for child in self.children:
            child.install(manager)

    def remove(self, manager):
        for child in reversed(self.children):
            child.remove(manager)
        if self.group_name in manager.components:
            del manager.components[self.group_name]
        print(f"[OK] Удалена группа: {self.group_name}")