# Utility functions


# List occurrences of ch in s
def list_occurences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]


def get_full_class_name(obj):
    # obj.__class__ comes out like "<class 'lv.Obj'>"
    # So strip all the other junk
    dirty_name = str(obj.__class__)
    single_qs = list_occurences(dirty_name, '\'')
    return dirty_name[single_qs[0]+1:single_qs[1]]
