from node import *

class OSTree():
    def __init__(self):
        self.nil = NIL()
        self.nil.left = self.nil
        self.nil.right = self.nil
        self.root = self.nil

    def leftRotate(self, node):
        r = node.right
        node.right = r.left

        if r.left != self.nil:
            r.left.parent = node
        
        r.parent = node.parent

        if node.parent == self.nil:
            self.root = r
        elif node == node.parent.left:
            node.parent.left = r
        else:
            node.parent.right = r

        r.left = node
        node.parent = r

        # update size
        r.size = node.size
        node.size = node.left.size + node.right.size + 1

    def rightRotate(self, node):
        l = node.left
        node.left = l.right

        if l.right != self.nil:
            l.right.parent = node

        l.parent = node.parent

        if node.parent == self.nil:
            self.root = l
        elif node == node.parent.right:
            node.parent.right = l
        else:
            node.parent.left = l

        l.right = node
        node.parent = l
        
        # update size
        l.size = node.size
        node.size = node.left.size + node.right.size + 1


    def insert(self, key):
        # check duplicity first to efficiently maintain node sizes
        if self.find(self.root, key) != self.nil:
            return 0

        z = Node(key, self.nil, self.nil)
        y = self.nil
        x = self.root

        while x != self.nil:
            y = x
            # update size
            y.size += 1

            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y

        if y == self.nil:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        
        w = z
        while w != self.root:
            w.parent.size = w.parent.left.size + w.parent.right.size + 1
            w = w.parent

        self.insertFixup(z)
        return key

    def insertFixup(self, z):
        while z.parent.color == 'R':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                # case 1
                if y.color == 'R': 
                    z.parent.color = 'B'
                    y.color = 'B'
                    z.parent.parent.color = 'R'
                    z = z.parent.parent
                
                else:
                    # case 2
                    if z == z.parent.right: 
                        z = z.parent
                        self.leftRotate(z)
                    # case 3
                    z.parent.color = 'B'
                    z.parent.parent.color = 'R'
                    self.rightRotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                # case 1
                if y.color == 'R':
                    z.parent.color = 'B'
                    y.color = 'B'
                    z.parent.parent.color = 'R'
                    z = z.parent.parent
                
                else:
                    # case 2
                    if z == z.parent.left:
                        z = z.parent
                        self.rightRotate(z)

                    # case 3
                    z.parent.color = 'B'
                    z.parent.parent.color = 'R'
                    self.leftRotate(z.parent.parent)
        self.root.color = 'B'

    def transplant(self, u, v):
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def find(self, node, key):
        if node == self.nil:
            return node
        elif key == node.key:
            return node
        elif key < node.key:
            return self.find(node.left, key)
        else:
            return self.find(node.right, key)

    def treeMinimum(self, node):
        if node.left == self.nil:
            return node
        else:
            return self.treeMinimum(node.left)

    def delete(self, key):
        # check duplicity first to efficiently maintain node sizes
        z = self.find(self.root, key)
        if z == self.nil:
            return 0

        y = z
        yOriginalColor = y.color

        if z.left == self.nil:
            x = z.right
            self.transplant(z, z.right)

        elif z.right == self.nil:
            x = z.left
            self.transplant(z, z.left)

        else:
            y = self.treeMinimum(z.right)
            yOriginalColor = y.color
            x = y.right

            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
                
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
            # update size
            y.size = z.size

        # update size
        w = x
        while w != self.root:
            w.parent.size -= 1
            w = w.parent

        if yOriginalColor == 'B':
            self.deleteFixup(x)

        return key

    def deleteFixup(self, x):
        while x != self.root and x.color == 'B':
            if x == x.parent.left:
                w = x.parent.right
                # case 1
                if w.color == 'R':
                    w.color = 'B'
                    x.parent.color = 'R'
                    self.leftRotate(x.parent)
                    w = x.parent.right
                # case 2
                if w.left.color == 'B' and w.right.color == 'B':
                    w.color = 'R'
                    x = x.parent
                else:
                    # case 3
                    if w.right.color == 'B':
                        w.left.color = 'B'
                        w.color = 'R'
                        self.rightRotate(w)
                        w = x.parent.right
                    # case 4
                    w.color = x.parent.color
                    x.parent.color = 'B'
                    w.right.color = 'B'
                    self.leftRotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                # case 1
                if w.color == 'R':
                    w.color = 'B'
                    x.parent.color = 'R'
                    self.rightRotate(x.parent)
                    w = x.parent.left
                # case 2
                if w.right.color == 'B' and w.left.color == 'B':
                    w.color = 'R'
                    x = x.parent
                else:
                    # case 3
                    if w.left.color == 'B':
                        w.right.color ='B'
                        w.color = 'R'
                        self.leftRotate(w)
                        w = x.parent.left
                    # case 4
                    w.color = x.parent.color
                    x.parent.color = 'B'
                    w.left.color = 'B'
                    self.rightRotate(x.parent)
                    x = self.root
        x.color = 'B'


    def osSelect(self, i):
        if i > self.root.size:
            return 0
        else:
            return self.select(self.root, i).key

    def select(self, x, i):
        r = x.left.size + 1
        if i == r:
            return x
        elif i < r:
            return self.select(x.left, i)
        else:
            return self.select(x.right, i-r)
    
    def osRank(self, key):
        x = self.find(self.root, key)
        if x == self.nil:
            return 0
        else:
            return self.rank(x)
    
    def rank(self, x):
        r = x.left.size + 1
        y = x
        while y != self.root:
            if y == y.parent.right:
                r = r + y.parent.left.size + 1
            y = y.parent
        return r