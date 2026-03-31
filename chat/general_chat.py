import logging
import re
from urllib.parse import quote

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeneralChat:
    def __init__(self):
        pass

    def _llm_answer(self, user_text: str) -> str:
        safe_search = quote(user_text)
        return f"I can help by searching this on the web: https://www.google.com/search?q={safe_search}"

    def reply(self, text: str) -> str:
        t = text.lower().strip()

        if t in {"hi", "hello", "hey", "hey jarvis", "good afternoon","good morning", "good evening"}:
            return "Hello, I am Jarvis AI. How can I help you?"

        if t in {"how are you", "how are you?"}:
            return "I am doing well, thanks! I am ready to assist you."

        if t in {"who are you", "who are you?"}:
            return "I am Jarvis AI, your personal assistant with safe general chat and web search support."

        if t in {"what is ai", "what is artificial intelligence", "define ai"}:
            return "AI (artificial intelligence) means machines that can perform tasks that normally require human intelligence, such as understanding language, recognising patterns, and making decisions."

        if t in {"who is cm of kerala", "who is the cm of kerala", "kerala cm"}:
            return "As of 2026, the Chief Minister of Kerala is Pinarayi Vijayan."

        if t in {"who is pm of india", "who is the prime minister of india", "india pm"}:
            return "As of 2026, the Prime Minister of India is Narendra Modi."

        if "browse" in t or "search" in t or "weather" in t:
            # Router will handle search tools; respond with web action suggestion.
            if "weather" in t:
                city = re.sub(r".*weather in", "", t).strip() or "your location"
                return f"Searching for weather updates for {city}..."
            query = t.replace("browse", "").replace("search", "").strip()
            if not query:
                query = "general information"
            return f"Searching the web for: {query}"

        # Named people or general info
        if re.search(r"who is|who are|cast of|tell me about", t):
            return self._llm_answer(text)

        # Evaluate explicit arithmetic first so simple math does not always hit LLM fallback
        if re.search(r'^\s*(what is|calculate|solve)\s+(-?\d+(\.\d+)?\s*[\+\-\*/]\s*-?\d+(\.\d+)?)\s*\??$', t):
            try:
                expr = re.findall(r'(-?\d+(?:\.\d+)?\s*[\+\-\*/]\s*-?\d+(?:\.\d+)?)', t)[0]
                result = eval(expr)
                return f"{expr} = {result}"
            except Exception:
                logger.warning("Safe math eval failed for: %s", t)

        if re.search(r"(what is|calculate|\\d+\\s*\\+\\s*\\d+)", t):
            return self._llm_answer(text)

        # Fallback to web search response
        return self._llm_answer(text)
