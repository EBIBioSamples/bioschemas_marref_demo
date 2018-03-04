import biosamples.client as biosd
import biosamples.aap_client as AAP
from populator import AAP_PASSWORD, AAP_USERNAME
import os
import json
import requests


def get_sample_accession(fin):
    content = json.load(fin)
    return next(x for x in content['identifier'] if not x.startswith("MMP"))


if __name__ == "__main__":
    base_dir = "./site/src/bioschemas"
    base_url_get = "https://www.ebi.ac.uk/biosamples/"
    base_url_post = "http://localhost:8081/biosamples/"
    filelist = os.listdir(base_dir)
    client_post = biosd.Client(base_url_post)
    client_fetch = biosd.Client(base_url_get)
    aap = AAP.get_token(username=AAP_USERNAME, password=AAP_PASSWORD)
    for fname in filelist:
        file_path = os.path.join(base_dir, fname)
        with open(file_path, 'r') as fin:
            accession = get_sample_accession(fin)
            if accession is None:
                print("Impossible to extract accession from {}".format(fname))
            response = client_fetch.fetch_sample(accession=accession)
            if response.status_code is not requests.codes.ok:
                raise Exception("An error occurred while retrieving {} from {}".format(accession, base_url))
            sample = response.json()
            client_post.persist_sample(sample)
