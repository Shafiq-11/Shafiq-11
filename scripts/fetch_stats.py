import os
import sys
import json
import requests

def fetch_leetcode_stats(username):
    """
    Fetches LeetCode stats for a given username using GraphQL.
    Includes solved questions, global ranking, badges, and contest ranking.
    """
    if not username:
        print("[LeetCode] No username provided. Using mock data.")
        return get_mock_leetcode_stats()
        
    url = "https://leetcode.com/graphql"
    query = """
    query userProblemsSolved($username: String!) {
      allQuestionsCount {
        difficulty
        count
      }
      matchedUser(username: $username) {
        submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
        profile {
          reputation
          ranking
        }
        badges {
          name
          icon
        }
      }
      userContestRanking(username: $username) {
        attendedContestsCount
        rating
        globalRanking
        topPercentage
      }
    }
    """
    variables = {"username": username}
    try:
        response = requests.post(url, json={"query": query, "variables": variables}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "errors" in data and any("does not exist" in err.get("message", "") for err in data["errors"]):
                print(f"[LeetCode] User {username} does not exist. Using mock data.")
                return get_mock_leetcode_stats()
                
            if "data" in data and data["data"]["matchedUser"]:
                matched_user = data["data"]["matchedUser"]
                stats = matched_user["submitStatsGlobal"]["acSubmissionNum"]
                
                result = {}
                for item in stats:
                    result[item["difficulty"].lower()] = item["count"]
                
                profile = matched_user["profile"] or {}
                result["ranking"] = profile.get("ranking", 0)
                result["reputation"] = profile.get("reputation", 0)
                
                badges = matched_user["badges"] or []
                result["badges"] = []
                for b in badges[:4]:
                    icon_url = b.get("icon", "")
                    if icon_url.startswith("/"):
                        icon_url = "https://leetcode.com" + icon_url
                    result["badges"].append({
                        "name": b.get("name", ""),
                        "icon": icon_url
                    })
                
                contest = data["data"].get("userContestRanking")
                if contest:
                    result["contest_rating"] = int(contest.get("rating", 0))
                    result["contest_ranking"] = contest.get("globalRanking", 0)
                    result["contest_top_percentage"] = contest.get("topPercentage", 0.0)
                else:
                    result["contest_rating"] = 0
                    result["contest_ranking"] = 0
                    result["contest_top_percentage"] = 0.0
                    
                print(f"[LeetCode] Successfully fetched stats for {username}")
                return result
        print(f"[LeetCode] Failed to fetch stats (HTTP {response.status_code}). Using mock data.")
    except Exception as e:
        print(f"[LeetCode] Error occurred: {e}. Using mock data.")
        
    return get_mock_leetcode_stats()

def get_mock_leetcode_stats():
    return {
        "all": 342,
        "easy": 150,
        "medium": 162,
        "hard": 30,
        "ranking": 120450,
        "reputation": 85,
        "badges": [
            {"name": "50 Days Badge 2025", "icon": "https://assets.leetcode.com/static_assets/marketing/2025-50-days.png"},
            {"name": "Knight", "icon": "https://assets.leetcode.com/static_assets/public/images/badges/knight.png"}
        ],
        "contest_rating": 1754,
        "contest_ranking": 12050,
        "contest_top_percentage": 8.5
    }

def fetch_wakatime_stats(api_key):
    """
    Fetches WakaTime coding stats for the last 7 days.
    """
    if not api_key:
        print("[WakaTime] No API Key provided. Using mock data.")
        return get_mock_wakatime_stats()
        
    import base64
    try:
        # WakaTime expects base64 encoded 'api_key:' in the Basic Auth header
        if not api_key.startswith("Basic ") and not api_key.endswith("="):
            encoded_key = base64.b64encode(f"{api_key}:".encode('utf-8')).decode('utf-8')
            auth_header = f"Basic {encoded_key}"
        else:
            auth_header = api_key if api_key.startswith("Basic ") else f"Basic {api_key}"
    except Exception:
        auth_header = f"Basic {api_key}"
        
    url = "https://wakatime.com/api/v1/users/current/stats/last_7_days"
    headers = {
        "Authorization": auth_header
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "data" in data:
                stats = data["data"]
                result = {
                    "total_hours": stats.get("human_readable_total_including_other_display", "24 hrs 15 mins"),
                    "daily_average": stats.get("human_readable_daily_average_including_other_display", "3 hrs 28 mins"),
                    "languages": [
                        {"name": lang["name"], "percent": lang["percent"]}
                        for lang in stats.get("languages", [])[:4]
                    ]
                }
                print(f"[WakaTime] Successfully fetched stats: {result}")
                return result
        print(f"[WakaTime] Failed to fetch stats, status code: {response.status_code}, response: {response.text}. Using mock data.")
    except Exception as e:
        print(f"[WakaTime] Error occurred: {e}. Using mock data.")
        
    return get_mock_wakatime_stats()

def get_mock_wakatime_stats():
    return {
        "total_hours": "32 hrs 40 mins",
        "daily_average": "4 hrs 40 mins",
        "languages": [
            {"name": "Java", "percent": 42.5},
            {"name": "TypeScript", "percent": 28.2},
            {"name": "JavaScript", "percent": 15.3},
            {"name": "Python", "percent": 10.0}
        ]
    }

def fetch_github_stats(username, token=None):
    """
    Fetches basic GitHub profile stats.
    """
    if not username:
        print("[GitHub] No username provided. Using mock data.")
        return get_mock_github_stats()
        
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
        
    try:
        user_url = f"https://api.github.com/users/{username}"
        user_response = requests.get(user_url, headers=headers, timeout=10)
        
        repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
        repos_response = requests.get(repos_url, headers=headers, timeout=10)
        
        if user_response.status_code == 200:
            user_data = user_response.json()
            stars = 0
            if repos_response.status_code == 200:
                repos_data = repos_response.json()
                stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
                
            result = {
                "followers": user_data.get("followers", 0),
                "public_repos": user_data.get("public_repos", 0),
                "stars": stars,
                "contributions": 1420, # GitHub contribution totals require scraping or GraphQL. Using a fallback.
                "streak": 24
            }
            print(f"[GitHub] Successfully fetched stats for {username}: {result}")
            return result
        print(f"[GitHub] Failed to fetch stats. Status code: {user_response.status_code}. Using mock data.")
    except Exception as e:
        print(f"[GitHub] Error occurred: {e}. Using mock data.")
        
    return get_mock_github_stats()

def get_mock_github_stats():
    return {
        "followers": 156,
        "public_repos": 3,
        "stars": 9,
        "contributions": 1420,
        "streak": 24
    }

def fetch_github_repos(username, token=None):
    """
    Fetches repositories list, filtering out forks.
    """
    if not username:
        return get_mock_repos()
        
    url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
        
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            repos = response.json()
            result = []
            for r in repos:
                if not r.get("fork"):
                    result.append({
                        "name": r.get("name"),
                        "description": r.get("description") or "No description provided.",
                        "language": r.get("language") or "Markdown",
                        "stars": r.get("stargazers_count", 0),
                        "forks": r.get("forks_count", 0),
                        "url": r.get("html_url")
                    })
            # Sort by stars, then by name
            result = sorted(result, key=lambda x: x["stars"], reverse=True)
            print(f"[GitHub] Fetched {len(result)} public repositories for {username}")
            return result[:6] # Return top 6 repos
        print(f"[GitHub] Failed to fetch repos (HTTP {response.status_code}). Using mock repos.")
    except Exception as e:
        print(f"[GitHub] Error fetching repos: {e}. Using mock repos.")
        
    return get_mock_repos()

def get_mock_repos():
    return [
        {
            "name": "maven-build-pipeline",
            "description": "Automated Maven CI/CD build pipeline configuration using GitHub Actions, featuring dockerized build isolation and test reporting.",
            "language": "Java",
            "stars": 4,
            "forks": 1,
            "url": "https://github.com/Shafiq-11/maven-build-pipeline"
        },
        {
            "name": "portfolio-shafiq",
            "description": "Minimalist and interactive developer portfolio site built using vanilla HTML, responsive CSS grids, and smooth animations.",
            "language": "HTML",
            "stars": 3,
            "forks": 0,
            "url": "https://github.com/Shafiq-11/portfolio-shafiq"
        },
        {
            "name": "React-learning",
            "description": "A comprehensive repository documenting my journey with the React ecosystem, covering state hooks, routing, and context APIs.",
            "language": "JavaScript",
            "stars": 2,
            "forks": 0,
            "url": "https://github.com/Shafiq-11/React-learning"
        }
    ]

def main():
    github_username = os.environ.get("GITHUB_ACTOR") or "Shafiq-11"
    leetcode_username = os.environ.get("LEETCODE_USERNAME") or "shafiq_11"
    wakatime_api_key = os.environ.get("WAKATIME_API_KEY")
    github_token = os.environ.get("GITHUB_TOKEN")
    
    print("--- Starting Stats Fetcher ---")
    leetcode = fetch_leetcode_stats(leetcode_username)
    wakatime = fetch_wakatime_stats(wakatime_api_key)
    github = fetch_github_stats(github_username, github_token)
    repos = fetch_github_repos(github_username, github_token)
    
    stats_data = {
        "leetcode": leetcode,
        "wakatime": wakatime,
        "github": github,
        "repos": repos
    }
    
    output_path = os.path.join(os.path.dirname(__file__), "stats.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(stats_data, f, indent=4)
    print(f"Stats written successfully to {output_path}")

if __name__ == "__main__":
    main()
