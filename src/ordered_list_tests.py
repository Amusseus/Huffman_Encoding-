import unittest
from ordered_list import*

class TestLab4(unittest.TestCase):

    def test_simple(self):
        t_list = OrderedList()
        empty_list = OrderedList()
        t_list.add(10)
        self.assertEqual(empty_list.python_list_reversed(),[])
        self.assertFalse(t_list.add(10))
        self.assertEqual(t_list.python_list(), [10])
        self.assertEqual(t_list.size(), 1)
        self.assertEqual(t_list.index(10), 0)
        self.assertTrue(t_list.search(10))
        self.assertFalse(t_list.is_empty())
        self.assertEqual(t_list.python_list_reversed(), [10])
        self.assertTrue(t_list.remove(10))
        t_list.add(10)
        self.assertEqual(t_list.pop(0), 10)
        with self.assertRaises(IndexError):
            t_list.pop(-1)
        t_list.add(2)
        t_list.add(1)
        t_list.add(10000)
        t_list.add(3)
        t_list.add(4)
        t_list.add(6)
        t_list.add(7)
        t_list.add(8)
        self.assertFalse(t_list.remove(5))
        self.assertTrue(t_list.remove(1))
        self.assertTrue(t_list.remove(3))
        self.assertTrue(t_list.remove(10000))
        self.assertEqual(t_list.index(9999999),None)
        self.assertEqual(t_list.pop(2),6)

if __name__ == '__main__': 
    unittest.main()
