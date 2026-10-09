from __future__ import annotations


def _book_token(book_id: str) -> str:
    token = book_id.strip().upper()
    if not token or any(not (char.isalnum() or char == "-") for char in token):
        raise ValueError("book_id must contain only letters, digits, and hyphens")
    return token


def _positive(value: int, name: str) -> int:
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def page_id(book_id: str, pdf_page: int) -> str:
    return f"PAGE-{_book_token(book_id)}-P{_positive(pdf_page, 'pdf_page'):04d}"


def content_id(book_id: str, pdf_page: int, sequence: int) -> str:
    return f"CONTENT-{_book_token(book_id)}-P{_positive(pdf_page, 'pdf_page'):04d}-{_positive(sequence, 'sequence'):03d}"


def figure_id(book_id: str, pdf_page: int, sequence: int) -> str:
    return f"FIG-{_book_token(book_id)}-P{_positive(pdf_page, 'pdf_page'):04d}-{_positive(sequence, 'sequence'):03d}"


def measurement_id(book_id: str, pdf_page: int, sequence: int) -> str:
    return f"MEAS-{_book_token(book_id)}-P{_positive(pdf_page, 'pdf_page'):04d}-{_positive(sequence, 'sequence'):03d}"


def rule_id(book_id: str, pdf_page: int, sequence: int) -> str:
    return f"RULE-{_book_token(book_id)}-P{_positive(pdf_page, 'pdf_page'):04d}-{_positive(sequence, 'sequence'):03d}"
