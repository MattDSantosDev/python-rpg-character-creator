## Quick orientation for AI coding agents

This repository is a small Streamlit-based Python app to help create RPG characters from PDF reference materials (D&D and "Ordem Paranormal"). The UI is in `main.py`; PDF parsing and helpers are in `functions.py` and `dndfunctions.py`. There are example assets under `assets/` and a small test harness in `scripts/test_extract.py`.

Key facts an agent should know (short):
- Entrypoint: `main.py` — a Streamlit app. Typical run: `streamlit run main.py`.
- PDF helpers: `functions.py` and `dndfunctions.py` implement most parsing logic. They prefer `pdfplumber` table extraction and fall back to `pytesseract` OCR.
- Class-to-PDF mapping lives in `dndfunctions.py` as `class_to_file_map` (look here when adding/removing class PDFs).
- Test harness: `scripts/test_extract.py` — imports project root and runs `extract_table_page_2` against an asset. Use it to reproduce parsing bugs.

Contract & important function shapes
- choose_dnd_class() (in `dndfunctions.py`): side-effecting Streamlit UI function. Returns `(character_class, class_to_file_map)` when invoked programmatically; otherwise it builds UI.
- extract_table_page_2(pdf_path, ...) -> list[list[str]] | None: returns rows (header row optional) or None on failure. Caller expects 1-indexed page numbers elsewhere.

Project-specific patterns and conventions
- PDF-first: functions try `pdfplumber.Page.extract_tables()` first; when that yields nothing they convert pages to images and run OCR via `pytesseract` (look for `.to_image()` and `.original` patterns).
- OCR language: many calls use Portuguese (`lang='por'`) in tests and functions — prefer `por` as a default when adding OCR-related fixes.
- Page indexing: when communicating page numbers back to UI, the code uses 1-indexed numbers; internal `PdfReader.pages` uses 0-based indexing. Preserve this mapping.
- Filenames contain accented characters (e.g., `D&D-Barbaro.pdf` with `Bárbaro` as a key). Use UTF-8-safe handling and avoid normalizing filenames unless necessary.

How to run locally (Windows PowerShell)
- Install dependencies inferred from imports (no requirements.txt present):

  pip install streamlit pdfplumber pytesseract pypdf pillow pandas

- Run the UI:

  streamlit run main.py

- Run the parser test (fast reproduce of extraction issues):

  python .\scripts\test_extract.py

Notes about debugging parsing
- Use `scripts/test_extract.py` to reproduce table extraction from a specific PDF. It prints the first extracted rows.
- Add `print()` or temporary `pdb.set_trace()` in `dndfunctions.basic_traits_table_extraction` or `extract_table_page_2` to inspect OCR output and header slicing.
- When OCR produces merged columns, inspect `lines` (the OCR text) and the header detection logic that slices fixed column positions based on keyword locations.

Integration and change points
- Adding new class PDFs: update `dndfunctions.class_to_file_map` and add the file in `assets/`.
- If adding a new RPG system, follow the `main.py` pattern: add a new selectbox option and call the corresponding chooser function.

Minimal PR guidance for agents
- Small, focused changes only. When changing parsing logic, add or update `scripts/test_extract.py` to include a targeted assertion (or at least a reproducible print-out) so maintainers can verify behavior.
- Preserve existing Streamlit UI flow — `main.py` wires selection -> chooser; prefer returning values from chooser functions so they can be unit-tested.

Files to inspect for examples
- `main.py` (UI wiring)
- `dndfunctions.py` (class mapping + extraction routines)
- `functions.py` (PDF search helpers)
- `scripts/test_extract.py` (parser reproduction harness)

If anything is ambiguous, ask these short questions:
1. Which RPG systems should be prioritized for bug fixes (D&D or Ordem Paranormal)?
2. Are we allowed to add a requirements.txt or pin dependency versions?

End of file
