import pandas as pd
import os
import requests
import traceback

class BinanceParser():

    def __init__(self, config_dict):

        self.config_dict = config_dict

        self.path_to_save_folder = config_dict['path']
        self.debug = config_dict['debug']
        self.asset = config_dict['asset']
        self.fiat_inflow = config_dict['fiat_inflow']
        self.fiat_outflow = config_dict['fiat_outflow']
        self.banks_inflow = config_dict['banks_inflow']
        self.banks_outflow = config_dict['banks_outflow']
        self.url = config_dict['url']
        self.headers = config_dict['header']
        self.timestamp = config_dict['timestamp']
        self.file_raw_name = config_dict['name_of_the_csv_for_raw_data']
        self.file_output_name = config_dict['name_of_the_csv_for_compared_data']
        self.save_files = config_dict['save']

        if self.save_files:
            self.path_to_base_folder = os.path.join(self.path_to_save_folder, 'data')
            if not os.path.exists(self.path_to_base_folder):
                os.makedirs(self.path_to_base_folder)

    def parse_binance(self, trade_type):

        if trade_type.upper() == 'BUY':
            bank_list = self.banks_inflow
            fiat = self.fiat_inflow
        elif trade_type.upper() == 'SELL':
            bank_list = self.banks_outflow
            fiat = self.fiat_outflow
        else:
            print('Parameter trade_type can be only BUY or SELL')

        if self.debug:
            print('Config: ', self.config_dict)
            print('Folder to save parsed dataframe: ', self.path_to_save_folder)
            print('Asset: ', self.asset)
            print('Fiat: ', fiat)
            print('Bank list: ', bank_list)
            print('Url: ', self.url)
            print('Headers: ', self.headers)
            print('Timestamp: ', self.timestamp)


        for bank in bank_list:

            payload = {"proMerchantAds": False,
                       "page": 1,
                       "rows": 5,
                       "payTypes": [bank],
                       "countries": [],
                       "publisherType": None,
                       "asset": self.asset,
                       "fiat": fiat,
                       "tradeType": trade_type}

            response = requests.post(self.url, headers=self.headers, json=payload)

            if self.debug:
                print("Status Code", response.status_code)
                print("JSON Response ", response.json())

            if response.status_code == 200:

                src0 = response.json()['data']

                dfs = []
                for src in src0:
                    src1 = src['adv']

                    id = src1['advNo']
                    limit_up = src1['maxSingleTransAmount']
                    limit_b = src1['minSingleTransAmount']
                    price = src1['price']
                    tradable_quantity = src1['tradableQuantity']

                    df_loc = pd.DataFrame({
                        'trade_type': [trade_type],
                        'asset': [self.asset],
                        'fiat': [fiat],
                        'bank': [bank],
                        'advNo': [id],
                        'maxSingleTransAmount': [limit_up],
                        'minSingleTransAmount': [limit_b],
                        'price': [price],
                        'tradableQuantity': [tradable_quantity],
                        'time': [self.timestamp]})

                    if self.debug:
                        print('Dataframe for bank {0}: '.format(bank), df_loc)

                    dfs.append(df_loc)

                df_banks = pd.concat(dfs, axis=0)

                df_banks['price'] = df_banks['price'].astype(float)
                df_banks['maxSingleTransAmount'] = df_banks['maxSingleTransAmount'].astype(float)
                df_banks['minSingleTransAmount'] = df_banks['minSingleTransAmount'].astype(float)
                df_banks['tradableQuantity'] = df_banks['tradableQuantity'].astype(float)

                if self.save_files:

                    path_to_raw_data = os.path.join(self.path_to_base_folder, self.file_raw_name + '.csv')

                    try:
                        df_base = pd.read_csv(path_to_raw_data)
                    except FileNotFoundError:
                        df_base = pd.DataFrame(columns=['trade_type', 'asset', 'fiat', 'bank',
                                                        'advNo', 'maxSingleTransAmount', 'minSingleTransAmount',
                                                        'price', 'tradableQuantity', 'time'])
                        print('File with raw data not found. Creating one at {0}'.format(path_to_raw_data))
                    except:
                        traceback.print_exc()

                    if self.debug:
                        print('Loaded dataframe from csv: ', df_base)

                    df_base = df_base.append(df_banks)
                    df_base.to_csv(path_to_raw_data, index=False)

                return df_banks

            else:
                print('No response from Binance')


    def parse_binance_from_to(self):

        df_buy = self.parse_binance('BUY')

        df_sell = self.parse_binance('SELL')

        # calculating output
        exchange_rate = df_sell['price'].max() / df_buy['price'].min()
        best_bank_inflow = df_buy[df_buy['price'] == df_buy['price'].min()]['bank'].iloc[0]
        best_bank_outflow = df_sell[df_sell['price'] == df_sell['price'].max()]['bank'].iloc[0]

        df_loc_ouput = pd.DataFrame({
            'time': [self.timestamp],
            'exchange_rate': [exchange_rate],
            'best_bank_inflow': [best_bank_inflow],
            'best_bank_outflow': [best_bank_outflow]})

        if self.save_files:

            path_to_output_data = os.path.join(self.path_to_base_folder, self.file_output_name + '.csv')

            try:
                df_base_output = pd.read_csv(path_to_output_data)
            except FileNotFoundError:
                df_base_output = pd.DataFrame(columns=['time', 'exchange_rate',
                                                       'best_bank_inflow', 'best_bank_outflow'])
                print('File with output data not found. Creating one at {0}'.format(path_to_output_data))
            except:
                traceback.print_exc()

            df_base_output = df_base_output.append(df_loc_ouput)
            df_base_output.to_csv(path_to_output_data, index=False)

        return df_loc_ouput