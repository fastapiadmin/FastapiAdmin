"""Workflow condition/expression unit tests (no database)."""

from app.modules.task.workflow.service import _condition_matches, _value


def test_value_supports_dotted_paths() -> None:
    assert _value({"user": {"amount": 120}}, "user.amount") == 120
    assert _value({"user": {}}, "user.amount") is None
    assert _value({}, "") is None


def test_condition_operators() -> None:
    ctx = {"amount": 120, "name": "Alice", "tags": ["a", "b"]}
    assert _condition_matches(ctx, {"field": "amount", "operator": "gt", "value": 100})
    assert _condition_matches(ctx, {"field": "amount", "operator": "gte", "value": 120})
    assert _condition_matches(ctx, {"field": "amount", "operator": "lt", "value": 121})
    assert _condition_matches(ctx, {"field": "name", "operator": "contains", "value": "lic"})
    assert not _condition_matches(ctx, {"field": "amount", "operator": "lt", "value": 120})
    assert not _condition_matches(ctx, {"field": "amount", "operator": "unknown", "value": 120})
    assert not _condition_matches(ctx, {"field": "", "operator": "eq", "value": None})
