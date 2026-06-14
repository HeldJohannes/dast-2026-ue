import os
import uuid
from datetime import datetime, timezone
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Import our tests package (which exposes the registry map)
from tests import registry

app = FastAPI(title="maDMP Assessment Service - Group 05")

# Environment variable for base URL setup
TEST_URL = os.getenv("TEST_URL", "http://localhost:8080/tests")

# Custom Exception Handler for JSONDecodeError or other parsing errors to return 400 with JSON-LD
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if "/assess/test/" in request.url.path:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body is not valid JSON."},
            media_type="application/ld+json"
        )
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error."},
        media_type="application/ld+json"
    )

@app.get("/tests/{id}")
async def get_test(id: int):
    test_case = registry.get(id)
    if not test_case:
        return JSONResponse(
            status_code=404,
            content={"error": f"Test {id} is not implemented by this service."},
            media_type="application/ld+json"
        )
        
    return JSONResponse(content=test_case.meta(TEST_URL), media_type="application/ld+json")

@app.post("/assess/test/{id}")
async def assess_test(id: int, request: Request):
    test_case = registry.get(id)
    if not test_case:
        return JSONResponse(
            status_code=404,
            content={"error": f"Test {id} is not implemented by this service."},
            media_type="application/ld+json"
        )
        
    # Attempt parsing request body as JSON
    try:
        madmp = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body is not valid JSON."},
            media_type="application/ld+json"
        )
        
    res = test_case.assess(madmp)
    outcome = res.get("outcome")
    log_message = res.get("log")
    
    result_uuid = str(uuid.uuid4())
    now_str = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    completion_value = "0" if outcome == "indeterminate" else "100"
    
    response_body = {
        "@context": {
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "prov": "http://www.w3.org/ns/prov#",
            "dcterms": "http://purl.org/dc/terms/",
            "dcat": "http://www.w3.org/ns/dcat#",
            "ftr": "https://w3id.org/ftr#",
            "sio": "http://semanticscience.org/resource/",
            "schema": "http://schema.org/"
        },
        "@id": f"urn:dmpEvaluationService:{result_uuid}",
        "@type": "ftr:TestResult",
        "dcterms:identifier": {"@id": f"urn:dmpEvaluationService:{result_uuid}"},
        "dcterms:title": {"@language": "en", "@value": f"{test_case.title} OUTPUT"},
        "dcterms:description": {"@language": "en", "@value": test_case.description},
        "dcterms:license": {"@id": "https://creativecommons.org/publicdomain/zero/1.0/"},
        "prov:value": {"@language": "en", "@value": outcome},
        "prov:generatedAtTime": {"@type": "xsd:dateTime", "@value": now_str},
        "ftr:log": {"@language": "en", "@value": log_message},
        "ftr:completion": {"@type": "xsd:int", "@value": completion_value},
        "ftr:outputFromTest": {"@id": str(id)},
        "ftr:assessmentTarget": {"@id": "https://www.rd-alliance.org/group/dmp-common-standards-wg/outcomes/rda"},
        "prov:wasGeneratedBy": {"@id": f"group-05.assessmentService.test{id}"}
    }
    return JSONResponse(content=response_body, media_type="application/ld+json")
