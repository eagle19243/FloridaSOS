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


def save_data(corp_name,
              fei_ein_number,
              date_filed,
              status,
              last_event,
              principal_addr,
              mailing_addr,
              registered_agent_addr,
              officer_addr):
    # print(corp_name)
    # print(fei_ein_number)
    # print(date_filed)
    # print(status)
    # print(last_event)
    # print(principal_addr)
    # print(mailing_addr)
    # print(registered_agent_addr)
    # print(officer_addr)
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
                   'Officer Direct Detail Name & Address']
    if file.is_file() is False:
        with open(output, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()

    with open(output, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writerow({'Corporation Name': corp_name,
                         'FEI/EIN Number': fei_ein_number,
                         'Date Filed': date_filed,
                         'Status': status,
                         'Last Event': last_event,
                         'Principal Address': principal_addr,
                         'Mailing Address': mailing_addr,
                         'Registered Agent Name & Address': registered_agent_addr,
                         'Officer Direct Detail Name & Address': officer_addr})
