

import requests

def fetch_news(query, country_code, api_key):
    """
    Fetch top relevant news for a given query and country using NewsAPI.
    Implements a fallback mechanism to broaden search if initial results are insufficient.
    """
    def make_request(params):
        url = "https://newsapi.org/v2/everything"
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching news: {response.status_code} - {response.text}")
        return response.json().get("articles", [])

    # Initial request parameters
    params = {
        "q": f"{query} AND {country_code}",
        "language": "en",
        "sortBy": "relevancy",
        "apiKey": api_key,
        "pageSize": 5,
    }

    articles = make_request(params)

    # Fallback to broader search if no articles found
    if not articles:
        params["q"] = query
        articles = make_request(params)

    news_list = []
    for article in articles:
        news_list.append({
            "title": article.get("title", "No Title"),
            "description": article.get("description", ""),
            "url": article.get("url", "#"),
            "source": article.get("source", {}).get("name", "Unknown")
        })

    return news_list

def generate_news_insights(news_articles):
    """Generate summary-style insights from news."""
    if not news_articles:
        return "No recent news found that could significantly impact this field."

    summary_points = []
    for article in news_articles:
        title = article['title']
        source = article['source']
        url = article['url']
        summary_points.append(f"🔹 **{title}**  \n(Source: {source})  \n[Read More]({url})")

    return "\n\n".join(summary_points)
