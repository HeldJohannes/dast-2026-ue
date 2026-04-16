const express = require('express');
const { randomUUID } = require('crypto');
const registry = require('./tests/registry');

const app = express();
const PORT = process.env.PORT || 8080;

// Parse JSON bodies; return 400 on malformed JSON
app.use((req, res, next) => {
  express.json()(req, res, (err) => {
    if (err) {
      return res.status(400)
        .set('Content-Type', 'application/ld+json')
        .json({ error: 'Request body is not valid JSON.' });
    }
    next();
  });
});

// GET /tests/:id
app.get('/tests/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  const entry = registry[id];
  if (!entry) {
    return res.status(404)
      .set('Content-Type', 'application/ld+json')
      .json({ error: `Test ${id} is not implemented by this service.` });
  }
  res.status(200)
    .set('Content-Type', 'application/ld+json')
    .json(entry.meta());
});

// POST /assess/test/:id
app.post('/assess/test/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  const entry = registry[id];
  if (!entry) {
    return res.status(404)
      .set('Content-Type', 'application/ld+json')
      .json({ error: `Test ${id} is not implemented by this service.` });
  }

  const madmp = req.body;
  const { outcome, log } = entry.assess(madmp);
  const uuid = randomUUID();
  const now = new Date().toISOString();
  const completion = outcome === 'indeterminate' ? '0' : '100';

  const result = {
    '@context': {
      xsd: 'http://www.w3.org/2001/XMLSchema#',
      prov: 'http://www.w3.org/ns/prov#',
      dcterms: 'http://purl.org/dc/terms/',
      dcat: 'http://www.w3.org/ns/dcat#',
      ftr: 'https://w3id.org/ftr#',
      sio: 'http://semanticscience.org/resource/',
      schema: 'http://schema.org/'
    },
    '@id': `urn:dmpEvaluationService:${uuid}`,
    '@type': 'ftr:TestResult',
    'dcterms:identifier': { '@id': `urn:dmpEvaluationService:${uuid}` },
    'dcterms:title': {
      '@language': 'en',
      '@value': `${entry.title} OUTPUT`
    },
    'dcterms:description': {
      '@language': 'en',
      '@value': entry.description
    },
    'dcterms:license': {
      '@id': 'https://creativecommons.org/publicdomain/zero/1.0/'
    },
    'prov:value': { '@language': 'en', '@value': outcome },
    'prov:generatedAtTime': { '@type': 'xsd:dateTime', '@value': now },
    'ftr:log': { '@language': 'en', '@value': log },
    'ftr:completion': { '@type': 'xsd:int', '@value': completion },
    'ftr:outputFromTest': { '@id': String(id) },
    'ftr:assessmentTarget': {
      '@id': 'https://www.rd-alliance.org/group/dmp-common-standards-wg/outcomes/rda'
    },
    'prov:wasGeneratedBy': {
      '@id': `group-teaching-example.referenceImplementation.test${String(id).padStart(3, '0')}`
    }
  };

  res.status(200)
    .set('Content-Type', 'application/ld+json')
    .json(result);
});

app.listen(PORT, () => {
  console.log(`maDMP Assessment Service (group-teaching-example) listening on port ${PORT}`);
});
