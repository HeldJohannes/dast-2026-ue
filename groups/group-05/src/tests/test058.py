title = 'Check license_ref for dataset licence'
description = (
    'Checks whether the license_ref field within the dataset distribution entry '
    'is present and non-empty, confirming that a license has been declared and '
    'users know the terms under which the data may be used.'
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
        "@id": "urn:dmpEvaluationService:58",
        "@type": ["https://w3id.org/ftr#Test", "http://www.w3.org/ns/dcat#DataService"],
        "dcterms:identifier": {"@id": "58"},
        'dcterms:title': {'@language': 'en', '@value': title},
        'dcterms:description': {'@language': 'en', '@value': description},
        "dcterms:license": {"@id": "https://creativecommons.org/licenses/by/4.0/"},
        "dcat:endpointURL": {"@id": f"{test_url_base}/58"},
        'dcat:endpointDescription': None,
        "dcat:version": {"@language": "en", "@value": "1.0.0"},
        "dcat:keyword": [
            {"@language": "en", "@value": "dataset licence"},
            {"@language": "en", "@value": "license reference"},
            {"@language": "en", "@value": "open licence"},
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

            checked += 1

            # license can either be an array of license objects (per RDA standard)
            # or contain license_ref directly on the distribution
            license_entries = dist.get("license")

            if isinstance(license_entries, list):
                for lic in license_entries:
                    if not isinstance(lic, dict):
                        continue
                    license_ref = lic.get("license_ref")
                    if isinstance(license_ref, str) and license_ref.strip():
                        return {
                            "outcome": "pass",
                            "log": "At least one distribution contains a non-empty license_ref."
                        }

            # Fallback: license_ref directly on distribution
            direct_ref = dist.get("license_ref")
            if isinstance(direct_ref, str) and direct_ref.strip():
                return {
                    "outcome": "pass",
                    "log": "At least one distribution contains a non-empty license_ref."
                }

    if checked == 0:
        return {
            "outcome": "fail",
            "log": "No distribution entries found."
        }

    return {
        "outcome": "fail",
        "log": "No distribution declares a non-empty license_ref."
    }
