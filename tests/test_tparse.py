import unittest
from tparse import tparse

class Test_parse_tables(unittest.TestCase):

    # Test for single tables tag
    def test_parse_tables_one_table(self):
        text = "<html><table>a table!</table></html>"
        tables = tparse.parse_tables(text)
        self.assertEqual(tables[0], "<table>a table!</table>")

    # Test for just a table
    def test_parse_tables_just_the_table(self):
        text = "<table>a table!</table>"
        tables = tparse.parse_tables(text)
        self.assertEqual(tables[0], "<table>a table!</table>")

    # Test for multiple tables tags
    def test_parse_tables_multiple_tables(self):
        text = "<html><table>first table</table><br><table>a second table!</table></html>"
        tables = tparse.parse_tables(text)
        self.assertEqual(tables[0], "<table>first table</table>")
        self.assertEqual(tables[1], "<table>a second table!</table>")
        self.assertEqual(len(tables), 2)

    # Test for no tables tag
    def test_parse_tables_no_tables(self):
        text = "<html><body>not a table!</body></html>"
        tables = tparse.parse_tables(text)
        self.assertEqual(len(tables), 0)

    # Test for invalid open tag
    def test_parse_tables_invalid_open(self):
        text = "<html><table a table!</table></html>"
        tables = tparse.parse_tables(text)
        self.assertEqual(len(tables), 0)

    # Test for invalid close tag
    def test_parse_tables_invalid_close(self):
        text = "<html><table> a table!<table></html>"
        tables = tparse.parse_tables(text)
        self.assertEqual(len(tables), 0)

class Test_matching_tags(unittest.TestCase):
    
    def test_open_close(self):
        n1 = tparse.Node("table")
        n2 = tparse.Node("/table")

        r = tparse.matching_tags(n1, n2)
        self.assertEqual(r, True)

    def test_open_open(self):
        n1 = tparse.Node("table")
        n2 = tparse.Node("table")

        r = tparse.matching_tags(n1, n2)
        self.assertEqual(r, False)

class Test_create_tree(unittest.TestCase):

    def test_create_tree_valid_stack(self):
        stack = []
        stack.append(tparse.Node("/table"))
        stack.append(tparse.Node("/tr"))
        stack.append(tparse.Node("/td"))
        stack.append(tparse.Node("td"))
        stack.append(tparse.Node("tr"))
        stack.append(tparse.Node("/tr"))
        stack.append(tparse.Node("tr"))
        stack.append(tparse.Node("table"))

        tree = tparse.create_tree(stack)

        self.assertEqual(tree.getType(), "table")
        self.assertEqual(len(tree.children), 2)
        self.assertEqual(tree.children[1].children[0].getType(), "td")

    def test_create_tree_invalid_stack_missing_tag(self):
        stack = []
        stack.append(tparse.Node("/table"))
        stack.append(tparse.Node("/tr"))
        stack.append(tparse.Node("/td"))
        stack.append(tparse.Node("td"))
        stack.append(tparse.Node("tr"))
        stack.append(tparse.Node("/tr"))
        stack.append(tparse.Node("tr"))

        tree = tparse.create_tree(stack)
        self.assertEqual(tree, -1)

class Test_build_table_stack(unittest.TestCase):

    def test_build_table_stack_valid(self):
        text = "<table><tr><td>hi there</td></tr><tr></tr></table>"
        stack = tparse.build_table_stack(text)
        #for item in stack:
            #print(item.getType())
        
        self.assertEqual(len(stack), 8)
        self.assertEqual(stack[2].text, "hi there")


class Test_build_list_of_text_rows(unittest.TestCase):

    def test_build_list_of_text_rows_valid(self):
        text = "<table><tr><td>hi</td><td>there</td></tr><tr><td>don</td><td>miguel</td><td>arninio</td></tr></table>"
        stack = tparse.build_table_stack(text)
        tree = tparse.create_tree(stack)
        #tableNode = stack[0]
        print(tree.getType())
        result = tree.build_list_of_text_rows()

        # for item in result: 
        #     print(item)
        self.assertEqual(len(result), 2)

class Test_parse_table_text(unittest.TestCase):

    def test_get_tables(self):
        text = "<table> asdfasdfasdf </table> <table> asdfasdf </table>"
        tables = tparse.get_tables(text)

        self.assertEqual(2, len(tables))
        self.assertEqual("<table> asdfasdfasdf </table>", tables[0])

class Test_build_table_tree(unittest.TestCase):

    def test_build_table_tree(self):
        text = """
        <table><thead><tr><th rowspan="2">Name</th><th rowspan="2">ID</th><th colspan="2">MembershipDates</th><th rowspan="2">Balance</th></tr><tr><th>Joined</th><th>Canceled</th></tr></thead><tbody><tr><th scope="row">MargaretNguyen</th><td>427311</td><td><time datetime="2010-06-03">June3,2010</time></td><td>n/a</td><td>0.00</td></tr><tr><th scope="row">EdvardGalinski</th><td>533175</td><td><time datetime="2011-01013">January13,2011</time></td><td><time datetime="2017-04008">April8,2017</time></td><td>37.00</td></tr><tr><th scope="row">HoshiNakamura</th><td>601942</td><td><time datetime="2012-07-23">July23,2012</time></td><td>n/a</td><td>15.00</td></tr></tbody></table>
        """

        tableTree = tparse.build_table_tree(text)

        # root has two children: thead & tbody
        self.assertEqual(2, len(tableTree.getChildren()))

if __name__ == '__main__':
    unittest.main()