from matchingengine import *
import sys


def main():
    orderBook = Orderbook()
    while True:
        try:
            """
            input is defined as:
                timestamp A order-id side price size
                    this input adds an order to the book
                    size inputArray: 6
                timestamp R order-id size
                    this input removes an order from the book
                    size inputArray: 4
            """
            inputLine = sys.stdin.readline().rstrip()
            inputArray = inputLine.split(" ")

            if len(inputArray) == 6:
                # size is good, check if order can be added
                orderBook.addOrder(Order("20210831", "A", "S", 10.4, 100))
                pass
            elif len(inputArray) == 4:
                # size is good, check if order can be removed
                pass
            elif inputArray[0] == "exit":
                print("Exiting program: {0}".format("OrderBook Matcher"))
                break
            elif inputArray[0] == "test":
                print("Dies ist nur ein {0}".format("TEST"))
            elif inputArray[0] == "help":
                print("print out help here lmao")
            elif inputArray[0] == "printbook":
                orderBook.printBook()
                pass
            else:
                print("unrecognized: {0}".format(inputArray))
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()