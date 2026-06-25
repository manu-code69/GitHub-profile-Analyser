import requests

def get_github_data(username):
    # 1. Fetch User Profile Info (for your HTML card)
    user_url = f"https://api.github.com/users/{username}"
    user_response = requests.get(user_url)
    
    # If the user doesn't exist, return None
    if user_response.status_code != 200:
        return "No User exist With This Username "
        
    user_data = user_response.json()

    # 2. Fetch Repositories to calculate languages
    repo_url = f"https://api.github.com/users/{username}/repos"
    repo_list = requests.get(repo_url).json()

    all_repo_name = [repo["name"] for repo in repo_list]
    
    languages = {}

    # 3. Fetch Languages for each repo
    for repo in all_repo_name:

        lang_url = f"https://api.github.com/repos/{username}/{repo}/languages"

        lang_data = requests.get(lang_url).json()

        for lang, bytes_count in lang_data.items():
            if lang in languages:
                languages[lang] += bytes_count
            else:
                languages[lang] = bytes_count

    # 4. Calculate Percentages
    total_bytes = sum(languages.values())

    language_percentage = {}

    if total_bytes > 0:
        for lang, bytes_count in languages.items():

            percentage = (bytes_count / total_bytes) * 100

            language_percentage[lang] = round(percentage, 2)

    # 5. Bundle everything together to send back to Flask
    return {
        "profile": {
            "username": user_data.get("login"),
            "name": user_data.get("name") or user_data.get("login"),
            "bio": user_data.get("bio"),
            "pic": user_data.get("avatar_url"),
            "followers": user_data.get("followers"),
            "following": user_data.get("following"),
            "public_repos": user_data.get("public_repos")
        },
        "languages": language_percentage
    }
