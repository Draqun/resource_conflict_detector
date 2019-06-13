class Tree:
    def __init__(self, body, nesting, function, parent):
        self.body = body
        self.nesting = nesting
        self.function = function
        self.right = None
        self.left = None
        self.parent = parent
        self.pthread_mutex_locked = True

    def __repr__(self):
        return 'Tree<{}>'.format(self.body)


def build_tree(tokens):
    root = list()
    for token, nesting, func in tokens:
        while "handler" in locals() and handler.parent and handler.nesting != nesting - 1:
            handler = handler.parent
        if nesting == 1:
            tree = Tree(token, nesting, func, None)
            root.append(tree)
            handler = tree
            continue
        if token.startswith("if"):
            handler.right = Tree(token, nesting, func, handler)
            handler = handler.right
        elif token.startswith("else"):
            handler.left = Tree(token, nesting, func, handler)
            handler = handler.left
        elif token.startswith("pthread_mutex_unlock"):
            handler.pthread_mutex_locked = False
    return root


def is_deadlock(tree, container):
    if tree.right is None and tree.left is None:
        if tree.pthread_mutex_locked:
            container.append(tree)
            return container
    if tree.right:
        container = is_deadlock(tree.right, container)
    if tree.left:
        container = is_deadlock(tree.left, container)
    return container
