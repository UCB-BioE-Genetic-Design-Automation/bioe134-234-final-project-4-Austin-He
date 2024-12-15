import pytest
from queries import (
    query_uniprot,
    query_alphafold,
    query_interpro_by_uniprot,
    query_go_annotations_uniprot,
    enrich_go_annotations_with_names
)
import requests

TEST_UNIPROT_ID = "P69905"  # Human hemoglobin subunit alpha, known UniProt ID
INVALID_UNIPROT_ID = "XXXXXXX"  # Invalid UniProt ID to test error handling
KNOWN_GO_ID = "GO:0008150"  # Biological process: "biological_process"


def test_query_uniprot_valid_id():
    # Test querying a valid UniProt ID
    data = query_uniprot(TEST_UNIPROT_ID)
    assert "primaryAccession" in data, "Expected 'primaryAccession' field in UniProt result"
    assert data["primaryAccession"] == TEST_UNIPROT_ID, "Returned UniProt ID does not match the queried ID"


def test_query_uniprot_invalid_id():
    # Test querying an invalid UniProt ID should raise HTTPError (e.g., 404)
    with pytest.raises(requests.HTTPError, match="404 Client Error"):
        query_uniprot(INVALID_UNIPROT_ID)


def test_query_alphafold_valid_id():
    # Test querying AlphaFold with a known UniProt ID
    data = query_alphafold(TEST_UNIPROT_ID)
    # AlphaFold might return multiple models in a list
    assert isinstance(data, list), "Expected a list of models from AlphaFold"
    assert len(data) > 0, "Expected at least one prediction model from AlphaFold"
    # Check if 'uniprotId' field is present in the first model
    assert data[0].get("uniprotId") == TEST_UNIPROT_ID, "AlphaFold model does not match the queried UniProt ID"


def test_query_interpro_valid_id():
    # Test querying InterPro with a known UniProt ID
    data = query_interpro_by_uniprot(TEST_UNIPROT_ID)
    # InterPro might return a dictionary with keys like 'metadata' or 'entries'
    assert "entries" in data, "Expected 'entries' field in InterPro result"
    # Check if we got at least one domain annotation
    assert len(data["entries"]) > 0, "Expected at least one InterPro entry for this UniProt ID"


def test_query_go_annotations_valid_id():
    # Test querying GO annotations with a known UniProt ID
    data = query_go_annotations_uniprot(TEST_UNIPROT_ID)
    assert "results" in data, "Expected 'results' field in GO annotations"
    # Check if we have at least one annotation
    assert len(data["results"]) > 0, "Expected at least one GO annotation"
    # Check if 'goId' is present in the first annotation
    assert "goId" in data["results"][0], "Expected 'goId' in GO annotation result"


def test_enrich_go_annotations_with_names():
    # Test that we can enrich annotations with GO names
    annotations = {
        "results": [
            {"goId": KNOWN_GO_ID}  # Biological process GO:0008150 should be known
        ]
    }
    enriched = enrich_go_annotations_with_names(annotations)
    # Check if 'goName' got added
    assert enriched["results"][0].get("goName") is not None, "Failed to enrich GO annotation with goName"
    assert isinstance(enriched["results"][0]["goName"], str), "goName should be a string"


def test_query_go_annotations_invalid_id():
    # Test querying GO annotations with invalid UniProt ID
    # This might not return a 404, but empty results or raise another error.
    # If the endpoint returns a 200 with no results, just check for empty results.
    data = query_go_annotations_uniprot(INVALID_UNIPROT_ID)
    # Likely empty results
    assert "results" in data, "Expected 'results' field even for invalid ID"
    assert len(data["results"]) == 0, "Expected no GO annotations for an invalid UniProt ID"


def test_query_alphafold_invalid_id():
    # AlphaFold might return a 404 if no prediction exists for the given UniProt ID
    with pytest.raises(requests.HTTPError, match="404 Client Error"):
        query_alphafold(INVALID_UNIPROT_ID)


def test_query_interpro_invalid_id():
    # InterPro might return a 404 for invalid IDs
    with pytest.raises(requests.HTTPError, match="404 Client Error"):
        query_interpro_by_uniprot(INVALID_UNIPROT_ID)
