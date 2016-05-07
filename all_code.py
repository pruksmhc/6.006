import math
import bisect
import StringIO
import collections



###################################################################
# Part (d)
#   Description:
#       Gradebook is a data structure that keeps track of every student
#       and their grade information. The cool thing about Gradebook is that
#       returning the k most average students takes only O(k) time, and 
#       updating a student's grade takes O(log(n) + k) time! Unfortunately,
#       it hasn't been implemented yet.
#
#   Hint:
#       In your data structure, you will need to keep a running average of
#       each student's grade. The way to do that is to keep track, for each
#       student, of the total number of credits the student has taken so far, 
#       and the sum of his grades weighted by the number of credits. 
#       For instance, if a student takes a 12-unit and then a 6-unit class and
#       gets a 5 then a 2, we keep track of (18, 72). SO we want the total number of credits, and then the weighted sum fo teh taol numbe rof credits.   Then, the student's 
#       GPA is 72/18=4.
#
#   TODO: 
#       Using your design in part (c), use "__init__" to define and initialize
#       the data structures you will need, and then fill in the methods 
#       "update_grade", "average", and "middle" (descriptions below).
###################################################################
class Gradebook:

    # TODO
    def __init__(self, student_names, k):
        # Define and initialize your data structure!
        #make the 
         #Initate a list of student name
        gpa = [0] * len(student_names) 
        n = len(student_names)
      # Check if n is odd or even:
        # Check if n is odd or even:
        if n % 2 == 0:
            if k %2 == 0:
                upper = int(math.floor((n-k)/float((2))))
            else: 
                upper = int(math.floor((n-k)/float((2))))+1 #7 = 2 + 2 +3  (15/2 = 2 


        else:
            upper = int(math.floor((n-k)/float((2)))) #7 = 2 + 2 +3  (15/2 = 2 
        lower = n - (upper + k) # =k3+5 = 8  = 2 10 - (2+4) = 3 
        values = [(0,0,0)] * len(student_names) 
        self.all_students_scores = dict(zip(student_names, values))
        self.lowerStudents = Max_Heap(student_names[:lower], gpa[:lower])
        self.middleStudentNames = student_names[lower:k+lower] #this is giving the two people. 
        self.upperStudents = Min_Heap(student_names[k+lower:n], gpa[k+lower:n])



    def sort(self, index):
            curr_index = index

            k = len(self.middleStudentNames)
            i = index
            # the element at i might be out of place
            while True:
              current_nm = self.middleStudentNames[i]
              #getting the current name
              current_el =  self.all_students_scores[current_nm][2]
              if i<k-1 and current_el  > self.all_students_scores[self.middleStudentNames[i+1]][2]:
                # swap to the right
                self.middleStudentNames[i] = self.middleStudentNames[i+1] 
                self.middleStudentNames[i+1] = current_nm
                i += 1

              elif i>0 and current_el < self.all_students_scores[self.middleStudentNames[i-1]][2]:
                self.middleStudentNames[i] = self.middleStudentNames[i-1]
                self.middleStudentNames[i-1] = current_nm
                i -= 1

              else:
                break
            return 





    def update_grade(self, student, credit, grade):
        # Updates student with the new credit and grade information, and 
        # makes sure "middle()" still returns the k most average students 
        # in O(k) time. Does not need to return anything.
        #updates studnet iwth the new credit and grade informaiton.  
        #here, you want to simply update these ones.
        #print("at the beginning of update_grade")
      #  self.lowerStudents.show_tree()
        #print(self.middle())
      #  self.upperStudents.show_tree()

        cm = credit*grade 
        current_cm, current_credits, oldGPA = self.all_students_scores[student]
        newGPA = 0
        new_entry = ( current_cm+cm,  current_credits+ credit, newGPA)
        self.all_students_scores[student] = new_entry
        newGPA = self.average(student) 
        new_entry = ( current_cm+cm,  current_credits+ credit, newGPA)
        self.all_students_scores[student] = new_entry
        #computing the GPA to insert 

        k = len(self.middleStudentNames)
        #Case I: If student is in the lower students - max heap. 
        if student in self.lowerStudents.key_to_index: 
            #Modify the student's GPA with the new GPA. 
            min_k = self.all_students_scores[self.middleStudentNames[0]][2]
            ##print("min_k is ")
            ##print(min_k)
            self.lowerStudents.max_heap_modify(student, newGPA)   
            #if the maximum of the lower quartile is more than the minimum of the k_array  
            if self.lowerStudents.data[0] > min_k:  
                #print("Swapping the lower with the middle")
                #get the names to swap. 
                k_student_name = self.middleStudentNames[0] 
                former_max_student_name = self.lowerStudents.keys[0] 
                self.middleStudentNames[0] = former_max_student_name
                #k_array --> lower Students
                self.sort(0)
                self.lowerStudents.extract_max()  
                self.lowerStudents.insert_key(k_student_name, min_k) 
                
                max_k = self.all_students_scores[self.middleStudentNames[k-1]][2]

                if max_k> self.upperStudents.data[0]: 
                    #print("Swapping upper with middle")
                    max_k_student_name = self.middleStudentNames[k-1]   
                    former_min_student_name = self.upperStudents.keys[0]  
                    #upperStudents --> k_array 
                    self.middleStudentNames[k-1] =  former_min_student_name
                    self.sort(k-1) #resort array. 
                    #from k_array --> upperStudents
                    self.upperStudents.extract_min()
                    self.upperStudents.insert_key(max_k_student_name, max_k) #should be inserte dinot the minmimum heap. 

        elif student in self.middleStudentNames:
            #get where the studnet is in the gpa list. 
            index = self.middleStudentNames.index(student)
            self.sort(index)
            max_k = self.all_students_scores[self.middleStudentNames[k-1]][2]
            ##print("computed average")
            ##print(max_k)
            if self.upperStudents.data[0] < max_k:
                #print("Swappin gupper with middle")
                max_k_student_name = self.middleStudentNames[k-1]   #k_array and middleStudents length should be the same. 
                former_min_student_name = self.upperStudents.keys[0]    
                self.middleStudentNames[k-1] =  former_min_student_name
                #now insert into the min_heap
                self.sort(k-1)
                self.upperStudents.extract_min()
                self.upperStudents.insert_key(max_k_student_name, max_k) #should be inserte dinot the minmimum heap. 
            min_k = self.all_students_scores[self.middleStudentNames[0]][2] 
            ##print("computed minimum of k")
            ##print(min_k)
            if min_k < self.lowerStudents.data[0]: 
                #print("Swapping lower iwth middle")
                k_student_name = self.middleStudentNames[0] #shoudl be the same index.

                former_max_student_name = self.lowerStudents.keys[0]
          #      ###print("swapping"  + k_student_name+" with "+ former_max_student_name)
                self.middleStudentNames[0] = former_max_student_name 
                self.sort(0)
                #doing the otehrway swap. 
                self.lowerStudents.extract_max()  #pop from teh lwoer students
                self.lowerStudents.insert_key(k_student_name, min_k) #insert_key 
        else: 
            #print("student is ")
            #print(student)
            #print("gpa is ")
            #print(newGPA)
            self.upperStudents.min_heap_modify(student, newGPA) 
            max_k = self.all_students_scores[self.middleStudentNames[k-1]][2]
            if self.upperStudents.data[0] < max_k: 
               #print("Swapping the upper with the middle")
               max_k_student_name = self.middleStudentNames[k-1]  #k_array and middleStudents length should be the same. 
               former_min_student_name = self.upperStudents.keys[0]  
               self.middleStudentNames[k-1] =  former_min_student_name
               self.sort(k-1) 
               self.upperStudents.extract_min()
               self.upperStudents.insert_key(max_k_student_name, max_k) #should be inserte dinot the minmimum heap. 

               min_k = self.all_students_scores[self.middleStudentNames[0]][2]
               if min_k < self.lowerStudents.data[0]:
                   #print("swapping the lower with the middle")
                   k_student_name = self.middleStudentNames[0] #shoudl be the same index. 
                   former_max_student_name = self.lowerStudents.keys[0] 
              #     ###print("swapping"  + k_student_name+" with "+ former_max_student_name)
                   self.middleStudentNames[0] = former_max_student_name
                   self.sort(0)
                    #doing the otehrway swap. 
                   self.lowerStudents.extract_max()  #pop from teh lwoer students
                   self.lowerStudents.insert_key(k_student_name, min_k) #insert_key 
        #print("at the end of this iteration of update_grade")
       # self.lowerStudents.show_tree()
        #print(self.middle())
      #  self.upperStudents.show_tree()

   
        return 


    # TODO
    def average(self, student):
        # Return a single number representing the GPA for student
        #you ahve the student name. 

        if self.all_students_scores[student][0] is 0 and    self.all_students_scores[student][1] is 0:
            return 0
        return self.all_students_scores[student][0]/self.all_students_scores[student][1]

    # TODO
    def middle(self):
        # Return the k most average students and their GPAs as a 
        #   list of tuples, e.g. [(s1, g1),(s2,g2)]
        #you wnt to cut away the part  fo the aray hat are (n-k)/2 in both sides, and then iterate through and reutnr that suarray. 
        #okay, lets do this, so you need to comptue the GPA of this. 
        middle_array =[]
        for index in range(0, len(self.middleStudentNames)):
            student_name = self.middleStudentNames[index] #get the keys that match up with that index. 
         #   ###print("the gpa")
          #  ###print( self.k_array[index] )
            entry = (student_name,  float(self.average(student_name)))
            middle_array.append(entry)

        return middle_array

