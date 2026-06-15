title = "Check for dataset license declarations"
description = "Verifies whether datasets have license information specified."

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
        "@id": f"urn:dmpEvaluationService:022",
        "@type": ["https://w3id.org/ftr#Test", "http://www.w3.org/ns/dcat#DataService"],
        "dcterms:identifier": {"@id": "022"},
        'dcterms:title': {'@language': 'en', '@value': title},
        'dcterms:description': {'@language': 'en', '@value': description},
        "dcterms:license": {"@id": "https://creativecommons.org/licenses/by/4.0/"},
        "dcat:endpointURL": {"@id": f"{test_url_base}/022"},
        'dcat:endpointDescription': None,
        "dcat:version": {"@language": "en", "@value": "1.0.0"},
        "dcat:keyword": [
            {"@language": "en", "@value": "license"},
            {"@language": "en", "@value": "data reuse"},
            {"@language": "en", "@value": "open access"},
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

    # Try both possible field names
    datasets = dmp.get("rdap:dataset") or dmp.get("dataset")

    if not isinstance(datasets, list) or len(datasets) == 0:
        return {
            "outcome": "fail",
            "log": "No dataset entries found in the DMP."
        }

    checked = 0
    for ds in datasets:
        if not isinstance(ds, dict):
            continue
        distributions = ds.get("rdap:distribution") or ds.get("distribution")
        if not isinstance(distributions, list):
            continue
        for dist in distributions:
            if not isinstance(dist, dict):
                continue
            license_field = dist.get("rdap:license") or dist.get("license")
            if license_field:
                checked += 1
                if isinstance(license_field, list) and len(license_field) > 0:
                    return {
                        "outcome": "pass",
                        "log": "At least one dataset distribution has a license declared."
                    }

    if checked == 0:
        return {
            "outcome": "fail",
            "log": "No license field found on any dataset distribution."
        }

    return {
        "outcome": "fail",
        "log": "License field present but empty or invalid."
    }