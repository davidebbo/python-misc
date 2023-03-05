import io
import unittest

from one_zoom.format_newick import format

test_tree = "(A,(BA,((BBAA_ott123,BBAB,BBAC,BBAD)BAA,(BBBA)BBB,(BBCA:12.34,BBCB)BBC_ott456:78.9)BB)B_ott789,((CAA,CAB),CB)C,D)Root;"

formatted_test_tree = \
'''(
  A,
  (
    BA,
    (
      (
        BBAA_ott123,
        BBAB,
        BBAC,
        BBAD
      )BAA,
      (
        BBBA
      )BBB,
      (
        BBCA:12.34,
        BBCB
      )BBC_ott456:78.9
    )BB
  )B_ott789,
  (
    (
      CAA,
      CAB
    ),
    CB
  )C,
  D
)Root;
'''

# Generate unit test class for format_newick.format
class TestFormatNewick(unittest.TestCase):
    def test_format_newick(self):
        # Create an in memory file object
        f = io.StringIO()
        format(test_tree, f, 2)
        f.seek(0)
        self.assertEqual(f.read(), formatted_test_tree)
