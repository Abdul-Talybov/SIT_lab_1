from typing import Tuple

def parse_version(ver: str) -> Tuple[int, ...]:
    return tuple(int(p) for p in ver.split("."))

def compare_versions(a: str, b: str) -> int:
    pa, pb = parse_version(a), parse_version(b)
    return (pa > pb) - (pa < pb)
