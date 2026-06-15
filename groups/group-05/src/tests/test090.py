title = "Check for ethical issues declaration"
description = "Verifies whether the DMP addresses ethical issues."

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
        "@id": f"urn:dmpEvaluationService:090",
        "@type": ["https://w3id.org/ftr#Test", "http://www.w3.org/ns/dcat#DataService"],
        "dcterms:identifier": {"@id": "090"},
        'dcterms:title': {'@language': 'en', '@value': title},
        'dcterms:description': {'@language': 'en', '@value': description},
        "dcterms:license": {"@id": "https://creativecommons.org/licenses/by/4.0/"},
        "dcat:endpointURL": {"@id": f"{test_url_base}/090"},
        'dcat:endpointDescription': None,
        "dcat:version": {"@language": "en", "@value": "1.0.0"},
        "dcat:keyword": [
            {"@language": "en", "@value": "ethics"},
            {"@language": "en", "@value": "compliance"},
            {"@language": "en", "@value": "data protection"},
            {"@language": "en", "@value": "maDMP"}
        ],
        'dcterms:type': None,
        'dcat:theme': None,
        'dqv:inDimension': None,
        'ftr:supportedBy': None,
        'dpv:isApplicableFor': None,
        "dcterms:creator": {"@id": "ComplianceEvaluator"},
        "dcat:contactPoint": [{"@id": "ComplianceEvaluator"}],
        'sio:SIO_000233': None
    }

def assess(madmp: dict) -> dict:
    if not isinstance(madmp, dict):
        return {"outcome": "fail", "log": "Request body is not a JSON object."}

    # Get the dmp object first
    dmp = madmp.get("dmp", {})
    
    if not isinstance(dmp, dict):
        return {
            "outcome": "fail",
            "log": "Root dmp object is missing or not a JSON object."
        }

    ethical_issues = dmp.get("rdap:ethicalIssuesExist") or dmp.get("ethicalIssuesExist")

    if ethical_issues is None:
        return {
            "outcome": "fail",
            "log": "No ethical issues declaration found in the DMP."
        }

    if isinstance(ethical_issues, str) and ethical_issues.lower() in ["no", "false"]:
        return {
            "outcome": "pass",
            "log": "DMP explicitly states no ethical issues exist."
        }
    elif isinstance(ethical_issues, str) and ethical_issues.lower() in ["yes", "true"]:
        return {
            "outcome": "pass",
            "log": "DMP acknowledges ethical issues and addresses them."
        }
    else:
        return {
            "outcome": "fail",
            "log": "Invalid or unrecognized value for ethical issues declaration."
        }