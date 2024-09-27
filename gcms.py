from bin import Bin
from node import Node
from avl import AVLTree,comp_id,usual_compare
from object import Object, Color
from exceptions import NoBinFoundException

class GCMS:
    def __init__(self):
        # Maintain all the Bins and Objects in GCMS
        self.object_id_tree = AVLTree(compare_function=comp_id, search='id')
        self.bin_id_tree = AVLTree(compare_function=comp_id, search='id')
        self.bin_cap_tree = AVLTree(compare_function=usual_compare, search='usual')
        pass 
    
    def add_bin_to_cap(self, bin):
        if self.bin_cap_tree.search_value(bin.cap) == None:
            self.bin_cap_tree.insert_node(Node(bin.cap))
        temp = self.bin_cap_tree.search_value(bin.cap)
        if temp.store is None:
            temp.store = AVLTree(compare_function=comp_id, search='id')
        temp.store.insert_node(Node(bin))


    def add_bin(self, bin_id, capacity):
        temp_bin = Bin(bin_id, capacity)
        # print('temp_bin: ',temp_bin)
        self.bin_id_tree.insert_node(Node(temp_bin))
        if self.bin_cap_tree.search_value(capacity) == None:
            self.bin_cap_tree.insert_node(Node(capacity))
        temp = self.bin_cap_tree.search_value(capacity)
        if temp.store is None:
            temp.store = AVLTree(compare_function=comp_id, search='id')
        temp.store.insert_node(Node(temp_bin))
        pass

    def add_object(self, object_id, size, colour):
        obj = Object(object_id, size, colour)
        self.object_id_tree.insert_node(Node(obj))
        if colour.value == 1:
            if self.bin_cap_tree.find_compact(size) is not None:
                req_bin = self.bin_cap_tree.find_compact(size).store.min_node().key
                req_bin_node = self.bin_cap_tree.search_value(req_bin.cap).store.search_value(req_bin.id)
                self.bin_cap_tree.search_value(req_bin.cap).store.delete_node(req_bin_node)
                if self.bin_cap_tree.search_value(req_bin.cap).store.root == None:
                    self.bin_cap_tree.delete_node(self.bin_cap_tree.search_value(req_bin.cap))
                req_bin.bin_add_object(obj)
                self.add_bin_to_cap(req_bin)
                return 
        if colour.value == 2:
            if self.bin_cap_tree.find_compact(size) is not None:
                req_bin = self.bin_cap_tree.find_compact(size).store.max_node().key
                req_bin_node = self.bin_cap_tree.search_value(req_bin.cap).store.search_value(req_bin.id)
                self.bin_cap_tree.search_value(req_bin.cap).store.delete_node(req_bin_node)
                if self.bin_cap_tree.search_value(req_bin.cap).store.root == None:
                    self.bin_cap_tree.delete_node(self.bin_cap_tree.search_value(req_bin.cap))
                req_bin.bin_add_object(obj)
                self.add_bin_to_cap(req_bin)
                return
        if colour.value == 3:
            if self.bin_cap_tree.max_node().key >= size:
                req_bin = self.bin_cap_tree.max_node().store.min_node().key
                req_bin_node = self.bin_cap_tree.search_value(req_bin.cap).store.search_value(req_bin.id)
                self.bin_cap_tree.search_value(req_bin.cap).store.delete_node(req_bin_node)
                if self.bin_cap_tree.search_value(req_bin.cap).store.root == None:
                    self.bin_cap_tree.delete_node(self.bin_cap_tree.search_value(req_bin.cap))
                req_bin.bin_add_object(obj)
                self.add_bin_to_cap(req_bin)
                return
        if colour.value == 4:
            if self.bin_cap_tree.max_node().key >= size:
                req_bin = self.bin_cap_tree.max_node().store.max_node().key
                req_bin_node = self.bin_cap_tree.search_value(req_bin.cap).store.search_value(req_bin.id)
                self.bin_cap_tree.search_value(req_bin.cap).store.delete_node(req_bin_node)
                if self.bin_cap_tree.search_value(req_bin.cap).store.root == None:
                    self.bin_cap_tree.delete_node(self.bin_cap_tree.search_value(req_bin.cap))
                req_bin.bin_add_object(obj)
                self.add_bin_to_cap(req_bin)
                return
        raise NoBinFoundException

    def delete_object(self, object_id):
        # Implement logic to remove an object from its bin
        obj_node = self.object_id_tree.search_value(object_id)
        req_bin = obj_node.key.bin
        req_bin_node = self.bin_cap_tree.search_value(req_bin.cap).store.search_value(req_bin.id)
        self.bin_cap_tree.search_value(req_bin.cap).store.delete_node(req_bin_node)
        if self.bin_cap_tree.search_value(req_bin.cap).store.root == None:
            self.bin_cap_tree.delete_node(self.bin_cap_tree.search_value(req_bin.cap))
        req_bin.remove_object(object_id)
        self.add_bin_to_cap(req_bin)
        self.object_id_tree.delete_node(obj_node)
        pass

    def bin_info(self, bin_id):
        # returns a tuple with current capacity of the bin and the list of objects in the bin (int, list[int])
        bin = self.bin_id_tree.search_value(bin_id).key
        return (bin.cap , bin.object_tree.inorder_list())
        # return (bin.cap, ) Implement inorder list here
        pass

    def object_info(self, object_id):
        # returns the bin_id in which the object is stored
        return self.object_id_tree.search_value(object_id).key.bin.id
        pass
    
# gcms = GCMS()

# gcms.add_bin(1234, 10)
# gcms.add_bin(4321, 20)
# gcms.add_bin(1111, 15)

# try:
#     gcms.add_object(8989, 6, Color.RED )
# except: 
#     print("Object 1 was not able to be added")
    
# try:
#     gcms.add_object(2892, 8, Color.YELLOW )
# except: 
#     print("Object 2 was not able to be added")

# try:
#     gcms.add_object(4839, 9, Color.RED )
# except: 
#     print("Object 3 was not able to be added")

# try:
#     gcms.add_object(3283, 2, Color.BLUE )
# except: 
#     print("Object 4 was not able to be added")

# try:
#     gcms.add_object(8983, 8, Color.RED )
# except: 
#     print("Object 5 was not able to be added")

# gcms.delete_object(8989)
        


# print(gcms.bin_info(1234))
# print(gcms.bin_info(4321))
# print(gcms.bin_info(1111))

