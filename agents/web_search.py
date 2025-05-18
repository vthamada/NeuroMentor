# agents/web_search.py

from __future__ import annotations

import html
import re
import urllib.parse
from typing import Dict, List, Union

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
    )
}

def _clean(t: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(t)).strip()

def _parse_duckduckgo(html_text: str, k: int) -> List[Dict]:
    soup = BeautifulSoup(html_text, "html.parser")
    out = []
    for res in soup.select("a.result__a")[:k]:
        title = _clean(res.get_text())
        link = res["href"]
        snippet_tag = (
            res.find_parent("div", class_="result").select_one(".result__snippet")
        )
        snippet = _clean(snippet_tag.get_text()) if snippet_tag else ""
        out.append({"title": title, "url": link, "snippet": snippet})
    return out

def _bing_scrape(query: str, k: int) -> List[Dict]:
    url = f"https://www.bing.com/search?q={query}"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    out = []
    for li in soup.select("li.b_algo")[:k]:
        a = li.find("a")
        title = _clean(a.get_text())
        url = a["href"]
        snippet_tag = li.find("p")
        snippet = _clean(snippet_tag.get_text()) if snippet_tag else ""
        out.append({"title": title, "url": url, "snippet": snippet})
    return out

def buscar_conteudo_web(tema: str, quantidade: int = 5) -> Union[List[Dict], str]:
    query = urllib.parse.quote_plus(tema)
    ddg_url = f"https://html.duckduckgo.com/html/?q={query}&kl=wt-wt"
    try:
        r = requests.get(ddg_url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        results = _parse_duckduckgo(r.text, quantidade)
        if results:
            return results
    except Exception:
        pass  # tenta Bing

    try:
        return _bing_scrape(query, quantidade)
    except Exception as exc:
        return f"*Falha na busca web*: {exc}"
