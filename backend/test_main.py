import pytest
from main import RCAValidator, RCAForm

def test_valid_rca_submission():
    """Test that a fully documented RCA passes validation."""
    rca = RCAForm(
        root_cause="Database connection pool exhausted due to sudden traffic spike.",
        fix_applied="Increased max_connections parameter and implemented Redis rate limiting to backpressure traffic."
    )
    is_valid, msg = RCAValidator.validate(rca)
    assert is_valid is True

def test_missing_root_cause():
    """Test that the system rejects an empty root cause."""
    rca = RCAForm(root_cause="", fix_applied="Restarted the server.")
    is_valid, msg = RCAValidator.validate(rca)
    assert is_valid is False

def test_insufficient_fix_details():
    """Test that the system enforces detailed fix explanations."""
    rca = RCAForm(root_cause="Network glitch.", fix_applied="Fixed it.")
    is_valid, msg = RCAValidator.validate(rca)
    assert is_valid is False

def test_whitespace_only_rejection():
    """Test that users cannot bypass the form using spaces."""
    rca = RCAForm(root_cause="   ", fix_applied="          ")
    is_valid, msg = RCAValidator.validate(rca)
    assert is_valid is False
