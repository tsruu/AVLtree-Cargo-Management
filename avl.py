from node import Node

def usual_compare(node_1,node_2):
    return node_1.key > node_2.key

def comp_id(node_1, node_2):
    return node_1.key.id > node_2.key.id

class AVLTree:
    def __init__(self, compare_function = usual_compare, search = 'usual'):
        self.root = None
        self.size = 0
        self.comparator = compare_function
        self.search_mode = search
        
    def height(self, node):
        if node is not None:
            return node.height
        return -1
            
    def balance(self, node):
        if node:
            return self.height(node.left) - self.height(node.right)
        return 0
    
    def min_node(self):
        current = self.root
        while current.left:
            current = current.left
        return current
    
    def max_node(self):
        current = self.root
        while current.right:
            current = current.right
        return current

    def del_min_node(self, root):
        current = root
        while current.left:
            current = current.left
        return current
        
    def isleaf(self, node):
        return node.left is None and node.right is None
    
    def left_rotate(self,z):
        y = z.right
        T2 = y.left
        
        y.left = z
        z.right = T2
        
        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        
        return y
    
    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y
        
    def insert(self, root, node):
        if not root:
            return node
        elif self.comparator(root,node):
            root.left = self.insert(root.left, node)
        else:
            root.right = self.insert(root.right, node)
        
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)
        
        if balance > 1 and self.comparator(root.left, node):
            return self.right_rotate(root)

        if balance < -1 and self.comparator(node, root.right):
            return self.left_rotate(root)

        if balance > 1 and self.comparator(node, root.left):
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and self.comparator(root.right, node):
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root
        
    def delete(self, root, node):
        if not root:
            return root

        if self.comparator(root, node):
            root.left = self.delete(root.left, node)
        elif self.comparator(node,root):
            root.right = self.delete(root.right, node)
        else:
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp
            
            temp = self.del_min_node(root.right)
            root.key = temp.key
            root.store = temp.store
            root.right = self.delete(root.right, temp)

        if not root:
            return root

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)

        # Left rotation
        if balance > 1 and self.balance(root.left) >= 0:
            return self.right_rotate(root)

        # Right rotation
        if balance < -1 and self.balance(root.right) <= 0:
            return self.left_rotate(root)

        # Left-Right rotation
        if balance > 1 and self.balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right-Left rotation
        if balance < -1 and self.balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root
    
    def search(self, root, node):
        if self.search_mode == 'usual':
            if not root or root.key == node.key:
                return root
            if self.comparator(node, root):
                return self.search(root.right, node)
            return self.search(root.left, node)
        elif self.search_mode == 'id':
            if not root or root.key.id == node.key.id:
                return root
            if self.comparator(node, root):
                return self.search(root.right, node)
            return self.search(root.left, node)
    
    def search_val(self, root, value):
        if self.search_mode == 'usual':
            if not root or root.key == value:
                return root
            if value > root.key:
                return self.search_val(root.right, value)
            return self.search_val(root.left, value)
        elif self.search_mode == 'id':
            if not root or root.key.id == value:
                return root
            if value > root.key.id:
                return self.search_val(root.right, value)
            return self.search_val(root.left, value)

    def insert_node(self, node):
        self.root = self.insert(self.root, node)

    def delete_node(self, node):
        self.root = self.delete(self.root, node)

    def search_node(self, node):
        return self.search(self.root, node)
    
    def search_value(self, value):
        return self.search_val(self.root, value)
    
    def inorder_traversal(self,root, list):
        if root:
            self.inorder_traversal(root.left, list)
            list.append(root.key.id),
            self.inorder_traversal(root.right, list)

    def inorder_list(self):
        list = []
        self.inorder_traversal(self.root, list)
        return list
        
    def min_greater_than(self, root, value):
        out = None
        while root:
            if root.key == value:
                return root
            elif root.key > value:
                out = root
                root = root.left
            else:
                root = root.right
        return out

    def find_compact(self,value):
        return self.min_greater_than(self.root, value)

# tree = AVLTree()
# tree.insert_node(Node(10))
# tree.insert_node(Node(20))
# print(tree.delete_node(Node(10)))
# print(tree.root)
# print(tree.delete_node(Node(20)))
# print(tree.root)

# def in_traversal(root):
#     if root:
#         in_traversal(root.left)
#         print(root.key),
#         in_traversal(root.right)


# tree = AVLTree()
# for i in range(10):
#     tree.insert_node(Node(i*5))

# in_traversal(tree.root)

# a = tree.search_value(10)
# tree.delete_node(a)

# b = tree.search_value(15)
# tree.delete_node(b)

# in_traversal(tree.root)
