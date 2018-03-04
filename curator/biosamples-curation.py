import argparse
import contextlib
import json
import logging
import sqlite3
import os
from biosamples import AAP_PASSWORD, AAP_USERNAME, BASEURL
import biosamples.converter as converter
import biosamples.client as biosamples
import biosamples.aap_client as AAP
from biosamples.utilities import is_status
from biosamples.Models import Curation
from boltons.iterutils import remap


def drop_empty_values(path, key, value):
    return value is not None and len(value) > 0


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MAIN
parser = argparse.ArgumentParser('Index extracted JSONLD into Solr.')
parser.add_argument('path_to_crawl_db', help='Path to the database used to store crawl information.')
parser.add_argument('url_to_index', nargs='?', help='URL to index using only data from the crawl DB')
args = parser.parse_args()

if not os.path.exists(args.path_to_crawl_db):
    logger.error('Crawl database %s does not exist', args.path_to_crawl_db)
    exit(1)

config = dict({
    'biosamples_base_url': 'http://localhost:8081/biosamples',
    'aap_username': AAP_USERNAME,
    'aap_password': AAP_PASSWORD,
    'curation_domain': 'self.MarRef'
})

jwt = AAP.get_token(AAP_USERNAME, AAP_PASSWORD)
client = biosamples.Client(baseurl=config['biosamples_base_url'])

with sqlite3.connect(args.path_to_crawl_db) as conn:
    conn.execute("PRAGMA busy_timeout = 30000")
    conn.row_factory = sqlite3.Row

    with contextlib.closing(conn.cursor()) as curs:
        curs.execute('SELECT COUNT(*) from jsonld')
        count = int(curs.fetchone()[0])
        i = 1
        rows = curs.execute('SELECT jsonld, url FROM jsonld')

        for row in rows:
            # curs.execute('SELECT jsonld, url FROM jsonld'):
            # print(row['jsonld'])

            jsonld = json.loads(row['jsonld'])
            tmp_curation_obj = converter.JSONLD2CurationConverter(jsonld).convert()
            sample_accession = tmp_curation_obj['sample']
            try:
                response = client.fetch_sample(accession=sample_accession)
                if response.status_code not in [200, 201]:
                    raise Exception("Unable to get samples {} from the provided url", sample_accession)
                sample = response.json()
                tmp_curation_obj.update(converter.Sample2CurationConverter(sample).convert())
                tmp_curation_obj = remap(tmp_curation_obj, drop_empty_values)
                curation_obj = Curation(accession=sample_accession,
                                        attributes_pre=tmp_curation_obj.get('attributesPre', None),
                                        attributes_post=tmp_curation_obj.get('attributesPost', None),
                                        external_references_pre=tmp_curation_obj.get('externalReferencesPre', None),
                                        external_references_post=tmp_curation_obj.get('externalReferencesPost', None),
                                        domain=config['curation_domain'])
                client.curate_sample(sample=sample, curation_object=curation_obj, jwt=jwt)
                logger.info('Curated sample {} ({:d} of {:d})'.format(sample_accession, i, count))
                # print('Curated sample {} ({:d} of {:d})'.format(sample_accession, i, count))
            except Exception as e:
                if is_status(e.args[1], 404):
                    logger.info('Unable to find {} on {}'.format(sample_accession, config['biosamples_base_url']))
                    # print("Unable to find {} on {}".format(sample_accession, config['biosamples_base_url']))
                    continue
            i += 1

        logger.info("Process finished")
