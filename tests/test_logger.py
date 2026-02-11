"""Tests for logger module."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.logger import get_logger, setup_logger


def test_get_logger_creates_logger():
    """Test that get_logger creates a logger instance."""
    logger = get_logger("test_module")

    assert logger is not None
    assert logger.name == "test_module"


def test_get_logger_same_instance():
    """Test that get_logger returns cached logger instance."""
    logger1 = get_logger("test_cached")
    logger2 = get_logger("test_cached")

    # Should return same cached instance
    assert logger1 is logger2


def test_setup_logger_creates_logger():
    """Test that setup_logger creates a logger with proper configuration."""
    logger = setup_logger("test_setup")

    assert logger is not None
    assert logger.name == "test_setup"
    assert logger.level >= 10  # DEBUG level is 10
    assert len(logger.handlers) > 0
