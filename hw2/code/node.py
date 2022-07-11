class Node():
    def __init__(self, key, left, right, size=1, color='R'):
        
        self.left = left
        self.right = right

        self.parent = None
        
        self.key = key
        self.size = size
        self.color = color

class NIL(Node):
    def __init__(self):
        Node.__init__(self, -1, None, None, size=0, color='B')
