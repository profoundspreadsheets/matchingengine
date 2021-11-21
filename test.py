import unittest
from matchingengine import *


class TestBook(unittest.TestCase):
    
    def testEmpty(self):
        testBook = Orderbook()
        self.assertTrue(testBook.isEmpty())
    
    def testAskIsLowest(self):
        testBook = Orderbook()
        testBook.addOrder(Order("20210831", "A", "B", 11.4, 100))
        testBook.addOrder(Order("20211031", "A", "B", 11.0, 100))
        highestBid = testBook.getHighestBid()
        self.assertEqual(highestBid, 11.4)

    def testBidIsHighest(self):
        testBook = Orderbook()
        testBook.addOrder(Order("20210831", "A", "S", 10.0, 100))
        testBook.addOrder(Order("20211031", "A", "S", 15.0, 100))
        lowestAsk = testBook.getLowestAsk()
        self.assertEqual(lowestAsk, 10.0)


class TestMatching(unittest.TestCase):
    def testMatchInstantly(self):
        testBook = Orderbook()
        testBook.addOrder(Order("20211031", "A", "S", 20.0, 100))
        incomingBid = Order("20211031", "A", "B", 20.0, 100)
        testBook.match(incomingBid)
        self.assertEqual(len(testBook.asks), 0)

    def testMatchPartiallyBidQuantLower(self):
        testBook = Orderbook()
        testBook.addOrder(Order("20211031", "A", "S", 20.0, 100))
        incomingBid = Order("20211031", "A", "B", 20.0, 50)
        testBook.match(incomingBid)
        self.assertEqual(len(testBook.asks), 1)
        self.assertEqual(testBook.asks[0].quant, 50)

    def testMatchPartiallyBidQuantHigher(self):
        testBook = Orderbook()
        testBook.addOrder(Order("20211031", "A", "S", 20.0, 100))
        incomingBid = Order("20211031", "A", "B", 20.0, 150)
        testBook.match(incomingBid)
        self.assertEqual(len(testBook.asks), 0)
        self.assertEqual(len(testBook.bids), 1)
        self.assertEqual(testBook.bids[0].quant, 50)


if __name__ == "__main__":
    unittest.main()
