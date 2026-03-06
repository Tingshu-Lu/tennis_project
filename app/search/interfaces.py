from typing import Protocol


class SearchProvider(Protocol):
    async def search(self, query: str) -> list[dict]:
        """Return normalized search results for a query."""
