"""Tests for financial mutations commands."""

import json

import responses

BASE = "https://moneybird.com/api/v2/123456"


@responses.activate
def test_list_all_uses_synchronization_in_batches(logged_in_runner):
    responses.add(
        responses.GET,
        f"{BASE}/financial_mutations/synchronization.json",
        json=[{"id": str(i), "version": 1} for i in range(150)],
    )
    responses.add(
        responses.POST,
        f"{BASE}/financial_mutations/synchronization.json",
        json=[{"id": "x"}],
    )
    result = logged_in_runner("--output", "json", "financial-mutations", "list", "--all")
    assert result.exit_code == 0, result.output
    posts = [json.loads(c.request.body)["ids"] for c in responses.calls[1:]]
    assert [len(p) for p in posts] == [100, 50]
