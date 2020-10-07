# Author: Luke LaCasse
# Date: October 1, 2020
# Title: ECE 241 Project 1: Sorting and Searching
# Description:

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




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    lib = COV19Library()
    lib.LoadData("cov19_city.csv")
    lib.linearSearch("23700","id")
    lib.linearSearch("Lafayette","name")
    lib.linearSearch("Beebo","name")
