import collections
#=========== Collection Wrapper: Queue ====================
class Queue: # A wrapper made around the collections library
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0
    
    def put(self,x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()

    def reverse(self):
        return self.elements.reverse()
