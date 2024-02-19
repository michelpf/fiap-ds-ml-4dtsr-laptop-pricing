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
    """ Realiza a transformação dos dados em features, com mapeamentos 
        específicos, como por exemplo, one-hot-enconding.
        Parâmetro de entrada recebe o conjunto de dados pré-procesado.
        Parâmetro de saída é o resultado do novo arquivo preparado como features a ser treinado.
    """
    
    logger = logging.getLogger(__name__)
    logger.info('Iniciando a transformação de dados.')

    df = pd.read_csv(input_filepath)

    df_transformed = df.copy()
    logger.info('One-hot enconding para os dados categóricos')

    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=["brand"], prefix="brand")
    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=["processor_brand"], prefix="processor_brand")
    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=["processor_name"], prefix="processor_name")
    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=["os"], prefix="os")
    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=["weight"], prefix="weight")
    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=["touchscreen"], prefix="touchscreen")
    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=["ram_type"], prefix="ram_type")
    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=["os_bit"], prefix="os_bit")

    logger.info('Exportação em arquivo CSV')

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
