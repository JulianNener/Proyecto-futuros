import pyRofex
import yfinance as yf
import time

  pyRofex.initialize(user="USERNAME",
                   password="PASSWORD",
                   account="ACCOUNT",
                   environment=pyRofex.Environment.REMARKET)

tickers_spots = yf.Tickers
prices_fwd = dict()
sizes_fwd = dict()

def market_data_handler(message):

    prices_fwd[ message["instrumentId"]["symbol"] ] = [ message["marketData"]["OF"][0]["price"],
                                                        message["marketData"]["BI"][0]["price"] ]

    sizes_fwd[ message["instrumentId"]["symbol"] ] = [ message["marketData"]["OF"][0]["size"],
                                                       message["marketData"]["BI"][0]["size"] ]

def order_report_handler(message):
    print("Order Report Message Received: {0}".format(message))

def error_handler(message):
    print("Error Message Received: {0}".format(message))

def exception_handler(e):
    print("Exception Occurred: {0}".format(e.message))

pyRofex.init_websocket_connection(market_data_handler, 
                                  order_report_handler, 
                                  error_handler,
                                  exception_handler,
                                  pyRofex.Environment.REMARKET)

pyRofex.order_report_subscription(environment=pyRofex.Environment.REMARKET)

def get_rates(cost_c=0, cost_t=0):    
    buy_spot = dict(); sell_spot = dict()
    for spot in spots:
        buy_spot[spot] = tickers_spots.tickers[spot].info["ask"]
        sell_spot[spot] = tickers_spots.tickers[spot].info["bid"]
    
    buy_fwd = dict(); sell_fwd = dict()
    for fwd in forwards:
        if prices_fwd[fwd][0] and prices_fwd[fwd][1]:
            buy_fwd[fwd] = prices_fwd[fwd][0]
            sell_fwd[fwd] = prices_fwd[fwd][1]
        else:
            buy_fwd[fwd] = sell_fwd[fwd] = None

    colocadora = []; tomadora = []
    for i in range(0, len(spots)):
        spot = spots[i]; fwd = forwards[i]
        if buy_fwd[fwd] and sell_fwd[fwd]:
            colocadora.append( round( (sell_fwd[fwd] - buy_spot[spot] - cost_c)/buy_spot[spot], 6 ) )
            tomadora.append( round( (buy_fwd[fwd] - sell_spot[spot] - cost_t)/sell_spot[spot], 6 ) )
        else:
            colocadora.append(None)
            tomadora.append(None)
    
    return colocadora, tomadora, buy_spot, sell_spot, buy_fwd, sell_fwd

def print_rates(colocadora, tomadora):
    for i in range(0, len(spots)):
        print(spots[i], "-", forwards[i], " ", colocadora[i], " ", tomadora[i])
    print("")

def check_opportunities(colocadora, tomadora, buy_spot, sell_spot, buy_fwd, sell_fwd):
    for i in range(0, len(spots)):
        if colocadora[i] > tomadora[i]:
            fwd = forwards[i]; spot = spots[i]

            profit = round((colocadora[i]-tomadora[i])*100, 2)
            print("** Oportunidad ", spots[i], "-", fwd, " **",
                  "\nSpot - Comprar a: ", buy_spot[spot], " Vender a: ", sell_spot[spot],
                  "\nProfit: ", profit, "%\n")

            pyRofex.send_order(ticker=fwd, 
                               size=sizes_fwd[fwd][0], 
                               side=pyRofex.Side.BUY, 
                               order_type=pyRofex.OrderType.LIMIT, 
                               price=buy_fwd[fwd],
                               cancel_previous=True)

            pyRofex.send_order(ticker=fwd, 
                               size=sizes_fwd[fwd][1], 
                               side=pyRofex.Side.SELL, 
                               order_type=pyRofex.OrderType.LIMIT, 
                               price=sell_fwd[fwd],
                               cancel_previous=True)

def update_rates(cost_c=0, cost_t=0, wait_time=1):
    colocadora_prev = [0]*len(spots); tomadora_prev = [0]*len(spots)
    
    while True:       
        colocadora, tomadora, buy_spot, sell_spot, buy_fwd, sell_fwd = get_rates(cost_c, cost_t)
        
        if (colocadora != colocadora_prev) or (tomadora != tomadora_prev):
            print_rates(colocadora, tomadora)
            colocadora_prev = colocadora
            tomadora_prev = tomadora

            check_opportunities(colocadora, tomadora, buy_spot, sell_spot, buy_fwd, sell_fwd)
            
        time.sleep(wait_time)

def init_tickers(forwards, spots):
    global tickers_spots
    tickers_spots = yf.Tickers(' '.join(spots)) 
    pyRofex.market_data_subscription(tickers=forwards, entries=[pyRofex.MarketDataEntry.BIDS, 
                                                                pyRofex.MarketDataEntry.OFFERS])

def read_config_file(filename):
    cost_c = 0; cost_t = 0
    with open(filename, 'r') as file:
        data = file.readlines()
        line1 = data[0].split('=')
        line2 = data[1].split('=')
        cost_c = float(line1[1])
        cost_t = float(line2[1])

    return cost_c, cost_t


cost_c, cost_t = read_config_file("cfg_file.txt")

forwards = ["GGAL/JUN21", "DLR/JUN21", "DLR/MAY21"]
spots = ["GGAL.BA", "ARS=X", "ARS=X"]

init_tickers(forwards, spots)
update_rates(cost_c=0, cost_t=0, wait_time=10)
