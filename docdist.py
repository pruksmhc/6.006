#!/usr/bin/python
import string
import sys
import math
import operator
    # math.acos(x) is the arccosine of x.
    # math.sqrt(x) is the square root of x.

# global variables needed for fast parsing
# translation table maps upper case to lower case and punctuation to spaces
translation_table = string.maketrans(string.punctuation+string.uppercase[0:26],
                                     " "*len(string.punctuation)+string.lowercase[0:26])

def extract_words(filename):
    """
    Return a list of words from a file
    """
    try:
        f = open(filename, 'r')
        doc = f.read()
        lines = doc.translate(translation_table)
        return lines.split()
    except IOError, e:
        #print("Error opening or reading input file: ",filename)
        #print(e)
        sys.exit()


##############################################
## Part a. Count the frequency of each word ##
##############################################
def count_freq(word_list):
    ptr_list_1 = 0
    L ={}
    word = word_list[ptr_list_1]
    L[word] = 1 
    ptr_list_1 = ptr_list_1 +1 
    while ptr_list_1 < len(word_list): 
        if word_list[ptr_list_1] == word: 
            L[word] = L[word] +1 
        else: 
            word = word_list[ptr_list_1] #set ht word to the new word
            L[word] = 1
        ptr_list_1 = ptr_list_1 +1 
#so htis is the lsit of words from theentire thing. 
    return L 

def inner_product(L1, L2):
    sum = 0 
    for word in L1:   #50
        #finding the dot product

        #print("Finding for word "+word)  
        #print("And getting the count for %i", L1[word])
        if word in L2:
            #print ("L2 has %i", L2[word] )
            sum += L1[word]* L2[word] 
            #print("Sum is ")
            #print(sum)
            #if L2 does not have, multiplied by 0, so sum is same.
    #print(sum)
    return sum



def doc_dist(L1, L2):
    numerator= inner_product(L1, L2) #o(M) for part a, O(N) for part c. 
    denominator = math.sqrt(inner_product(L1, L1) * inner_product(L2, L2)) #o(2M) O(2N) 
    return math.acos(numerator/denominator) #o(1)

def normal_count(document_list1, document_list2):
    document_list1.sort() #O(nlogn)
    document_list2.sort() #O(nlogn)
    frequency_1 = count_freq(document_list1)  #On)
    frequency_2 = count_freq(document_list2)
    angle = doc_dist(frequency_1, frequency_2) 
    #print(angle)
    print(angle)
    return angle
    #o2NLOGN) +o(N) + o(3M) 
    

##############################################
## Part b. Count the frequency of each pair ##
##############################################
def word_frequencies_pair(word_list):
    #for each pair in the filanmee, simply put htem together.  
    consec_words_list = {}
    ptr = 1
    while ptr < len(word_list): #O(n) 
        word_1 = word_list[ptr-1] 
        word_2 = word_list[ptr]
        word_pair = word_1+ " "+ word_2
        #print("inserting "+word_pair)
        if(word_pair not in consec_words_list):
            consec_words_list[word_pair] = 1
        else:
            consec_words_list[word_pair] = consec_words_list[word_pair]+1
        ptr = ptr + 1 #You want all combinations of two consecutive pairs of wrods

    return consec_words_list
def doc_dist_pairs(word_list1, word_list2):
    """
    Returns a float representing the document distance
    in radians between two files based on unique 
    consecutive pairs of words when given the list of
    words from both files
    """
    count_file_1 = word_frequencies_pair(word_list1) #O(n) 
    count_file_2= word_frequencies_pair(word_list2)
    angle = doc_dist(count_file_1, count_file_2)  #O(3N)
    print(angle)
    return angle

#############################################################
## Part c. Count the frequency of the 50 most common words ##
#############################################################

def get_fifty(word_list):
    curr_freq = 0 
    fifty_word_list ={}
    candidate_freq =0
    ties=[]
    ptr = 0
    #the second you can substirn git. 
    #TODO case for when there are not fifty distint words 
    while len(fifty_word_list) < 50 and ptr < len(word_list) : 
        #print(word_list[ptr])
        candidate_freq= word_list[ptr][1] #this is the candidate list. 
        if(word_list[ptr+1][1] < candidate_freq): 
            #add the word and its freqeuncy.  
            fifty_word_list[word_list[ptr][0]] =  word_list[ptr][1] 
            ptr = ptr+1

        else:  
            #continue inserting the words iwth the same freqs. 
            ties = []
            tuple_insert = (word_list[ptr][0], ptr)
            ties.append(tuple_insert) 
            j = ptr+1
            while(word_list[j][1] == candidate_freq): #O(m*), or thenubmer of words with that freqency,w hich is at most O(m). 
                tuple_insert = (word_list[j][0], j)  
                ties.append(tuple_insert) #O(1)
                j= j+1
            #now sort by alphabet 
            ties.sort() #O(nlog(m*))
            index_selected =  int(ties[0][1]) #index selected 
            fifty_word_list[word_list[index_selected][0]] =  word_list[index_selected][1] 
            ptr = ptr + len(ties) #skip over the ones you already inserted 
    return fifty_word_list






def doc_dist_50(word_list1, word_list2):
    """
    Returns a float representing the document distance
    in radians between two files based on the 
    50 most common unique words when given the list of
    words from both files
    """
    word_list1.sort() #O(2logn)
    word_list2.sort()
    frequency_1 = count_freq(word_list1) #O(N
    frequency_2 = count_freq(word_list2) 
    #sort in descending order. 
    frequency_1 = sorted(frequency_1.items(), key=operator.itemgetter(1), reverse=True) #Onlogn 
    frequency_2 = sorted(frequency_2.items(), key=operator.itemgetter(1),reverse=True) #sorted by most freuqent of 2.   O(nlogn) 
    frequency_1= get_fifty(frequency_1)  
    frequency_2= get_fifty(frequency_2)#
    angle = doc_dist(frequency_1, frequency_2)  #O(150)
    print(angle)
    return angle





def main():
    new_list = ["hello", "hello"]
    new_set = set(new_list)
  
    if len(sys.argv) != 3:
         "Usage: docdist1.py filename_1 filename_2" 
    else:
        filename_1 = sys.argv[1]
        filename_2 = sys.argv[2]
        word_list1 = extract_words(filename_1)  
        word_list2 = extract_words(filename_2)  
        doc_dist_50(word_list1, word_list2)
        normal_count(word_list1, word_list2)
        doc_dist_pairs(word_list1, word_list2)

        



if __name__ == "__main__":
    import cProfile
    cProfile.run("main()")




    




