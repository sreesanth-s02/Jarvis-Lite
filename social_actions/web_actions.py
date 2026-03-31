import webbrowser
from urllib.parse import quote

class WebActions:
    def open_youtube(self, query: str) -> str:
        url = f"https://www.youtube.com/results?search_query={quote(query)}"
        webbrowser.open(url)
        return f"Opened YouTube search for {query}."

    def open_spotify(self, query: str) -> str:
        url = f"https://open.spotify.com/search/{quote(query)}"
        webbrowser.open(url)
        return f"Opened Spotify search for {query}."

    def open_linkedin(self) -> str:
        webbrowser.open("https://www.linkedin.com/")
        return "Opened LinkedIn."

    def open_instagram(self) -> str:
        webbrowser.open("https://www.instagram.com/")
        return "Opened Instagram."

    def open_gmail_compose(self, to: str = "", subject: str = "", body: str = "") -> str:
        url = (
            "https://mail.google.com/mail/?view=cm&fs=1"
            f"&to={quote(to)}&su={quote(subject)}&body={quote(body)}"
        )
        webbrowser.open(url)
        return "Opened Gmail compose window."

    def open_search(self, query: str) -> str:
        if not query:
            return "No query provided for web search."
        url = f"https://www.google.com/search?q={quote(query)}"
        webbrowser.open(url)
        return f"Opened browser search for '{query}'."