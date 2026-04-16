const TEST_URL = process.env.TEST_URL || 'http://localhost:8080/tests';

const title = 'Check ethical_issues_exist for valid value';
const description =
  'Verifies that the maDMP declares dmp.ethical_issues_exist and that its value is ' +
  'one of the controlled vocabulary terms: "yes", "no", or "unknown".';

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
    '@id': 'urn:dmpEvaluationService:63',
    '@type': ['https://w3id.org/ftr#Test', 'http://www.w3.org/ns/dcat#DataService'],
    'dcterms:identifier': { '@id': '63' },
    'dcterms:title': { '@language': 'en', '@value': title },
    'dcterms:description': { '@language': 'en', '@value': description },
    'dcterms:license': { '@id': 'https://creativecommons.org/licenses/by/4.0/' },
    'dcat:endpointURL': { '@id': `${TEST_URL}/63` },
    'dcat:endpointDescription': null,
    'dcat:version': { '@language': 'en', '@value': '1.0.0' },
    'dcat:keyword': [
      { '@language': 'en', '@value': 'ethics' },
      { '@language': 'en', '@value': 'ethical_issues_exist' },
      { '@language': 'en', '@value': 'controlled vocabulary' },
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

const VALID_VALUES = new Set(['yes', 'no', 'unknown']);

function assess(madmp) {
  const value = madmp?.dmp?.ethical_issues_exist;
  if (value === undefined || value === null) {
    return { outcome: 'fail', log: 'Field dmp.ethical_issues_exist is missing.' };
  }
  if (VALID_VALUES.has(String(value).toLowerCase())) {
    return { outcome: 'pass', log: `dmp.ethical_issues_exist is "${value}", which is a valid value.` };
  }
  return {
    outcome: 'fail',
    log: `dmp.ethical_issues_exist is "${value}" which is not one of the allowed values: yes, no, unknown.`
  };
}

module.exports = { meta, assess, title, description };
