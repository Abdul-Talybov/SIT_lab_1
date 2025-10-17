from typing import Tuple

def parse_version(ver: str) -> Tuple[int, ...]:
    parts = ver.split(".")
    nums = []
    for p in parts:
        try:
            nums.append(int(p))
        except ValueError:
            nums.append(sum(ord(ch) for ch in p))
    return tuple(nums)

def compare_versions(a: str, b: str) -> int:
    pa, pb = parse_version(a), parse_version(b)
    if pa < pb: return -1
    if pa > pb: return 1
    return 0
