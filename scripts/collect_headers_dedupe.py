#!/usr/bin/env python3
"""Extract candidate header/origin names from OP PDFs, clean and dedupe,
and persist them into `data/lists.json` under the key `op_origins`.

Usage:
	python scripts/collect_headers_dedupe.py [--preview] [pdf1 pdf2 ...]

If no PDFs are passed, the script will look for files matching
`assets/*Origens*.pdf`.

Notes:
- Writes `data/lists.json` with encoding utf-8-sig so Streamlit/OP functions
  can load it reliably even when a BOM is present.
"""
from pathlib import Path
import json
import re
import sys
from collections import OrderedDict
from pypdf import PdfReader
import glob


def find_pdfs(args):
	if args:
		return [Path(p) for p in args]
	# default: any file in assets containing 'Origens' in the filename
	return [Path(p) for p in glob.glob("assets/*Origens*.pdf")]


def extract_candidates_from_pdf(pdf_path):
	reader = PdfReader(str(pdf_path))
	candidates = []
	for pageno, page in enumerate(reader.pages, start=1):
		text = page.extract_text() or ""
		for raw in text.splitlines():
			line = raw.strip()
			if not line:
				continue
			# quick filters
			if len(line) < 2 or len(line) > 80:
				continue
			if any(ch.isdigit() for ch in line):
				continue
			# remove weird separators
			if set(line.strip()) <= set('-=–—*·•'):
				continue
			# token count: origins are typically short (1-4 words)
			words = [w for w in line.split() if w.strip()]
			if len(words) > 5:
				continue
			# must contain at least 2 alphabetic characters
			alpha_count = sum(1 for c in line if c.isalpha())
			if alpha_count < 2:
				continue
			# heuristic: start with uppercase (including accented uppercase)
			if not re.match(r'^[A-ZÀ-ÖØ-Ý]', line):
				# allow some titles that start with quote or parenthesis
				if not re.match(r'^["\'\(\[]?[A-ZÀ-ÖØ-Ý]', line):
					continue

			# clean trailing punctuation
			cleaned = re.sub(r"[\.:;,-]+$", '', line).strip()
			candidates.append((pdf_path.name, pageno, cleaned))
	return candidates


def collect_and_clean(pdf_paths):
	seen = OrderedDict()
	for p in pdf_paths:
		for _, _, candidate in extract_candidates_from_pdf(p):
			key = candidate.strip()
			# normalize repeated whitespace
			key = re.sub(r'\s+', ' ', key)
			# de-duplicate preserving first-seen order
			if key.lower() not in seen:
				seen[key.lower()] = key
	# final cleaning: remove obvious non-origin words
	final = []
	blacklist = set(["índice", "sumário", "conteúdo", "origens", "origem"])
	for k in seen.values():
		low = k.lower()
		if low in blacklist:
			continue
		# drop overly short tokens
		if len(k) <= 1:
			continue
		final.append(k)
	return final


def write_lists_json(op_list, lists_path=Path('data/lists.json')):
	lists_path.parent.mkdir(parents=True, exist_ok=True)
	data = {}
	if lists_path.exists():
		with open(lists_path, 'r', encoding='utf-8-sig') as f:
			try:
				data = json.load(f)
			except Exception:
				data = {}
	data['op_origins'] = op_list
	with open(lists_path, 'w', encoding='utf-8-sig') as f:
		json.dump(data, f, ensure_ascii=False, indent=2)


def main(argv):
	preview = False
	args = []
	for a in argv:
		if a in ('--preview', '-p'):
			preview = True
		else:
			args.append(a)

	pdfs = find_pdfs(args)
	if not pdfs:
		print('No OP Origens PDFs found in assets/. Pass file paths as arguments to override.')
		return 1

	print(f'Found {len(pdfs)} PDF(s): {[p.name for p in pdfs]}')
	cleaned = collect_and_clean(pdfs)
	print(f'Collected {len(cleaned)} candidate origins after cleaning.')
	if preview:
		for item in cleaned:
			print(' -', item)
		return 0

	write_lists_json(cleaned)
	print(f'Wrote {len(cleaned)} origins to data/lists.json')
	return 0


if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))