###################################################################
# Part (a)
#   Description:
#       Max_Heap is a general implementation of a max-heap modified to accept
#       (key, data) pairs. For instance, in the student GPA problem, the 
#       "key" would a student name and the "data" would be the student's GPA,
#       e.g. ("Bob Dylan", 1) 
#
#   Implementation/Initialization Details:
#       The keys (i.e. student names) are stored in a list called "self.keys"
#       The data (i.e. student GPAs) are stored in a list called "self.data"
#       Additionally, a dictionary called "self.key_to_index_mapping" keeps
#       track of the index of the key in the array. For instance, if we had 
#       the following list of (key, data) pairs, which already satisfies the 
#       max-heap property:
#
#           [("Ray Charles", 4), ("Bob Dylan", 1), ("Bob Marley", 3)]
#           
#       then,       self.keys = ["Ray Charles", "Bob Dylan", "Bob Marley"]
#                   self.data = [4, 1, 3]
#           self.key_to_index = {"Ray Charles": 0, 
#                                "Bob Dylan": 1,
#                                "Bob Marley": 2} 
#       where 0, 1, 2 corresponds to the index in "self.keys" #so the sself.keys respond to the inde xin the slef. keys index. 
#
#   Provided Methods:
#       All the methods presented in lecture and recitation are provided, with
#       only slight changes to accomodate the (key, data) pair modification.
#       In addition, we provide the method show_tree(self) so that you may 
#       ###print out what your heap looks like.
#
#   TODO: Fill out the method "max_heap_modify(self, key, data)", which modifies, 
#       the data of "key" to the new "data" and restores the heap invariant. 
#       For instance, using the example above, we may call:
#           
#           heap.max_heap_modify("Bob Marley", 5)
#
#       This should change Bob Marley's grade to 5, and then restore
#       the heap invariant so that the data structure looks like this:
#   
#so you want to ssrot the keys, and then sort the dakte, ,a but int he self.key_to_index youw ant to simply chagne the idnicews f where 
#the keys rae lined up to adn not the order ot he anems ro tuples. 
#               self.keys = ["Bob Marley", "Bob Dylan", "Ray Charles"]
#               self.data = [5, 1, 4]  #so this is a max heap 
#       self.key_to_index = {"Ray Charles": 2, 
#                           "Bob Dylan": 1,
#                           "Bob Marley: 0"} 
# ARE STUDNET GPAs discrete. 
###################################################################
class Max_Heap:

    def __init__(self, keys, data):
        try:
            assert len(keys) == len(data)
            
            self.keys = collections.deque(keys)
            self.data = collections.deque(data)
            self.key_to_index = dict(zip(self.keys, range(len(self.keys)))) #!
            self.heapify()
        except Exception as e: 
            pass 

    # TODO
    def max_heap_modify(self, key, data): 
        curr_index = self.key_to_index[key]
        curr_data = self.data[curr_index]
        if data < curr_data:
            self.data[curr_index] = data
            self.max_heapify(curr_index) 
        if data > curr_data:
            self.increase_key(curr_index, data)
        
        #assert self.check_heap_invariant()
        return 

    def maximum(self):
        return (self.keys[0], self.data[0])

    def extract_max(self):
        if len(self.keys)<1:
            raise Exception("No elements in heap!")
        sm, gm = self.keys.popleft(), self.data.popleft()
        del self.key_to_index[sm]
        if len(self.keys) > 0:
            s, g = self.keys.pop(), self.data.pop()
            self.keys.appendleft(s)
            self.data.appendleft(g)
            self.key_to_index[s] = 0
            self.max_heapify(0)
        return (sm, gm)

    def insert_key(self, k, d):
        self.keys.append(k)
        self.data.append(-float("inf"))
        self.key_to_index[k] = len(self.keys)-1 #!
        self.increase_key(len(self.keys)-1, d)

    def max_heapify(self, i):
        heap_size = len(self.keys)
        l = i*2 + 1
        r = i*2 + 2
        largest = i
        if l < heap_size and self.data[l] > self.data[i]:
            largest = l
        if r < heap_size and self.data[r] > self.data[largest]:
            largest = r
        if largest != i:
            self.swap(largest, i)
            self.max_heapify(largest)

    def increase_key(self, i, key):
        if key < self.data[i]:
            raise Exception("New key is smaller than current key.")
        self.data[i] = key
        parent = (i-1)/2
        while i > 0 and self.data[i] > self.data[parent]:  #yyou want to get the self = self.data is more than kelf.data  of the parents. SO 
        #I  is the current key of the =actualy key, but the idnex oc that. 
            self.swap(i, parent)
            i = parent
            parent = (i-1)/2


    def heapify(self):
        for i in range(len(self.keys)/2)[::-1]:
            self.max_heapify(i)



    def swap(self, i1, i2):
        self.key_to_index[self.keys[i1]] = i2 #!
        self.key_to_index[self.keys[i2]] = i1 #!
        self.data[i1], self.data[i2] = self.data[i2], self.data[i1]
        self.keys[i1], self.keys[i2] = self.keys[i2], self.keys[i1]

    # modified from https://pymotw.com/2/heapq/
    # Displays the heap as a tree
    def show_tree(self, total_width=60, fill=' '):
        """Pretty-###print a tree."""
        output = StringIO.StringIO()
        last_row = -1
        for i, n in enumerate(self.keys):
            if i:
                row = int(math.floor(math.log(i+1, 2)))
            else:
                row = 0
            if row != last_row:
                output.write('\n')
            columns = 2**row
            col_width = int(math.floor((total_width * 1.0) / columns))
            towrite = str(n) + " (" + str(self.data[i]) + ")"
            output.write(str(towrite).center(col_width, fill))
            last_row = row
        #print(output.getvalue())
        #print( '-' * total_width)

        return ""

    ########################################################################
    # The following methods are methods used for testing and may be ignored.
    ########################################################################

    def check_heap_invariant(self):
        n = len(self.data)
        for i in range(n/2):
            parent = self.data[i]
            if parent < self.data[2*i+1]:
                return False
            if 2*i + 2 < n:
                if parent < self.data[2*i+2]:
                    return False
        return True

    def check_student_index(self):
        for s,i in self.key_to_index.iteritems():
            if i >= len(self.keys):
                return False
            if self.keys[i] != s:
                return False
        return True


