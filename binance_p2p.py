import configparser
import pathlib
import codecs
import os
import datetime
import argparse
from res import binance_parser, utils


if __name__ == '__main__':

    # get default params
    current_path = str(pathlib.Path().absolute())
    current_timestamp = utils.get_utc_time()

    # get parameters from config file
    config = configparser.ConfigParser(allow_no_value=True)
    config.read_file(codecs.open(os.path.join(current_path, 'config.ini'), "r", "utf8"))

    url = config['parser_parameters']['url']
    header = eval(config['parser_parameters']['header'])
    asset = config['parser_parameters']['asset']
    fiat_inflow = config['parser_parameters']['fiat_inflow']
    fiat_outflow = config['parser_parameters']['fiat_outflow']
    banks_inflow = eval(config['parser_parameters']['banks_inflow'])
    banks_outflow = eval(config['parser_parameters']['banks_outflow'])

    debug = eval(config['local_parameters']['debug'])
    save_to_files = eval(config['local_parameters']['save_to_files'])
    path_to_save_folder = config['local_parameters']['path_to_save_folder']
    name_of_the_csv_for_raw_data = config['local_parameters']['name_of_the_csv_for_raw_data']
    name_of_the_csv_for_compared_data = config['local_parameters']['name_of_the_csv_for_compared_data']

    parsing_type = config['local_parameters']['parsing_type']

    # construct argument parser
    parser = argparse.ArgumentParser(description="Binance P2P parser",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # parser.add_argument("-a", "--archive", action="store_true", help="archive given parameters to config")  # TODO add func to save config
    parser.add_argument("-s", "--save", type=bool, default=save_to_files, help="save results of the parser to files")
    parser.add_argument("-d", "--debug", type=bool, default=debug, help="debug mode - activates print statements across the functions")
    parser.add_argument("-pt", "--parsing-type", type=str, default=parsing_type, help="which direction should parser collect. If all - collects buy and sell")
    parser.add_argument("-p", "--path", type=str, default=current_path,  help="path to save folder")
    parser.add_argument("-u", "--url", type=str, default=url, help="binance search url")
    parser.add_argument("-hd", "--header", type=dict, default=header, help="header for binance request")
    parser.add_argument("-as", "--asset", type=str, default=asset, help="asset to buy or sell")
    parser.add_argument("-fi", "--fiat-inflow", type=str, default=fiat_inflow, help="fiat currency to buy")
    parser.add_argument("-fo", "--fiat-outflow", type=str, default=fiat_outflow, help="fiat currency to sell")
    parser.add_argument("-bi", "--banks-inflow", type=list, default=banks_inflow, help="list of banks to transfer fiat from")
    parser.add_argument("-bo", "--banks-outflow", type=list, default=banks_outflow, help="list of banks to transfer fiat to")
    args = parser.parse_args()
    config = vars(args)

    config['timestamp'] = current_timestamp
    config['name_of_the_csv_for_raw_data'] = name_of_the_csv_for_raw_data
    config['name_of_the_csv_for_compared_data'] = name_of_the_csv_for_compared_data

    print(config)

    parser_class = binance_parser.BinanceParser(config)

    if parsing_type.lower() == 'all':
        df_output = parser_class.parse_binance_from_to()
    elif parsing_type.lower() == 'buy' or parsing_type.lower() == 'sell':
        df_output = parser_class.parse_binance(parsing_type)
    else:
        print('Parameter parsing_type must one of the following: buy, sell or all.')

    print('Binance P2P has been parsed successfully at ', datetime.datetime.now())