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
        for item in stack:
            print(item.getType())
        
        self.assertEqual(len(stack), 8)
        # todo: self.assertEqual(stack[2].text, "hi there")


if __name__ == '__main__':
    unittest.main()