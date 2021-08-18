def bitcount(n):
    count = 0
    if count is not None:
        while n:
            n &= n - 1
            count += 1
        return count

