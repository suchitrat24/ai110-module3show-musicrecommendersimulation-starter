# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

**Goal:** VibeMatch suggests the top 5 songs from a small catalog that best fit what a user says they like: a favorite genre, a favorite mood, an energy level, and whether they like acoustic music.

**Intended use:**
- A classroom project for learning how content-based recommenders score and rank items.
- Trying out different user profiles and weights to see how the results change.

**Not intended for:**
- Real users or a real music app. The catalog has only 18 songs, which is far too small.
- Judging what someone "should" like. It only knows four preferences, so it can't capture anyone's full taste.
- Anything where a bad suggestion matters, like picking music for therapy or for events.

It assumes the user can describe their taste with one genre, one mood and one energy number, and that they want the same vibe across all 5 songs.

---

## 3. How the Model Works  

The recommender looks at each song's genre, mood, energy and acousticness. It compares them to what the user says they like.

- A song gets 2 points if its genre matches the user's favorite genre and 1 point if its mood matches.
- It gets up to 1 more point based on how close its energy is to the user's target. A perfect match gets the full point, and songs that are much calmer or much more intense get less.
- If the user likes acoustic music, songs that sound mostly acoustic get a 0.5 point bonus.

Every song in the catalog is scored this way. The list is sorted from highest to lowest score, and the top 5 are shown with the reasons each one earned its points.

Compared to the starter code, I added the energy closeness score and the acoustic bonus, and each recommendation now comes with a list of reasons.

---

## 4. Data  

- **Size:** 18 songs in `data/songs.csv`. The starter had 10, and I added 8 more.
- **Features per song:** genre, mood, energy, tempo_bpm, valence, danceability and acousticness. The numbers are on a 0–1 scale, except tempo, which is in beats per minute.
- **What I added:** one song for each of hip hop, country, classical, metal, r&b, edm, reggae and folk, each with a new mood (confident, nostalgic, peaceful, angry, romantic, energetic, uplifting, sad).
- **Limits:**
  - Most genres have only one song. Lofi has the most, with 3.
  - The songs and numbers are made up, not real listening data.
  - There's no lyrics, language, artist popularity or listening history.
  - Tempo, valence and danceability are in the data but not used in scoring yet.

---

## 5. Strengths  

- Works well when the user's genre and mood both exist in the catalog. Chill Lofi, Deep Intense Rock and High-Energy Pop all got a #1 song that felt exactly right.
- Clearly separates opposite tastes. "Intense rock" and "chill lofi" share no songs in their top 5.
- When the genre doesn't exist (like k-pop), it still gives sensible picks based on mood and energy instead of breaking.
- Every recommendation shows its reasons, like `genre match (+2.0)`, so it's easy to see why a song ranked where it did.

---

## 6. Limitations and Bias 

The biggest weakness I found is that **energy points go to every song, for every user**, so very loud songs keep sneaking into lists where they don't belong. Gym Hero showed up in the top 5 for 4 of my 6 profiles (pop, rock, sad folk and metal) just because its energy is 0.93, which is close to what most of those users asked for. The system also has no idea that mood and energy can conflict: a user who wants "sad" music at energy 0.9 gets one sad folk song and then four loud songs that aren't sad at all. Genre has to match exactly, so a "k-pop" fan gets no genre points at all, and "indie pop" doesn't count as "pop." Finally, most genres only have one song in the catalog, so after the first match the rest of the list is filled by energy alone, and that creates a filter bubble of high-energy songs.

---

## 7. Evaluation  

I tested 6 profiles: 3 normal ones (High-Energy Pop, Chill Lofi, Deep Intense Rock) and 3 edge cases meant to trick the scoring (Sad but High Energy, Unknown Genre, Loud Acoustic Fan). Here's the top 5 for each, from `python -m src.main`. (These outputs were captured before I added the diversity penalty and table layout, so a few rankings are slightly different now.)

```
=== High-Energy Pop ===
Profile: genre=pop, mood=happy, energy=0.8
--------------------------------------------------
1. Sunrise City by Neon Echo  (Score: 3.98)
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.98)
2. Gym Hero by Max Pulse  (Score: 2.87)
   Because: genre match (+2.0), energy closeness (+0.87)
3. Rooftop Lights by Indigo Parade  (Score: 1.96)
   Because: mood match (+1.0), energy closeness (+0.96)
4. Concrete Crown by Blockline  (Score: 0.98)
   Because: energy closeness (+0.98)
5. Night Drive Loop by Neon Echo  (Score: 0.95)
   Because: energy closeness (+0.95)
```

