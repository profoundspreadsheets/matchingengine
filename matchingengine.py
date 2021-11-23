import sortedcontainers
import itertools

class Order:
    def __init__(self, time, orderId, side, price, quant):
        self.time = time
        self.orderId = orderId
        self.side = side
        self.price = price
        self.quant = quant


class Trade:
    def __init__(self, price, quant):
        self.price = price
        self.quant = quant

    def __str__(self):
        return "Trade: {} at {}".format(self.quant, self.price)


class Orderbook:
    def __init__(self, bids=[], asks=[]):
        self.bids = sortedcontainers.SortedList(
            bids, key=lambda order: -order.price)  # sell orders
        self.asks = sortedcontainers.SortedList(
            bids, key=lambda order: order.price)  # buy orders

    def isEmpty(self):
        return len(self.bids) == 0 and len(self.asks) == 0

    def printBook(self):
        print ("Limit Order Book".rjust(20))
        print ("Bids" + "|Asks".rjust(14))
        print("Quant Price  |Price   Quant")

        zipped = list(itertools.zip_longest(self.bids, self.asks))
        for paar in zipped:
            bid = paar[0]
            ask = paar[1]
            priceBid = ""
            quantBid = ""
            priceAsk = ""
            quantAsk = ""

            if bid:
                priceBid = format(bid.price, ".2f")
                quantBid = bid.quant
            if ask:
                priceAsk = format(ask.price, ".2f")
                quantAsk = ask.quant

            print(str(quantBid).rjust(5) + str(priceBid).rjust(8) + "|" + str(priceAsk).rjust(7) + str(quantAsk).rjust(6))
          
    def addOrder(self, order):
        if order.side == "B":
            self.bids.add(order)
        elif order.side == "S":
            self.asks.add(order)

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
                    #print("removing order at index: {}".format(str(index)))
                    liste.pop(index)
                    return True
                elif liste[index].quant > quant:
                    #print("adjusting order at index: {}".format(str(index)))
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

    def match(self, order):
        # match incoming asks
        if order.side == "S" and order.price <= self.getHighestBid(): # spread crossed, start filling order
            for bid in self.bids:
                if order.quant == 0:  # filled
                     break
                elif bid.price < order.price:  # nächstbester bid ist zu niedrig
                    break
                # filling logic
                if order.quant <= bid.quant:  # fill whole order
                    trade = Trade(order.price, order.quant)  # new trade, price is ask price
                    self.removeOrder(bid.orderId, order.quant)  # remove ask                        
                    print ("Trade at {} with quant: {}. Total amount: {}".format(trade.price, trade.quant, trade.price * trade.quant))
                    break  # can already break as order will be filled completely
                elif order.quant > bid.quant:  # fill order until ask, then adjust order quant
                    trade = Trade(order.price, bid.quant)  # new trade
                    order.quant -= bid.quant  # adjust size of incoming bid, some will be filled but not all
                    self.removeOrder(bid.orderId, bid.quant)
                    print ("Trade at {} with quant: {}. Total amount: {}".format(trade.price, trade.quant, trade.price * trade.quant))
            if order.quant > 0:
                self.addOrder(order)

        # match incoming bids
        elif order.side == "B" and order.price >= self.getLowestAsk():  # spread crossed, start filling order
            '''
            case1: bid und best ask ist gleiche größe:
                führe aus zu ask

            case2: bid ist kleinere size als best ask:
                führe aus zu ask und adjustiere größe best ask

                remove order logik ist so geschrieben, dass case 1 & 2 gleichzeitig gehandelt werden

            case3: bid ist größer size als best ask:
                führe aus zu ask und schau ob nächstbester ask gefüllt werden kann
                case3.1:
                    nächstbester ask passt: führe aus und check cases 1-3
                case3.2:
                    nächstbester ask passt nicht: führe rest des bids in orderbook ein
            '''

            # filling order as much as possible
            for ask in self.asks:
                if order.quant == 0:  # order was filled completely
                    break
                elif ask.price > order.price:  # next ask is too expensive
                    break
                # filling logic
                if order.quant <= ask.quant:  # fill whole order
                    trade = Trade(ask.price, order.quant)  # new trade
                    self.removeOrder(ask.orderId, order.quant)  # remove ask
                    order.quant = 0
                    print ("Trade at {} with quant: {}. Total amount: {}".format(trade.price, trade.quant, trade.price * trade.quant))
                    break  # can already break as order will be filled completely
                elif order.quant > ask.quant:  # fill order until ask, then adjust order quant
                    trade = Trade(ask.price, ask.quant)  # new trade
                    order.quant -= ask.quant  # adjust size of incoming bid, some will be filled but not all
                    self.removeOrder(ask.orderId, ask.quant) # remove ask

                    print ("Trade at {} with quant: {}. Total amount: {}".format(trade.price, trade.quant, trade.price * trade.quant))
            if order.quant > 0: #if there is some rest of the order unfilled
                self.addOrder(order)

                
        else:
            self.addOrder(order)  # order didnt cross spread