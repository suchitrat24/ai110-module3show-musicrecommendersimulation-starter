# 🎵 Music Recommender Simulation

## Project Summary

My version is called **VibeMatch**. It's a small content-based music recommender that runs in the terminal. It reads 18 songs from `data/songs.csv`, compares each one to a user's taste profile, and prints the top 5 matches in a table with a score and the reasons behind each pick.

What it does:

- **Scores songs** on genre, mood and how close the energy is to what the user wants, plus optional extras: popularity, release decade, mood tags (like "nostalgic" or "dreamy"), instrumental songs and live-sounding songs.
- **Has 3 scoring modes** you can switch between: `genre_first` (default), `mood_first` and `energy_focused`. Run `python -m src.main mood_first` to try one.
- **Keeps the top 5 varied** by taking points off a song if its artist or genre is already in the list.
- **Explains every pick**, e.g. `genre match (+2.0), repeat artist (-1.0)`.

I tested it with several user profiles, including tricky ones like "sad but high energy," and wrote up what works and what doesn't in [model_card.md](model_card.md).

---

## How The System Works

Apps like Spotify recommend songs based on what similar people listen to and on what the songs sound like. My version only does the second part: it compares each song's features to what the user likes. Genre matters most, then mood, then energy. For energy, a song scores higher the closer it is to the user's target, so higher energy doesn't automatically win. Each song gets a score, then all the songs are sorted and the top few are recommended.

- **Song features:** genre, mood, energy, tempo_bpm, valence, danceability, acousticness, plus advanced ones: popularity (0–100), release_decade, mood_tags, instrumentalness, liveness
- **UserProfile features:** favorite_genre, favorite_mood, target_energy, likes_acoustic

### Algorithm Recipe

For each song:

- **+2.0** if the genre matches
- **+1.0** if the mood matches
- **+0 to 1.0** for energy closeness: `1 - |song energy - target energy|`
- **+0.5** if the user likes acoustic and the song's acousticness is above 0.6

Then sort all songs by score (highest first) and return the top K.

These are the `genre_first` weights. See the Project Summary for the other scoring modes, the advanced features and the diversity penalty.

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

Output of `python -m src.main` (first two profiles, default `genre_first` mode):

```
Loaded songs: 18
Scoring mode: genre_first

=== High-Energy Pop ===
Profile: genre=pop, mood=happy, energy=0.8
+-----+------------------------+------------------+--------+------------------------------------------------+
| #   | Title                  | Artist           | Score  | Reasons                                        |
+=====+========================+==================+========+================================================+
| 1   | Sunrise City           | Neon Echo        | 3.98   | genre match (+2.0), mood match (+1.0), energy  |
|     |                        |                  |        | closeness (+0.98)                              |
+-----+------------------------+------------------+--------+------------------------------------------------+
| 2   | Gym Hero               | Max Pulse        | 2.37   | genre match (+2.0), energy closeness (+0.87),  |
|     |                        |                  |        | repeat genre (-0.5)                            |
+-----+------------------------+------------------+--------+------------------------------------------------+
| 3   | Rooftop Lights         | Indigo Parade    | 1.96   | mood match (+1.0), energy closeness (+0.96)    |
+-----+------------------------+------------------+--------+------------------------------------------------+
| 4   | Concrete Crown         | Blockline        | 0.98   | energy closeness (+0.98)                       |
+-----+------------------------+------------------+--------+------------------------------------------------+
| 5   | Storm Runner           | Voltline         | 0.89   | energy closeness (+0.89)                       |
+-----+------------------------+------------------+--------+------------------------------------------------+

=== Chill Lofi ===
Profile: genre=lofi, mood=chill, energy=0.4, likes_acoustic=True
+-----+------------------------+------------------+--------+------------------------------------------------+
| #   | Title                  | Artist           | Score  | Reasons                                        |
+=====+========================+==================+========+================================================+
| 1   | Midnight Coding        | LoRoom           | 4.48   | genre match (+2.0), mood match (+1.0), energy  |
|     |                        |                  |        | closeness (+0.98), acoustic sound (+0.5)       |
+-----+------------------------+------------------+--------+------------------------------------------------+
| 2   | Library Rain           | Paper Lanterns   | 3.95   | genre match (+2.0), mood match (+1.0), energy  |
|     |                        |                  |        | closeness (+0.95), acoustic sound (+0.5),      |
|     |                        |                  |        | repeat genre (-0.5)                            |
+-----+------------------------+------------------+--------+------------------------------------------------+
| 3   | Spacewalk Thoughts     | Orbit Bloom      | 2.38   | mood match (+1.0), energy closeness (+0.88),   |
|     |                        |                  |        | acoustic sound (+0.5)                          |
+-----+------------------------+------------------+--------+------------------------------------------------+
| 4   | Focus Flow             | LoRoom           | 2.00   | genre match (+2.0), energy closeness (+1.00),  |
|     |                        |                  |        | acoustic sound (+0.5), repeat artist (-1.0),   |
|     |                        |                  |        | repeat genre (-0.5)                            |
+-----+------------------------+------------------+--------+------------------------------------------------+
| 5   | Coffee Shop Stories    | Slow Stereo      | 1.47   | energy closeness (+0.97), acoustic sound       |
|     |                        |                  |        | (+0.5)                                         |
+-----+------------------------+------------------+--------+------------------------------------------------+
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



