DEFAULT_CONFIG = {

    # The properties that must exist on schemas for us to accept them for indexing
    'mandatory_properties': {
        # 'Thing': ['@type', 'name', 'url'],
        'Thing': ['@type', 'name'],
        'DataCatalog': ['description', 'keywords'],
        'PhysicalEntity': ['additionalType'],
        'BioChemEntity:Sample': ['identifier'],
        'Sample': ['identifier']
    },

    # The properties that will be indexed if present
    'optional_properties': {
        'Thing': ['alternateName', 'identifier'],
        'BioChemEntity:Sample': ['name', 'url', 'description', 'dataset', 'additionalProperty'],
        'PropertyValue': ['name', 'value', 'unitCode', 'unitText', 'valueReference'],
        'CategoryCode': ['codeValue', 'name', 'url'],
        'Sample': ['name', 'url', 'description','dataset','additionalProperty']
    },

    # The inheritance graph of the schemas that we care about
    'schema_inheritance_graph': {
        'Sample': 'Thing',
        'BioChemEntity:Sample': 'Thing',
        'CreativeWork': 'Thing',
        'DataCatalog': 'CreativeWork',
        'PhysicalEntity': 'Thing',
        'Thing': None
    },

    # The schemas that we want to index
    'schemas_to_parse': ['DataCatalog', 'PhysicalEntity', 'Sample', 'BioChemEntity:Sample'],

    # To capture older Bioschemas markup, we want to map some older schemas onto newer ones
    'schema_map': {'BiologicalEntity': 'PhysicalEntity'},

    # To capture older Bioschemas markup, we want to map some older properties onto newer ones
    'properties_map': {
        'PhysicalEntity': {
            'biologicalType': 'additionalType'
        }
    },

    # Map jsonld keys to how we will store them in Solr
    # If a type is not in the map then the keys are identical
    'jsonld_to_solr_map': {'@type': 'AT_type'},
}