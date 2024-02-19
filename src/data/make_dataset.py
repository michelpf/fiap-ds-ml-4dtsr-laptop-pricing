# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path

import pandas as pd
import numpy as np

from dotenv import find_dotenv, load_dotenv

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Realiza o pré-processamento dos dados originais.
        Parâmetro de entrada recebe o data frame original.
        Parâmetro de saída envia o data set pré-processado.
    """
    
    logger = logging.getLogger(__name__)
    logger.info('Iniciando análise dos dados originais (raw).')

    df = pd.read_csv(input_filepath)

    logger.info('Convertendo os dados em caixa baixa.')


    df_transformed = df.copy()
    df_transformed = df_transformed.astype(str).apply(lambda x: x.str.lower())

    logger.info('Remoção de campos não necessários.')

    df_transformed.drop("rating", axis=1, inplace=True)
    df_transformed.drop("Number of Ratings", axis=1, inplace=True)
    df_transformed.drop("Number of Reviews", axis=1, inplace=True)
    df_transformed.drop("msoffice", axis=1, inplace=True)
    df_transformed.drop("processor_gnrtn", axis=1, inplace=True)

    logger.info('Removendo caracteres para transformar em atributos numéricos.')

    df_transformed['ram_gb'] = df_transformed['ram_gb'].replace({' gb' : ''}, regex=True)
    df_transformed['ssd'] = df_transformed['ssd'].replace({' gb' : ''}, regex=True)
    df_transformed['hdd'] = df_transformed['hdd'].replace({' gb' : ''}, regex=True)
    df_transformed['graphic_card_gb'] = df_transformed['ram_gb'].replace({' gb' : ''}, regex=True)
    df_transformed['warranty'] = df_transformed['warranty'].replace({'no warranty' : '0'}, regex=True)
    df_transformed['warranty'] = df_transformed['warranty'].replace({' (years|year)' : ''}, regex=True)
    df_transformed['Touchscreen'] = df_transformed['Touchscreen'].replace({'no' : '0'}, regex=True)
    df_transformed['Touchscreen'] = df_transformed['Touchscreen'].replace({'yes' : '1'}, regex=True)

    logger.info('Renomear coluna para padronização.')

    df_transformed = df_transformed.rename(columns={"Touchscreen": "touchscreen","Price": "price"})

    logger.info('Conversão de tipos de dados para cada feature.')

    df_transformed['ram_gb'] = pd.to_numeric(df_transformed['ram_gb'], errors='coerce').fillna(0).astype(np.int64)
    df_transformed['hdd'] = pd.to_numeric(df_transformed['hdd'], errors='coerce').fillna(0).astype(np.int64)
    df_transformed['ssd'] = pd.to_numeric(df_transformed['ssd'], errors='coerce').fillna(0).astype(np.int64)
    df_transformed['graphic_card_gb'] = pd.to_numeric(df_transformed['graphic_card_gb'], errors='coerce').fillna(0).astype(np.int64)
    df_transformed['warranty'] = pd.to_numeric(df_transformed['warranty'], errors='coerce').fillna(0).astype(np.int64)
    df_transformed['price'] = pd.to_numeric(df_transformed['price'], errors='coerce').fillna(0).astype(np.float64)
    df_transformed['touchscreen'] = pd.to_numeric(df_transformed['touchscreen'], errors='coerce').fillna(0).astype(np.int64)
    df_transformed['price'] = pd.to_numeric(df_transformed['price'], errors='coerce').fillna(0).astype(np.int64)

    logger.info('Ajustando balanço de tipos de dados.')

    replace_dict = {'mac': 'other', 'dos': 'other'}
    df_transformed['os'].replace(replace_dict, inplace=True)

    replace_dict = {'lpddr4x': 'other', 'lpddr4': 'other', 'lpddr3': 'other','ddr5':'other','ddr3':'other'}
    df_transformed['ram_type'].replace(replace_dict, inplace=True)

    replace_dict = {'core i9': 'other', 'pentium quad': 'other', 'm1': 'other','celeron dual':'other','ryzen 9':'other','ryzen 3':'ryzen 7'}
    df_transformed['processor_name'].replace(replace_dict, inplace=True)

    replace_dict = {'acer': 'other', 'msi': 'other', 'apple': 'other','avita':'other'}
    df_transformed['brand'].replace(replace_dict, inplace=True)

    logger.info('Remoção de duplicados.')

    df_transformed.drop_duplicates(inplace=True)

    logger.info('Exportação para arquivo CSV.')

    df_transformed.to_csv(output_filepath, index=False)

    logger.info('Processo terminado.')

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
