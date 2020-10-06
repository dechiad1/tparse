"""
Accept a long string & return a list of strings that start & end with '<table' & '</table>'
"""
table = 'table'
valid_tags = ['caption', 'colgroup', 'col', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td']

class Node:
    def __init__(self, t):
        self.type = t
        self.children = []

    def addText(self, text):
        self.text = text

    def setParent(self, p):
        self.parent = p

    def getParent(self):
        return self.parent

    def addChild(self, c):
        self.children.append(c)

    def getType(self):
        return self.type

class TableNode(Node):
    def __init__(self, t):
        super().__init__(t)
        self.rows = []

    def getRows(self):
        return self.rows

    def getRowAtIndex(self, index):
        if index < len(self.rows):
            return self.rows[index]
        else:
            return None

def parse_tables(text):
    tag = ''
    table_index = -1
    tflag = False
    full_tag = False
    is_end_tag = False

    tables = []

    for i,c in enumerate(text):
        # find the start of the table
        if c == '<':
            tflag = True
        elif tflag:
            #character will be a space or > - ending the tag
            if c == ' ' or c == '>':
                if c == ' ': # expecting classes, etc
                    continue
                tflag = False
                full_tag = True
            #character will be a '<' - invalid tag
            elif c == '<':
                tflag = True
                tag = ''
            #character will be a '/' & come second to denote a closing tag
            elif c == '/' and len(tag) == 0:    
                is_end_tag = True
            #character will be part of a tag
            else:
                tag += c
        
        # evaluate full tag in same loop
        if full_tag:
            if tag == table:
                if is_end_tag:
                    tables.append(text[table_index:i+1])
                    is_end_tag = False
                else:
                    table_index = i - 6 # <table is 6 characters
            tag = ''
            full_tag = False

    return tables

def build_table_stack(text):
    i = 0
    n = len(text)
    """
        Iterate through the table string
        Process tags that start & end with < & >
        Process data - everything else
    """
    stack = []
    while i < n:
        """
        Process a tag:
            - comment
            - end tag
            - start tag
        """
        # the second parameter i tells find where to start
        start = text.find('<', i)
        # -1 means it doesnt exist
        if start < 0:
            break
        else:
            t = text[start:start+2] # get the < character plus what follows it
            # process comment
            if t == '<!': 
                pass
            # process end tag
            elif t == '</':
                end = text.find('>')
                if end < 0:
                    break
                node = process_end_tag(text[start:end+1])
            # process start tag
            else:
                end = text.find('>')
                if end < 0:
                    break # invalid tag
                node = process_start_tag(text[start:end+1])
                stack.append(node)
        
        """
        Process data
        """
        # if the first '<' tag is after text, then we have some data to process
        if i < start:
            node = stack.pop()
            process_data(node, text[i:start])
            stack.append(node)

        # update position of i
        i = start + 1

    return stack

def matching_tags(o, t):
    one = o.getType()
    two = t.getType()
    if len(one) > len(two):
        if one[1:] == two:
            return True
    else:
        if two[1:] == one:
            return True
    return False

def create_tree(stack):
    """
    After while loop builds the stack, take items off & build the tree 
    and/or other structures to help process data
    """
    # odd amount of tags on stack - invalid tag block; a start & end tag means the count should be even
    if len(stack) % 2 == 1:
        return -1
    """
    stack:
        </table>
        </tr>
        </td>
        <td>
        </td>
        <td>
        <tr>
        <table>
        1. if the item popped off is equal to the current item, no children & set parent to current
        2. if the item is new, add as child to current node. set parent relationships & update current
    """
    current = stack.pop(0) # removes first item from list

    for i, n in enumerate(stack):
        if matching_tags(n, current):
            # if last element, we are at the root & there is no parent
            if i != len(stack) -1:
                current = current.getParent()
        else: #
            current.addChild(n)
            n.setParent(current)
            current = n
    
    # will always return root if the stack is proper
    return current


def process_start_tag(text):
    t = ''
    attrs = []
    if text.find(' ') > 0:
        contents = text.split(' ')
        for i,c in contents:
            if i == 0:
                t = c
            else:
                if c.find('='):
                    attr = (c.split('=')[0], c.split('=')[1])
    else:
        t = text

    return Node(t)

def process_data(node, text):
    node.addText(text)

def process_end_tag(text):
    t = '/' + text
    return Node(t)

    
            



                
        
        


