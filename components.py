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
    def dependencies(self) -> List[str]: ...

class PackageLeaf(PackageComponent):
    def __init__(self, pkg_spec: str, deps: Optional[List[str]] = None):
        self.pkg_spec = pkg_spec
        self._deps = deps or []

    def name(self) -> str:
        return self.pkg_spec.split("==",1)[0] if "==" in self.pkg_spec else self.pkg_spec

    def version(self) -> Optional[str]:
        if "==" in self.pkg_spec:
            return self.pkg_spec.split("==",1)[1]
        return None

    def dependencies(self) -> List[str]:
        return list(self._deps)

    def install(self, manager: PackageManager) -> None:
        manager.install(self.pkg_spec)

    def remove(self, manager: PackageManager) -> None:
        manager.remove(self.pkg_spec)

    def __repr__(self):
        return f"PackageLeaf({self.pkg_spec})"

class PackageGroup(PackageComponent):
    def __init__(self, group_name: str):
        self.group_name = group_name
        self.children: List[PackageComponent] = []

    def add(self, comp: PackageComponent) -> None:
        self.children.append(comp)

    def remove_child(self, comp: PackageComponent) -> None:
        self.children.remove(comp)

    def name(self) -> str:
        return self.group_name

    def dependencies(self) -> List[str]:
        deps = []
        for c in self.children:
            deps.extend(c.dependencies())
        return deps

    def install(self, manager: PackageManager) -> None:
        for c in self.children:
            c.install(manager)

    def remove(self, manager: PackageManager) -> None:
        for c in reversed(self.children):
            c.remove(manager)

    def __repr__(self):
        return f"PackageGroup({self.group_name}, children={self.children})"
