#!/usr/bin/env python3
"""Polite crawler for Military Archives Ireland online collections (Collins Papers etc.).

Usage:
  python3 crawl_collins.py --index-url https://www.militaryarchives.ie/en/online-collections/the-collins-papers-1917-1922 --out downloads/

Walks the catalogue pages, records every item descriptor, downloads PDFs, and writes
catalogue.jsonl with {url, title, descriptor, pdf_paths, cipher_hit}. Requires: requests,
beautifulsoup4. Respects robots.txt-ish manners: 1 req/2s, resumable, caches everything.

NOTE: written blind (site egress-blocked in the authoring session). Link-extraction
selectors may need one pass of adjustment against the live DOM; the structure below
assumes catalogue list pages -> item pages -> PDF links, which matches the site's
public description. Adjust ITEM_LINK_RE / PDF_RE if needed.
"""
import argparse, json, pathlib, re, time, urllib.parse
import requests
from bs4 import BeautifulSoup

CIPHER_TERMS = re.compile(
    r'\b(cypher|cipher|coded?|decoded?|undecipherable|in code|key ?word|playfair|'
    r'transposition|vigen|cryptic|secret writing)\b', re.I)
PDF_RE = re.compile(r'\.pdf($|\?)', re.I)

def get(session, url, delay=2.0, retries=4):
    for i in range(retries):
        try:
            r = session.get(url, timeout=60)
            if r.status_code == 200:
                time.sleep(delay)
                return r
        except requests.RequestException:
            pass
        time.sleep(2 ** (i + 1))
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--index-url', required=True)
    ap.add_argument('--out', default='downloads')
    ap.add_argument('--max-pages', type=int, default=100000)
    args = ap.parse_args()
    out = pathlib.Path(args.out); out.mkdir(parents=True, exist_ok=True)
    cat = open(out / 'catalogue.jsonl', 'a', encoding='utf-8')
    seen_path = out / 'seen.txt'
    seen = set(seen_path.read_text().split()) if seen_path.exists() else set()
    s = requests.Session()
    s.headers['User-Agent'] = 'collins-cipher-survey/1.0 (historical research; contact in repo)'
    queue = [args.index_url]
    host = urllib.parse.urlparse(args.index_url).netloc
    n = 0
    while queue and n < args.max_pages:
        url = queue.pop(0)
        if url in seen: continue
        seen.add(url); n += 1
        r = get(s, url)
        if r is None: continue
        if PDF_RE.search(url):
            name = re.sub(r'[^A-Za-z0-9._-]', '_', url.split('/')[-1])[:150]
            (out / name).write_bytes(r.content)
            continue
        soup = BeautifulSoup(r.text, 'html.parser')
        text = soup.get_text(' ', strip=True)
        title = soup.title.get_text(strip=True) if soup.title else ''
        pdfs = []
        for a in soup.find_all('a', href=True):
            u = urllib.parse.urljoin(url, a['href'])
            if urllib.parse.urlparse(u).netloc != host: continue
            if PDF_RE.search(u):
                pdfs.append(u)
            # stay inside the collections area
            if '/online-collections/' in u or '/collections/' in u or 'search' in u:
                if u not in seen: queue.append(u)
        for p in pdfs:
            if p not in seen: queue.append(p)
        rec = {'url': url, 'title': title,
               'descriptor': text[:2000],
               'pdf_links': pdfs,
               'cipher_hit': bool(CIPHER_TERMS.search(text))}
        cat.write(json.dumps(rec, ensure_ascii=False) + '\n'); cat.flush()
        seen_path.write_text('\n'.join(seen))
    print(f'crawled {n} pages; catalogue at {out}/catalogue.jsonl')

if __name__ == '__main__':
    main()
