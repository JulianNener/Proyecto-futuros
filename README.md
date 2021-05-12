# Proyecto-futuros
Mini proyecto de arbitraje de futuros.

Aclaración de la notacion utilizada para las variables:

- buy = ask
- sell = bid
- fwd = futuro

###### Funciones

- **get_rates**: devuelve una tupla con las tasas colocadora y tomadora pedidas, utilizando información de los precios de futuros obtenida con *pyRofex* e información de los precios del spot utilizando *yfinance*. Inputs: (nombre del spot en yahoo finance, nombre del futuro en Rofex, costo asociado con tasa colocadora, costo asociado con tasa tomadora). Outputs: tupla (tasa colocadora, tasa tomadora, precio compra spot, precio venta spot, precio compra futuro, precio venta futuro).
- **print_rates**: printea las tasas colocadora y tomadora en consola cada vez que cambian, chequeando cada un cierto intervalo de tiempo configurable en el input. Si se encuentra que la tasa colocadora es superior a la tomadora, se alerta al usuario en consola con los precios correspondientes de compra y venta de futuros y spot, y el porcentaje de profit. Inputs: (nombre del spot en yahoo finance, nombre del futuro en Rofex, costo asociado con tasa colocadora, costo asociado con tasa tomadora, tiempo entre actualizaciones).
- **read_config_file**: lee los costos del archivo de configuración de ejemplo *cfg_file.txt*.
