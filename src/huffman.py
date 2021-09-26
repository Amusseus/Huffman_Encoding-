from ordered_list import*
from huffman_bit_writer import HuffmanBitWriter

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right
        
    #overides the basic __eq__ function and checks to see if nodes have the same frequency 
    def __eq__(self, other):
        if other == None:
            return False
        if self.freq == other.freq:
            return True
        return False

    #function redifing less than operator, used to check if self should go before other
    def __lt__(self, other):
        if self == other:
            return self.char < other.char
        return self.freq < other.freq
    
    #used to represent the node, used for testing 
    def __repr__(self):
        return f"chr: {self.char} freq: {self.freq} "

# filename -> list
# takes the filename and return a list of frequency for each character
def cnt_freq(filename):
    '''Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file'''
    #uses try except to check if the input file exists
    try:
        read_file = open(filename,"r")
        ascii_lst = [0]*256
        for line in read_file:
            for character in line:
                ascii_lst[ord(character)] += 1
        read_file.close()
        return ascii_lst
    except FileNotFoundError:
        raise FileNotFoundError

# turn_ordered_lst and make_tree_node are helper functions for create_huff_tree

# list -> orederedlist
# returns a orderedlist of huffman nodes for all characters with a non-zero frequency 
def turn_ordered_list(value_lst):
    od = OrderedList()
    for i in range(len(value_lst)):
        if value_lst[i] > 0:
            temp_huffman_node = HuffmanNode(i,value_lst[i])
            od.add(temp_huffman_node)
    return od

# nodes -> node
# creates a link between too nodes and returns the parent node
def make_tree_node(node1,node2):
    total_freq = node1.freq + node2.freq
    if node1.char < node2.char:
        new_huffman_node = HuffmanNode(node1.char,total_freq)
    if node2.char < node1.char:
        new_huffman_node = HuffmanNode(node2.char,total_freq)
    if node1 < node2:
        new_huffman_node.left = node1
        new_huffman_node.right = node2
    elif node2 < node1:
        new_huffman_node.left = node2
        new_huffman_node.right = node1
    return new_huffman_node

# list -> node
# Creates a binary tree out of the list of frequencies, returns the root node
def create_huff_tree(char_freq):
    '''Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree'''
    od_freq = turn_ordered_list(char_freq)
    while od_freq.size() > 1:
        node_x = od_freq.pop(0)
        node_y = od_freq.pop(0)
        node_parent = make_tree_node(node_x,node_y)
        od_freq.add(node_parent)
    return od_freq.pop(0)

# recur_huffman_tree is a helper function for create_code

# list, node, string -> none
# creates huffman codes through recursion
def recur_huffman_tree(add_lst, root_node,string_huff):
    if root_node.left is None and root_node.right is None:
        add_lst[root_node.char] = string_huff
    if root_node.left is not None:
        recur_huffman_tree(add_lst,root_node.left,string_huff + "0")
    if root_node.right is not None:
        recur_huffman_tree(add_lst,root_node.right,string_huff + "1")

# node -> list
# returns  a list of huffman codes, the codes are on the ascii index of the character in the list
def create_code(node):
    '''Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location'''
    ascii_code = [None]*256
    recur_huffman_tree(ascii_code,node,"")
    return ascii_code

# list -> string 
# creates a header for the files using a list of freq
def create_header(freqs):
    '''Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” '''
    header = ""
    for i in range(len(freqs)):
        if freqs[i] != 0:
            temp_char = i
            temp_freq = freqs[i]
            header += f"{temp_char} {temp_freq} "
    header = header[:-1]
    return header

# create_file is a helper function for huffman_encode

# string -> none
# creates a new file if it already doesn't exist
def create_file(file_name):
    try:
        f = open(file_name,"x")
        f.close()
        return True
    except:
        return False

# input file, output file -> none
# uses the functions above to create a huffman version of the input file, also creates a compressed huffman file
def huffman_encode(in_file, out_file):
    '''Takes inout file name and output file name as parameters - both files will have .txt extensions
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Also creates a second output file which adds _compressed before the .txt extension to the name of the file.
    This second file is actually compressed by writing individual 0 and 1 bits to the file using the utility methods 
    provided in the huffman_bits_io module to write both the header and bits.
    Take not of special cases - empty file and file with only one unique character'''
    freq_lst = cnt_freq(in_file)            # list of frequencies
    header_string = create_header(freq_lst) # header string for the output file
    Huff_node = create_huff_tree(freq_lst)  # root node of the huffman tree
    code_lst = create_code(Huff_node)       # list of huffman codes
    with open(in_file, "r") as rf:
        with open(out_file, "w") as wf:
            wf.write(header_string + "\n")
            for line in rf:
                for character in line:
                    index = ord(character)
                    wf.write(code_lst[index])
    wf.close()
    rf.close()
    txt_index = out_file.index(".txt")
    compressed_file_name = out_file[:txt_index] + "_compressed.txt"
    create_file(compressed_file_name) 
    huff_writter = HuffmanBitWriter(compressed_file_name)
    with open(out_file,"r") as rwf:
        huff_writter.write_str(rwf.readline())
        huff_writter.write_code(rwf.readline())
        huff_writter.close()
    rwf.close()

# recur_ord and tree_depth functions were used in testing 
def recur_ord(nodex): # return lst in order through recursion
        if nodex is not None:
            temp_lst = []
            temp_lst += recur_ord(nodex.left)
            temp_lst += [nodex.freq]
            temp_lst += recur_ord(nodex.right)
            return temp_lst
        else:
            return []

def tree_depth(nodex): # finds the depth through recursion  
        if nodex == None:
            return -1
        else:
            left_depth = tree_depth(nodex.left)
            right_depth = tree_depth(nodex.right)
            if left_depth >= right_depth:
                return left_depth + 1
            elif left_depth < right_depth:
                return right_depth + 1

'''
freq_lst = cnt_freq("multiline.txt")
print("od --------------------")
od = turn_ordered_list(freq_lst)
od.printorderedlist()
print("huffman tree created ----------------------")
huff_node = create_huff_tree(freq_lst)
print(recur_ord(huff_node))
print(f"size of tree {tree_depth(huff_node)}")
print("list of huffman codes ----------------------")
code_lst = create_code(huff_node)
print(code_lst)
huffman_encode("declaration.txt","declaration_out.txt")
'''
#huffman_encode("file_WAP.txt","test_functionz_sol.txt")
#freq_lst = cnt_freq("file1.txt")
#print(freq_lst)
#huffman_encode("declaration.txt","declaration_out.txt")