# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Apps like Spotify recommend songs based on what similar people listen to and on what the songs sound like. My version only does the second part: it compares each song's features to what the user likes. Genre matters most, then mood, then energy. For energy, a song scores higher the closer it is to the user's target, so higher energy doesn't automatically win. Each song gets a score, then all the songs are sorted and the top few are recommended.

- **Song features:** genre, mood, energy, tempo_bpm, valence, danceability, acousticness
- **UserProfile features:** favorite_genre, favorite_mood, target_energy, likes_acoustic

### Algorithm Recipe

For each song:

- **+2.0** if the genre matches
- **+1.0** if the mood matches
- **+0 to 1.0** for energy closeness: `1 - |song energy - target energy|`
- **+0.5** if the user likes acoustic and the song's acousticness is above 0.6

Then sort all songs by score (highest first) and return the top K.

### Data Flow

```
User prefs  ->  Loop: score every song in songs.csv  ->  Sort by score  ->  Top K songs
```

### Expected Biases

- Genre is worth the most, so a great song that matches the mood but not the genre might get skipped.
- Genre has to match exactly, so "indie pop" doesn't count as "pop."
- The catalog is small (18 songs) and some genres only have one song, so those users get fewer good matches.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



