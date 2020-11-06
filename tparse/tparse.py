"""
Accept a long string & return a list of strings that start & end with '<table' & '</table>'
"""
table = 'table'
valid_tags = ['caption', 'colgroup', 'col', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td']

class Node:
    def __init__(self, t):
        self.type = t
        self.children = []
        self.parent = None

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text

    def setParent(self, p):
        self.parent = p

    def getParent(self):
        return self.parent

    def addChild(self, c):
        self.children.append(c)
    
    def getChildren(self):
        return self.children

    def getType(self):
        return self.type

    def hasChildren(self):
        if len(self.children) > 0:
            return True
        return False

    # DPS on a node while executing a function on each node
    def traverseChildren(self, function):
        for child in self.getChildren()
            function(child)
            child.traverseChildren()

class RowNode(Node):
    def __init__(self, t):
        super().__init__(t)
        self.cols = []

    def getCols(self):
        return self.cols

    def getTextRow(self):
        text_row = []
        for c in self.cols:
            text_row.append(c.getText())

class ColumnNode(Node):
    def __init__(self, t):
        super().__init__(t)
        # each column should have but one text element
        self.child = None
        self.text = None

    def getText(self):
        if self.text is None:
            self.child.getText()
        else:
            return self.text


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

    """
    Create a list of lists that contains the text
    contents of each row

    <tr><td>1</td><td>2</td></tr>
    <tr><td>3</td><td>4</td></tr>
    
    Should return [[1,2], [3,4]]
    """
    def buildTableTextTable(self):
        result = []

        node = self
        while node.hasChildren():


        # for node in queue: if its a row node, get its text values
        for n in node.getChildren():
            if n.getType() == 'tr':
                row = n.getTextRow()
                result.append(row)
            
            

            

def get_tables(text):
    start = text.find("<table")
    table_strings = []
    while start > -1:
        end = text.find("</table>", start+1)
        table_strings.append(text[start:end + 8])  # 8 is the length of </table>
        start = text.find("<table", end)

    return table_strings
    # return a list of text that start & end with table tags

def build_table_tree(text):
    # use a stack to verify the tag validity of the table segment
    stack = []

    i = text.find('<')
    while i < len(text):
        # case '<': element is a tag
        if text[i] == '<':
            end = text.find('>', i)

            # extract every character between the opening & closing tags
            tag = text[i+1:end]
            # first element is the type of tag, which is what we care about
            tag_type = tag.split(' ')[0]
            
            # closing tag
            if tag_type[0] == '/':
                open_tag = stack.pop() # TODO: catch this?
                close_type = tag_type[1:]
                if not open_tag.getType() == close_type:
                    print('invalid tags found!', open_tag.getType(), close_type)
                    return -1
                elif open_tag.getType() == 'table' and len(stack) == 0:
                    # end condition
                    return open_tag
            # opening tag
            else:
                node = create_node_type(tag_type)
                if node.getType() != 'table':
                    stack[len(stack)-1].addChild(node)
                stack.append(node)

            # start at the character after the closing of the tag
            i = end + 1
        # otherwise we have text or whitespace
        else:
            end = text.find('<', i)
            if end == -1:
                print('Warn: No tags left to process & we dont have a handle on the root node')
                return -1

            # all white space means no text to process
            content = text[i:end].strip()

            # set i and then add content to node
            i = end
            if content == '':
                continue

            index = len(stack)
            stack[index-1].setText(content)

    # iteration of elements is complete - should have returned when seeing the table close element
    if len(stack) != 0:
        print('Error: stack is not empty... printing')
        for item in stack:
            print(item.get_type())
        return -1

    print('Warn: reached end with empty stack & we dont have a handle on the root node')
    return -1


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
        
        """
        Process data first, to attach
        the text to the open tag
        """
        # if the first '<' tag is after text, then we have some data to process
        if i < start and len(stack) > 0:
            node = stack.pop()
            process_data(node, text[i:start+1]) # start +1 will exist because it came from a find call
            stack.append(node)
        
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
                end = text.find('>', start)
                if end < 0:
                    break
                node = process_end_tag(text[start:end+1])
                stack.append(node)
            # process start tag
            else:
                end = text.find('>', start)
                if end < 0:
                    break # invalid tag
                node = process_start_tag(text[start:end+1])
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
    current = stack.pop() 
    # the list acts as a backwards stack - append adds to end, pop removes from end
    i = len(stack) - 1
    while i >= 0:
        if matching_tags(stack[i], current):
            # if last element, we are at the root & there is no parent
            if not i == 0:
                current = current.getParent()
        else: #
            current.addChild(stack[i])
            stack[i].setParent(current)
            current = stack[i]
        i -= 1
    
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

    return create_node_type(t)

def process_data(node, text):
    # if characters appear between the > & the <, save to text
    s = text.find('>')
    e = text.find('<')

    if s < 0 or e < 0:
        return
    else:
        node.addText(text[s+1:e])

def process_end_tag(text):
    #t = '/' + text
    return create_node_type(text)
       
def create_node_type(t):
    if t.find('table') > -1:
        return TableNode(t)
    elif t.find('tr') > -1:
        return RowNode(t)
    elif t.find('td') > -1 or t.find('span') > -1:
        return ColumnNode(t)
    return Node(t)