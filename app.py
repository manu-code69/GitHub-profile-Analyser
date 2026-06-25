from flask import Flask, render_template, request
from services.data_collection import get_github_data    # services file ka under ha 
import requests     # for json requests

app = Flask(__name__)

@app.route("/")
def base():
    return render_template("base.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():

    name = request.form.get("username")

#******************************************************************
    # url = f"https://api.github.com/users/{name}"

    # response = requests.get(url)

    # if response.status_code != 200:               THIS PORTION IS DUPLICATE API CALLING
    #     return "No Such User Found"

    # data = response.json()

    # followers = data.get("followers", 0)
    # following = data.get("following", 0)
    # repos = data.get("public_repos", 0)
    # photo = data.get("avatar_url")
    # nme = data.get("name")
#*****************************************************************
    
    github_data = get_github_data(name)

    if github_data is None:
        return "No Data Found"
    
    languages_ka_data = github_data["languages"]

    
    
    if languages_ka_data is None:
        return "No Language found"

    profile = github_data["profile"]

    return render_template(
        "result.html",
        user=profile["username"],
        flwr=profile["followers"],
        flwing = profile["following"],
        public_repos = profile["public_repos"],
        pic = profile["pic"],
        orgname = profile["name"],
        languages = github_data["languages"]
    )

if __name__ == "__main__":
    app.run(debug=True)