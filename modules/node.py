from printer import log
import gc
class NodeHandler(object):
    def __init__(self,parsehandler):
        self.parsehandler = parsehandler
        # One-item queue
        self.queue = None
        self.nodes = []
    
    # Check before appending to nodes
    def add(self,new):
        if self.queue == None:
            self.queue = new
        else:
            if (new.key == self.queue.key and
                new.cc == self.queue.cc and
                len(self.queue.key) > 1):
                self.queue.char = self.queue.char + new.char
            else:

                self.nodes.append(self.queue)
                self.queue = new

    def clearQueue(self):
        if (self.queue != None):
            self.nodes.append(self.queue)
        self.queue = None

# All pertainent characters in a text are represented
# as nodes.
class Node(object):
    def __init__(self,char,cc,pos,key):
        self.pos = pos
        self.cc = cc
        self.char = char
        self.key = key
        self.edges = []
        self.id = self.key + "_" + str(self.pos)

    # Get right position for multi-character nodes
    def getRight(self):
        rpos = self.pos + len(self.char) - 1
        return rpos
    
    # returns an edge count
    def countEdges(self):
        count = len(self.edges)
        return count
    
    def add(self,edge):
        self.edges.append(edge)
    
    # Prints all of the good info about a node
    def printNode(self):
        print("\t#### Node ####")
        print("\tClass: " + self.cc.id)
        print("\tKey: " + self.key)
        for e in self.edges:
            e.printEdge()

# The relationship between two nodes, directed from
# origin node as a focal node to dest as a compare
class Edge(object):
    def __init__(self,dest,cost):
        self.id = dest.id + "_" + str(cost)
        self.cost = cost
        self.cc = dest.cc.id
        self.pos = dest.pos
    
    # Prints all of the good info about an edge
    def printEdge(self):
        print("\t\t#### Edge ####")
        print("\t\tClass: " + self.cc)
        print("\t\tId: " + self.id)
        print("\t\tCost: " + str(self.cost))
        print("\t\tAbsolute cost: " + str(abs(self.cost)) + "\n")

