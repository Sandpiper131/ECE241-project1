# Author: Luke LaCasse
# Date: October 1, 2020
# Title: ECE 241 Project 1: Sorting and Searching
# Description:

#from BinarySearchTree import BinarySearchTree

class City:

    def __init__(self, cid, cname, cstate, pop, cities):
        self.cid = cid
        self.cname = cname
        self.cstate = cstate
        self.pop = pop
        self.cities = cities

    def __str__(self):
        return "cid: %s; cname: %s; cstate: %s; cases:%s" % (self. cid, self.cname, self.cstate, self.cities)


class COV19Library:

    def __init__(self):
        self.cityArray = []
        self.size = 0
        self.isSorted = False
        #self.BST = None
        self.root = None

    def LoadData(self, filename):
        file = open(filename, "r")  # open csv file as read-only
        file.readline()  # skip first line
        while True:
            cindex = []  # keeps track of comma indexes per line
            index = 0
            line = file.readline()  # read line of the input file
            for char in line:  # sort through the line character by character
                if char == ',': cindex.append(index)  # add index to location to cindex if ',' is found
                index += 1
            if len(cindex) == 0: break
            citsta = str.split(line[cindex[0] + 1 : cindex[1]])  # splits city and state field by space into array of string
            stindex = len(citsta) - 1  # index of state name
            stateName = citsta[stindex]  # Store state name
            if len(citsta) == 1:
                citName = citsta[0]
            else:
                citName = line[cindex[0] + 1: cindex[1] - (len(stateName) + 1)]  # Format City Name
            dlen = len(line) - len(line[cindex[3] + 1: cindex[len(cindex) - 1]])  #how many characters are left after the last comma
            temp = City(line[0:cindex[0]], citName, stateName, line[cindex[2] + 1: cindex[3]], line[cindex[len(cindex) - 1] + 1 : cindex[len(cindex) - 1] + dlen]) #line[cindex[3] + 1: cindex[len(cindex) - 1] + dlen])
            self.cityArray.append(temp)
        self.size = len(self.cityArray)

    def linearSearch(self, city, attribute):
        for tempcity in self.cityArray:
            if attribute == "id":
                if tempcity.cid == city:
                    return str(tempcity)
            elif attribute == "name":
                if tempcity.cname == city:
                    return str(tempcity)
        return "City not found"

    def quickSort(self):
        self.quickSortHelper(0,len(self.cityArray) - 1)
        self.isSorted = True

    def quickSortHelper(self, first, last):
        if first < last:
            splitpoint = self.partition(first, last)

            self.quickSortHelper(first, splitpoint - 1)
            self.quickSortHelper(splitpoint + 1, last)

    def partition(self, first, last):
        pivotvalue = self.cityArray[first].cname

        leftmark = first + 1
        rightmark = last

        done = False
        while not done:

            while leftmark <= rightmark and self.cityArray[leftmark].cname <= pivotvalue:
                leftmark = leftmark + 1

            while self.cityArray[rightmark].cname >= pivotvalue and rightmark >= leftmark:
                rightmark = rightmark - 1

            if rightmark < leftmark:
                done = True
            else:
                temp = self.cityArray[leftmark]
                self.cityArray[leftmark] = self.cityArray[rightmark]
                self.cityArray[rightmark] = temp

        temp = self.cityArray[first]
        self.cityArray[first] = self.cityArray[rightmark]
        self.cityArray[rightmark] = temp

        return rightmark

    def buildBST(self):
        for city in self.cityArray:
            self.put(int(city.cid), city)

    def searchBST(self, cid):
        try:
            temp = self.get(int(cid))
            if temp != None:
                return temp
            else:
                return "City not found"
        except:
            return "City not found"

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def put(self, key, val):
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)
        self.size = self.size + 1

    def _put(self,key, val, currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key, val, parent=currentNode)
                self.updateBalance(currentNode.leftChild)
        else:
            if currentNode.hasRightChild():
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key, val, parent=currentNode)
                self.updateBalance(currentNode.rightChild)

    def __setitem__(self, k, v):
        self.put(k, v)

    def updateBalance(self, node):
        if node.balanceFactor > 1 or node.balanceFactor < -1:
            self.rebalance(node)
            return
        if node.parent != None:
            if node.isLeftChild():
                node.parent.balanceFactor += 1
            elif node.isRightChild():
                node.parent.balanceFactor -= 1
            if node.parent.balanceFactor != 0:
                self.updateBalance(node.parent)

    def rotateLeft(self, rotRoot):
        newRoot = rotRoot.rightChild

        rotRoot.rightChild = newRoot.leftChild
        if newRoot.leftChild != None:
            newRoot.lrftChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isLeftChild():
                rotRoot.parent.leftChild = newRoot
            else:
                rotRoot.parent.rightChild = newRoot
        newRoot.leftChild = rotRoot
        rotRoot.parent = newRoot
        rotRoot.balanceFactor = rotRoot.balanceFactor - 1 - max(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor - 1 + min(rotRoot.balanceFactor, 0)

    def rotateRight(self, rotRoot):
        newRoot = rotRoot.leftChild

        rotRoot.leftChild = newRoot.rightChild
        if newRoot.rightChild != None:
            newRoot.rightChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isRightChild():
                rotRoot.parent.rightChild = newRoot
            else:
                rotRoot.parent.leftChild = newRoot
        newRoot.rightChild = rotRoot
        rotRoot.parent = newRoot
        rotRoot.balanceFactor = rotRoot.balanceFactor - 1 - max(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor - 1 + min(rotRoot.balanceFactor, 0)

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

    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None

    def _get(self, key, currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key, currentNode.leftChild)
        else:
            return self._get(key, currentNode.rightChild)

    def __getitem__(self, key):
        return self.get(key)

    def __contains__(self, key):
        if self._get(key, self.root):
            return True
        else:
            return False


class TreeNode:
    def __init__(self, key, val, left=None, right=None, parent=None):
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


class BinarySearchTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def put(self, key, val):
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)
        self.size = self.size + 1

    def _put(self,key, val, currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key, val, parent=currentNode)
                self.updateBalance(currentNode.leftChild)
        else:
            if currentNode.hasRightChild():
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key, val, parent=currentNode)
                self.updateBalance(currentNode.rightChild)

    def __setitem__(self, k, v):
        self.put(k, v)

    def updateBalance(self, node):
        if node.balanceFactor > 1 or node.balanceFactor < -1:
            self.rebalance(node)
            return
        if node.parent != None:
            if node.isLeftChild():
                node.parent.balanceFactor += 1
            elif node.isRightChild():
                node.parent.balanceFactor -= 1
            if node.parent.balanceFactor != 0:
                self.updateBalance(node.parent)

    def rotateLeft(self, rotRoot):
        newRoot = rotRoot.rightChild

        rotRoot.rightChild = newRoot.leftChild
        if newRoot.leftChild != None:
            newRoot.lrftChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isLeftChild():
                rotRoot.parent.leftChild = newRoot
            else:
                rotRoot.parent.rightChild = newRoot
        newRoot.leftChild = rotRoot
        rotRoot.parent = newRoot
        rotRoot.balanceFactor = rotRoot.balanceFactor - 1 - max(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor - 1 + min(rotRoot.balanceFactor, 0)

    def rotateRight(self, rotRoot):
        newRoot = rotRoot.leftChild

        rotRoot.leftChild = newRoot.rightChild
        if newRoot.rightChild != None:
            newRoot.rightChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isRightChild():
                rotRoot.parent.rightChild = newRoot
            else:
                rotRoot.parent.leftChild = newRoot
        newRoot.rightChild = rotRoot
        rotRoot.parent = newRoot
        rotRoot.balanceFactor = rotRoot.balanceFactor - 1 - max(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor - 1 + min(rotRoot.balanceFactor, 0)

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

    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None

    def _get(self, key, currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key, currentNode.leftChild)
        else:
            return self._get(key, currentNode.rightChild)

    def __getitem__(self, key):
        return self.get(key)

    def __contains__(self, key):
        if self._get(key, self.root):
            return True
        else:
            return False




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    lib = COV19Library()
    lib.LoadData("cov19_city.csv")
    lib.linearSearch("23700","id")
    lib.linearSearch("Lafayette","name")
    lib.linearSearch("Beebo","name")
    lib.quickSort()
    lib.buildBST()
    print(lib.searchBST("14780"))