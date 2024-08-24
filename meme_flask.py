from flask import Flask, render_template, jsonify
import requests
import random

app = Flask(__name__)

def get_meme():
    url = "https://api.imgflip.com/get_memes"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure we got a valid response
        data = response.json()  # Convert to JSON
        memes = data['data']['memes']
        if not memes:
            return None, "No memes available"
        # Randomly select a meme
        meme = random.choice(memes)
        meme_pic = meme['url']  # URL of the meme image
        meme_title = meme['name']  # Title of the meme
        return meme_pic, meme_title
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None, "Error fetching meme"
    except ValueError as e:
        print(f"JSON decode error: {e}")
        return None, "Error parsing JSON"
    except KeyError as e:
        print(f"Key error: {e}")
        return None, "Error parsing meme data"

@app.route("/")
def index():
    meme_pic, meme_title = get_meme()
    return render_template("meme_index.html", meme_pic=meme_pic, meme_title=meme_title)

@app.route("/new_meme")
def new_meme():
    meme_pic, meme_title = get_meme()
    if meme_pic:
        return jsonify(meme_pic=meme_pic, meme_title=meme_title)
    else:
        return jsonify(meme_pic=None, meme_title="Error fetching meme"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
