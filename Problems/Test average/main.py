def average_mark(*marks):
    return round(sum(mark for mark in marks) / len(marks), 1)
