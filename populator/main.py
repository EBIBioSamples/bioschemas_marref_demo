import biosamples.client as biosd
import biosamples.aap_client as AAP
from biosamples.utilities import is_successful, is_ok, is_status
from biosamples import AAP_PASSWORD, AAP_USERNAME, AAP_TOKEN_URL
import os
import json


def get_sample_accession(fin):
    content = json.load(fin)
    temp_accession =  next(x for x in content['identifier'] if not x.startswith("MMP"))
    return temp_accession.replace("biosamples:","")


if __name__ == "__main__":
    base_dir = "./site/src/bioschemas"
    base_url_get = "https://wwwdev.ebi.ac.uk/biosamples/"
    base_url_post = "http://localhost:8081/biosamples/"
    filelist = os.listdir(base_dir)
    client_post = biosd.Client(base_url_post)
    client_fetch = biosd.Client(base_url_get)
    aap = AAP.get_token(username=AAP_USERNAME, password=AAP_PASSWORD, url=AAP_TOKEN_URL)
    for fname in filelist:
        file_path = os.path.join(base_dir, fname)
        with open(file_path, 'r') as fin:
            accession = get_sample_accession(fin)
            if accession is None:
                print("Impossible to extract accession from {}".format(fname))
            try:
                response = client_fetch.fetch_sample(accession=accession)
            except Exception as e:
                if len(e.args) > 1:
                    if is_status(e.args[1], 404):
                        print("Sample {} not found on {}".format(accession, base_url_get))
                        continue
                else:
                    raise e

            if not is_ok(response):
                raise Exception("An error occurred while retrieving {} from {}".format(accession, base_url_get))
            sample = response.json()
            sample["domain"] = "self.BiosampleIntegrationTest"
            response = client_post.persist_sample(sample, jwt=aap)
            if not is_successful(response):
                raise Exception("An error occurred while persisting sample {} to {}".format(accession, base_url_post))
            print("Submitted sample {} to BioSamples on {}".format(accession, base_url_post))
