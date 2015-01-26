__author__ = 'Andrew'
import unittest
import traceback
import os
import Greedy
import time
from Greedy import KnapsackFile


class TestGreedy(unittest.TestCase):
    def setUp(self):
        """
        The setUp() is run at the beginning of each test method
        Unfortunately the (Windows) OS is a bit of a git,
            so we have to be sneaky and try hard to make this work
        """
        self.times = 0

        def set_up_file():
            try:
                self.f = open("test.txt", 'w')
                self.f.write("2.44,3.98,Kendal Mint Cake\n"
                             "3.97,1.71,Pith Helmet\n"
                             "4.02,4.00,Bread\n"
                             "1.41,1.55,Olive Oil\n"
                             "3.35,3.65,Tent\n"
                             "3.46,1.78,Firewood\n"
                             "1.19,2.70,Water\n"
                             "4.64,1.04,Ammunition\n"
                             "4.53,3.11,Tinned Food\n"
                             "4.17,0.20,Weapon")
                self.f.close()
            except (IOError, WindowsError) as e:
                print e.filename + " Cannot be opened!\nThis is an OS lock, " \
                                   "nothing we can do. Re-run the test."
                print "Python traceback follows: \n"
                traceback.print_exc()
                if self.times < 2:
                    self.times += 1
                    print "Trying again in 5 seconds: "
                    time.sleep(5)  # Seconds
                    set_up_file()
        set_up_file()

    def tearDown(self):
        """
        The tearDown() is run after each test method
        """
        try:
            os.remove("test.txt")
        except OSError as e:
            traceback.print_exc()  # Get some output
            raise e  # Do nothing, this is a test, let it fail

    def test_ksf(self):
        ksf = KnapsackFile("test.txt")
        lines = ksf.getlines()
        self.assertEqual(len(lines), 10)

    def test_item_creation(self):
        ksf = KnapsackFile("test.txt")
        lines = ksf.getlines()
        items = Greedy.create_items(lines)
        for i in items:
            self.assertIsInstance(i, Greedy.Item, "i is Not an Item object")
            self.assertIsNotNone(i, "Item creation failed.")

    def test_sort_by_efficiency(self):
        ksf = KnapsackFile("test.txt")
        lines = ksf.getlines()
        items = Greedy.create_items(lines)
        items = Greedy.sort_by_efficiency(items, descending=True)
        last = 0.0
        for i in items:
            if last is not 0.0:
                self.assertTrue(i.efficiency < last)
            last = i.efficiency
        items = Greedy.sort_by_efficiency(items, descending=False)
        last = 0.0
        for i in items:
            if last is not 0.0:
                self.assertTrue(i.efficiency > last)
            last = i.efficiency

    def test_sum_by_weight(self):
        ksf = KnapsackFile("test.txt")
        lines = ksf.getlines()
        items = Greedy.create_items(lines)
        weight_items = Greedy.sum_by_value(limit=3, list_of_items=items, func=lambda item: item.weight)
        self.assertIs(len(weight_items), 1)
        weight_items = Greedy.sum_by_value(limit=4, list_of_items=items, func=lambda item: item.weight)
        self.assertIs(len(weight_items), 2)
        weight_items = Greedy.sum_by_value(limit=6, list_of_items=items, func=lambda item: item.weight)
        self.assertIs(len(weight_items), 3)

    def test_sum_by_profit(self):
        ksf = KnapsackFile("test.txt")
        lines = ksf.getlines()
        items = Greedy.create_items(lines)
        weight_items = Greedy.sum_by_value(limit=6, list_of_items=items, func=lambda item: item.profit)
        self.assertIs(len(weight_items), 1)
        weight_items = Greedy.sum_by_value(limit=7, list_of_items=items, func=lambda item: item.profit)
        self.assertIs(len(weight_items), 2)
        weight_items = Greedy.sum_by_value(limit=9, list_of_items=items, func=lambda item: item.profit)
        self.assertIs(len(weight_items), 3)

if __name__ == '__main__':
    unittest.main()