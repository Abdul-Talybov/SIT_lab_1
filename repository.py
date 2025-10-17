from typing import Dict, List, Optional
import functools
from utils import compare_versions

class PackageRepository:
    def __init__(self):
        self.repo: Dict[str, Dict[str, List[str]]] = {}

    def add_package(self, name: str, version: str, deps: Optional[List[str]] = None):
        self.repo.setdefault(name, {})[version] = deps or []

    def available_versions(self, name: str) -> List[str]:
        return list(self.repo.get(name, {}).keys())

    def best_available(self, name: str) -> Optional[str]:
        versions = self.available_versions(name)
        if not versions: return None
        return max(versions, key=functools.cmp_to_key(lambda a,b: compare_versions(a,b)))

    def get_deps(self, name: str, version: str) -> List[str]:
        return self.repo.get(name, {}).get(version, [])
