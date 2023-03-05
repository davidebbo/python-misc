import unittest

from one_zoom.newick_parser import parse_tree


class TestNewickParser(unittest.TestCase):
    def test_full_parse_result(self):
        node_list = list(parse_tree("(A_ott123,B:1.2)C_ott789:5.5;"))
        self.assertEqual(node_list, [
            {'taxon': 'A', 'ott': '123', 'edge_length': 0.0, 'start': 1, 'end': 9, 'full_name_start_index': 1, 'depth': 1},
            {'taxon': 'B', 'ott': None, 'edge_length': 1.2, 'start': 10, 'end': 15, 'full_name_start_index': 10, 'depth': 1},
            {'taxon': 'C', 'ott': '789', 'edge_length': 5.5, 'start': 0, 'end': 28, 'full_name_start_index': 16, 'depth': 0}])

    def test_quoted_taxa(self):
        node_list = list(parse_tree("('Abc/def_ott123','qw e$r&ty':1.2)'C_*(ot)t789_ott987':5.5;"))
        self.assertEqual(node_list[0]['taxon'], 'Abc/def')
        self.assertEqual(node_list[1]['taxon'], 'qw e$r&ty')
        self.assertEqual(node_list[2]['taxon'], 'C_*(ot)t789')

    def verify_exception(self, tree_string, exception_text):
        exception = False
        try:
            node_list = list(parse_tree(tree_string))
        except SyntaxError as e:
            exception = True

            # Assert that the error message contains the expected text
            self.assertIn(exception_text, e.msg)

        self.assertTrue(exception)

    def test_syntax_error_too_many_closed_braces(self):
        self.verify_exception("(A,B))(C,D);", "expected a semicolon at the end of the tree")
        self.verify_exception("A)))", "expected a semicolon at the end of the tree")

    def test_syntax_error_too_many_open_braces(self):
        self.verify_exception("((A,B);", "expected ',' or ')'")
        self.verify_exception("(();", "expected ',' or ')'")

    def test_syntax_error_missing_edge_length_after_colon(self):
        self.verify_exception("(Blah,Foo:);", "'' is not a valid edge length")
        self.verify_exception("(Blah,Foo:a$3);", "'a$3' is not a valid edge length")

    def test_syntax_error_invalid_edge_length(self):
        self.verify_exception("(Blah,Foo_ott67:14z);", "'14z' is not a valid edge length")
