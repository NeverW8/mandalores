from flask import Flask, redirect, url_for, render_template, abort, request, send_file
from flask_discord import DiscordOAuth2Session, requires_authorization
from threading import Thread
from dotenv import load_dotenv
from app.models import SoundClip
from app.scripts.soundboard_clip_generator import downloadClip
from app import db, create_app
from functools import wraps
import requests
import os

app = create_app()  # Use the create_app function to get the app instance

if os.path.exists('.envrc'):
    load_dotenv('.envrc')
else:
    load_dotenv()

print("DISCORD_CLIENT_ID:", os.getenv("DISCORD_CLIENT_ID"))
print("DATABASE_URL:", os.getenv("DATABASE_URL"))

app.secret_key = b"random bytes representing flask secret key"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "false"

app.config["DISCORD_CLIENT_ID"] = os.getenv("DISCORD_CLIENT_ID")
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_CLIENT_SECRET")
app.config["DISCORD_REDIRECT_URI"] = os.getenv("DISCORD_REDIRECT_URI")
app.config["DISCORD_WEBHOOK_URL"] = os.getenv("DISCORD_WEBHOOK_URL")

discord = DiscordOAuth2Session(app)
ALLOWED_USERS = ["fiskenhero", "soew", "exosist"]


def discord_webhook(username, message):
    if not os.getenv("DISCORD_WEBHOOK_URL"):
        print("No Discord webhook URL found.")
    else:
        webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        username = discord.fetch_user()
        message = f"{username} logged in.."
        data = {"content": message}
        response = requests.post(webhook_url, json=data)

        if response.status_code == 204:
            print("Message sent successfully.")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")


def allowed_user(func):
    @wraps(func)
    def is_allowed(*args, **kwargs):
        user = discord.fetch_user()
        if user.name in ALLOWED_USERS:
            return func(*args, **kwargs)
        else:
            abort(403)
    return is_allowed


def welcome_user(user):
    return f"Welcome, {user.name}!"


@app.route("/")
def index():
    return redirect(url_for("login_page"))


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/start-login")
def start_login():
    return discord.create_session(scope=['identify'], prompt=False)


@app.route("/callback/")
def callback():
    discord.callback()
    user = discord.fetch_user()
    discord_webhook(user.name, "has logged in")
    return redirect(url_for("home"))


@app.route("/home/")
@requires_authorization
@allowed_user
def home():
    user = discord.fetch_user()
    return render_template("home.html", user=user)


@app.route("/media")
@requires_authorization
@allowed_user
def media():
    user = discord.fetch_user()
    return render_template("media.html", user=user)


@app.route("/soundboard-clip-generator", methods=["GET", "POST"])
@requires_authorization
@allowed_user
def soundboard_clip_generator():
    user = discord.fetch_user()
    clip = None
    if request.method == "POST":
        url = request.form['url']
        start_time = request.form['start_time']
        stop_time = request.form['stop_time']

        clip = SoundClip(url=url, start_time=start_time, stop_time=stop_time, status='Pending')
        db.session.add(clip)
        db.session.commit()

        thread = Thread(target=generate_clip, args=(clip.id,))
        thread.start()

    return render_template("soundboard_clip_generator.html", user=user, clip=clip)


def generate_clip(clip_id):
    with app.app_context():
        clip = SoundClip.query.get(clip_id)
        if clip is None:
            print(f"No clip found with ID: {clip_id}")
            return

        try:
            downloadClip(clip.url, clip.start_time, clip.stop_time, clip_id)
            clip.status = 'Completed'
            clip.file_path = f'media/soundclip_{clip_id}.mp3'
        except Exception as e:
            print(f"Error generating clip: {e}")
            clip.status = 'Failed'

        db.session.commit()
        print(f"Clip status updated to {clip.status} for clip ID: {clip.id}")


@app.route("/get_clip_status/<int:clip_id>")
@requires_authorization
@allowed_user
def get_clip_status(clip_id):
    clip = SoundClip.query.get(clip_id)
    if clip:
        return {"status": clip.status}
    else:
        return {"status": "Not Found"}, 404


@app.route("/download_clip/<int:clip_id>")
@requires_authorization
@allowed_user
def download_clip(clip_id):
    clip = SoundClip.query.get(clip_id)
    if clip and clip.file_path:
        return send_file(clip.file_path, as_attachment=True)
    else:
        abort(404)


@app.route("/emoji_resizer")
@requires_authorization
@allowed_user
def emoji_resizer():
    user = discord.fetch_user()
    return render_template("emoji_resizer.html", user=user)


@app.route("/TBA/")
@requires_authorization
@allowed_user
def tba():
    user = discord.fetch_user()
    return render_template("home.html", message=welcome_user(user), user=user)



if __name__ == "__main__":
    app.run(debug=True)
