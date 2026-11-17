from flask import Flask, render_template, redirect, abort, request

app = Flask(__name__)

MOODS = {
    "happy":     {"label": "Happy",     "emoji": "😄", "color": "#ffd23f", "query": "happy upbeat songs playlist"},
    "calm":      {"label": "Calm",      "emoji": "😌", "color": "#7bdff2", "query": "calm relaxing songs playlist"},
    "sad":       {"label": "Sad",       "emoji": "😢", "color": "#b8a1ff", "query": "comforting sad songs playlist"},
    "energetic": {"label": "Energetic", "emoji": "⚡", "color": "#ff7b54", "query": "energetic workout songs playlist"},
}

LANGUAGES = ["English", "Malayalam", "Tamil", "Telugu", "Kannada", "Hindi"]

# Your songs: ("Language", "mood"): "file name inside static/music"
LOCAL_SONGS = {
    ("English", "sad"):       "sad.mp3",
    ("English", "happy"):     "happy.mp3",
    ("English", "calm"):      "calm.mp3",
    ("English", "energetic"): "energetic.mp3",
}

def pick_language():
    lang = request.args.get("lang")
    return lang if lang in LANGUAGES else None

@app.route("/")
def home():
    return render_template("index.html", moods=MOODS, languages=LANGUAGES, lang=pick_language())

@app.route("/mood/<name>")
def mood(name):
    if name not in MOODS:
        abort(404)
    lang = pick_language()
    if not lang:
        return redirect("/")
    song = LOCAL_SONGS.get((lang, name))
    if not song:
        return f"No song added yet for {lang} · {MOODS[name]['label']}. <a href='/?lang={lang}'>Go back</a>"
    return render_template("play.html", m=MOODS[name], lang=lang, song=song)

if __name__ == "__main__":
    app.run()