from avl import AVLTree,comp_id
from object import Object, Color
from node import Node

class Bin:
    def __init__(self, bin_id, capacity):
        self.id = bin_id
        self.cap = capacity
        self.object_tree = AVLTree(compare_function=comp_id, search= 'id')

    def bin_add_object(self, object):
        # Implement logic to add an object to this bin
        object.bin = self
        self.cap -= object.size
        self.object_tree.insert_node(Node(object))
        pass

    def remove_object(self, object_id):
        # Implement logic to remove an object by ID
        temp_obj_node = self.object_tree.search_value(object_id)
        self.cap += temp_obj_node.key.size
        self.object_tree.delete_node(temp_obj_node)
        pass
