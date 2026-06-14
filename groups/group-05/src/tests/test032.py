import os
import json
import jsonschema

# Load the schema once at startup
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "madmp_schema.json")
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    SCHEMA = json.load(f)

title = 'Check maDMP JSON Validates Against DMP Common Standard Schema'
description = 'Checks if the JSON matches with DMP Common Standard schema.'

def meta(test_url_base: str) -> dict:
    return {
        "@context": {
            "schema": "http://schema.org/",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "ftr": "https://w3id.org/ftr#",
            "sio": "http://semanticscience.org/resource/",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "dcterms": "http://purl.org/dc/terms/",
            "dcat": "http://www.w3.org/ns/dcat#",
            "prov": "http://www.w3.org/ns/prov#"
        },
        "@id": "urn:dmpEvaluationService:32",
        "@type": ["https://w3id.org/ftr#Test", "http://www.w3.org/ns/dcat#DataService"],
        "dcterms:identifier": {"@id": "32"},
        "dcterms:title": {"@language": "en", "@value": title},
        "dcterms:description": {"@language": "en", "@value": description},
        "dcterms:license": {"@id": "https://creativecommons.org/licenses/by/4.0/"},
        "dcat:endpointURL": {"@id": f"{test_url_base}/32"},
        "dcat:version": {"@language": "en", "@value": "1.0.0"},
        "dcat:keyword": [
            {"@language": "en", "@value": "schema validation"},
            {"@language": "en", "@value": "DMP Common Standard"},
            {"@language": "en", "@value": "maDMP"},
            {"@language": "en", "@value": "completeness"}
        ],
        "dcterms:creator": {"@id": "ComplianceEvaluator"},
        "dcat:contactPoint": [{"@id": "ComplianceEvaluator"}]
    }

def assess(madmp: dict) -> dict:
    if not isinstance(madmp, dict):
        return {"outcome": "fail", "log": "Request body is not a JSON object."}
    
    try:
        jsonschema.validate(instance=madmp, schema=SCHEMA)
    except jsonschema.exceptions.ValidationError as e:
        path = ".".join(str(p) for p in e.path) if e.path else "root"
        err_msg = f"Validation error at '{path}': {e.message} (failed validator: '{e.validator}')"
        return {"outcome": "fail", "log": err_msg}
    except Exception as e:
        return {"outcome": "fail", "log": f"Unexpected error during schema validation: {str(e)}"}
        
    return {"outcome": "pass", "log": "JSON matches with DMP Common Standard schema."}
