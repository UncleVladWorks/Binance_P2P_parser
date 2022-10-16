# Binance P2P parser

Binance P2P parser is a very simple parser of p2p orders with extensive configuration support.

## Usage

```bash
binance_p2p.py -h


Binance P2P parser

optional arguments:

  -h, --help            show this help message and exit

  -s SAVE, --save SAVE  save results of the parser to files (default: True)

  -d DEBUG, --debug DEBUG
                        debug mode - activates print statements across the
                        functions (default: False)

  -pt PARSING_TYPE, --parsing-type PARSING_TYPE
                        which direction should parser collect. If all -
                        collects buy and sell (default: all)

  -p PATH, --path PATH  path to save folder

  -u URL, --url URL     binance search url 

  -hd HEADER, --header HEADER

  -as ASSET, --asset ASSET
                        asset to buy or sell (default: usdt)

  -fi FIAT_INFLOW, --fiat-inflow FIAT_INFLOW
                        fiat currency to buy

  -fo FIAT_OUTFLOW, --fiat-outflow FIAT_OUTFLOW
                        fiat currency to sell

  -bi BANKS_INFLOW, --banks-inflow BANKS_INFLOW
                        list of banks to transfer fiat from

  -bo BANKS_OUTFLOW, --banks-outflow BANKS_OUTFLOW
                        list of banks to transfer fiat to
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)