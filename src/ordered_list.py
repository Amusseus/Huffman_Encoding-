class Node:
    '''Node for use with doubly-linked list'''
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class OrderedList:
    '''A doubly-linked ordered list of items, from lowest (head of list) to highest (tail of list)'''

    def __init__(self):
        '''Use ONE dummy node as described in class
           ***No other attributes***
           DO NOT have an attribute to keep track of size'''
        self.head = None

    # none -> boolean
    # returns True if the list is empty
    def is_empty(self):
        '''Returns True if OrderedList is empty
            MUST have O(1) performance'''
        return self.head == None

    # object(comparable item) -> boolean
    # adds the item in the list based on order
    def add(self, item):
        '''Adds an item to OrderedList, in the proper location based on ordering of items
           from lowest (at head of list) to highest (at tail of list) and returns True.
           If the item is already in the list, do not add it again and return False.
           MUST have O(n) average-case performance'''
        item_node = Node(item)
        # check to see if item already exists in list
        if self.is_empty():
            self.head = item_node
        # special case when the item is smaller than the first item of the list
        elif item < self.head.data:
            self.head.prev = item_node
            item_node.next = self.head
            self.head = item_node
        else:
            added_item = False
            current_node = self.head
            pointer_node = self.head
            while current_node is not None and not added_item:
                if current_node.data < item:
                    current_node = current_node.next
                    pointer_node = pointer_node.next
                elif item < current_node.data:
                    temp_node = pointer_node.prev
                    pointer_node.prev = item_node
                    item_node.next = pointer_node
                    temp_node.next = item_node
                    item_node.prev = temp_node
                    added_item = True
            # special case when the item is bigger than the last item of the list 
            if not added_item:
                last_node = self.return_last_node(self.head)
                last_node.next = item_node
                item_node.prev = last_node
        return True

    # object(comparable item) -> boolean
    # removes item from the list       
    def remove(self, item):
        '''Removes the first occurrence of an item from OrderedList. If item is removed (was in the list) 
          returns True.  If item was not removed (was not in the list) returns False
           MUST have O(n) average-case performance'''
        if not self.search(item):
            return False
        # special case when only one item exists in the list
        if self.size() == 1:
            self.head = None
            return True
        current_node = self.head
        pointer_node = self.head
        while current_node is not None:
            if current_node.data == item:
                temp_node_prev = pointer_node.prev
                temp_node_next = pointer_node.next
                # if the item is the last item in the list
                if temp_node_next == None:
                    temp_node_prev.next =temp_node_next
                # if the item is the first item in the list
                elif temp_node_prev == None:
                    temp_node_next.prev = temp_node_prev
                    self.head = temp_node_next
                else:
                    temp_node_prev.next = temp_node_next
                    temp_node_next.prev = temp_node_prev
                return True
            current_node = current_node.next
            pointer_node = pointer_node.next

    # item -> num
    # gives the index of the item in the list
    def index(self, item):
        '''Returns index of the first occurrence of an item in OrderedList (assuming head of list is index 0).
           If item is not in list, return None
           MUST have O(n) average-case performance'''
        current_node = self.head
        index_num = 0
        while current_node is not None:
            if current_node.data == item:
                return index_num
            index_num +=1 
            current_node = current_node.next
        return None

    # num(index) -> item
    # returns the item at the given index and removes it from the list
    def pop(self, index):
        '''Removes and returns item at index (assuming head of list is index 0).
           If index is negative or >= size of list, raises IndexError
           MUST have O(n) average-case performance'''
        # to check if the index is in bounds
        if index < 0 or index >= self.size():
            raise IndexError
        current_node = self.head
        index_start = 0
        while current_node is not None:
            if index_start == index:
                return_temp = current_node.data
                self.remove(return_temp)
                return return_temp
            index_start += 1
            current_node = current_node.next

    def peek(self, index):
        '''Removes and returns item at index (assuming head of list is index 0).
           If index is negative or >= size of list, raises IndexError
           MUST have O(n) average-case performance'''
        # to check if the index is in bounds
        if index < 0 or index >= self.size():
            raise IndexError
        current_node = self.head
        index_start = 0
        while current_node is not None:
            if index_start == index:
                return_temp = current_node.data
                return return_temp
            index_start += 1
            current_node = current_node.next

    # item -> boolean
    # returns True if the item exists in the list, otherwise returns False
    def search(self, item):
        '''Searches OrderedList for item, returns True if item is in list, False otherwise"
           To practice recursion, this method must call a RECURSIVE method that
           will search the list
           MUST have O(n) average-case performance'''
        current_node = self.head
        temp_boolean = self.recur_lst(current_node,item)
        return temp_boolean

    # Node and item -> boolean
    # returns if the item exists in the list
    def recur_lst(self,nodex,item):
        if nodex == None:
            return False
        elif nodex.data == item:
            return True
        else:
            return self.recur_lst(nodex.next,item)

    # none -> list
    # returns python list version of Orderedlist from head to tail
    def python_list(self):
        '''Return a Python list representation of OrderedList, from head to tail
           For example, list with integers 1, 2, and 3 would return [1, 2, 3]
           MUST have O(n) performance'''
        lst_size = self.size()
        temp_lst = [None]*lst_size
        start_ind = 0
        current_node = self.head
        while current_node is not None:
            temp_lst[start_ind] = current_node.data
            start_ind +=1
            current_node = current_node.next
        return temp_lst

    # none -> list 
    # returns python list version of Orderedlist from tail
    def python_list_reversed(self):
        '''Return a Python list representation of OrderedList, from tail to head, using recursion
           For example, list with integers 1, 2, and 3 would return [3, 2, 1]
           To practice recursion, this method must call a RECURSIVE method that
           will return a reversed list
           MUST have O(n) performance'''
        if self.size() == 0:
            return []
        current_node = self.head
        last_node = self.return_last_node(current_node)
        return self.make_rev_python_lst(last_node)

    # node -> node
    # returns the last node linked to the given node
    def return_last_node(self,nodex):
        if nodex.next == None:
            return nodex
        else:
             return self.return_last_node(nodex.next)
    
    # node -> list 
    # returns a python list of the nodes starting from tail to head
    def make_rev_python_lst(self,nodex):
        if nodex == None:
            return []
        temp_lst = [nodex.data]
        return temp_lst + self.make_rev_python_lst(nodex.prev)

    # none -> int
    # returns the size of the list 
    def size(self):
        '''Returns number of items in the OrderedList
           To practice recursion, this method must call a RECURSIVE method that
           will count and return the number of items in the list
           MUST have O(n) performance'''
        current_node = self.head
        size_counter = self.calc_size(current_node)
        return size_counter

    # node -> int
    # recursive method to calculate size of list
    def calc_size(self,nodex):
        if nodex == None:
            return 0
        return 1 + self.calc_size(nodex.next)
    
    def printorderedlist(self):
      currentNode = self.head
      while currentNode is not None:
          print(currentNode.data)
          currentNode = currentNode.next