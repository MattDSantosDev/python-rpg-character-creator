import sys
import pathlib
# ensure project root is on sys.path so imports from scripts/ work
proj_root = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

import dndfunctions as d
from pprint import pprint

pdf = d.class_to_file_map.get('Bárbaro')
print('Using PDF:', pdf)
rows = d.extract_table_page_2(pdf, ncols=6, ocr_lang='por', ocr_resolution=300)
if not rows:
    print('No rows extracted')
else:
    print('Extracted rows (first 10):')
    pprint(rows[:10])
