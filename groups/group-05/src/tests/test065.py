title = 'Check data_access for open status'
description = (
    'Checks that data_access is set to open (accepted values: open, shared, closed).'
)

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
        "@id": "urn:dmpEvaluationService:65",
        "@type": ["https://w3id.org/ftr#Test", "http://www.w3.org/ns/dcat#DataService"],
        "dcterms:identifier": {"@id": "65"},
        'dcterms:title': {'@language': 'en', '@value': title},
        'dcterms:description': {'@language': 'en', '@value': description},
        "dcterms:license": {"@id": "https://creativecommons.org/licenses/by/4.0/"},
        "dcat:endpointURL": {"@id": f"{test_url_base}/65"},
        'dcat:endpointDescription': None,
        "dcat:version": {"@language": "en", "@value": "1.0.0"},
        "dcat:keyword": [
            {"@language": "en", "@value": "open access"},
            {"@language": "en", "@value": "data access status"},
            {"@language": "en", "@value": "openness"},
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

    dmp = madmp.get("dmp", {})
    if not isinstance(dmp, dict):
        return {
            "outcome": "fail",
            "log": "Root dmp object is missing or not a JSON object."
        }

    datasets = dmp.get("dataset") or dmp.get("rdap:dataset")

    if not isinstance(datasets, list) or len(datasets) == 0:
        return {
            "outcome": "fail",
            "log": "No dataset entries found."
        }

    checked = 0

    for ds in datasets:
        if not isinstance(ds, dict):
            continue

        distributions = ds.get("distribution") or ds.get("rdap:distribution")

        if not isinstance(distributions, list):
            continue

        for dist in distributions:
            if not isinstance(dist, dict):
                continue

            # Generic dataset-level field
            data_access = dist.get("data_access")

            if isinstance(data_access, str):
                checked += 1

                if data_access.strip().lower() == "open":
                    return {
                        "outcome": "pass",
                        "log": "At least one dataset has data_access set to 'open'."
                    }

    if checked == 0:
        return {
            "outcome": "fail",
            "log": "No data_access field found."
        }

    return {
        "outcome": "fail",
        "log": "No dataset has data_access set to 'open'."
    }