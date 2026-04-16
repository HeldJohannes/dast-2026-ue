const TEST_URL = process.env.TEST_URL || 'http://localhost:8080/tests';

const title = 'Check maDMP JSON Validates Against DMP Common Standard Schema';
const description =
  'Checks that the maDMP JSON contains the minimum required top-level fields of the ' +
  'RDA DMP Common Standard: dmp.title, dmp.created, and dmp.dmp_id.';

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
    '@id': 'urn:dmpEvaluationService:32',
    '@type': ['https://w3id.org/ftr#Test', 'http://www.w3.org/ns/dcat#DataService'],
    'dcterms:identifier': { '@id': '32' },
    'dcterms:title': { '@language': 'en', '@value': title },
    'dcterms:description': { '@language': 'en', '@value': description },
    'dcterms:license': { '@id': 'https://creativecommons.org/licenses/by/4.0/' },
    'dcat:endpointURL': { '@id': `${TEST_URL}/32` },
    'dcat:endpointDescription': null,
    'dcat:version': { '@language': 'en', '@value': '1.0.0' },
    'dcat:keyword': [
      { '@language': 'en', '@value': 'schema validation' },
      { '@language': 'en', '@value': 'DMP Common Standard' },
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
  const dmp = madmp?.dmp;
  if (!dmp) {
    return { outcome: 'fail', log: 'Root dmp object is missing.' };
  }
  const missing = [];
  if (!dmp.title || String(dmp.title).trim() === '') missing.push('dmp.title');
  if (!dmp.created || String(dmp.created).trim() === '') missing.push('dmp.created');
  if (!dmp.dmp_id) missing.push('dmp.dmp_id');

  if (missing.length > 0) {
    return { outcome: 'fail', log: `Missing required fields: ${missing.join(', ')}.` };
  }
  return { outcome: 'pass', log: 'dmp.title, dmp.created, and dmp.dmp_id are all present.' };
}

module.exports = { meta, assess, title, description };
