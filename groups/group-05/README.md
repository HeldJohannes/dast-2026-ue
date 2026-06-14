# maDMP Assessment Service - Group 05

This service is a machine-actionable Data Management Plan (maDMP) evaluation service implemented in Python using FastAPI. Its design directly mirrors the structure and patterns of the reference Express application in `group-teaching-example/`.

## Group members

| Name | Student ID |
|------|------------|
| Johannes HELD | 11705340 |
| Habib AHMAD | 12532822 |
| Kyzer GEREZ | 12427543 |
| Gevorg ZAKARYAN | 11941370 |

---

## Architecture

The project is structured under the `src/` directory:

- `main.py`: The entry point for the FastAPI application. It defines the endpoint routes (`GET /tests/{id}` and `POST /assess/test/{id}`) which look up test modules from the registry.
- `tests/registry.py`: Defines the central manual mapping (dictionary) of test IDs to Python test modules.
- `tests/__init__.py`: Package index exposing the registry mapping.
- `tests/test001.py`, `test016.py`, `test032.py`: Independent modules defining the evaluation logic:
  - `title`: String description title of the test.
  - `description`: Detailed description of the test.
  - `meta(test_url)`: Returns a JSON-LD compliant dict representation of the test metadata.
  - `assess(madmp)`: Evaluates the parsed JSON and returns `{"outcome": "pass" | "fail", "log": "Explanation text"}`.

---

## Setup and Installation

### Running Locally
To set up a local virtual environment and start the service on port `8080`:

1. Navigate to the `src/` directory:
   ```bash
   cd src/
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI server using Uvicorn:
   ```bash
   python3 -m uvicorn main:app --host 127.0.0.1 --port 8080
   ```

### Running with Docker
To build and run the service inside a container:

1. Build the Docker image:
   ```bash
   docker build -t dast-group-05 .
   ```
2. Run the Docker container on port `8080` (ensure port `8080` on your host is free):
   ```bash
   docker run -p 8080:8080 dast-group-05
   ```

---

## Executing the Test Cases

### 1. Test Metadata (GET)
To retrieve the metadata of Test 1:
```bash
curl -i http://127.0.0.1:8080/tests/1
```

### 2. Run Test Assessment (POST)
To evaluate a maDMP document against Test 1 using the example pass/fail files:

- **Evaluate passing case**:
  ```bash
  curl -i -X POST -H "Content-Type: application/json" \
    -d @examples/test-001_pass.json \
    http://127.0.0.1:8080/assess/test/1
  ```

- **Evaluate failing case**:
  ```bash
  curl -i -X POST -H "Content-Type: application/json" \
    -d @examples/test-001_fail.json \
    http://127.0.0.1:8080/assess/test/1
  ```

---

## Developer Guide: How to Add New Test Cases (e.g., Test 4)

Adding new evaluation logic is extremely easy and mirrors the pattern of the Express reference app:

1. Create a new file under `src/tests/` named `test004.py`.
2. Implement `title`, `description`, `meta(test_url_base)`, and `assess(madmp)`.
3. Example implementation for `test004.py`:
   ```python
   title = "Check for license declaration"
   description = "Verifies whether a license is specified for the dataset."

   def meta(test_url_base: str) -> dict:
       return {
           # ... standard JSON-LD structure matching the required schema ...
       }

   def assess(madmp: dict) -> dict:
       dmp = madmp.get("dmp", {})
       datasets = dmp.get("dataset", [])
       for ds in datasets:
           if isinstance(ds, dict) and "license" in ds:
               return {"outcome": "pass", "log": "License field present on dataset."}
       return {"outcome": "fail", "log": "No license defined on any dataset."}
   ```
4. Register the new test module in `src/tests/registry.py`:
   ```python
   from . import test001, test016, test032, test004

   registry = {
       1: test001,
       16: test016,
       32: test032,
       4: test004,  # Map the new test ID here
   }
   ```
5. Restart the server. The endpoints `GET /tests/4` and `POST /assess/test/4` will now be dynamically available.
