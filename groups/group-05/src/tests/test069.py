title = 'Check distribution license_ref for Horizon Europe CC-BY compliance'
description = (
    'Checks if the maDMP dataset.distribution.license_ref matches Horizon Europe '
    'RDM requirements, i.e. CC-BY.'
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
        "@id": "urn:dmpEvaluationService:69",
        "@type": ["https://w3id.org/ftr#Test", "http://www.w3.org/ns/dcat#DataService"],
        "dcterms:identifier": {"@id": "69"},
        'dcterms:title': {'@language': 'en', '@value': title},
        'dcterms:description': {'@language': 'en', '@value': description},
        "dcterms:license": {"@id": "https://creativecommons.org/licenses/by/4.0/"},
        "dcat:endpointURL": {"@id": f"{test_url_base}/69"},
        'dcat:endpointDescription': None,
        "dcat:version": {"@language": "en", "@value": "1.0.0"},
        "dcat:keyword": [
            {"@language": "en", "@value": "funder licence"},
            {"@language": "en", "@value": "Horizon Europe"},
            {"@language": "en", "@value": "CC-BY"},
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

def _is_cc_by(value: str) -> bool:
    if not isinstance(value, str):
        return False

    normalized = value.strip().lower()

    if not normalized:
        return False

    # Strip protocol and trailing slash to make comparison robust
    for prefix in ("https://", "http://"):
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):]
            break
    normalized = normalized.rstrip("/")

    cc_by_patterns = (
        "creativecommons.org/licenses/by/",
        "spdx.org/licenses/cc-by-",
    )

    if normalized in {
        "cc-by",
        "cc-by-4.0",
        "cc-by-3.0",
        "cc-by-2.5",
        "cc-by-2.0",
        "cc-by-1.0",
    }:
        return True

    for pattern in cc_by_patterns:
        if pattern in normalized:
            # Make sure it's not a CC-BY-NC, CC-BY-SA, CC-BY-ND variant
            # by looking at the segment after the pattern.
            tail = normalized.split(pattern, 1)[1]
            head_segment = tail.split("/", 1)[0]
            # head_segment is like "4.0", "3.0", or empty
            if head_segment == "" or head_segment.replace(".", "").isdigit():
                return True

    return False


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

    seen_license_ref = False

    for ds in datasets:
        if not isinstance(ds, dict):
            continue

        distributions = ds.get("distribution") or ds.get("rdap:distribution")

        if not isinstance(distributions, list):
            continue

        for dist in distributions:
            if not isinstance(dist, dict):
                continue

            license_entries = dist.get("license")

            if isinstance(license_entries, list):
                for lic in license_entries:
                    if not isinstance(lic, dict):
                        continue
                    license_ref = lic.get("license_ref")
                    if isinstance(license_ref, str) and license_ref.strip():
                        seen_license_ref = True
                        if _is_cc_by(license_ref):
                            return {
                                "outcome": "pass",
                                "log": (
                                    "At least one distribution declares a CC-BY "
                                    "licence (Horizon Europe compliant)."
                                )
                            }

            direct_ref = dist.get("license_ref")
            if isinstance(direct_ref, str) and direct_ref.strip():
                seen_license_ref = True
                if _is_cc_by(direct_ref):
                    return {
                        "outcome": "pass",
                        "log": (
                            "At least one distribution declares a CC-BY "
                            "licence (Horizon Europe compliant)."
                        )
                    }

    if not seen_license_ref:
        return {
            "outcome": "fail",
            "log": "No distribution declares a license_ref."
        }

    return {
        "outcome": "fail",
        "log": "No declared license_ref corresponds to a CC-BY licence."
    }
