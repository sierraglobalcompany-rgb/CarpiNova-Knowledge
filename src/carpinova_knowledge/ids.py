from __future__ import annotations
import re

BOOK_RE = re.compile(r'^[A-Z0-9][A-Z0-9-]*$')

def _validate(book_id: str, pdf_page: int, sequence: int | None = None) -> None:
    if not BOOK_RE.fullmatch(book_id):
        raise ValueError('invalid book_id')
    if pdf_page < 1:
        raise ValueError('pdf_page must be >= 1')
    if sequence is not None and sequence < 1:
        raise ValueError('sequence must be >= 1')

def page_id(book_id: str, pdf_page: int) -> str:
    _validate(book_id, pdf_page)
    return f'PAGE-{book_id}-P{pdf_page:04d}'

def content_id(book_id: str, pdf_page: int, sequence: int) -> str:
    _validate(book_id, pdf_page, sequence)
    return f'CONTENT-{book_id}-P{pdf_page:04d}-{sequence:03d}'

def figure_id(book_id: str, pdf_page: int, sequence: int) -> str:
    _validate(book_id, pdf_page, sequence)
    return f'FIG-{book_id}-P{pdf_page:04d}-{sequence:03d}'

def measurement_id(book_id: str, pdf_page: int, sequence: int) -> str:
    _validate(book_id, pdf_page, sequence)
    return f'MEAS-{book_id}-P{pdf_page:04d}-{sequence:03d}'

def rule_id(book_id: str, pdf_page: int, sequence: int) -> str:
    _validate(book_id, pdf_page, sequence)
    return f'RULE-{book_id}-P{pdf_page:04d}-{sequence:03d}'
