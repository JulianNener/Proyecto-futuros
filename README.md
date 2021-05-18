# Proyecto-futuros
Mini proyecto de arbitraje de futuros.

Aclaración de la notacion utilizada para las variables:

- buy = ask
- sell = bid
- fwd = futuro

###### Funciones

- **get_rates**: devuelve una tupla con las tasas colocadora y tomadora pedidas, utilizando información de los precios de futuros obtenida con *pyRofex* e información de los precios del spot utilizando *yfinance*. Tambien devuelve listas de buy y sell para cada spot y futuro.
- **print_rates**: printea la lista de tasas colocadora y tomadora.
- **check_opportunities**: chequea si la tasa colocadora es superior a la tomadora para alguno de los instrumentos, y manda las ordenes a Rofex en caso de que asi sea. Tambien printea los precios a los que se deberia operar el spot.
- **update_rates**: printea la lista de tasas colocadora y tomadora de cada spot vs futuro en consola cada vez que cambia alguna de ellas.
- **init_tickers**: inicializa los tickers de spots en Yahoo Finance y de los futuros en Rofex, utilizando una lista de spots y una lista de futuros.
- **read_config_file**: lee los costos del archivo de configuración de ejemplo *cfg_file.txt*.

