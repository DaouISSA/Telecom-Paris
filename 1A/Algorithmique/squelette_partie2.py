# skewbinarylists.py

from completetrees import Node

class SkewBinaryList():
    def __init__(self, hd = None, tl = None):
        if not(isinstance(hd, Node)):
            raise ValueError("Arguments are not of the right type")
        self.head = hd
        if not(isinstance(tl, SkewBinaryList) or tl is None):
            raise ValueError("Arguments are not of the right type")
        self.next = tl
    def cons(self, item):
        if self.next is None :
            return SkewBinaryList(Node(item), self)
        elif self.head.height == self.next.head.height:
            return SkewBinaryList(Node(item, self.head, self.next.head), self.next.next)
        else:
            return SkewBinaryList(Node(item), self)
        pass
    def to_list(self):
        if self.next is None:
            return self.head.to_list()
        return [self.head.to_list()] + [self.next.to_list()]
        pass
    def __contains__(self, item):
        if self.next is None:
            return item in self.head
        return item in self.head or item in self.next

        pass
    def __len__(self):
        if self.next is None:
            return len(self.head)
        else: 
            return len(self.head) + len(self.next)
        pass
    def __getitem__(self, key):
        if key not in range(len(self)):
            raise IndexError("Index out of range")
        elif key <len(self.head):
            return self.head[key-1]
        else:
            return self.next[key-len(self.head)-1]
        pass
    def tail(self):
        self.next
        pass

if __name__ == "__main__":
    print("Exécution terminée")

a3= Node(28,Node(40,Node(11),Node(12)), Node(27,Node(7),Node(55)))
a2= Node(34,Node(23),Node(11))
b1 = SkewBinaryList(a3, SkewBinaryList(a2, SkewBinaryList(Node(92))))
#print(b1.to_list())
print(b1.tail().to_list()) 
