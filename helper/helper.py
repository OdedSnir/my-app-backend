# helper function used to check that code is the same
def codes_match(code: str, solution: str) -> bool:
    normalize = lambda s: ''.join(s.split())
    return normalize(code) == normalize(solution)