# ----------------------------------------------------------------------------
# Adam Lefaivre
# CPSC 5110 - Intro to Facility Location
# Assignment 2 - a2median.py
# Dr. Robert Benkoczi
# ----------------------------------------------------------------------------

#!/usr/bin/python3.6
import networkx as nx
import argparse
import os
from random import randint

# Function to check if the graph is a path
def isNotSimplePath(G, startNode, endNode):
    paths = list(nx.all_simple_paths(G, startNode, endNode))
    if ((len(paths)) != 1):
       return False
    else:
       return True

# Function to check if the graph has proper weights and lengths
def allNodesHaveWeightsAndLengths(G):
    for source,target,edge in G.edges(data=True):
        if(not(G.has_edge(source, target))):
            print("No edge between nodes", str(source), " and ", str(target))
            return False
        if(not('length' in G[source][target])):
            print("No length attribute for edge of nodes", str(source), "and", str(target))
            return False
        elif(edge['length'] < 1):
            print("Length attribute less than 1 for edge of nodes", str(source), "and", str(target))
            return False

    for v in G.nodes():
        if(not('weight' in G.node[v])):
            print("No weight attribute for node", str(v))
            return False
        elif(G.node[v]['weight'] < 1):
            print("Weight attribute less than 1 for node", str(v))
            return False

    return True

# Function to initialize
def initializeNewRandomGraphWithFile(n):

    n = int(n)
    G = nx.path_graph(n)
    print("Note: Smallest weight/length starts at 1.")

    # -----------------------------------------------------
    # NOTE: This is just some code to prompt the user for
    # the largest random weight and length
    # -----------------------------------------------------

    largestWeight = input("Please enter the largest random weight that can be assigned: ")
    largestWeight = str(largestWeight)
    while (not (largestWeight.isdigit()) or (int(largestWeight) < 1)):
        if (not (largestWeight.isdigit())):
            print("Sorry, largestWeight is incorrect (must be a positive integer)!")
        if (largestWeight == "0"):
            print("Sorry, largestWeight cannot be 0")
        largestWeight = input("Please enter the largest random weight that can be assigned, or type \"no\" to exit: ")
        largestWeight = str(largestWeight)
        largestWeight = largestWeight.strip()
        largestWeight = largestWeight.lower()
        if ((largestWeight == "no") or (largestWeight == "n")):
            exit()

    largestLength = input("Please enter the largest random length that can be assigned: ")
    largestLength = str(largestLength)
    while (not (largestLength.isdigit()) or (int(largestLength) < 1)):
        if (not (largestLength.isdigit())):
            print("Sorry, largestLength is incorrect (must be a positive integer)!")
        if(largestLength == "0"):
            print("Sorry, largestLength cannot be 0")
        largestLength = input("Please enter the largest random length that can be assigned, or type \"no\" to exit: ")
        largestLength = str(largestLength)
        largestLength = largestLength.strip()
        largestLength = largestLength.lower()
        if ((largestLength == "no") or (largestLength == "n")):
            exit()


    count = 0
    largestWeight = int(largestWeight)
    largestLength = int(largestLength)

    while (count < (n - 1)):

        randWeight = randint(1, largestWeight)
        G.node[count]['weight'] = randWeight

        randLength = randint(1, largestLength)
        G[count][count+1]['length'] = randLength

        count = count + 1

    randWeight = randint(1, largestWeight)
    G.node[n-1]['weight'] = randWeight

    # We are now done making our graph, write it out.
    nx.write_gml(G, "file.gml")
    return G

# parse input
parser = argparse.ArgumentParser(description='___________Calculate the 1-median___________')
parser.add_argument('-n', nargs='?', type=int, help='Specifies the number of nodes needed on the path')
parser.add_argument('file', type=str, help='Specifies the GML file used')
args = parser.parse_args()
n = args.n
file = args.file

createNewFile = False
# If n does not exist read from a file
if(n is None):


    if(not os.path.isfile(file)):
        print("There is no file " + file + ", a new file will now be created")
        n = input("Please enter an n value to specify the number of nodes for a new graph, or type \"no\" to quit: ")

        n = n.strip().lower()
        if ((n == "no") or (n=="n")):
            exit()
        while (not (n.isdigit())):
            print("Sorry n is not an integer (or you did not type \"no\") try again!")
            n = input("Please enter an n value to specify the number of nodes for a new graph, or type \"no\" to quit: ")
            n = n.strip().lower()
            if ((n == "no") or (n == "n")):
                exit()
        G = initializeNewRandomGraphWithFile(n)


    # If there is still nothing in the file.
    if(os.stat(file).st_size == 0):
        print("There are no contents in the file " + file + " ... A new file will now be created.")
        n = input("Please enter an n value to specify the number of nodes for a new graph, or type \"no\" to quit: ")

        n = n.strip().lower()
        if ((n == "no") or (n=="n")):
            exit()
        while (not (n.isdigit())):
            print("Sorry n is not an integer (or you did not type \"no\") try again!")
            n = input("Please enter an n value to specify the number of nodes for a new graph, or type \"no\" to quit: ")
            n = n.strip().lower()
            if ((n == "no") or (n == "n")):
                exit()
        G = initializeNewRandomGraphWithFile(n)

    # If the file is filled
    else:
        try:
            G = nx.read_gml(file, destringizer=int)
            print("GML file has been read successfully!")

        # If the file is filled and still cannot be read in properly (i.e. perhaps the wrong extension is used)
        except:
            print("GML file: " + file + " cannot be read ... A new file will now be created.")
            n = input("Please enter an n value to specify the number of nodes for a new graph, or type \"no\" to quit: ")

            n=n.strip().lower()
            if ((n == "no") or (n == "n")):
                exit()
            while (not (n.isdigit())):
                print("Sorry n is not an integer (or you did not type \"no\") try again!")
                n = input("Please enter an n value to specify the number of nodes for a new graph, or type \"no\" to quit: ")
                n = n.strip().lower()
                if ((n == "no") or (n == "n")):
                    exit()
            G = initializeNewRandomGraphWithFile(n)

# n exists ... so generate a path with a value of n number of nodes.
# Lengths & weights are set randomly
# Save it to "file" overwriting it. Store lengths and weights.
else:
    G = initializeNewRandomGraphWithFile(n)


# Check if the graph is a path
if (not (isNotSimplePath(G, 0, len(G) - 1))):
    print("Graph input from file is not a simple path, exiting!")
    exit()

# Check if the graph has nodes without weight and length
if (not allNodesHaveWeightsAndLengths(G)):
    print("Not all nodes have correctly set weight and length attributes, exiting!")
    exit()

nx.write_gml(G, file)

# PHEW! Now we're all setup and ready to go!
# Lets just implement 1-median by brute force here.

facilityCosts = []
facilities = []
for facility in G.nodes():
    facilitySum = 0
    for customer in G.nodes():
        if(customer != facility):
            weight = G.node[customer]['weight']
            distance = nx.shortest_path_length(G,source=customer, target=facility,  weight='length')
            facilitySum = (facilitySum + (weight * float(distance)))

    facilityCosts.append([facilitySum, facility])

minTuple = min(facilityCosts, key=lambda t: (t[0]))

# Note that we need to find all of the optimal solutions.
optimalTuples = []
for tuple in facilityCosts:
    if(tuple[0] == minTuple[0]):
        optimalTuples.append(tuple)
optimalFacilities = [x[1] for x in optimalTuples]

print("The cost for 1-median is: " + str(minTuple[0]))
print("The IDs of the 1-median nodes are: " + str(optimalFacilities)[1:-1])
