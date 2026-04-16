const TEST_URL = process.env.TEST_URL || 'http://localhost:8080/tests';

const title = 'Check dmp.contributor name, role, and contact';
const description =
  'Verifies that the maDMP declares at least one contributor with a non-empty name, ' +
  'a role array with at least one entry, and a contact email address (mbox).';

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
    '@id': 'urn:dmpEvaluationService:97',
    '@type': ['https://w3id.org/ftr#Test', 'http://www.w3.org/ns/dcat#DataService'],
    'dcterms:identifier': { '@id': '97' },
    'dcterms:title': { '@language': 'en', '@value': title },
    'dcterms:description': { '@language': 'en', '@value': description },
    'dcterms:license': { '@id': 'https://creativecommons.org/licenses/by/4.0/' },
    'dcat:endpointURL': { '@id': `${TEST_URL}/97` },
    'dcat:endpointDescription': null,
    'dcat:version': { '@language': 'en', '@value': '1.0.0' },
    'dcat:keyword': [
      { '@language': 'en', '@value': 'contributor' },
      { '@language': 'en', '@value': 'role' },
      { '@language': 'en', '@value': 'contact' },
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
  const contributors = madmp?.dmp?.contributor;
  if (!Array.isArray(contributors) || contributors.length === 0) {
    return { outcome: 'fail', log: 'No contributor entries found in dmp.contributor.' };
  }
  const valid = contributors.find(
    (c) =>
      c.name && String(c.name).trim() !== '' &&
      Array.isArray(c.role) && c.role.length > 0 &&
      c.mbox && String(c.mbox).trim() !== ''
  );
  if (valid) {
    return { outcome: 'pass', log: `Contributor "${valid.name}" has name, role, and mbox declared.` };
  }
  return {
    outcome: 'fail',
    log: 'No contributor has all three required fields: name, role (non-empty array), and mbox.'
  };
}

module.exports = { meta, assess, title, description };
