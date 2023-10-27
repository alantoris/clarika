def check_deep_children_structure(structure):
    """
    Recursive functionality for checking the deep of the data for creating new node
    """
    max = 0
    for child in structure["children"]:
        deep = 1 + check_deep_children_structure(child)
        if deep > max:
            max = deep
    return max
