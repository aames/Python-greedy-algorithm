__author__ = 'Andrew'
import traceback
import os
import sys
import re


class SomeDecorating(object):
    def __init__(self, f):
        """
        Decorator function only, just to show it off.
        :param f: The function to decorate
        """
        self.f = f

    def __call__(self):
        print "Entering", self.f.__name__
        self.f()
        print "Exited", self.f.__name__


def timing(f):
    import time

    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2 - time1) * 1000.0)
        return ret

    return wrap


class Item(object):
    """
    The Item is used to represent each item in a collection,
    which forms the knapsack.
    """

    def __init__(self, name, weight, profit):
        """
        :param name: The name of the Item
        :param weight: The weight of the Item
        :param profit: The profit of the Item
        """
        self.name = name
        self.weight = weight
        self.profit = profit
        self.efficiency = profit / weight

    def __repr__(self):
        return "Name: " + self.name + \
               " Weight: " + str(self.weight) + \
               " Profit: " + str(self.profit) + \
               " Efficiency: " + str(round(self.efficiency, 3))

    def __str__(self):
        return "Name: " + self.name + \
               " Weight: " + str(self.weight) + \
               " Profit: " + str(self.profit) + \
               " Efficiency: " + str(round(self.efficiency, 3))


class KnapsackFile(object):
    """
    The KnapsackFile class demonstrates use of an object to fetch data from a file.
    """

    def __init__(self, file_path):
        """
        :param file_path: The file path, no default
        """
        self.file_path = file_path

    def getlines(self, file_path=None):
        """
        :param file_path: The file path to the file containing a list of Items
        :rtype : ordered list of lines from optional file_path variable
        """
        if file_path is None:
            file_path = self.file_path
        lines = None
        try:
            f = open(file_path, 'r')
            assert type(f) is not None, "File f is None type!"
            lines = list(f)
            f.close()
        except Exception as e:
            print "Caught an error in getListOfLines(), raising..."
            traceback.print_exc()
            # now re-raise the exception
            raise e("Unable to open and read " + file_path)
        finally:
            return lines


def create_items(lines):
    """
    :param lines: The list of lines from the Items file
    :rtype : list of Item objects, created from list of strings from file
    """
    items = []
    for line in lines:
        args = line.split(',')
        #print args
        args[2].strip('\n')
        item = Item(args[2], float(args[0]), float(args[1]))
        items.append(item)
    return items


def sort_by_efficiency(list_of_items, descending=True):
    """
    :param list_of_items: The list of items to sort (takes a collection of Item objects)
    :param descending: Sort direction, True is default
    :rtype : sorted list of Items (specifically by efficiency) from original list: list_of_items
        sorting can be default reverse (largest first) or ascending (smallest first)
    """
    return sorted(list_of_items, key=lambda x: x.efficiency, reverse=descending)


def sum_by_value(limit, list_of_items, func):
    """
    :param limit: The limit to sum up to
    :param list_of_items: The list of items to sum (takes a collection of Item objects)
    :param func: The function to perform the Sum on, takes a lambda expression
    :rtype : sorted list of Items from original list: items
    """
    import time
    time1 = time.time()
    sorted_items = sort_by_efficiency(list_of_items, descending=True)
    total = 0.0
    new_items = []
    for item in sorted_items:
        if (total + func(item)) > limit:
            # don't add it, just return
            time2 = time.time()
            print 'SUM function took ' + str((time2 - time1) * 1000.0) + ' ms'
            return new_items
        new_items.append(item)
        total += func(item)
    time2 = time.time()
    print 'SUM function took ' + str((time2 - time1) * 1000.0) + ' ms'
    return new_items


def print_items(items):
    """
    Print out the Item object(s) in the given collection of items
    """
    for i in items:
        print str(i)


def setup():
    f = open("temp.txt", 'w')
    f.write("2.44,3.98,Kendal Mint Cake\n"
            "3.97,1.71,Pith Helmet\n"
            "4.02,4.00,Bread\n"
            "1.41,1.55,Olive Oil\n"
            "3.35,3.65,Tent\n"
            "3.46,1.78,Firewood\n"
            "1.19,2.70,Water\n"
            "4.64,1.04,Ammunition\n"
            "4.53,3.11,Tinned Food\n"
            "4.17,0.20,Weapon")
    f.close()


def teardown():
    try:
        os.remove("temp.txt")
    except OSError as e:
        traceback.print_exc()  # Get some output
        raise e  # re-raise the exception


def check_version():
    def _exit():
        """
        _exit is an in-built function.
        Python interpreter must be 2 and minor must be >=7 because
        no tests have been made for Py3 or less than minor version 7
        """
        print("This script requires Python version 2.7 or higher, but not Python 3!")
        sys.exit(1)

    if sys.version_info.major is not 2:
        _exit()
    else:
        if sys.version_info.minor < 7:
            _exit()


@SomeDecorating
def main(file_path=None, total=None, key=None, remove_file=False):
    """
    :param file_path: The file path to open or default None
    :param total: The total amount to sum by or default None
    :param value: The value expressed as a lambda function or default None
    :param remove_file: Should the file be removed after you're finished?
    :rtype : void
    Operations are:
    1) Create a text file
    2) Create a knapsackFile object
    3) Get the lines of text as a list
    4) Perform knapsack option
    5) Print resulting items in order
    6) Remove the text file
    """
    check_version()

    # Hey! Check out this nested function!
    def menu():
        """
        :rtype : Tuple of String, String representing String, Int
        """

        def get_input(text):
            r = re.compile("[0-9][0-9]", re.IGNORECASE)
            numbers = r.findall(text)
            r1 = re.compile("[a-z]", re.IGNORECASE)
            values = r1.findall(text)
            assert values is not None
            assert numbers is not None
            return values[0], numbers[0]

        def _print_menu():
            print "Do you want to sum for Weight or Profit?"
            print "Enter w for weight or p for profit"
            print "Followed by the amount... "
            print "Here's an example: w,6"

        while True:
            _print_menu()
            raw_text = raw_input()
            try:
                val, num = get_input(raw_text)
                return val, num
            except AssertionError as ae:
                print ae.message + " Caught in get_input()"
                print "Python traceback follows:"
                traceback.print_exc()
            break

    if file_path is None:
        setup()
        ksf = KnapsackFile("temp.txt")
    else:
        ksf = KnapsackFile(file_path)
    items = create_items(ksf.getlines())
    import time
    if total is None or key is None:
        v, total = menu()
        print "v and total are " + str(v) + " and " + str(total)
        time1 = time.time()
        if v is "w":
            items = sum_by_value(limit=int(total), list_of_items=items, func=lambda item: item.weight)
        elif v is "p":
            items = sum_by_value(limit=int(total), list_of_items=items, func=lambda item: item.profit)
        else:
            print "Oops! Something went very wrong here! Did you actually enter w or p?\nRun it again!"
    else:
        items = sum_by_value(limit=total, list_of_items=key)
    time2 = time.time()
    print 'function took ' + str((time2 - time1) * 1000.0) + ' ms'

    print_items(items)
    if remove_file or file_path is None:
        teardown()


if __name__ == '__main__':
    """
    Options of different ways to run are:
    Provide everything it needs..
    main("items.txt", 9, value=lambda item: item.profit)
    Provide no file path, it'll use a temporary file
    main(file_path=None, 9, value=lambda item: item.profit)
    Provide nothing, it'll ask you for what it needs
    main()
    """
    main()