###################################################################
# Part (b)
#   The implementation of Min_Heap is the same as Max_Heap, but modified
#   to be a min-heap. Please refer to the description for Max_Heap.
###################################################################
class Min_Heap:
    '''
    keys: list of key values
    data: list of data that corresponds to the key values
    student_index: a dictionary that maps students names to their index in the
        list representation of the heap
    '''
    def __init__(self, keys, data):
        assert len(keys) == len(data)
        self.keys = collections.deque(keys)
        self.data = collections.deque(data)
        self.key_to_index = dict(zip(self.keys, range(len(self.keys)))) #!
        self.heapify()

    # TODO
    def min_heap_modify(self, key, data):
        #  self.show_tree()

        curr_index = self.key_to_index[key]
        curr_data = self.data[curr_index]
        if data > curr_data:
            self.data[curr_index] = data  
            self.min_heapify(curr_index)
        if data < curr_data:
            self.decrease_key(curr_index, data)
#
   #     assert self.check_heap_invariant()
        return 

    def minimum(self):
        return (self.keys[0], self.data[0])

    def extract_min(self):
        if len(self.keys)<1:
            raise Exception("No elements in heap!")
        sm, gm = self.keys.popleft(), self.data.popleft()
        del self.key_to_index[sm]
        if len(self.keys) > 0:
            s, g = self.keys.pop(), self.data.pop()
            self.keys.appendleft(s)
            self.data.appendleft(g)
            self.key_to_index[s] = 0
            self.min_heapify(0)
        return (sm, gm)

    def insert_key(self, k, d):
        self.keys.append(k)
        self.data.append(float("inf"))
        self.key_to_index[k] = len(self.keys)-1 #!
        self.decrease_key(len(self.keys)-1, d)

    def min_heapify(self, i):
        heap_size = len(self.keys)
        l = i*2 + 1
        r = i*2 + 2
        smallest = i
        if l < heap_size and self.data[l] < self.data[i]:
            smallest= l
        if r < heap_size and self.data[r] < self.data[smallest]:
            smallest = r
        if smallest != i:
            self.swap(smallest, i)
            self.min_heapify(smallest)

    def decrease_key(self, i, key):
        if key > self.data[i]:
            raise Exception("New key is larger than current key.")
        self.data[i] = key
        parent = (i-1)/2
        while i > 0 and self.data[i] < self.data[parent]:
            self.swap(i, parent)
            i = parent
            parent = (i-1)/2

    def heapify(self):
        for i in range(len(self.keys)/2)[::-1]:
            self.min_heapify(i)

    # Exchanges the students and GPAs at two indices
    def swap(self, i1, i2):
        self.key_to_index[self.keys[i1]] = i2 #!
        self.key_to_index[self.keys[i2]] = i1 #!
        self.data[i1], self.data[i2] = self.data[i2], self.data[i1]
        self.keys[i1], self.keys[i2] = self.keys[i2], self.keys[i1]

    # modified from https://pymotw.com/2/heapq/
    # Displays the heap as a tree
    def show_tree(self, total_width=60, fill=' '):
        """Pretty-###print a tree."""
        output = StringIO.StringIO()
        last_row = -1
        for i, n in enumerate(self.keys):
            if i:
                row = int(math.floor(math.log(i+1, 2)))
            else:
                row = 0
            if row != last_row:
                output.write('\n')
            columns = 2**row
            col_width = int(math.floor((total_width * 1.0) / columns))
            towrite = str(n) + " (" + str(self.data[i]) + ")"
            output.write(str(towrite).center(col_width, fill))
            last_row = row
        #print(output.getvalue())
        #print('-' * total_width)
        ###print
        return ""

    ########################################################################
    # The following methods are methods used for testing and may be ignored.
    ########################################################################

    def check_heap_invariant(self):
        n = len(self.data)
        for i in range(n/2):
            parent = self.data[i]
            if parent > self.data[2*i+1]:
                return False
            if 2*i + 2 < n:
                if parent > self.data[2*i+2]:
                    return False
        return True

    def check_student_index(self):
        for s,i in self.key_to_index.iteritems():
            if i >= len(self.keys):
                return False
            if self.keys[i] != s:
                return False
        return True


def main():
    students = ["yo" , "a", "b", "c", 'd']
   # student_names= [("Yada", 10.0, 2) , ("Nancy", 1.0, 5) , ("Wally", 2.3, 3.5), ("Carrot", 2.0, 2),("Bob", 1.0, 2), ("Hellium", 3, 10), ("Hala", 4, 1.0), ("Peet",5.0, 1.0), ("Actor1", 2.3, 4), ("Melanie",3.0, 5.0)]
   # ###print(student_names)
    gradebook = Gradebook(students, 2) 
    #so I need to do  this basically. 


        



if __name__ == "__main__":
    import cProfile
    cProfile.run("main()")




