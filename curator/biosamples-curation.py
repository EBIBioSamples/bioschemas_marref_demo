import sys

import biosamples.converter as converter
import contextlib
import logging
import json
import os
import sqlite3
from biosamples.models import Curation
from boltons.iterutils import remap
from configparser import RawConfigParser

from biosamples.api import Client as api_client
from biosamples.aap import Client as aap_client

from biosamples.utilities import is_status

import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='./config.ini', help="The configuration file to use")
    return parser.parse_args()


def read_config(filename):
    """
    Read configuration from file
    :param filename: name of the configuration file
    :return: the config object
    """
    config = RawConfigParser()
    config.read_file(open(filename))
    return config


def drop_empty_values(path, key, value):
    return value is not None and len(value) > 0


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    args = parse_arguments()

    config = read_config(args.config)

    if not os.path.exists(config.get('General', 'crawl_db_path')):
        logger.error('Crawl database %s does not exist', config.get('General', 'crawl_db_path'))
        exit(1)

    aap = aap_client(
        config.get('General', 'aap_username'),
        config.get('General', 'aap_password'),
        config.get('General', 'aap_url'))
    biosd = api_client(url=config.get('General', 'biosamples_url'))

    with sqlite3.connect(config.get('General', 'crawl_db_path')) as conn:
        conn.execute("PRAGMA busy_timeout = 30000")
        conn.row_factory = sqlite3.Row

        with contextlib.closing(conn.cursor()) as curs:
            curs.execute('SELECT COUNT(*) from jsonld')
            count = int(curs.fetchone()[0])
            i = 1
            rows = curs.execute('SELECT jsonld, url FROM jsonld')

            for row in rows:

                jsonld = json.loads(row['jsonld'])
                tmp_curation_obj = converter.JSONLD2CurationConverter(jsonld).convert()
                sample_accession = tmp_curation_obj['sample']
                try:
                    sample = biosd.fetch_sample(accession=sample_accession)
                    tmp_curation_obj.update(converter.Sample2CurationConverter(sample).convert())
                    tmp_curation_obj = remap(tmp_curation_obj, drop_empty_values)
                    curation_obj = Curation(attributes_pre=tmp_curation_obj.get('attributesPre', None),
                                            attributes_post=tmp_curation_obj.get('attributesPost', None),
                                            external_references_pre=tmp_curation_obj.get('externalReferencesPre', None),
                                            external_references_post=tmp_curation_obj.get('externalReferencesPost',
                                                                                          None))
                    curation_response = biosd.curate_sample(sample=sample,
                                                            curation_object=curation_obj,
                                                            domain=config.get('General', 'curation_domain'),
                                                            jwt=aap.get_token())
                    logger.info('Curated sample {} ({:d} of {:d})'.format(sample_accession, i, count))
                except Exception as e:
                    if len(e.args) > 1:
                        if is_status(e.args[1], 404):
                            logger.info('Unable to find {} on {}'.format(sample_accession, config['biosamples_base_url']))
                            continue
                    else:
                        logger.error(e)
                        sys.exit(1)
                i += 1

            logger.info("Process finished")
