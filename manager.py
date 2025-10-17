from typing import Dict, Set, Optional, Tuple
from repository import PackageRepository
from utils import compare_versions

class PackageManager:
    def __init__(self, repo: PackageRepository):
        self.repo = repo
        self.installed: Dict[str, str] = {}
        self.reverse_deps: Dict[str, Set[str]] = {}

    def _split(self, spec: str) -> Tuple[str, Optional[str]]:
        if "==" in spec:
            n,v = spec.split("==",1)
            return n, v
        return spec, None

    def _ensure_reverse(self, name: str):
        self.reverse_deps.setdefault(name, set())

    def _add_reverse_dep(self, dep: str, parent: str):
        self._ensure_reverse(dep)
        self.reverse_deps[dep].add(parent)

    def _remove_reverse_dep(self, dep: str, parent: str):
        if dep in self.reverse_deps and parent in self.reverse_deps[dep]:
            self.reverse_deps[dep].remove(parent)

    def _has_conflict(self, name: str, target_version: str) -> bool:
        for pkg, ver in self.installed.items():
            if pkg == name:
                continue
            deps = self.repo.get_deps(pkg, ver)
            for d in deps:
                dn, dv = self._split(d)
                if dn == name and dv and dv != target_version:
                    return True
        return False

    def is_installed(self, spec: str) -> bool:
        name, ver = self._split(spec)
        if name not in self.installed:
            return False
        if ver is None:
            return True
        return self.installed[name] == ver

    def install(self, spec: str) -> None:
        name, ver = self._split(spec)
        if ver is None:
            ver = self.repo.best_available(name)
            if ver is None:
                print(f"[ERROR] Пакет {name} не найден.")
                return
        if name not in self.repo.repo or ver not in self.repo.repo[name]:
            print(f"[ERROR] {name}=={ver} недоступен.")
            return
        if name in self.installed and self.installed[name] == ver:
            print(f"[INFO] {name}=={ver} уже установлен.")
            return

        snapshot_installed = dict(self.installed)
        snapshot_reverse = {k:set(v) for k,v in self.reverse_deps.items()}

        deps = self.repo.get_deps(name, ver)
        for d in deps:
            dn, dv = self._split(d)
            if dv is None:
                dv = self.repo.best_available(dn)
                if dv is None:
                    print(f"[ERROR] Зависимость {dn} не найдена.")
                    self.installed = snapshot_installed
                    self.reverse_deps = snapshot_reverse
                    return
                d = f"{dn}=={dv}"
            if dn in self.installed and self.installed[dn] != dv:
                if self._has_conflict(dn, dv):
                    print(f"[CONFLICT] Невозможно обновить {dn} до {dv}.")
                    self.installed = snapshot_installed
                    self.reverse_deps = snapshot_reverse
                    return
                else:
                    print(f"[INFO] Обновление {dn} {self.installed[dn]} -> {dv}")
                    self.installed[dn] = dv
            elif dn not in self.installed:
                print(f"[INFO] Установка зависимости {d}.")
                self.install(d)
            self._add_reverse_dep(dn, name)

        self.installed[name] = ver
        print(f"[OK] Установлен {name}=={ver}. Состояние: {self.installed}")

    def remove(self, spec: str) -> None:
        name, _ = self._split(spec)
        if name not in self.installed:
            print(f"[INFO] {name} не установлен.")
            return
        dependents = self.reverse_deps.get(name, set())
        if dependents:
            print(f"[ERROR] Нельзя удалить {name}, на него ссылаются: {dependents}")
            return
        ver_inst = self.installed.get(name)
        deps = self.repo.get_deps(name, ver_inst) if name in self.repo.repo and ver_inst in self.repo.repo[name] else []
        for d in deps:
            dn, _ = self._split(d)
            self._remove_reverse_dep(dn, name)
        del self.installed[name]
        if name in self.reverse_deps and not self.reverse_deps[name]:
            del self.reverse_deps[name]
        print(f"[OK] Удалён {name}. Состояние: {self.installed}")

    def update(self, spec: str) -> None:
        name, ver = self._split(spec)
        if name not in self.installed:
            print(f"[ERROR] {name} не установлен.")
            return
        current = self.installed[name]
        best = ver or self.repo.best_available(name)
        if best is None:
            print(f"[ERROR] Нет доступных версий {name}.")
            return
        if compare_versions(best, current) <= 0:
            print(f"[INFO] Нет более новой версии для {name}. Текущая: {current}")
            return
        print(f"[INFO] Обновление {name} {current} -> {best}")
        self.install(f"{name}=={best}")

    def list_installed(self) -> None:
        if not self.installed:
            print("[INFO] Ничего не установлено.")
            return
        print("Установленные пакеты:")
        for n,v in sorted(self.installed.items()):
            deps = self.repo.get_deps(n, v) if n in self.repo.repo and v in self.repo.repo[n] else []
            print(f" - {n}=={v}, deps: {deps}, reverse_deps: {sorted(self.reverse_deps.get(n, []))}")

    def show_tree(self, name: Optional[str]=None) -> None:
        if name:
            if name not in self.installed:
                print(f"[INFO] {name} не установлен.")
                return
            self._print_tree(name, 0, set())
        else:
            for n in sorted(self.installed.keys()):
                self._print_tree(n, 0, set())

    def _print_tree(self, name: str, level: int, seen: Set[str]) -> None:
        if name in seen:
            print("  "*level + f"- {name} (cyclic)")
            return
        seen.add(name)
        ver = self.installed.get(name, "?")
        print("  "*level + f"- {name}=={ver}")
        deps = self.repo.get_deps(name, ver) if name in self.repo.repo and ver in self.repo.repo[name] else []
        for d in deps:
            dn, _ = self._split(d)
            if dn in self.installed:
                self._print_tree(dn, level+1, seen)
            else:
                print("  "*(level+1) + f"- {d} (not installed)")