```
=== Chill Lofi ===
Profile: genre=lofi, mood=chill, energy=0.4, likes_acoustic=True
--------------------------------------------------
1. Midnight Coding by LoRoom  (Score: 4.48)
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.98), acoustic sound (+0.5)
2. Library Rain by Paper Lanterns  (Score: 4.45)
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.95), acoustic sound (+0.5)
3. Focus Flow by LoRoom  (Score: 3.50)
   Because: genre match (+2.0), energy closeness (+1.00), acoustic sound (+0.5)
4. Spacewalk Thoughts by Orbit Bloom  (Score: 2.38)
   Because: mood match (+1.0), energy closeness (+0.88), acoustic sound (+0.5)
5. Coffee Shop Stories by Slow Stereo  (Score: 1.47)
   Because: energy closeness (+0.97), acoustic sound (+0.5)
```

```
=== Deep Intense Rock ===
Profile: genre=rock, mood=intense, energy=0.9
--------------------------------------------------
1. Storm Runner by Voltline  (Score: 3.99)
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.99)
2. Gym Hero by Max Pulse  (Score: 1.97)
   Because: mood match (+1.0), energy closeness (+0.97)
3. Laser Rush by Pulse Theory  (Score: 0.95)
   Because: energy closeness (+0.95)
4. Iron Furnace by Grave Signal  (Score: 0.93)
   Because: energy closeness (+0.93)
5. Sunrise City by Neon Echo  (Score: 0.92)
   Because: energy closeness (+0.92)
```

```
=== Sad but High Energy ===
Profile: genre=folk, mood=sad, energy=0.9
--------------------------------------------------
1. Empty Train Station by Hollow Pines  (Score: 3.40)
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.40)
2. Storm Runner by Voltline  (Score: 0.99)
   Because: energy closeness (+0.99)
3. Gym Hero by Max Pulse  (Score: 0.97)
   Because: energy closeness (+0.97)
4. Laser Rush by Pulse Theory  (Score: 0.95)
   Because: energy closeness (+0.95)
5. Iron Furnace by Grave Signal  (Score: 0.93)
   Because: energy closeness (+0.93)
```

```
=== Unknown Genre ===
Profile: genre=k-pop, mood=happy, energy=0.7
--------------------------------------------------
1. Rooftop Lights by Indigo Parade  (Score: 1.94)
   Because: mood match (+1.0), energy closeness (+0.94)
2. Sunrise City by Neon Echo  (Score: 1.88)
   Because: mood match (+1.0), energy closeness (+0.88)
3. Night Drive Loop by Neon Echo  (Score: 0.95)
   Because: energy closeness (+0.95)
4. Concrete Crown by Blockline  (Score: 0.92)
   Because: energy closeness (+0.92)
5. Island Sundown by Roots Tide  (Score: 0.88)
   Because: energy closeness (+0.88)
```

```
=== Loud Acoustic Fan ===
Profile: genre=metal, mood=angry, energy=0.95, likes_acoustic=True
--------------------------------------------------
1. Iron Furnace by Grave Signal  (Score: 3.98)
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.98)
2. Dusty Porch Swing by Willow Creek  (Score: 1.07)
   Because: energy closeness (+0.57), acoustic sound (+0.5)
3. Laser Rush by Pulse Theory  (Score: 1.00)
   Because: energy closeness (+1.00)
4. Gym Hero by Max Pulse  (Score: 0.98)
   Because: energy closeness (+0.98)
5. Midnight Coding by LoRoom  (Score: 0.97)
   Because: energy closeness (+0.47), acoustic sound (+0.5)
```

### Did the results feel right?

Mostly yes. For **Chill Lofi**, the top 3 are all lofi study tracks, and then it suggests ambient and jazz songs that are just as calm. That's exactly what I'd want. For **High-Energy Pop**, Sunrise City at #1 makes sense: it's pop, it's happy and its energy is 0.82, almost exactly the 0.8 target, so it got the most points in every category (2.0 + 1.0 + 0.98 = 3.98).

### Why does "Gym Hero" keep showing up for Happy Pop?

Gym Hero is a pop song, so it gets the full 2 points for genre even though it's a workout song with an "intense" mood, not a happy one. That 2-point genre bonus is bigger than the 1-point mood bonus, so Gym Hero (2.87) beats Rooftop Lights (1.96), even though Rooftop Lights is actually happy. Basically the system cares more about the label "pop" than about how the song feels.

