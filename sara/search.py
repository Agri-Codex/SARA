import logging
import urllib.parse

import requests
from bs4 import BeautifulSoup

SEARCH_URL = "https://html.duckduckgo.com/html"


def duckduckgo_search(query: str, max_results: int = 5):
    """Search DuckDuckGo and return structured search results."""
    try:
        response = requests.post(SEARCH_URL, data={"q": query}, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for item in soup.select("a.result__a")[:max_results]:
            title = item.get_text(strip=True)
            url = item.get("href")
            snippet_tag = item.find_parent("div", class_="result").select_one("a.result__snippet")
            snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
            results.append({"title": title, "url": url, "description": snippet})

        if not results:
            for item in soup.select("div.result")[:max_results]:
                link = item.select_one("a.result__a")
                title = link.get_text(strip=True) if link else ""
                url = link.get("href") if link else ""
                snippet = item.select_one("a.result__snippet")
                snippet_text = snippet.get_text(strip=True) if snippet else ""
                results.append({"title": title, "url": url, "description": snippet_text})

        return results
    except Exception as exc:
        logging.warning("Internet search failed: %s", exc)
        return []


def summarize_search_results(results):
    """Create a short summary of the top search results."""
    if not results:
        return None

    summary_lines = []
    for index, item in enumerate(results[:3], start=1):
        title = item.get("title", "No title")
        url = item.get("url", "")
        description = item.get("description", "No description available.")
        if url and url.startswith("/"):
            url = urllib.parse.unquote(url)
        summary_lines.append(f"{index}. {title}\n   {description}\n   {url}")

    return "\n\n".join(summary_lines)
