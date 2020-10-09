# Author: Luke LaCasse
# Date: October 9, 2020
# Title: ECE 241 Project 1: Binary Search Tree
# Description: A binary search tree to store COVID19 Cities


class BinarySearchTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.root.__iter__()

    def put(self, key, val):
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)
        self.size = self.size + 1

    def _put(self, key, val, cnode):
        if key < cnode.key:
            if cnode.hasLeftChild():
                self._put(key, val, cnode.leftChild)
            else:
                cnode.leftChild = TreeNode(key, val, parent=cnode)
        else:
            if cnode.hasRightChild():
                self._put(key, val, cnode.rightChild)
            else:
                cnode.rightChild = TreeNode(key, val, parent=cnode)

    def __setitem__(self, key, value):
        self.put(key, value)

    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None

    def _get(self, key, cnode):
        if not cnode:
            return None
        elif cnode.key == key:
            return cnode
        elif key < cnode.key:
            return self._get(key, cnode.leftChild)
        else:
            return self._get(key, cnode.rightChild)

    def __getitem__(self, key):
        return self.get(key)


class AVLTree(BinarySearchTree):

    def _put(self, key, val, cnode):
        if key < cnode.key:
            if cnode.hasLeftChild():
                self._put(key, val, cnode.leftChild)
            else:
                cnode.leftChild = TreeNode(key, val, parent=cnode)
                self.updateBalance(cnode.leftChild)
        else:
            if cnode.hasRightChild():
                self._put(key, val, cnode.rightChild)
            else:
                cnode.rightChild = TreeNode(key, val, parent=cnode)
                self.updateBalance(cnode.rightChild)

    def updateBalance(self, node):
        if node.balanceFactor > 1 or node.balanceFactor < -1:
            self.rebalance(node)
            return
        if node.parent is not None:
            if node.isLeftChild():
                node.parent.balanceFactor += 1
            elif node.isRightChild():
                node.parent.balanceFactor -= 1

            if node.parent.balanceFactor != 0:
                self.updateBalance(node.parent)

    def rotateLeft(self, rRoot):
        nRoot = rRoot.rightChild
        rRoot.rightChild = nRoot.leftChild
        if nRoot.leftChild is not None:
            nRoot.leftChild.parent = rRoot
        nRoot.parent = rRoot.parent
        if rRoot.isRoot():
            self.root = nRoot
        else:
            if rRoot.isLeftChild():
                rRoot.parent.leftChild = nRoot
            else:
                rRoot.parent.rightChild = nRoot
        nRoot.leftChild = rRoot
        rRoot.parent = nRoot
        rRoot.balanceFactor = rRoot.balanceFactor + 1 - min(nRoot.balanceFactor, 0)
        nRoot.balanceFactor = nRoot.balanceFactor + 1 + max(rRoot.balanceFactor, 0)

    def rotateRight(self, rRoot):
        nRoot = rRoot.leftChild
        rRoot.leftChild = nRoot.rightChild
        if nRoot.rightChild is not None:
            nRoot.rightChild.parent = rRoot
        nRoot.parent = rRoot.parent
        if rRoot.isRoot():
            self.root = nRoot
        else:
            if rRoot.isRightChild():
                rRoot.parent.rightChild = nRoot
            else:
                rRoot.parent.leftChild = nRoot
        nRoot.rightChild = rRoot
        rRoot.parent = nRoot
        rRoot.balanceFactor = rRoot.balanceFactor - 1 - max(nRoot.balanceFactor, 0)
        nRoot.balanceFactor = nRoot.balanceFactor - 1 + min(rRoot.balanceFactor, 0)

    def rebalance(self, node):
        if node.balanceFactor < 0:
            if node.rightChild.balanceFactor > 0:
                self.rotateRight(node.rightChild)
                self.rotateLeft(node)
            else:
                self.rotateLeft(node)
        elif node.balanceFactor > 0:
            if node.leftChild.balanceFactor < 0:
                self.rotateLeft(node.leftChild)
                self.rotateRight(node)
            else:
                self.rotateRight(node)

class TreeNode:

    def __init__(self, key, val, left = None, right = None, parent = None):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
        self.balanceFactor = 0

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent