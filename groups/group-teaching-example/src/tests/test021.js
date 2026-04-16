const TEST_URL = process.env.TEST_URL || 'http://localhost:8080/tests';

const title = 'Check dataset_id exists';
const description =
  'Checks that at least one dataset in the maDMP declares a dataset_id with a ' +
  'non-empty identifier value, enabling persistent identification of the dataset.';

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
    '@id': 'urn:dmpEvaluationService:21',
    '@type': ['https://w3id.org/ftr#Test', 'http://www.w3.org/ns/dcat#DataService'],
    'dcterms:identifier': { '@id': '21' },
    'dcterms:title': { '@language': 'en', '@value': title },
    'dcterms:description': { '@language': 'en', '@value': description },
    'dcterms:license': { '@id': 'https://creativecommons.org/licenses/by/4.0/' },
    'dcat:endpointURL': { '@id': `${TEST_URL}/21` },
    'dcat:endpointDescription': null,
    'dcat:version': { '@language': 'en', '@value': '1.0.0' },
    'dcat:keyword': [
      { '@language': 'en', '@value': 'dataset_id' },
      { '@language': 'en', '@value': 'identifier' },
      { '@language': 'en', '@value': 'PID' },
      { '@language': 'en', '@value': 'maDMP' }
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
  const found = datasets.some(
    (ds) => ds.dataset_id?.identifier && String(ds.dataset_id.identifier).trim() !== ''
  );
  if (found) {
    return { outcome: 'pass', log: 'At least one dataset has a non-empty dataset_id.identifier.' };
  }
  return { outcome: 'fail', log: 'No dataset declares a dataset_id.identifier.' };
}

module.exports = { meta, assess, title, description };
