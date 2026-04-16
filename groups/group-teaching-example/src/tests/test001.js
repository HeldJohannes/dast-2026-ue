const TEST_URL = process.env.TEST_URL || 'http://localhost:8080/tests';

const title = 'Check for reused dataset declaration';
const description =
  'Given a maDMP JSON document, inspect dataset objects and verify the presence ' +
  'of a field indicating whether the dataset is reused.';

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
    '@id': 'urn:dmpEvaluationService:1',
    '@type': ['https://w3id.org/ftr#Test', 'http://www.w3.org/ns/dcat#DataService'],
    'dcterms:identifier': { '@id': '1' },
    'dcterms:title': { '@language': 'en', '@value': title },
    'dcterms:description': { '@language': 'en', '@value': description },
    'dcterms:license': { '@id': 'https://creativecommons.org/licenses/by/4.0/' },
    'dcat:endpointURL': { '@id': `${TEST_URL}/1` },
    'dcat:endpointDescription': null,
    'dcat:version': { '@language': 'en', '@value': '1.0.0' },
    'dcat:keyword': [
      { '@language': 'en', '@value': 'reused dataset' },
      { '@language': 'en', '@value': 'data reuse' },
      { '@language': 'en', '@value': 'maDMP' },
      { '@language': 'en', '@value': 'completeness' }
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
  const found = datasets.some((ds) => Object.prototype.hasOwnProperty.call(ds, 'is_reused'));
  if (found) {
    return { outcome: 'pass', log: 'At least one dataset contains the is_reused field.' };
  }
  return { outcome: 'fail', log: 'No dataset entry declares the is_reused field.' };
}

module.exports = { meta, assess, title, description };
