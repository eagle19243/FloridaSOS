"""florida_sos Utility methods
"""
import os
import yaml
import logging
import csv
from pathlib import Path


def load_config():
    """Load conf file defined by ENV var FLORIDA_SOS_CONF.
    If not available load ./conf.yaml
    """
    config = {}
    try:
        cfg_file = os.environ.get('FLORIDA_SOS_CONF')
        if not cfg_file:
            cfg_file = os.getcwd() + '/conf.yml'
            logging.warning('using default configuration from %s', cfg_file)
        with open(cfg_file, 'rt') as cfg:
            config = yaml.safe_load(cfg.read())
            logging.debug('config=%s', config)
    except IOError:
        logging.error('Error loading configuration', exc_info=1)
    return config


def remove_output_csv():
    CFG = load_config()
    output = CFG.get('OUTPUT')
    file = Path(output)
    try:
        file.unlink()
    except FileNotFoundError:
        print('No output file')


def save_data(corp_name,
              fei_ein_number,
              date_filed,
              status,
              last_event,
              principal_addr,
              mailing_addr,
              registered_agent_addr,
              officer_addr,
              url):
    CFG = load_config()
    output = CFG.get('OUTPUT')
    file = Path(output)

    field_names = ['Corporation Name',
                   'FEI/EIN Number',
                   'Date Filed',
                   'Status',
                   'Last Event',
                   'Principal Address',
                   'Mailing Address',
                   'Registered Agent Name & Address',
                   'Officer Direct Detail Name & Address',
                   'Link']
    if file.is_file() is False:
        with open(output, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()

    with open(output, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([corp_name,
                         fei_ein_number,
                         date_filed,
                         status,
                         last_event,
                         principal_addr,
                         mailing_addr,
                         registered_agent_addr,
                         officer_addr,
                         url])
