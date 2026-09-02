#!/usr/bin/env python3
"""Extract cryptanalysis corpus from EEBO-TCP XMLs (A64608 Logopandecteision 1653,
A95749 The Jewel 1652): the 32 Proquiritations as word lists, and per-printed-page
word lists for both books. Output: corpus.json.
Long-s and ligatures are normalized; EOL hyphens joined (TCP marks them with <g ref="char:EOLhyphen"/>).
"""
import re, json, hashlib, unicodedata
NS = '{http://www.tei-c.org/ns/1.0}'
import xml.etree.ElementTree as ET

def load(path):
    raw = open(path, 'rb').read()
    print(path, hashlib.sha256(raw).hexdigest())
    return raw.decode('utf-8')

def normalize(txt):
    txt = txt.replace('ſ', 's').replace('æ', 'ae').replace('œ', 'oe').replace('Æ','AE')
    txt = unicodedata.normalize('NFKD', txt)
    return txt

def tokens(txt):
    return re.findall(r"[A-Za-z][A-Za-z']*", normalize(txt))

def strip_tags_join_hyphens(xml_fragment):
    s = re.sub(r'<g ref="char:EOLhyphen"/>\s*', '', xml_fragment)
    s = re.sub(r'<note\b[^>]*>.*?</note>', ' ', s, flags=re.S)  # margin notes are not body text
    s = re.sub(r'<[^>]+>', ' ', s)
    s = s.replace('&amp;', ' & ')
    return s

def pages(data):
    """Split body text by <pb n="..."> milestones; return {printed_n: [wordlists]} —
    a list per occurrence, since printed numbers repeat in A95749."""
    body_start = data.find('<body>')
    body = data[body_start:]
    parts = re.split(r'(<pb[^>]*/>)', body)
    out = {}
    cur = None
    buf = []
    def flush():
        if cur is not None:
            out.setdefault(cur, []).append(tokens(strip_tags_join_hyphens(''.join(buf))))
    for seg in parts:
        if seg.startswith('<pb'):
            m = re.search(r'n="(\d+)"', seg)
            if m:
                flush(); cur = int(m.group(1)); buf = []
            # unnumbered pb: continue current page (front matter etc.)
        else:
            buf.append(seg)
    flush()
    return out

def proquiritations(data):
    s = data.find('<div n="1" type="part">')
    e = data.find('<div type="epigraph">', s)
    if e == -1: e = len(data)
    chunk = data[s:e]
    divs = re.split(r'<div n="(\d+)" type="part">', chunk)
    parts = {}
    for i in range(1, len(divs), 2):
        n = int(divs[i]); body = divs[i+1]
        body = re.sub(r'<head>.*?</head>', ' ', body, flags=re.S)
        parts[n] = tokens(strip_tags_join_hyphens(body))
    return parts

logo = load('../sources/A64608.xml')
jewel = load('../sources/A95749.xml')
corpus = {
    'proq': proquiritations(logo),
    'logo_pages': pages(logo),
    'jewel_pages': pages(jewel),
}
print('proq sections:', len(corpus['proq']), 'wordcounts', [len(corpus['proq'][i]) for i in sorted(corpus['proq'])])
print('logo pages:', len(corpus['logo_pages']), 'max n', max(corpus['logo_pages']))
print('jewel pages:', len(corpus['jewel_pages']), 'max n', max(corpus['jewel_pages']))
json.dump({k: ({str(i): v for i, v in val.items()} if isinstance(val, dict) else val) for k, val in corpus.items()}, open('corpus.json', 'w'))
