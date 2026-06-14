title = 'Check for new data (no is_reused)'
description = (
    'This test checks whether the maDMP includes at least one dataset entry '
    'that does not carry an is_reused flag, confirming that a new dataset has been declared.'
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
        "@id": "urn:dmpEvaluationService:16",
        "@type": ["https://w3id.org/ftr#Test", "http://www.w3.org/ns/dcat#DataService"],
        "dcterms:identifier": {"@id": "16"},
        "dcterms:title": {"@language": "en", "@value": title},
        "dcterms:description": {"@language": "en", "@value": description},
        "dcterms:license": {"@id": "https://creativecommons.org/licenses/by/4.0/"},
        "dcat:endpointURL": {"@id": f"{test_url_base}/16"},
        "dcat:version": {"@language": "en", "@value": "1.0.0"},
        "dcat:keyword": [
            {"@language": "en", "@value": "new dataset"},
            {"@language": "en", "@value": "new data"},
            {"@language": "en", "@value": "maDMP"},
            {"@language": "en", "@value": "completeness"}
        ],
        "dcterms:creator": {"@id": "ComplianceEvaluator"},
        "dcat:contactPoint": [{"@id": "ComplianceEvaluator"}]
    }

def assess(madmp: dict) -> dict:
    if not isinstance(madmp, dict):
        return {"outcome": "fail", "log": "Request body is not a JSON object."}
    dmp = madmp.get("dmp", {})
    if not isinstance(dmp, dict):
        return {"outcome": "fail", "log": "Root dmp object is missing or not a JSON object."}
    
    # Support both "dataset" and "rdap:dataset" namespaces
    datasets = dmp.get("dataset") or dmp.get("rdap:dataset")
    if not isinstance(datasets, list) or len(datasets) == 0:
        return {"outcome": "fail", "log": "No dataset entries found in dmp.dataset."}
    
    found_new = False
    for ds in datasets:
        if not isinstance(ds, dict):
            continue
        
        has_is_reused = "is_reused" in ds
        
        # Check if any distribution declares "is_reused"
        distributions = ds.get("distribution") or ds.get("rdap:distribution")
        if isinstance(distributions, list):
            for dist in distributions:
                if isinstance(dist, dict) and "is_reused" in dist:
                    has_is_reused = True
                    break
                    
        if not has_is_reused:
            found_new = True
            break
            
    if found_new:
        return {"outcome": "pass", "log": "At least one dataset does not contain the is_reused field, indicating new data."}
    return {"outcome": "fail", "log": "All datasets contain the is_reused field."}
