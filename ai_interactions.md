# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

**What task did you give the agent?**

I asked Claude Code (in agent mode) to add 5 or more advanced song features to the dataset and make the scoring logic use them. In the same session I also had it add scoring modes, a diversity penalty and a table layout for the terminal output.

**Prompts used:**

> Introduce 5 or more complex attributes to the dataset that aren't in the baseline data, like Song Popularity (0-100), Release Decade, or Detailed Mood Tags (e.g., "nostalgic," "aggressive," "euphoric"). Update both data/songs.csv and the scoring logic in src/recommender.py so scoring accounts for the new attributes.

> Implement a "Diversity Penalty" that penalizes a song's score if its artist is already in the top recommendations list, and also if too many songs share a genre.

> Use a library like tabulate or simple ASCII formatting to show the top recommendations as a table. The table must include the reasons for each score.

**What did the agent generate or change?**

- `data/songs.csv`: added 5 columns to all 18 songs:
  - `popularity`: 0–100
  - `release_decade`: e.g. 1980
  - `mood_tags`: e.g. `nostalgic;dreamy`
  - `instrumentalness`: 0–1
  - `liveness`: 0–1
- `src/recommender.py`:
  - `load_songs`: converts the new number columns and splits `mood_tags` into a list.
  - `score_song`: gives optional points for each new feature, but only if the user profile asks for it.
    - popularity: up to +0.5 for being close to the target
    - decade match: +0.5
    - each matching mood tag: +0.3
    - instrumental: +0.5
    - live feel: +0.3
  - `recommend_songs`: picks songs one at a time and takes 1.0 off for a repeat artist and 0.5 off for a repeat genre.
- `src/main.py`:
  - Added a "Nostalgic Night Drive" profile that uses the new features.
  - Added mode switching from the command line.
  - Replaced the plain list with an ASCII table that wraps the reasons column.
- I didn't use `tabulate`: it isn't installed, and simple ASCII formatting avoids adding a dependency.

**What did you verify or fix manually?**

- Ran `python -m src.main` after each change and checked the "Because" reasons matched the math. For example, Night Drive Loop scored 5.93 for the nostalgic profile: 2.0 + 1.0 + 0.85 + 0.48 + 0.5 + 0.3 + 0.3 + 0.5.
- Ran `pytest` after each step. The tests build `Song` objects without the new fields, so the scoring uses `.get()` for them and both tests still pass.
- Checked the diversity penalty on Chill Lofi: Focus Flow (same artist as #1, LoRoom, and also lofi) dropped from #3 to #4. For High-Energy Pop, a second Neon Echo song dropped out of the top 5.
- The agent's first edit to the table code broke `main.py` with a syntax error: its script calculated a position in the file and then shifted the text before inserting. The error showed up on the next run, and it was fixed and re-run before committing.

---

## Design Pattern (SF10)

**Which design pattern did you use?**

**Strategy pattern.** Each scoring mode is its own "strategy," a set of weights, and the scoring function takes whichever one you choose.

**How did AI help you brainstorm or implement it?**

I asked for a simple, modular way to switch between "Genre-First," "Mood-First" and "Energy-Focused" ranking. The AI compared two options:

1. A separate class per mode, each with its own `score()` method.
2. A dictionary of named weight sets that one shared scoring function reads from.

Since the modes only differ by their weights, we went with option 2. It's still a Strategy pattern, just lighter, and it avoids repeating the same scoring code three times. Adding a new mode is just adding one line to the dictionary. I built it on a separate branch (`experiment/mood-first`) so the working genre-first version on `main` stayed safe, then merged it back once the tests passed.

**How does the pattern appear in your final code?**

- `SCORING_MODES` at the top of [src/recommender.py](src/recommender.py) holds the three weight sets: `genre_first`, `mood_first` and `energy_focused`.
- `score_song(user_prefs, song, mode)` and `recommend_songs(..., mode=...)` look up the chosen strategy by name.
- `main.py` reads the mode from the command line: `python -m src.main mood_first`. An unknown mode prints the list of valid choices.
