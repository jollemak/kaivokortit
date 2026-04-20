"""
Integration tests for POST /ocr/analyze using real PDF sample files.

These tests call the actual Mistral OCR API and require MISTRAL_KEY in .env.
Run with:  pytest test/ -v -m integration
"""

import io
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

EXAMPLES = Path(__file__).parent.parent / "samples"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _analyze(filename: str):
    pdf_path = EXAMPLES / filename
    with open(pdf_path, "rb") as f:
        return client.post(
            "/ocr/analyze",
            files={"file": (filename, f, "application/pdf")},
        )


def _total_cards(body: dict) -> int:
    return sum(len(cards) for cards in body["cards_by_page"].values())


# ---------------------------------------------------------------------------
# Input validation (no API call, instant)
# ---------------------------------------------------------------------------

def test_wrong_content_type_returns_400():
    resp = client.post(
        "/ocr/analyze",
        files={"file": ("test.txt", io.BytesIO(b"not a pdf"), "text/plain")},
    )
    assert resp.status_code == 400
    assert "PDF" in resp.json()["detail"]


def test_empty_file_returns_400():
    resp = client.post(
        "/ocr/analyze",
        files={"file": ("empty.pdf", io.BytesIO(b""), "application/pdf")},
    )
    assert resp.status_code == 400
    assert "empty" in resp.json()["detail"].lower()


# ---------------------------------------------------------------------------
# Real OCR integration tests
# ---------------------------------------------------------------------------

@pytest.mark.integration
# def test_sample1():
#     resp = _analyze("sitowise.pdf")
#     assert resp.status_code == 200, resp.text
#     body = resp.json()

#     print_info(body)

#     assert body["company_name"] == "Sitowise"
#     assert _total_cards(body) == 50

def test_sample2():
    resp = _analyze("a-insinoorit.pdf")
    assert resp.status_code == 200, resp.text
    body = resp.json()

    print_info(body)

    # assert body["company_name"] == "A-INSINÖÖRIT"
    assert _total_cards(body) == 33

def test_sample3():
    resp = _analyze("afry.pdf")
    assert resp.status_code == 200, resp.text
    body = resp.json()

    print_info(body)

    # assert body["company_name"] == "AFRY"
    assert _total_cards(body) == 74

# def test_sample4():
#     resp = _analyze("fcg.pdf")
#     assert resp.status_code == 200, resp.text
#     body = resp.json()

#     print_info(body)

#     assert body["company_name"] == "FCG"
#     assert _total_cards(body) == 30


def print_info(body):
    print("\n=====================================================================================================================================================")
    print(f"Company name: {body["company_name"]}")
    print(f"Total cards: {_total_cards(body)}")
    print(f"Cards by page: {body["cards_by_page"]}")

