def parse_version(ver: str):
    return tuple(int(p) for p in ver.split("."))

def compare_versions(a: str, b: str):
    pa, pb = parse_version(a), parse_version(b)
    return (pa > pb) - (pa < pb)