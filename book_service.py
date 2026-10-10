import requests


BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"
OPEN_LIBRARY_API_URL = "https://openlibrary.org/search.json"
FALLBACK_THUMBNAIL = (
    "https://images.unsplash.com/photo-1543002588-bfa74002ed7e"
    "?auto=format&fit=crop&w=400&q=80"
)


def search_books(query):
    """
    Search Google Books, falling back to Open Library when Google is unavailable
    or returns no matches.
    """
    if not query or not query.strip():
        return []

    search_query = query.strip()
    try:
        books = _search_google_books(search_query)
    except requests.RequestException:
        books = []

    return books or _search_open_library(search_query)


def _search_google_books(query):
    response = requests.get(
        BOOKS_API_URL,
        params={"q": query, "maxResults": 12},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    books = []
    for item in data.get("items", []):
        volume_info = item.get("volumeInfo", {})
        image_links = volume_info.get("imageLinks", {})
        thumbnail = image_links.get("thumbnail") or image_links.get("smallThumbnail")
        if thumbnail and thumbnail.startswith("http://"):
            thumbnail = "https://" + thumbnail[7:]

        books.append({
            "id": item.get("id"),
            "title": volume_info.get("title", "Unknown Title"),
            "authors": ", ".join(volume_info.get("authors", ["Unknown Author"])),
            "publishedDate": volume_info.get("publishedDate", "N/A"),
            "publisher": volume_info.get("publisher", "Unknown Publisher"),
            "description": volume_info.get("description", "No description available."),
            "thumbnail": thumbnail or FALLBACK_THUMBNAIL,
            "previewLink": volume_info.get("previewLink", "#"),
        })

    return books


def _search_open_library(query):
    response = requests.get(
        OPEN_LIBRARY_API_URL,
        params={"q": query, "limit": 12},
        headers={"User-Agent": "BookFinderApp/1.0"},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    books = []
    for item in data.get("docs", []):
        cover_id = item.get("cover_i")
        work_key = item.get("key")
        books.append({
            "id": work_key,
            "title": item.get("title", "Unknown Title"),
            "authors": ", ".join(item.get("author_name", ["Unknown Author"])),
            "publishedDate": str(item.get("first_publish_year", "N/A")),
            "publisher": ", ".join(item.get("publisher", [])[:1]) or "Unknown Publisher",
            "description": "No description available.",
            "thumbnail": (
                f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                if cover_id else FALLBACK_THUMBNAIL
            ),
            "previewLink": (
                f"https://openlibrary.org{work_key}" if work_key else "#"
            ),
        })

    return books