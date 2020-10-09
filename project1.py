# Author: Luke LaCasse
# Date: October 1, 2020
# Title: ECE 241 Project 1: Sorting and Searching
# Description:

from BinarySearchTree import *
from time import time_ns
from random import randint

class City:

    def __init__(self, cid, cname, cstate, pop, cities):
        self.cid = cid
        self.cname = cname
        self.cstate = cstate
        self.pop = pop
        self.cities = cities

    def __str__(self):
        return ("cid: %s; cname: %s; cstate: %s; cases:%s" % (self. cid, self.cname, self.cstate, self.cities)).rstrip("\n")


class COV19Library:

    def __init__(self):
        self.cityArray = []
        self.size = 0
        self.isSorted = False
        self.BST = None
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
            if len(citsta) == 1:  # Deals with cities with no state name
                citName = citsta[0]
            else:
                citName = line[cindex[0] + 1: cindex[1] - (len(stateName) + 1)]  # Format City Name
            dlen = len(line) - len(line[cindex[3] + 1: cindex[len(cindex) - 1]])  # how many characters are left after the last comma
            temp = City(line[0:cindex[0]], citName, stateName, line[cindex[2] + 1: cindex[3]], line[cindex[len(cindex) - 1] + 1 : cindex[len(cindex) - 1] + dlen])  # line[cindex[3] + 1: cindex[len(cindex) - 1] + dlen])
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
        if not self.isSorted:
            self.BST = AVLTree()
            for city in self.cityArray:
                self.BST.put(int(city.cid), city)
            self.root = self.BST.root



    def searchBST(self, cid):
        try:
            temp = self.BST.get(int(cid))
            if temp is not None:
                return temp
            else:
                return "City not found"
        except:
            return "City not found"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    lib = COV19Library()
    lib.LoadData("cov19_city.csv")
    lib.linearSearch("23700","id")
    lib.linearSearch("Lafayette","name")
    lib.linearSearch("Beebo","name")
    #lib.quickSort()

    #Find city with largest population
    maxPop = None
    for city in lib.cityArray:
        if maxPop is None or int(city.pop) > int(maxPop.pop):
            maxPop = city
    print(maxPop)

    # Test average execution of building the Binary Search Tree
    totalTime = 0
    iterations = 10
    for i in range(0, iterations):
        lib.BST = None  # reset BST
        start = time_ns()
        lib.buildBST()
        end = time_ns()
        totalTime = totalTime + (end - start)
    avgTime = (totalTime / iterations) * (1e-9)
    print("Average time to build BST, iterations = %s: %s [Seconds]" % (iterations, avgTime))

    # Generate list of randomly selected CIDs
    randCID = list()
    lib.BST = None
    lib.buildBST()
    numCity = 100
    for i in range(0,numCity):
        rand = randint(0, lib.size)  # Generates random 6-Digit Number
        randCID.append(lib.cityArray[rand].cid)

    # Test average execution time of a linear search
    totalTime = 0
    iterations = 10
    for i in range(0, iterations):
        start = time_ns()
        for j in range(0, len(randCID) - 1):
            lib.linearSearch(randCID[j], "id")
        end = time_ns()
        totalTime = totalTime + (end - start)
    avgTime = (totalTime / iterations) * (1e-9)
    print("Average time to linearSearch through %s random CIDs, iterations = %s: %s [Seconds]" % (numCity, iterations, avgTime))

    # Test average execution time of a linear search
    totalTime = 0
    iterations = 10
    for i in range(0, iterations):
        start = time_ns()
        for j in range(0, len(randCID) - 1):
            lib.searchBST(randCID[j])
        end = time_ns()
        totalTime = totalTime + (end - start)
    avgTime = (totalTime / iterations) * (1e-9)
    print("Average time to searchBST %s random CIDs, iterations = %s: %s [Seconds]" % (numCity, iterations, avgTime))
