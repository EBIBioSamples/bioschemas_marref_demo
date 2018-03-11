class JSONLD2CurationConverter:
    def __init__(self, jsonld):
        self.jsonld = jsonld

    def convert(self):
        biosd_acc = self._get_biosd_accession()
        if biosd_acc is None:
            raise Exception('No BioSamples accession has been found for the provided bioschemas')
        crts = self._get_characteristics()
        ext_references = self._get_datasets()
        curation_obj = dict()
        curation_obj['sample'] = biosd_acc
        if crts:
            curation_obj['attributesPost'] = crts

        if ext_references:
            curation_obj['externalReferencesPost'] = ext_references
        return curation_obj

    def _get_biosd_accession(self):
        identifiers = self.jsonld.get('identifier', None)
        if identifiers is None:
            raise Exception('Identifier is a minimal information for bioschemas:Sample')
        return next(
            (acc.replace("biosamples:", "") for acc in identifiers if acc.startswith("biosamples:")),
            None
        )

    def _get_characteristics(self):
        properties = self.jsonld.get('additionalProperty', list())
        characteristics = list()
        for prop in properties:
            crt = dict()
            crt['type'] = prop['name']
            crt['value'] = prop['value']
            value_references = prop.get('valueReference', list())
            crt['iri'] = [vr.get('url') for vr in value_references if vr.get('url', None) is not None]
            characteristics.append(crt)
        return characteristics

    def _get_datasets(self):
        datasets = self.jsonld.get('dataset', list())
        external_references = list()
        for dataset in datasets:
            ext_ref = dict()
            ext_ref['url'] = dataset
            external_references.append(ext_ref)
        return external_references


class Sample2CurationConverter:
    def __init__(self, sample):
        self.sample = sample

    def convert(self):
        accession = self.sample.get('accession', None)
        if accession is None:
            raise Exception("Sample doesn't have an accession")
        attributes = self._get_curation_attributes()
        external_references = self._get_external_references()
        curation_obj = dict()
        curation_obj['sample'] = accession
        curation_obj['attributesPre'] = attributes
        curation_obj['externalReferencesPre'] = external_references
        return curation_obj

    def _get_curation_attributes(self):
        attributes = list()
        for key, values in self.sample.get('characteristics',dict()).items():
            for value in values:
                attr_pre = dict()
                attr_pre['type'] = key
                attr_pre['value'] = value.get('text', None)
                attr_pre['iri'] = value.get('ontologyTerms', list())
                attributes.append(attr_pre)
        return attributes

    def _get_external_references(self):
        external_references = list()
        for ext_ref in self.sample.get('externalReferences', list()):
            ext_ref_url = ext_ref.get('url', None)
            if ext_ref_url is not None:
                external_references.append(ext_ref_url)
        return external_references
