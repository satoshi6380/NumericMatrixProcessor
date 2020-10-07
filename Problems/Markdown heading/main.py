def heading(s, n=1):
    if n < 1:
        n = 1
    elif n > 6:
        n = 6
    return f"{'#' * n} {s}"
