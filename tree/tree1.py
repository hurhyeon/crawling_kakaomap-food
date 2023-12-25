class Node:
    def __init__(self, value):
        self.value = value 
        self.right = None 
        self.left = None 
        
head = Node(1)
print(  head.value,
        head.right,
        head.left)