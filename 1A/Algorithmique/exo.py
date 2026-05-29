class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.last = None
        pass
class double_linked_list:
    def __init__(self):
        self.head = None
        self.tail = None
        pass
    def add(self, value):
        new_node = Node(value)
        if self.head == None:
            self.head = new_node
            self.tail = new_node
        else:
            
            self.tail.next = new_node
            new_node.next = None
        pass
    def remove(self, value):
        current_node = self.head
        while current_node != None:
            if current_node.value == value:
                if current_node == self.head:
                    self.head = current_node.next
                    self.head.last = None
                elif current_node == self.tail:
                    self.tail = current_node.last
                    self.tail.next = None
                else:
                    current_node.last.next = current_node.next
                    current_node.next.last = current_node.last
                break
            current_node = current_node.next
        pass
    def __str__(self):
        current_node = self.head
        result = []
        while current_node != None:
            result.append(str(current_node.value))
            current_node = current_node.next
        return '->'.join(result)
    pass
    
a= double_linked_list()
b= Node(1)
c= Node(2)
a.head = b
a.tail = c
a.add(1)
a.add(2)
a.add(3)
a.add(4)
print(a.head.value)
print(a.tail.value)
