title = 'Check distribution.format is specified'
description = (
    'Checks whether the format field within the dataset distribution entry is '
    'present and non-empty, confirming that the file format of the data has been '
    'declared so users know what tools are needed to open it.'
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
        "@id": "urn:dmpEvaluationService:26",
        "@type": ["https://w3id.org/ftr#Test", "http://www.w3.org/ns/dcat#DataService"],
        "dcterms:identifier": {"@id": "26"},
        'dcterms:title': {'@language': 'en', '@value': title},
        'dcterms:description': {'@language': 'en', '@value': description},
        "dcterms:license": {"@id": "https://creativecommons.org/licenses/by/4.0/"},
        "dcat:endpointURL": {"@id": f"{test_url_base}/26"},
        'dcat:endpointDescription': None,
        "dcat:version": {"@language": "en", "@value": "1.0.0"},
        "dcat:keyword": [
            {"@language": "en", "@value": "file format"},
            {"@language": "en", "@value": "distribution"},
            {"@language": "en", "@value": "interoperability"},
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
            "log": "No dataset entries found in dmp.dataset."
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

            # Support both generic and schema.org naming
            fmt = (
                dist.get("format")
                or dist.get("schema:encodingFormat")
            )

            if (
                fmt is None
                or (isinstance(fmt, str) and not fmt.strip())
                or (isinstance(fmt, list) and len(fmt) == 0)
            ):
                return {
                    "outcome": "fail",
                    "log": "At least one distribution is missing a non-empty format field."
                }

    if checked == 0:
        return {
            "outcome": "fail",
            "log": "No distribution entries found."
        }

    return {
        "outcome": "pass",
        "log": "All distribution entries specify a non-empty format."
    }
