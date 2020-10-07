def find_my_list(all_list, my_list):
    for i, lst in enumerate(all_list):
        # Change the next line
        if id(my_list) == id(lst):
            return i
    return None
