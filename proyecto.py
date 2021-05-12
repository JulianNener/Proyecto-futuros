import pyRofex
import yfinance as yf
import time

pyRofex.initialize(user="USERNAME",
                   password="PASSWORD",
                   account="ACCOUNT",
                   environment=pyRofex.Environment.REMARKET)

# get_rates me devuelve las tasas colocadora y tomadora, y los buy (ask) y sell (bid) de los futuros (fwd) y spot.
# Separé los costos de transacciones en cost_c y cost_t.
def get_rates(spot, fwd, cost_c=0, cost_t=0):    
    ticker_spot = yf.Ticker(spot) # info del spot que me da yahoo finance
    info_spot = ticker_spot.info
    buy_spot = info_spot["ask"]
    sell_spot = info_spot["bid"]
    
    info_fwd = pyRofex.get_market_data(ticker=fwd, entries=[pyRofex.MarketDataEntry.OFFERS, pyRofex.MarketDataEntry.BIDS]) # info de futuros que me da Rofex
    while not info_fwd["marketData"]["OF"] or not info_fwd["marketData"]["BI"]: # si no hay ordenes de compra o venta entonces nunca podria obtener buy_fwd o sell_fwd
        print("No hay órdenes")
        time.sleep(5)
        
    buy_fwd = info_fwd["marketData"]["OF"][0]["price"]
    sell_fwd = info_fwd["marketData"]["BI"][0]["price"]
    
    colocadora = (sell_fwd - buy_spot - cost_c)/buy_spot
    tomadora = (buy_fwd - sell_spot - cost_t)/sell_spot
    
    return round(colocadora, 6), round(tomadora, 6), buy_spot, sell_spot, buy_fwd, sell_fwd

# print_rates se fija si las tasas colocadora y tomadora cambian cada wait_time segundos,
# y si son distintas a las previas las imprime en consola.
# Cuando las tasas cambian, tambien se fija si hay alguna oportunidad (colocadora > tomadora).
def print_rates(spot, fwd, cost_c=0, cost_t=0, wait_time=1):
    colocadora_prev = 0; tomadora_prev = 0 # inicializo las tasas previas (nunca van a ser 0 asi que las primeras siempre se imprimen)
    
    while True:       
        colocadora, tomadora, buy_spot, sell_spot, buy_fwd, sell_fwd = get_rates(spot, fwd, cost_c, cost_t)

        if (colocadora != colocadora_prev) or (tomadora != tomadora_prev):
            print(colocadora, "\t", tomadora)
            colocadora_prev = colocadora
            tomadora_prev = tomadora
            
            if colocadora > tomadora:
                profit = round((colocadora-tomadora)*100, 2)
                print("**Oportunidad** \nFuturo - Comprar a:", buy_fwd, "\tVender a:", sell_fwd,
                      "\nSpot - Comprar a: ", buy_spot, "\tVender a: ", sell_spot,
                      "\nProfit: ", profit, "%\n")
            
        time.sleep(wait_time)


# Si los costos quisieran leerse de algun archivo de configuración, 
# por ejemplo podría utilizarse una función como esta para el archivo de ejemplo dado.
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

# Caso en que no hay órdenes de futuros
#get_rates("ARS=X", "SOJ.MIN/NOV21") 

# Buscar oportunidades para el spot contra el futuro correspondiente
print_rates("GGAL.BA", "GGAL/JUN21", cost_c, cost_t)
#print_rates("ARS=X", "DLR/AGO21", cost)