### Comparing profiles

- **High-Energy Pop vs. Chill Lofi:** these two share no songs at all. Pop gets loud, upbeat songs (energy around 0.8) and lofi gets quiet, acoustic ones (energy around 0.4). This makes sense because genre, mood and energy all point in opposite directions.
- **High-Energy Pop vs. Deep Intense Rock:** both want high energy, so they share Gym Hero and Sunrise City. The difference is at #1: rock gets Storm Runner because only it matches both "rock" and "intense." Gym Hero jumps to #2 for rock because its mood is "intense," not because of its genre.
- **Chill Lofi vs. Deep Intense Rock:** completely different lists. Rock fills up with the loudest songs in the catalog (Laser Rush, Iron Furnace) while lofi fills up with calm acoustic songs. This shows the energy score really does separate "intense rock" from "chill lofi."
- **Deep Intense Rock vs. Sad but High Energy:** after #1 these lists are almost the same (Storm Runner, Gym Hero, Laser Rush, Iron Furnace). Asking for "sad" only changed one song, because there's only one sad song in the catalog. After that, energy decides everything.
- **High-Energy Pop vs. Unknown Genre:** the k-pop user gets almost the same list as the pop user but without the genre bonus, so Rooftop Lights (indie pop) moves up to #1. The system "falls back" to mood and energy when it doesn't know the genre, which is actually reasonable.
- **Deep Intense Rock vs. Loud Acoustic Fan:** both want very loud music, but the acoustic bonus pulled Dusty Porch Swing (country, energy 0.52) and Midnight Coding (lofi, energy 0.42) into the metal fan's top 5. That's the most wrong result I saw: no metal fan wants a lofi study track.

### What surprised me

- One sad folk song beat all the loud songs for the "Sad but High Energy" user even though its energy (0.30) is far from 0.9. Genre + mood (3 points) outweighs the whole energy score (1 point max).
- A small +0.5 acoustic bonus was enough to push quiet songs into a metal list.

### Experiment: Weight Shift (genre x0.5, energy x2)

I changed genre from 2.0 to 1.0 and energy from 1.0 to 2.0 (the max score stays the same, 4.5, so the math still works) and ran the same 6 profiles.

- **High-Energy Pop:** Rooftop Lights (2.92) moved above Gym Hero (2.74). **More accurate**, because the happy song now beats the intense one.
- **Loud Acoustic Fan:** the quiet songs (Dusty Porch Swing, Midnight Coding) dropped out and Storm Runner and Sunrise City came in. **More accurate.**
- **Chill Lofi and Deep Intense Rock:** same top 5, just different scores. **Only different, not better.**
- **Sad but High Energy:** the folk song still won, but its lead shrank from 2.4 points to 0.8. **Different**, since the conflict between "sad" and "high energy" still can't really be solved with this catalog.

Overall the weight shift made things a bit more accurate, mostly by stopping genre from overruling how a song actually feels. I kept the original weights in the code, but I'd consider switching.

---

## 8. Future Work  

1. **Lower the genre weight or give partial credit for related genres**, so "indie pop" counts a little toward "pop," and a happy song isn't beaten by an intense one just because of its label.
2. **Use more features**, like valence for how happy or sad a song sounds and tempo. Then "sad" and "high energy" could be balanced better.
3. **Add variety to the top 5**, for example a limit of one song per artist, or making sure the same loud song (Gym Hero) doesn't fill every list.

---

## 9. Personal Reflection  

**Biggest learning moment:** I learned how much the weights decide everything. Changing the genre weight from 2 to 1 changed which song came second for pop fans. The "intelligence" of the system is really just a few numbers I picked.

**Using AI tools:** AI helped me write the CSV loader, the scoring function and the edge-case profiles quickly. I still had to check its work by running the program and reading the output. For example, the acoustic bonus looked fine in code, but the output showed it pushed lofi songs into a metal fan's list. The AI didn't catch that until we looked at real results.

**What surprised me:** Even simple rules like "add 2 points for genre" produced lists that felt like real recommendations. The reasons printed next to each song made it feel smart, even though it's just addition and sorting.

**What I'd try next:** I'd add valence and tempo to the score, give partial credit for similar genres, and test with a bigger catalog to see if the "Gym Hero everywhere" problem goes away.
