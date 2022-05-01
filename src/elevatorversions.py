def elevatorversions(l):
    """
        `elevatorversions(l)`
    Given a list `l` of major.minor.patch version number strings, sort them into increasing order and return the sorted list.

    Each of major, minor, patch represents an int >= 0. Minor and patch are optional, but if patch is given minor must also
    be given. (I.e. no string of the form "major..patch".) Missing minor and patch numbers are equivalent to 0.
    
    Major is required.
    
    If two version numbers are equal but have a different number of components (e.g. 2, 2.0, 2.0.0),
    then subsort these by increasing number of components.

    No instruction is given on comparing e.g. "1.01" vs. "1.1". We'll try first off dropping the leading zeros and see
    if the verifier is happy with that, so that ["1.01", "1.1"] will return ["1.1", "1.1"]. 
    """

    vs = [[int(v) for v in x.split('.')] for x in l]

    return ['.'.join(str(u) for u in v) for v in sorted(vs)]