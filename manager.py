# manager.py
from typing import Dict, Set, Optional, Tuple
from repository import PackageRepository
from utils import compare_versions

class PackageManager:
    def __init__(self, repo: PackageRepository):
        self.repo = repo
        self.installed: Dict[str, str] = {}

    def _split(self, spec: str):
        if "==" in spec:
            return tuple(spec.split("==", 1))
        return spec, None

    def install(self, spec: str):
        name, ver = self._split(spec)
        if not ver:
            ver = self.repo.best_available(name)
        if not ver or name not in self.repo.repo or ver not in self.repo.repo[name]:
            print(f"[ERROR] {spec} недоступен")
            return
        if name in self.installed and self.installed[name] == ver:
            print(f"[INFO] {name}=={ver} уже установлен")
            return

        # Установка зависимостей
        for dep in self.repo.get_deps(name, ver):
            self.install(dep)

        self.installed[name] = ver
        print(f"[OK] Установлен {name}=={ver}")

    def remove(self, spec: str):
        name, _ = self._split(spec)
        # Проверка зависимостей
        dependents = [p for p,v in self.installed.items() if name in [d.split("==")[0] for d in self.repo.get_deps(p,v)]]
        if dependents:
            print(f"[ERROR] Нельзя удалить {name}, требуется: {dependents}")
            return
        if name in self.installed:
            del self.installed[name]
            print(f"[OK] Удалён {name}")
        else:
            print(f"[INFO] {name} не установлен")

    def update(self, spec: str):
        name, _ = self._split(spec)
        if name not in self.installed:
            print(f"[ERROR] {name} не установлен")
            return
        best = self.repo.best_available(name)
        if compare_versions(best, self.installed[name]) > 0:
            self.install(f"{name}=={best}")
        else:
            print(f"[INFO] Нет обновления для {name}")

    def list_installed(self):
        for n,v in sorted(self.installed.items()):
            print(f" - {n}=={v}")

    def show_tree(self):
        def _print(name: str, level: int):
            ver = self.installed.get(name, "?")
            print("  "*level + f"- {name}=={ver}")
            for dep in self.repo.get_deps(name, ver):
                _print(dep.split("==")[0], level+1)
        for n in sorted(self.installed.keys()):
            _print(n, 0)