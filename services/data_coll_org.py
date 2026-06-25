import requests
from flask import request,Flask,render_template,url_for
app = Flask(__name__)

@app.route("/result", methods=["POST"])
def result():

    all_repo_name = []

    username = request.form.get("username")

    url = f"https://api.github.com/users/{username}"

    repo_url = f"https://api.github.com/users/{username}/repos"

    repo_list = requests.get(repo_url).json()

    for repo in repo_list :
        all_repo_name.append(repo["name"])

    languages = {}

    for repo in all_repo_name:
        lang_url = f"https://api.github.com/repos/{username}/{repo}/languages"

        lang_data = requests.get(lang_url).json()

        for lang,bytes_count in lang_data.items():

            if lang in languages :
                languages[lang] += bytes_count
            
            else :
                languages[lang] = bytes_count
            

