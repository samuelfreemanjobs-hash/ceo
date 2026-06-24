"""Tests for GTM artifact helpers."""

from marketing_director.gtm_chain import list_gtm_artifacts, read_gtm_artifact
from marketing_director.integrations import find_repo_root


def test_list_gtm_artifacts_includes_example_offer():
    root = find_repo_root()
    assert root is not None
    result = list_gtm_artifacts("offers", repo_root=root)
    paths = [a["path"] for a in result["artifacts"]]
    assert any("example-discovery-sprint-offer" in p for p in paths)


def test_read_gtm_artifact_example_offer():
    root = find_repo_root()
    assert root is not None
    path = "docs/marketing/offers/example-discovery-sprint-offer-2026-06-24.md"
    result = read_gtm_artifact(path, repo_root=root)
    assert "Discovery Sprint" in result["content"]
