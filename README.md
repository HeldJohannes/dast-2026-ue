# Data Stewardship 2026 — maDMP Assessment Service

> **Submission deadline:** _TBD — ask the teaching team_

This repository is the submission hub for the **maDMP Assessment Service** exercise. Each group implements a small REST API that evaluates machine-actionable Data Management Plans (maDMPs) against a set of FAIR tests and returns results in the [FTR v1.2.0](https://w3id.org/ftr) JSON-LD vocabulary.

---

## Table of contents

1. [Exercise overview](#exercise-overview)
2. [Repository structure](#repository-structure)
3. [Submission rules](#submission-rules)
4. [Required files](#required-files)
5. [API specification](#api-specification)
6. [Response format (JSON-LD)](#response-format-json-ld)
7. [Docker requirements](#docker-requirements)
8. [CI/CD pipeline](#cicd-pipeline)
9. [Reference implementation](#reference-implementation)
10. [How to submit](#how-to-submit)

---

## Exercise overview

Each group is assigned a set of test IDs from the [maDMP Catalogue of Tests](https://docs.ostrails.eu/en/latest/commons/dmp/dmp-catalogue-of-tests.html). For each assigned test the group must:

1. Implement the test logic as a REST endpoint.
2. Return a structured JSON-LD response following the FTR vocabulary.
3. Package the service in a Docker image.
4. Provide example input files (one that produces `pass`, one that produces `fail`) for every test.

The number of tests per group is _TBD — ask the teaching team_.

---

## Repository structure

```
groups/
  group-01/           ← your group folder (name = your branch name)
    Dockerfile
    LICENSE
    README.md
    tests.json        ← machine-readable list of your assigned test IDs
    examples/
      test-001_pass.json
      test-001_fail.json
      ...             ← one pass + one fail file per assigned test ID
    src/              ← your application source code (any language)
      ...

  group-teaching-example/   ← reference implementation (read-only)
```

---

## Submission rules

| Rule | Detail |
|------|--------|
| **One folder per group** | All your files must live inside `groups/group-NN/`. Changes outside this folder will be rejected by the pipeline. |
| **Branch name** | Your working branch must be named exactly `group-NN` (e.g. `group-01`, `group-12`). This name is used as your group identifier throughout the pipeline. |
| **No changes outside your folder** | Do not touch `groups/group-teaching-example/`, or any other group's folder. The pipeline enforces this automatically. |
| **Merge request target** | Open your MR against the `submissions` branch — not `main`. |
| **One MR per group** | Keep a single open MR for your group. Push new commits to update it; do not open multiple MRs. |

---

## Required files

Every group folder **must** contain the following files or the `validate-structure` pipeline job will fail.

### `LICENSE`

Any standard open-source licence (MIT, Apache-2.0, CC-BY-4.0, etc.). The file must exist.

### `tests.json`

A non-empty JSON array of the integer test IDs your group was assigned:

```json
[1, 4, 21]
```

### `README.md`

Must contain a **Group members** section with a table listing every member's name and student ID:

```markdown
## Group members

| Name | Student ID |
|------|------------|
| Jane Doe | 12345678 |
| John Smith | 87654321 |
```

### `examples/test-NNN_pass.json` and `examples/test-NNN_fail.json`

One pair of example maDMP files per assigned test ID (zero-padded three-digit number):

- `test-001_pass.json` — a maDMP that your implementation should assess as `pass`
- `test-001_fail.json` — a maDMP that your implementation should assess as `fail`

### `Dockerfile`

Builds and starts your service on port `8080`. See [Docker requirements](#docker-requirements).

---

## API specification

Your service must expose two endpoints on port `8080`.

### `GET /tests/:id`

Returns the metadata of a single test in JSON-LD (`ftr:Test` type).

- **200 OK** — test found; body is a JSON-LD document (see format below)
- **404 Not Found** — test ID not registered in your service

### `POST /assess/test/:id`

Accepts a maDMP JSON document in the request body and returns an assessment result.

- **Request**: `Content-Type: application/json`, body is a maDMP object
- **200 OK** — assessment completed; body is a JSON-LD document (`ftr:TestResult` type)
- **400 Bad Request** — request body is not valid JSON
- **404 Not Found** — test ID not registered

---

## Response format (JSON-LD)

All responses must use `Content-Type: application/ld+json`.

### `GET /tests/:id` — `ftr:Test`

```json
{
  "@context": {
    "schema": "http://schema.org/",
    "rdf":    "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "ftr":    "https://w3id.org/ftr#",
    "sio":    "http://semanticscience.org/resource/",
    "xsd":    "http://www.w3.org/2001/XMLSchema#",
    "dcterms":"http://purl.org/dc/terms/",
    "dcat":   "http://www.w3.org/ns/dcat#",
    "prov":   "http://www.w3.org/ns/prov#"
  },
  "@id":   "urn:dmpEvaluationService:1",
  "@type": ["https://w3id.org/ftr#Test", "http://www.w3.org/ns/dcat#DataService"],
  "dcterms:identifier":        { "@id": "1" },
  "dcterms:title":             { "@language": "en", "@value": "Check for reused dataset declaration" },
  "dcterms:description":       { "@language": "en", "@value": "..." },
  "dcterms:license":           { "@id": "https://creativecommons.org/licenses/by/4.0/" },
  "dcat:endpointURL":          { "@id": "http://localhost:8080/tests/1" },
  "dcat:version":              { "@language": "en", "@value": "1.0.0" },
  "dcat:keyword":              [{ "@language": "en", "@value": "maDMP" }],
  "dcterms:creator":           { "@id": "ComplianceEvaluator" },
  "dcat:contactPoint":         [{ "@id": "ComplianceEvaluator" }]
}
```

### `POST /assess/test/:id` — `ftr:TestResult`

```json
{
  "@context": {
    "xsd":    "http://www.w3.org/2001/XMLSchema#",
    "prov":   "http://www.w3.org/ns/prov#",
    "dcterms":"http://purl.org/dc/terms/",
    "dcat":   "http://www.w3.org/ns/dcat#",
    "ftr":    "https://w3id.org/ftr#",
    "sio":    "http://semanticscience.org/resource/",
    "schema": "http://schema.org/"
  },
  "@id":   "urn:dmpEvaluationService:<uuid>",
  "@type": "ftr:TestResult",
  "dcterms:identifier":   { "@id": "urn:dmpEvaluationService:<uuid>" },
  "dcterms:title":        { "@language": "en", "@value": "Check for reused dataset declaration OUTPUT" },
  "dcterms:description":  { "@language": "en", "@value": "..." },
  "dcterms:license":      { "@id": "https://creativecommons.org/publicdomain/zero/1.0/" },
  "prov:value":           { "@language": "en", "@value": "pass" },
  "prov:generatedAtTime": { "@type": "xsd:dateTime", "@value": "2026-04-16T10:00:00Z" },
  "ftr:log":              { "@language": "en", "@value": "Field is_reused found on at least one dataset." },
  "ftr:completion":       { "@type": "xsd:int", "@value": "100" },
  "ftr:outputFromTest":   { "@id": "1" },
  "ftr:assessmentTarget": { "@id": "https://www.rd-alliance.org/group/dmp-common-standards-wg/outcomes/rda" },
  "prov:wasGeneratedBy":  { "@id": "group-01.assessmentService.test1" }
}
```

Key fields:

| Field | Values | Notes |
|-------|--------|-------|
| `prov:value` | `"pass"` \| `"fail"` \| `"indeterminate"` | The assessment outcome |
| `ftr:completion` | `"100"` for pass/fail, `"0"` for indeterminate | Typed as `xsd:int` |
| `@id` (result) | A unique URN per request | Use a UUID or similar |

---

## Docker requirements

| Requirement | Detail |
|-------------|--------|
| **Port** | Service must listen on `8080` |
| **Base image** | Any — but prefer slim/alpine variants |
| **Max image size** | **500 MB** compressed. Larger images will slow down the CI runner for everyone. Use `docker images` to check locally before pushing. |
| **No root secrets** | Do not bake credentials, API keys, or `.env` files into the image |
| **Self-contained** | The image must start with `docker run -p 8080:8080 <image>` and no extra flags |

Tips to keep images small:
- Use `node:20-alpine`, `python:3.11-alpine`, `eclipse-temurin:21-jre-alpine`, etc.
- In multi-stage builds, copy only the production artifact into the final stage
- For Node.js: install only production dependencies (`npm install --omit=dev`)
- For Python: do not install dev/test packages in the final image
- For Java: use JRE (not JDK) in the final stage

---

## CI/CD pipeline

Every MR targeting the `submissions` branch automatically runs a three-stage pipeline:

### Stage 1 — `validate`

Two jobs run in parallel:

**`validate-changes`** — Ensures all changed files are within your group folder (`groups/group-NN/`). Any file outside that path fails the job.

**`validate-structure`** — Checks:
- `LICENSE` file exists
- `tests.json` exists and is a non-empty JSON array
- `README.md` exists and has a non-empty **Group members** section with at least one member row
- Both `test-NNN_pass.json` and `test-NNN_fail.json` exist in `examples/` for every ID in `tests.json`

### Stage 2 — `build`

Runs `docker build` against your `Dockerfile`. Fails on any build error.

### Stage 3 — `test`

Starts the container and runs automated checks for each test ID:

1. `GET /tests/:id` — expects HTTP 200 and `@type` containing `ftr#Test`
2. `POST /assess/test/:id` with the `_pass.json` example — expects `prov:value = "pass"`
3. `POST /assess/test/:id` with the `_fail.json` example — expects `prov:value = "fail"`

All three checks must pass for every assigned test ID. The full request and response bodies are printed in the job log for inspection.

---

## Reference implementation

`groups/group-teaching-example/` contains a working Node.js + Express implementation covering 8 test IDs. Use it to understand:

- The expected folder structure
- The exact JSON-LD response shapes
- How to wire up the Docker setup
- How example files should look

The reference uses **mocked logic** (simple field-presence checks). Your implementation should implement the actual test logic described in the [test catalogue](https://docs.ostrails.eu/en/latest/commons/dmp/dmp-catalogue-of-tests.html).

---

## How to submit

### Step 1 — Fork the repository

1. Open the repository on GitLab: `https://gitlab.tuwien.ac.at/crdm/data-stewardship/dast-2026-ue`
2. Click the **Fork** button (top-right corner of the project page).
3. Select your personal namespace or your group's namespace as the destination.
4. GitLab will create a copy of the repository under your account.

> **Why fork?** Forking gives you full write access to your own copy while keeping the upstream repository clean. Your MR will be opened from your fork back into the main repository.

### Step 2 — Clone your fork and set up your branch

```bash
# Clone your fork (replace <your-username> with your GitLab username)
git clone git@gitlab.tuwien.ac.at:<your-username>/dast-2026-ue.git
cd dast-2026-ue

# Add the upstream repository as a remote (useful to pull future updates)
git remote add upstream git@gitlab.tuwien.ac.at:crdm/data-stewardship/dast-2026-ue.git

# Create your group branch (replace NN with your group number)
git checkout -b group-NN
```

### Step 3 — Create your group folder

```bash
# Copy the reference structure as a starting point
cp -r groups/group-teaching-example groups/group-NN

# Replace the contents with your own implementation
```

### Step 4 — Commit and push

```bash
git add groups/group-NN/
git commit -m "group-NN: initial submission"
git push -u origin group-NN
```

### Step 5 — Open a Merge Request

1. Go to your fork on GitLab.
2. Click **Create merge request** (GitLab will suggest it after your push).
3. Set the target:
   - **Source branch**: `group-NN` (your fork)
   - **Target repository**: `crdm/data-stewardship/dast-2026-ue`
   - **Target branch**: `submissions`
4. Fill in the MR title and description, then click **Create merge request**.

The pipeline runs automatically on every push to the MR. Fix any failing jobs and push again — the pipeline re-runs on each commit.

---

## Questions and support

Open an issue in this repository or contact the teaching team via the course platform.