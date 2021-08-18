count = 0
def bitcount(n, count=None):
    while n:
        n ^= n - 1
        count += 1
    return count
