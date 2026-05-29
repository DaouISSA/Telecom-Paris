class Node():
    def __init__(self, data):
        self.data = data
        self.next = None
class LinkedList():
    def __init__(self):
        self.head = None
    def ajouter (self,data):
        new_node=Node(data)
        if self.head is None:
            self.head=new_node
        else:
            curent=self.head
            while curent.next is not None:
                curent=curent.next
            curent.next=new_node
            new_node.next=None
    def afficher(self):
        current=self.head 
        while current is not None:
            print(current.data)
            current=current.next
    def inverser(self): 
        curent = self.head
        while curent.next is not None:
            curent
            curent=curent.next
t=23.18
hours = int(t)
minutes= int((t-hours)*60)
secondes= ((t-hours)*60-minutes)*60
print(hours)
print(minutes)
print(secondes)

#print(int(0.9))


