import unittest
from matchingengine import *


class TestBook(unittest.TestCase):
    def testAskIsLowest(self):
        testBook = Orderbook()
        testBook.addOrder(Order("20210831", "A", "B", 11.4, 100))
        testBook.addOrder(Order("20211031", "A", "B", 11.0, 100))
        lowestAsk = testBook.getLowestAsk()
        self.assertEqual(lowestAsk, 11.0)

    def testBidIsHighest(self):
        testBook = Orderbook()
        testBook.addOrder(Order("20210831", "A", "S", 10.0, 100))
        testBook.addOrder(Order("20211031", "A", "S", 15.0, 100))
        highestBid = testBook.getHighestBid()
        self.assertEqual(highestBid, 15.0)


if __name__ == "__main__":
    unittest.main()
