
from serpapi import GoogleSearch

def fetch_business_details(location: str, business_type: str, serpapi_key: str):
    query = f"{business_type} in {location}"

    params = {
        "engine": "google",
        "q": query,
        "location": location,
        "api_key": serpapi_key
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        details = []
        for result in organic_results:
            title = result.get("title", "N/A")
            link = result.get("link", "N/A")
            snippet = result.get("snippet", "No description available.")
            details.append({"title": title, "link": link, "snippet": snippet})
        return details
    except Exception as e:
        return [{"title": "Error", "link": "N/A", "snippet": f"Error: {e}"}]
