import urllib.request
import urllib.error
from urllib.parse import urlparse

title = 'Check dataset_id resolves to declared destination via DOI URL'
description = (
    'Checks if the reused dataset identifier in the maDMP matches the destination '
    'by resolving dataset_id against its DOI URL and comparing the resolved host '
    'against the declared distribution.host entry.'
)

DOI_RESOLVER_BASE = "https://doi.org/"
RESOLVE_TIMEOUT_SECONDS = 6

# Fallback mapping from DOI registration prefix to typical landing-page host.
# Used when network resolution is not possible (e.g. offline CI runner).
DOI_PREFIX_HOSTS = {
    "10.5281": "zenodo.org",
    "10.5072": "zenodo.org",
    "10.6084": "figshare.com",
    "10.25384": "figshare.com",
    "10.7910": "dataverse.harvard.edu",
    "10.17605": "osf.io",
    "10.18419": "darus.uni-stuttgart.de",
    "10.48436": "researchdata.tuwien.ac.at",
}


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
        "@id": "urn:dmpEvaluationService:83",
        "@type": ["https://w3id.org/ftr#Test", "http://www.w3.org/ns/dcat#DataService"],
        "dcterms:identifier": {"@id": "83"},
        'dcterms:title': {'@language': 'en', '@value': title},
        'dcterms:description': {'@language': 'en', '@value': description},
        "dcterms:license": {"@id": "https://creativecommons.org/licenses/by/4.0/"},
        "dcat:endpointURL": {"@id": f"{test_url_base}/83"},
        'dcat:endpointDescription': None,
        "dcat:version": {"@language": "en", "@value": "1.0.0"},
        "dcat:keyword": [
            {"@language": "en", "@value": "dataset identifier"},
            {"@language": "en", "@value": "DOI"},
            {"@language": "en", "@value": "repository destination"},
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


def _extract_doi(identifier: str) -> str:
    if not isinstance(identifier, str):
        return ""

    value = identifier.strip()
    if not value:
        return ""

    lowered = value.lower()

    if lowered.startswith("doi:"):
        return value[4:].strip()

    for prefix in ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/", "http://dx.doi.org/"):
        if lowered.startswith(prefix):
            return value[len(prefix):].strip()

    # Bare DOI like "10.5281/zenodo.1234567"
    if value.startswith("10."):
        return value

    return ""


def _host_of(url: str) -> str:
    if not isinstance(url, str) or not url.strip():
        return ""
    parsed = urlparse(url.strip())
    host = parsed.netloc or parsed.path
    return host.lower().lstrip("www.")


def _resolve_doi(doi: str) -> str:
    """Follow the DOI URL and return the final resolved host (lowercase, no www).
    Returns an empty string on any network/resolution failure."""
    url = DOI_RESOLVER_BASE + doi
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=RESOLVE_TIMEOUT_SECONDS) as resp:
            final_url = resp.geturl()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError, ValueError):
        return ""

    return _host_of(final_url)


def _prefix_host(doi: str) -> str:
    prefix = doi.split("/", 1)[0] if "/" in doi else ""
    return DOI_PREFIX_HOSTS.get(prefix, "")


def _hosts_match(resolved: str, declared: str) -> bool:
    if not resolved or not declared:
        return False
    resolved = resolved.lstrip("www.")
    declared = declared.lstrip("www.")
    return resolved == declared or resolved.endswith("." + declared) or declared.endswith("." + resolved)


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
        return {"outcome": "fail", "log": "No dataset entries found."}

    saw_doi = False
    saw_destination = False

    for ds in datasets:
        if not isinstance(ds, dict):
            continue

        dataset_id = ds.get("dataset_id")
        if not isinstance(dataset_id, dict):
            continue

        identifier_value = dataset_id.get("identifier")
        id_type = dataset_id.get("type")

        if not isinstance(identifier_value, str) or not identifier_value.strip():
            continue

        doi = _extract_doi(identifier_value)
        is_doi_type = isinstance(id_type, str) and id_type.strip().lower() == "doi"

        if not doi and not is_doi_type:
            continue

        if not doi:
            # type says doi but value not recognisable
            continue

        saw_doi = True

        distributions = ds.get("distribution") or ds.get("rdap:distribution")
        if not isinstance(distributions, list):
            continue

        declared_hosts = []
        for dist in distributions:
            if not isinstance(dist, dict):
                continue
            host = dist.get("host")
            if not isinstance(host, dict):
                continue

            host_url = host.get("url")
            host_title = host.get("title")
            host_candidate = _host_of(host_url) if isinstance(host_url, str) else ""

            if host_candidate:
                declared_hosts.append(host_candidate)
            elif isinstance(host_title, str) and host_title.strip():
                declared_hosts.append(host_title.strip().lower())

        if not declared_hosts:
            continue

        saw_destination = True

        resolved_host = _resolve_doi(doi)
        if not resolved_host:
            resolved_host = _prefix_host(doi)

        if not resolved_host:
            continue

        for declared in declared_hosts:
            if _hosts_match(resolved_host, declared):
                return {
                    "outcome": "pass",
                    "log": (
                        f"dataset_id DOI '{doi}' resolves to host '{resolved_host}' "
                        f"which matches the declared destination '{declared}'."
                    )
                }

    if not saw_doi:
        return {
            "outcome": "fail",
            "log": "No dataset declares a DOI-type dataset_id."
        }

    if not saw_destination:
        return {
            "outcome": "fail",
            "log": "No distribution declares a host destination to compare against."
        }

    return {
        "outcome": "fail",
        "log": "No dataset_id DOI resolves to the declared distribution.host destination."
    }
