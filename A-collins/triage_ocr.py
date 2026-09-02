#!/usr/bin/env python3
"""OCR + triage for crawled despatch PDFs.

Usage: python3 triage_ocr.py downloads/ [--triage-dir triage]
Requires: pdftoppm (poppler-utils), tesseract, pytesseract, pillow.

Classifies each page into:
  (a) pair/      — ciphertext with adjacent decrypt (crib + key-recovery material)
  (b) targets/   — ciphertext with no decrypt
  (c) keys/      — key sheets / cipher instructions
  (-) plain/     — everything else
Heuristics tuned for 1918-22 GHQ practice: hand or typed 4/5-letter groups, digit groups,
"in cypher", keyword tables, alphabet squares.
"""
import argparse, pathlib, re, shutil, subprocess, sys

GROUPS = re.compile(r'(?:\b[A-Z]{4,5}\b[ .,]*){6,}')          # letter-group runs
DIGGROUPS = re.compile(r'(?:\b\d{2,5}\b[ .,]*){8,}')          # number-group runs
KEYISH = re.compile(r'\b(key ?word|cypher key|code key|alphabet|square|columns numbered)\b', re.I)
CIPHERWORD = re.compile(r'\bin cypher\b|\bcipher\b|\bcoded\b|\bdecode', re.I)

def ocr_pdf(pdf, tmp):
    subprocess.run(['pdftoppm', '-r', '300', '-gray', '-png', str(pdf), str(tmp / 'p')],
                   check=True)
    import pytesseract
    from PIL import Image
    out = []
    for img in sorted(tmp.glob('p*.png')):
        out.append(pytesseract.image_to_string(Image.open(img)))
        img.unlink()
    return out

def classify(pages):
    txt = '\n'.join(pages)
    has_ct = bool(GROUPS.search(txt) or DIGGROUPS.search(txt))
    has_key = bool(KEYISH.search(txt))
    mentions = bool(CIPHERWORD.search(txt))
    # decrypt adjacency: ciphertext page followed/preceded by prose covering same length
    if has_key: return 'keys'
    if has_ct and mentions: return 'pair'      # candidate pair; human confirms adjacency
    if has_ct: return 'targets'
    if mentions: return 'pair'                 # "in cypher"/"decoded" prose — inspect
    return 'plain'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('--triage-dir', default='triage')
    a = ap.parse_args()
    src, tdir = pathlib.Path(a.src), pathlib.Path(a.triage_dir)
    for sub in ('pair', 'targets', 'keys', 'plain'):
        (tdir / sub).mkdir(parents=True, exist_ok=True)
    tmp = tdir / '_tmp'; tmp.mkdir(exist_ok=True)
    for pdf in sorted(src.glob('*.pdf')):
        try:
            pages = ocr_pdf(pdf, tmp)
        except Exception as e:
            print(f'{pdf.name}: OCR failed ({e})', file=sys.stderr); continue
        cls = classify(pages)
        shutil.copy2(pdf, tdir / cls / pdf.name)
        (tdir / cls / (pdf.stem + '.txt')).write_text('\n\f\n'.join(pages))
        print(f'{pdf.name} -> {cls}')

if __name__ == '__main__':
    main()
