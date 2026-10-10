import requests

def search_books(query):
    """
    Fetches books from the Google Books API based on the search query.
    Returns a formatted list of book dictionaries.
    """
    if not query or not query.strip():
        return []

    url = f"https://www.googleapis.com/books/v1/volumes?q={requests.utils.quote(query.strip())}&maxResults=12"
    
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    books = []
    for item in data.get("items", []):
        volume_info = item.get("volumeInfo", {})

        # Extract image thumbnail safely
        image_links = volume_info.get("imageLinks", {})
        thumbnail = image_links.get("thumbnail") or image_links.get("smallThumbnail")
        # Replace http with https for security
        if thumbnail and thumbnail.startswith("http://"):
            thumbnail = "https://" + thumbnail[7:]

        book = {
            "id": item.get("id"),
            "title": volume_info.get("title", "Unknown Title"),
            "authors": ", ".join(volume_info.get("authors", ["Unknown Author"])),
            "publishedDate": volume_info.get("publishedDate", "N/A"),
            "publisher": volume_info.get("publisher", "Unknown Publisher"),
            "description": volume_info.get("description", "No description available."),
            "thumbnail": thumbnail or "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?auto=format&fit=crop&w=400&q=80",
            "previewLink": volume_info.get("previewLink", "#")
        }
        books.append(book)

    return books