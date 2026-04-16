const TEST_URL = process.env.TEST_URL || 'http://localhost:8080/tests';

const title = 'Check license_ref for dataset licence';
const description =
  'Verifies that at least one distribution within the maDMP datasets contains a ' +
  'license entry with a non-empty license_ref URL, ensuring legal terms are declared.';

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
    '@id': 'urn:dmpEvaluationService:58',
    '@type': ['https://w3id.org/ftr#Test', 'http://www.w3.org/ns/dcat#DataService'],
    'dcterms:identifier': { '@id': '58' },
    'dcterms:title': { '@language': 'en', '@value': title },
    'dcterms:description': { '@language': 'en', '@value': description },
    'dcterms:license': { '@id': 'https://creativecommons.org/licenses/by/4.0/' },
    'dcat:endpointURL': { '@id': `${TEST_URL}/58` },
    'dcat:endpointDescription': null,
    'dcat:version': { '@language': 'en', '@value': '1.0.0' },
    'dcat:keyword': [
      { '@language': 'en', '@value': 'license' },
      { '@language': 'en', '@value': 'license_ref' },
      { '@language': 'en', '@value': 'distribution' },
      { '@language': 'en', '@value': 'open access' }
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
  for (const ds of datasets) {
    for (const dist of (ds.distribution || [])) {
      for (const lic of (dist.license || [])) {
        if (lic.license_ref && String(lic.license_ref).trim() !== '') {
          return { outcome: 'pass', log: `Found license_ref '${lic.license_ref}' in a distribution.` };
        }
      }
    }
  }
  return { outcome: 'fail', log: 'No distribution contains a non-empty license_ref.' };
}

module.exports = { meta, assess, title, description };
