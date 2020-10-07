def print_book_info(title, author=None, year=None):
    #  Write your code here
    written = " was written" if author or year else ""
    print(f""""{title}"{written}{" by " + author if author else ""}{" in " + year if year else ""}""")
