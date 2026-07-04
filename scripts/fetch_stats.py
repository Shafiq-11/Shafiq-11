import os
import sys
import json
import requests

def fetch_leetcode_stats(username):
    """
    Fetches LeetCode stats for a given username using GraphQL.
    Returns a dictionary of stats.
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
      }
    }
    """
    variables = {"username": username}
    try:
      response = requests.post(url, json={"query": query, "variables": variables}, timeout=10)
      if response.status_code == 200:
          data = response.json()
          if "data" in data and data["data"]["matchedUser"]:
              stats = data["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]
              result = {}
              for item in stats:
                  result[item["difficulty"].lower()] = item["count"]
              print(f"[LeetCode] Successfully fetched stats for {username}: {result}")
              return result
      print(f"[LeetCode] Failed to fetch stats, status code: {response.status_code}. Using mock data.")
    except Exception as e:
      print(f"[LeetCode] Error occurred: {e}. Using mock data.")
      
    return get_mock_leetcode_stats()

def get_mock_leetcode_stats():
    return {
        "all": 342,
        "easy": 150,
        "medium": 162,
        "hard": 30
    }

def fetch_wakatime_stats(api_key):
    """
    Fetches WakaTime coding stats for the last 7 days.
    """
    if not api_key:
        print("[WakaTime] No API Key provided. Using mock data.")
        return get_mock_wakatime_stats()
        
    url = "https://wakatime.com/api/v1/users/current/stats/last_7_days"
    headers = {
        "Authorization": f"Basic {api_key}"
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
        print(f"[WakaTime] Failed to fetch stats, status code: {response.status_code}. Using mock data.")
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
        # User details
        user_url = f"https://api.github.com/users/{username}"
        user_response = requests.get(user_url, headers=headers, timeout=10)
        
        # Repos details to sum stars
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
                "contributions": 1248, # Placeholder as contributions requires GraphQL/scraping
                "streak": 18
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
        "public_repos": 34,
        "stars": 82,
        "contributions": 1420,
        "streak": 24
    }

def main():
    # Usernames & configuration
    github_username = os.environ.get("GITHUB_ACTOR") or "Shafiq-11"
    leetcode_username = os.environ.get("LEETCODE_USERNAME") or "shafiq_11"
    wakatime_api_key = os.environ.get("WAKATIME_API_KEY")
    github_token = os.environ.get("GITHUB_TOKEN")
    
    print("--- Starting Stats Fetcher ---")
    leetcode = fetch_leetcode_stats(leetcode_username)
    wakatime = fetch_wakatime_stats(wakatime_api_key)
    github = fetch_github_stats(github_username, github_token)
    
    stats_data = {
        "leetcode": leetcode,
        "wakatime": wakatime,
        "github": github,
        "project50": {
            "coding": 92,
            "dsa": 86,
            "gym": 100,
            "projects": 90,
            "learning": 95,
            "day": 45
        },
        "workout": {
            "consistency": 96,
            "sessions_this_month": 22,
            "current_streak": 12
        },
        "bike": {
            "progress": 78,
            "distance_completed": 780,
            "target_distance": 1000,
            "status": "Cruising"
        }
    }
    
    # Save stats to a JSON file in output directory
    output_path = os.path.join(os.path.dirname(__file__), "stats.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(stats_data, f, indent=4)
    print(f"Stats written successfully to {output_path}")

if __name__ == "__main__":
    main()
