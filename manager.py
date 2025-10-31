from typing import Dict, List, Optional
from repository import PackageRepository
from components import PackageLeaf, PackageGroup
from utils import compare_versions

class PackageManager:
    def __init__(self, repo: PackageRepository):
        self.repo = repo
        self.installed: Dict[str, str] = {}  # name -> version
        self.components: Dict[str, PackageComponent] = {}
        self.history: List[PackageComponent] = []

    def _split(self, spec: str):
        if "==" in spec:
            return tuple(spec.split("==", 1))
        return spec, None

    def install(self, spec: str):
        name, ver = self._split(spec)
        if not ver:
            ver = self.repo.best_available(name)
            if not ver:
                print(f"[ERROR] {name} недоступен")
                return
            spec = f"{name}=={ver}"

        if name in self.installed and self.installed[name] != ver:
            print(f"[ERROR] Конфликт: {name}=={self.installed[name]} уже установлен, требуется {ver}")
            return

        # Создаём компонент
        deps = self.repo.get_deps(name, ver)
        leaf = PackageLeaf(f"{name}=={ver}", deps)
        self._install_component(leaf)

    def _install_component(self, component: 'PackageComponent'):
        for dep_spec in component.dependencies():
            dep_name, dep_ver = self._split(dep_spec)
            if dep_name in self.installed and self.installed[dep_name] != dep_ver:
                print(f"[ERROR] Конфликт зависимости: {dep_name}=={dep_ver} требуется, но установлен {self.installed[dep_name]}")
                return
            self.install(dep_spec)

        name = component.name()
        if name not in self.installed:
            self.installed[name] = component.version()
            self.components[name] = component
            self.history.append(component)
            print(f"[OK] Установлен {name}=={component.version()}")
        else:
            print(f"[INFO] {name}=={component.version()} уже установлен")

    def remove(self, spec: str):
        name, _ = self._split(spec)
        if name not in self.installed:
            print(f"[INFO] {name} не установлен")
            return

        dependents = [
            p for p, v in self.installed.items()
            if p != name and name in [d.split("==")[0] for d in self.repo.get_deps(p, v)]
        ]
        if dependents:
            print(f"[ERROR] Нельзя удалить {name}, требуется: {', '.join(dependents)}")
            return

        component = self.components[name]
        component.remove(self)
        print(f"[OK] Удалён {name}")

    def update(self, spec: str):
        name, _ = self._split(spec)
        if name not in self.installed:
            print(f"[ERROR] {name} не установлен")
            return

        best = self.repo.best_available(name)
        if not best or compare_versions(best, self.installed[name]) <= 0:
            print(f"[INFO] Нет обновления для {name}")
            return

        target_version = best
        to_update = self._collect_update_chain(name, target_version)

        for pkg_name in to_update:
            if pkg_name in self.installed:
                dependents = [
                    p for p, v in self.installed.items()
                    if p not in to_update and p != pkg_name
                       and pkg_name in [d.split("==")[0] for d in self.repo.get_deps(p, v)]
                ]
                if dependents:
                    print(f"[ERROR] Нельзя обновить {pkg_name}, требуется: {', '.join(dependents)}")
                    return

        for pkg_name in reversed(to_update):
            if pkg_name in self.installed:
                component = self.components[pkg_name]
                component.remove(self)
                print(f"[OK] Удалена старая версия {pkg_name}")

        self.install(f"{name}=={target_version}")

    def _collect_update_chain(self, root_name: str, target_version: str) -> List[str]:
        to_update = set()
        from collections import deque
        queue = deque([(root_name, target_version)])

        while queue:
            name, ver = queue.popleft()
            if name in to_update:
                continue
            to_update.add(name)

            deps = self.repo.get_deps(name, ver)
            for dep_spec in deps:
                dep_name, dep_ver = self._split(dep_spec)
                current_ver = self.installed.get(dep_name)
                if current_ver != dep_ver or dep_name not in self.installed:
                    queue.append((dep_name, dep_ver))

        return list(to_update)

    def list_installed(self):
        for n, v in sorted(self.installed.items()):
            print(f" - {n}=={v}")

    def show_tree(self):
        def _print(name: str, level: int, visited: set):
            if name in visited:
                return
            visited.add(name)
            ver = self.installed.get(name, "?")
            print("  " * level + f"- {name}=={ver}")
            component = self.components.get(name)
            if component:
                for dep in component.dependencies():
                    dep_name = dep.split("==")[0]
                    _print(dep_name, level + 1, visited)

        visited = set()
        for n in sorted(self.installed.keys()):
            if n not in visited:
                _print(n, 0, visited)

    def install_group(self, group_name: str, specs: List[str]):
        group = PackageGroup(group_name)
        for spec in specs:
            name, ver = self._split(spec)
            if not ver:
                ver = self.repo.best_available(name)
            full_spec = f"{name}=={ver}"
            leaf = PackageLeaf(full_spec, self.repo.get_deps(name, ver))
            group.add(leaf)
        group.install(self)
        self.components[group_name] = group
        self.history.append(group)

    def undo_last(self):
        if not self.history:
            print("[INFO] Нет действий для отмены")
            return
        last = self.history.pop()
        last.remove(self)
        print(f"[UNDO] Отменена установка: {last.name()}")