import sortedcontainers


class Order:
    def __init__(self, time, orderId, side, price, quant):
        self.time = time
        self.orderId = orderId
        self.side = side
        self.price = price
        self.quant = quant


class Orderbook:
    def __init__(self, bids=[], asks=[]):
        self.bids = sortedcontainers.SortedList(
            bids, key=lambda order: -order.price)  # sell orders
        self.asks = sortedcontainers.SortedList(
            bids, key=lambda order: order.price)  # buy orders

    def printBook(self):
        print("ORDER BOOK")
        print("BIDS\nQuant Price")
        for bid in self.bids:
            print(str(bid.quant) + " " + str(bid.price))

        print("ASKS\nQuant Price")
        for ask in self.asks:
            print(str(ask.quant) + " " + str(ask.price))

    def addOrder(self, order):
        if order.side == "B":
            self.asks.add(order)
        elif order.side == "S":
            self.bids.add(order)

    def removeOrder(self, orderId, quant):
        # find order with id then adjust quant
        # if quant is zero, remove order completely
        if not self.removeOrder_(self.bids, orderId, quant):
            if not self.removeOrder_(self.asks, orderId, quant):
                print("didn't delete nothing")

    def removeOrder_(self, liste, orderId, quant):
        for order in liste:
            if order.orderId == orderId:
                index = liste.index(order)
                if liste[index].quant == quant:
                    print("removing order at index: {}".format(str(index)))
                    liste.pop(index)
                    return True
                elif liste[index].quant > quant:
                    print("adjusting order at index: {}".format(str(index)))
                    liste[index].quant -= quant
                    return True
                else:
                    return False

    def getSpread(self):
        return self.asks[0].price - self.bids[0].price

    def getHighestBid(self):
        if len(self.bids) == 0:
            return 0
        else:
            return self.bids[0].price

    def getLowestAsk(self):
        if len(self.asks) == 0:
            return 0
        else:
            return self.asks[0].price

    def match(self):
        # check if spread passt
        # sell order preis muss kleiner gleich sein als lowest bid
        # buy order preis muss größer gleich sein als highest ask

        # bids buy orders, guy who posted bid is ready to buy stock for limit price
        # asks sell orders, guy who posted ask is ready to sell stock for limit price
        # therefore bids are usually lower than asks
        #
        # wenn ein neues bid reinkommt, prüfen wir ob der limit preis dieses bids größer ist als
        # der höchste ask. bid wird solange gefüllt bis der limit preis erreicht ist, dann kommt
        # der rest ins orderbook
        #
        # gleichwohl wenn ein neuer ask reinkommt, prüfen wir ob dieser ask
        # kleiner ist als der geringste bid
        # ask wird solange gefüllt bis der limit preis erreicht ist, dann kommt der rest ins
        # orderbook
        #
        pass