class NodeProfile(object):
    def __init__(self,focals,stopwords,delims,compares,focal,
                 compare,stopword,delim,maxcost):
        self.focals = focals
        self.stopwords = stopwords
        self.delims = delims
        self.compares = compares
        self.focal = focal
        self.compare = compare
        self.stopword = stopword
        self.delim = delim
        self.maxcost = maxcost
        self.id = (focal.id + "_" + compare.id + "_" +
                   stopword.id + "_" + delim.id + "_" + str(maxcost))
        self.generateEdges()
    

    def generateEdges(self):
        log("Generating edges for " + self.id)
        max = self.maxcost
        neg_max = (-1 * max)
        edge_count = 0
        # The list position of the first found element so we don't need to
        # keep checking the beginning of the list when abs(cost) > maxcost
        first_stop = 0
        first_delim = 0
        first_compare = 0
        # Optimizations tricks
        stopword = self.stopword.id
        delim = self.delim.id
        for f in self.focals:
            gc.disable()
            f_pos = f.pos
            # For each newly-minted focal node, determine the distance to
            # each stopword if the node is within maxcost absolute distance.
            # This is because we don't want to count these words towards the
            # distance of future nodes.
            found_first_stop = False
            stop_index = first_stop
            for s in self.stopwords[first_stop:]:
                s_cost = f_pos - s.pos
                if s_cost < neg_max:
                    break
                if abs(s_cost) <= max and s_cost != 0:
                    if found_first_stop == False:
                        found_first_stop = True
                        first_stop = (stop_index)
                    f.add(Edge(s,s_cost))
                    edge_count += 1
                stop_index += 1
        
            # Do the same for the delimiters.
            found_first_delim = False
            delim_index = first_delim
            for d in self.delims[first_delim:]:
                d_pos = d.pos
                d_cost = f_pos - d_pos
                d_takeaway = 0
                if d_cost < neg_max:
                    break
                for e in f.edges:
                    e_pos = e.pos
                    if (((e_pos > d_pos and e_pos < f_pos) or
                            (e_pos < d_pos and e_pos > f_pos)) and
                                (e.cc == stopword)):
                        d_takeaway += 1
                if d_cost < 0:
                    d_cost += d_takeaway
                elif d_cost > 0:
                    d_cost -= d_takeaway
                if abs(d_cost) <= max and d_cost != 0:
                    if found_first_delim == False:
                        found_first_delim = True
                        first_delim = (delim_index)
                    f.add(Edge(d,d_cost))
                    edge_count += 1
                delim_index += 1
            
            # Now we can calculate the compares by the distance ignoring
            # stopwords and delimiters, giving a better true distance
            found_first_compare = False
            compare_index = first_compare
            for c in self.compares[first_compare:]:
                c_pos = c.pos
                c_cost = f_pos - c_pos
                if c_cost < neg_max:
                    break
                takeaway = 0
                for e in f.edges:
                    e_pos = e.pos
                    if (((e_pos > c_pos and e_pos < f_pos) or
                         (e_pos < c_pos and e_pos > f_pos)) and
                            (e.cc == stopword or
                             e.cc == delim)):
                        takeaway += 1
                if c_cost < 0:
                    c_cost += takeaway
                elif c_cost > 0:
                    c_cost -= takeaway
                if abs(c_cost) <= max and c_cost != 0:
                    if found_first_compare == False:
                        found_first_compare = True
                        first_compare = (compare_index)
                    f.add(Edge(c,c_cost))
                    edge_count += 1
                compare_index += 1
            gc.enable()
        log("Edge count was " + str(edge_count))

    def printProfile(self):
        print("\n#### Profile ####")
        print("Focals: " + self.focal.id)
        print("Compares: " + self.compare.id)
        for f in self.focals:
            print("\n")
            f.printNode()

    def getColocations(self,abscost):
        colocations = []
        print("Compare class was : " + self.compare.id)
        for f in self.focals[:]:
            for e in f.edges:
                if e.cc == self.compare.id and abs(e.cost) <= abscost:
                    colocations.append(f)
        return colocations

    def countColocations(self,abscost):
        count = len(self.getColocations(abscost))
        return count
    
    def countFocalEdges(self):
        count = 0
        for f in self.focals:
            count = count + f.countEdges()
        return count

    def countCompareNodes(self):
        return len(compares)
    
    def getClosestTwoDelimiterPositions(self,edges):
        first = -1
        second = -1
        for e in edges:
            if first == -1 and e.cc == self.delim.id:
                first = e.pos
            elif second == -1 and e.cc == self.delim.id:
                second = e.pos
            elif (first != -1 and second != -1) or (abs(e.cost) > self.maxcost):
                break
        return first,second
    
    def countInSentence(self):
        count = 0
        for f in self.focals:
            edges = self.mergesort(f.edges)
            closest = self.getClosestTwoDelimiterPositions(edges)
            left = min(closest[0],closest[1])
            right = max(closest[0],closest[1])
            for e in edges:
                pos = e.pos
                if (e.cc == self.compare.id and
                  ((pos >= left and pos < f.pos) or
                   (pos <= right and pos > f.pos))):
                    count = count + 1
        return count

    def mergesort(self,list):
        mid = int(len(list)/2)
        result = self.merge(list[mid:],list[:mid])
        return result

    def merge(self,left,right):
        result = []
        left_idx, right_idx = 0, 0
        while left_idx < len(left) and right_idx < len(right):
            # change the direction of this comparison to change the direction of the sort
            if abs(left[left_idx].cost) <= abs(right[right_idx].cost):
                result.append(left[left_idx])
                left_idx += 1
            else:
                result.append(right[right_idx])
                right_idx += 1
        if left:
            result.extend(left[left_idx:])
        if right:
            result.extend(right[right_idx:])
        return result

            

# A set of characters with a unique identifier
class CharacterClass(object):
    def __init__(self,id,chars):
        # a string identifier such as "gods" or "delimiters"
        self.id = id
        # A list of character-phrases
        # Each with one or more character
        self.chars = chars