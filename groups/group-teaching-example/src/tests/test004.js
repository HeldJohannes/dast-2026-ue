const TEST_URL = process.env.TEST_URL || 'http://localhost:8080/tests';

const title = 'Check Distribution Entry is Present';
const description =
  'Verifies that at least one dataset in the maDMP declares a distribution array ' +
  'with at least one entry, confirming that storage or access information is provided.';

function meta() {
  return {
    '@context': {
      schema: 'http://schema.org/',
      rdf: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
      ftr: 'https://w3id.org/ftr#',
      sio: 'http://semanticscience.org/resource/',
      xsd: 'http://www.w3.org/2001/XMLSchema#',
      dcterms: 'http://purl.org/dc/terms/',
      dcat: 'http://www.w3.org/ns/dcat#',
      prov: 'http://www.w3.org/ns/prov#'
    },
    '@id': 'urn:dmpEvaluationService:4',
    '@type': ['https://w3id.org/ftr#Test', 'http://www.w3.org/ns/dcat#DataService'],
    'dcterms:identifier': { '@id': '4' },
    'dcterms:title': { '@language': 'en', '@value': title },
    'dcterms:description': { '@language': 'en', '@value': description },
    'dcterms:license': { '@id': 'https://creativecommons.org/licenses/by/4.0/' },
    'dcat:endpointURL': { '@id': `${TEST_URL}/4` },
    'dcat:endpointDescription': null,
    'dcat:version': { '@language': 'en', '@value': '1.0.0' },
    'dcat:keyword': [
      { '@language': 'en', '@value': 'distribution' },
      { '@language': 'en', '@value': 'dataset' },
      { '@language': 'en', '@value': 'maDMP' },
      { '@language': 'en', '@value': 'access' }
    ],
    'dcterms:type': null,
    'dcat:theme': null,
    'dqv:inDimension': null,
    'ftr:supportedBy': null,
    'dpv:isApplicableFor': null,
    'dcterms:creator': { '@id': 'ComplianceEvaluator' },
    'dcat:contactPoint': [{ '@id': 'ComplianceEvaluator' }],
    'sio:SIO_000233': null
  };
}

function assess(madmp) {
  const datasets = madmp?.dmp?.dataset;
  if (!Array.isArray(datasets) || datasets.length === 0) {
    return { outcome: 'fail', log: 'No dataset entries found in dmp.dataset.' };
  }
  const found = datasets.some((ds) => Array.isArray(ds.distribution) && ds.distribution.length > 0);
  if (found) {
    return { outcome: 'pass', log: 'At least one dataset has a non-empty distribution array.' };
  }
  return { outcome: 'fail', log: 'No dataset entry contains a distribution array.' };
}

module.exports = { meta, assess, title, description };
