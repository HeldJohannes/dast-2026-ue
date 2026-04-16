const TEST_URL = process.env.TEST_URL || 'http://localhost:8080/tests';

const title = 'Check cost fields for budget specification';
const description =
  'Verifies that the maDMP includes at least one cost entry with both a title and a ' +
  'numeric value, confirming that a budget for the DMP activities has been specified.';

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
    '@id': 'urn:dmpEvaluationService:104',
    '@type': ['https://w3id.org/ftr#Test', 'http://www.w3.org/ns/dcat#DataService'],
    'dcterms:identifier': { '@id': '104' },
    'dcterms:title': { '@language': 'en', '@value': title },
    'dcterms:description': { '@language': 'en', '@value': description },
    'dcterms:license': { '@id': 'https://creativecommons.org/licenses/by/4.0/' },
    'dcat:endpointURL': { '@id': `${TEST_URL}/104` },
    'dcat:endpointDescription': null,
    'dcat:version': { '@language': 'en', '@value': '1.0.0' },
    'dcat:keyword': [
      { '@language': 'en', '@value': 'cost' },
      { '@language': 'en', '@value': 'budget' },
      { '@language': 'en', '@value': 'value' },
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
  const costs = madmp?.dmp?.cost;
  if (!Array.isArray(costs) || costs.length === 0) {
    return { outcome: 'fail', log: 'No cost entries found in dmp.cost.' };
  }
  const valid = costs.find(
    (c) => c.title && String(c.title).trim() !== '' && c.value !== undefined && c.value !== null
  );
  if (valid) {
    return { outcome: 'pass', log: `Cost entry "${valid.title}" has both title and value declared.` };
  }
  return { outcome: 'fail', log: 'No cost entry has both a title and a value.' };
}

module.exports = { meta, assess, title, description };
