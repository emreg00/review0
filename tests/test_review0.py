#!/usr/bin/env python

"""Tests for `review0` package."""

import pytest

from review0 import llm

@pytest.fixture
def model():
    """pytest fixture for the llm model.
    """
    return llm.load_model(model_name="mistral", temperature=0.7, num_predict = 256, num_ctx=2048, is_chat=True)


def test_content(model):
    """Function to test functionality of the ollama model."""
    assert '42' in llm.query(model, "The answer to the Ultimate Question of Life, the Universe, and Everything is").content 
