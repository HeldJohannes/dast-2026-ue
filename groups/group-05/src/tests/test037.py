title = 'Check distribution format is open'
description = (
    'Checks distribution_format to be open.'
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
        "@id": "urn:dmpEvaluationService:37",
        "@type": ["https://w3id.org/ftr#Test", "http://www.w3.org/ns/dcat#DataService"],
        "dcterms:identifier": {"@id": "37"},
        'dcterms:title': {'@language': 'en', '@value': title},
        'dcterms:description': {'@language': 'en', '@value': description},
        "dcterms:license": {"@id": "https://creativecommons.org/licenses/by/4.0/"},
        "dcat:endpointURL": {"@id": f"{test_url_base}/37"},
        'dcat:endpointDescription': None,
        "dcat:version": {"@language": "en", "@value": "1.0.0"},
        "dcat:keyword": [
            {"@language": "en", "@value": "template keyword"}
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

    # Example open-format registry
    OPEN_FORMATS = {
        "csv",
        "tsv",
        "json",
        "json-ld",
        "xml",
        "rdf",
        "ttl",
        "txt",
        "md",
        "pdf",
        "png",
        "jpeg",
        "jpg",
        "svg",
        "geojson",
        "netcdf",
        "hdf5",
        "parquet",
        "ods",
        "odt",
        "openapi",
        "application/json",
        "text/csv",
        "application/xml",
        "text/plain",
        "markdown"
    }

    checked = 0

    for ds in datasets:
        if not isinstance(ds, dict):
            continue

        distributions = (
            ds.get("distribution")
            or ds.get("rdap:distribution")
        )

        if not isinstance(distributions, list):
            continue

        for dist in distributions:
            if not isinstance(dist, dict):
                continue

            checked += 1

            fmt = (
                dist.get("format")
                or dist.get("schema:encodingFormat")
            )

            if fmt is None:
                return {
                    "outcome": "fail",
                    "log": "At least one distribution has no declared format."
                }

            # Normalize to list
            if isinstance(fmt, str):
                fmt = [fmt]

            if not isinstance(fmt, list) or len(fmt) == 0:
                return {
                    "outcome": "fail",
                    "log": "At least one distribution has an empty format declaration."
                }

            for value in fmt:
                if not isinstance(value, str):
                    return {
                        "outcome": "fail",
                        "log": "Distribution format contains an invalid value."
                    }

                normalized = value.strip().lower()

                if normalized.startswith("."):
                    normalized = normalized[1:]

                if normalized not in OPEN_FORMATS:
                    return {
                        "outcome": "fail",
                        "log": f"Format '{value}' is not classified as open."
                    }

    if checked == 0:
        return {
            "outcome": "fail",
            "log": "No distribution entries found."
        }

    return {
        "outcome": "pass",
        "log": "All declared distribution formats are classified as open."
    }
