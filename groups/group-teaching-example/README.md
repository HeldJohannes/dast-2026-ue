# Group Teaching Example — Reference Implementation

> **Note for students:** This is the teaching team's reference implementation. It demonstrates the expected project structure, JSON-LD response formats, and Docker setup. Your own implementation should follow the same patterns but implement your assigned test IDs with real logic.

---

## Group members

| Name | Student ID |
|------|------------|
| Teaching Team (reference) | 0255187 |
| Teaching Team (reference) | 0255187 |

---

## Assigned tests

| ID  | Title |
|-----|-------|
| 1   | Check for reused dataset declaration |
| 4   | Check Distribution Entry is Present |
| 21  | Check dataset_id exists |
| 32  | Check maDMP JSON Validates Against DMP Common Standard Schema |
| 58  | Check license_ref for dataset licence |
| 63  | Check ethical_issues_exist for valid value |
| 97  | Check dmp.contributor name, role, and contact |
| 104 | Check cost fields for budget specification |

---

## Technology stack

| Component | Choice |
|-----------|--------|
| Language | Node.js 20 |
| Framework | Express 4 |
| Base image | `node:20-alpine` |

---

## Local development

Install dependencies and start the server:

```bash
cd src
npm install
node index.js
```

The service will be available at `http://localhost:8080`.

Test an endpoint:

```bash
# Get test metadata
curl http://localhost:8080/tests/1

# Assess a maDMP (pass example)
curl -X POST http://localhost:8080/assess/test/1 \
  -H "Content-Type: application/json" \
  -d @examples/test-001_pass.json

# Assess a maDMP (fail example)
curl -X POST http://localhost:8080/assess/test/1 \
  -H "Content-Type: application/json" \
  -d @examples/test-001_fail.json
```

To override the base URL used in `dcat:endpointURL` responses:

```bash
TEST_URL=https://my-service.example.org/tests node index.js
```

---

## Design decisions

- **One file per test** — each test lives in `src/tests/testNNN.js` and exports a `meta()` function (static JSON-LD) and an `assess(madmp)` function. Adding a new test only requires creating a new file and registering it in `src/tests/registry.js`.
- **Mocked logic** — the assess functions perform simple field-presence checks on the maDMP structure. This is intentional for a reference/teaching example; real implementations should implement the full test procedure described in the test catalogue.
- **Inline `@context`** — the JSON-LD context is inlined in every response (rather than by reference) so the document is self-contained and usable offline.
- **`prov:value` for outcome** — the outcome of each assessment is expressed as `prov:value` following the actual FTR vocabulary usage.
