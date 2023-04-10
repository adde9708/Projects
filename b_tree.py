def b_tree(node1=0, node2=1):
    key1 = {node1: node2}
    key2 = {node2: node1}
    keys = (key1, key2)
    max_len = max(len(key1), len(key2))
    min_len = min(len(key1), len(key2))
    for leaf_page in keys:
        print(leaf_page)
        if len(leaf_page) > max_len or len(leaf_page) < min_len:
            return leaf_page
    return leaf_page


b_tree()
