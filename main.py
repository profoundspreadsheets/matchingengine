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

            if len(inputArray) == 6 or len(inputArray) == 4:
                # size is good, check if order can be added
                if inputArray[1] == "A":
                    order = Order(inputArray[0], inputArray[2],
                              inputArray[3], float(inputArray[4]), int(inputArray[5]))
                    orderBook.match(order)
                if inputArray[1] == "R":
                    orderBook.removeOrder(inputArray[3], inputArray[5])
            elif inputArray[0] == "exit":
                print("Exiting program: {0}".format("OrderBook Matcher"))
                break
            elif inputArray[0] == "help":
                print("print out help here lmao")
            elif inputArray[0] == "printbook":
                orderBook.printBook()
            elif inputArray[0] == "trades":
                orderBook.printTrades()        
            elif inputArray[0] == "read":
                infile = open("matchTest.in", "r", encoding="utf-8")
                for line in infile:
                    #inputLine = sys.stdin.readline().rstrip()
                    inputArray = line.split(" ")

                    if len(inputArray) == 6 or len(inputArray) == 4:
                        # size is good, check if order can be added
                        if inputArray[1] == "A":
                            order = Order(inputArray[0], inputArray[2],
                                    inputArray[3], float(inputArray[4]), int(inputArray[5]))
                            orderBook.match(order)
                        if inputArray[1] == "R":
                            orderBook.removeOrder(inputArray[2], int(inputArray[3]))
            else:
                print("unrecognized: {0}".format(inputArray))
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
