from biosamples.api import Client as BiosdClient
from biosamples.aap import Client as AapClient
from configparser import RawConfigParser

from biosamples.utilities import is_successful, is_ok, is_status
import os
import json


def read_config(filename):
    """
    Read configuration from file
    :param filename: name of the configuration file
    :return: the config object
    """
    config = RawConfigParser()
    config.read_file(open(filename))
    return config


def get_sample_accession(fin):
    content = json.load(fin)
    temp_accession = next(x for x in content['identifier'] if not x.startswith("MMP"))
    return temp_accession.replace("biosamples:", "")


if __name__ == "__main__":
    config = read_config('./populator/config.ini')
    base_dir = "./site/src/bioschemas"
    base_url_get = "https://wwwdev.ebi.ac.uk/biosamples/"
    base_url_post = "http://localhost:8081/biosamples/"
    filelist = os.listdir(base_dir)
    client_post = BiosdClient(base_url_post)
    client_fetch = BiosdClient(base_url_get)
    aap = AapClient(username=config.get('General', 'aap_username'),
                    password=config.get('General', 'aap_password'),
                    url=config.get('General', 'aap_url'))
    for fname in filelist:
        file_path = os.path.join(base_dir, fname)
        with open(file_path, 'r') as fin:
            sample = dict()
            accession = get_sample_accession(fin)
            if accession is None:
                print("Impossible to extract accession from {}".format(fname))
            try:
                sample = client_fetch.fetch_sample(accession=accession, jwt=aap.get_token())
            except Exception as e:
                if len(e.args) > 1:
                    if is_status(e.args[1], 404):
                        print("Sample {} not found on {}".format(accession, base_url_get))
                        continue
                else:
                    raise e

            sample["domain"] = "self.BiosampleIntegrationTest"
            updated_sample = client_post.update_sample(sample, jwt=aap.get_token())
            print("Submitted sample {} to BioSamples on {}".format(accession, base_url_post))
