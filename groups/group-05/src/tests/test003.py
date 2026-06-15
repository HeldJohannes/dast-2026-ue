title = "Check for contributor ORCID identifiers"
description = "Verifies whether contributors have valid ORCID identifiers."

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
        "@id": f"urn:dmpEvaluationService:003",
        "@type": ["https://w3id.org/ftr#Test", "http://www.w3.org/ns/dcat#DataService"],
        "dcterms:identifier": {"@id": "003"},
        'dcterms:title': {'@language': 'en', '@value': title},
        'dcterms:description': {'@language': 'en', '@value': description},
        "dcterms:license": {"@id": "https://creativecommons.org/licenses/by/4.0/"},
        "dcat:endpointURL": {"@id": f"{test_url_base}/003"},
        'dcat:endpointDescription': None,
        "dcat:version": {"@language": "en", "@value": "1.0.0"},
        "dcat:keyword": [
            {"@language": "en", "@value": "contributor"},
            {"@language": "en", "@value": "ORCID"},
            {"@language": "en", "@value": "persistent identifier"},
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

    # Get the dmp object first (as per README structure)
    dmp = madmp.get("dmp", {})
    
    if not isinstance(dmp, dict):
        return {
            "outcome": "fail",
            "log": "Root dmp object is missing or not a JSON object."
        }

    contributors = dmp.get("contributor")

    if not isinstance(contributors, list) or len(contributors) == 0:
        return {
            "outcome": "fail",
            "log": "No contributor entries found in the DMP."
        }

    for contributor in contributors:
        if not isinstance(contributor, dict):
            continue
        orcid_id = contributor.get("@id", "")
        if not isinstance(orcid_id, str) or not orcid_id.startswith("orcid:"):
            return {
                "outcome": "fail",
                "log": f"Contributor '{contributor.get('schema:name', 'Unknown')}' missing valid ORCID identifier."
            }

    return {
        "outcome": "pass",
        "log": f"All {len(contributors)} contributors have valid ORCID identifiers."
    }