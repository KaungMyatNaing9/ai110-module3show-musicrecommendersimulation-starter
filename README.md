# 🎵 Music Recommender Simulation

## Project Summary

This project is a content-based music recommender system called VibeFinder 1.0. It reads a catalog of 20 songs from a CSV file and compares each song's features to a user's stored taste preferences. Features include genre, mood, energy, tempo, valence, danceability, and acousticness. Each song receives a compatibility score based on how closely it matches the user's preferences, and the top five highest-scoring songs are returned as recommendations. The scoring rewards closeness rather than magnitude, meaning a song does not rank higher just for being loud or fast. It ranks higher because its values are near what the user asked for. The system was tested with six different user profiles including standard profiles like High-Energy Pop and Chill Lofi, and adversarial profiles like Conflicted Energy and All-Low/Dark to explore where the logic breaks down.

---

## How The System Works

Real-world recommendation systems like Spotify and YouTube use **hybrid recommendation systems** — combining two main approaches. **Collaborative filtering** looks at patterns in user behavior (likes, skips, playlists) and finds other users with similar habits to inform suggestions. **Content-based filtering** analyzes the actual properties of a song — energy, tempo, mood, danceability — and finds other songs with similar characteristics. These systems operate at massive scale, processing millions of interactions per second using machine learning models trained on billions of data points. They continuously update recommendations in real time, so the more you listen, the more personalized your feed becomes. Real systems also optimize for engagement metrics like watch time and retention, meaning recommendations are shaped not just by what you like but by what keeps you on the platform longest. This combination of behavioral signals and audio features is what makes modern recommenders feel surprisingly accurate at capturing your "vibe."

Our system takes a simpler but conceptually grounded approach. We implement a **content-based recommendation system** that generates recommendations by directly comparing each song's features to a stored user taste profile — no listening history needed. Every song is represented as a vector of numerical and categorical features (energy, valence, tempo, danceability, acousticness, genre, mood) that describe the "feel" of that track. To score a song, we compute how close its feature values are to the user's preferences using a **distance-based scoring function** that rewards closeness rather than just higher or lower values. Categorical features (genre and mood) are matched directly for a binary full-weight or zero contribution. All features are then combined into a normalized final score between 0 and 1.

### Algorithm Recipe

| Feature | Weight | How It's Scored |
|---|---|---|
| `genre` match | **2.0** | +2.0 if genre matches, +0 otherwise |
| `mood` match | **1.5** | +1.5 if mood matches, +0 otherwise |
| `energy` similarity | **1.0** | `1 - \|song - user\| / 1.0` × 1.0 |
| `valence` similarity | **1.0** | `1 - \|song - user\| / 1.0` × 1.0 |
| `danceability` similarity | **0.75** | `1 - \|song - user\| / 1.0` × 0.75 |
| `tempo_bpm` similarity | **0.75** | `1 - \|song - user\| / 120` × 0.75 |
| `acousticness` similarity | **0.5** | `1 - \|song - user\| / 1.0` × 0.5 |
| **Total max score** | **7.5** | Final score normalized to 0–1 range |

**Numerical similarity formula:** `similarity = 1 - (|song_value - user_value| / max_range)`
This rewards closeness — a song perfectly matching the user's preferred energy scores 1.0, while the maximum possible distance scores 0.0.

### Scoring vs. Ranking

**Scoring** assigns a compatibility number to each individual song in the catalog. **Ranking** is the final step — all scored songs are sorted in descending order and the **top K** are returned as recommendations. Scoring answers *"how compatible is this song?"* Ranking answers *"which songs are best relative to each other?"*

See the full system flowchart: [docs/system_flowchart.md](docs/system_flowchart.md)

### Sample Output

![Recommender terminal output](docs/output.png)

### Limitations and Bias

- The high genre weight (2.0) means a song with a different genre label but nearly identical energy, mood, and tempo will rank much lower than it deserves — the system may miss great cross-genre matches.
- Users with niche preferences (e.g., classical or metal) will receive weaker recommendations from a catalog that underrepresents those genres, since the genre match bonus is rarely triggered.
- All features are treated as independent — the system doesn't capture combined signals like "high energy AND high acousticness" (typical of live recordings), so those combinations may be scored misleadingly.

---

## Features Used in This Simulation

### Song Object Features

- `genre` — the musical category of the song (e.g. pop, hip-hop, jazz)
- `mood` — the emotional tone of the song (e.g. happy, melancholic, aggressive)
- `energy` — a 0–1 score reflecting intensity and activity level
- `tempo_bpm` — the speed of the song in beats per minute (realistic range: 60–180)
- `valence` — a 0–1 score reflecting musical positivity (high = upbeat, low = somber)
- `danceability` — a 0–1 score reflecting how suitable the song is for dancing
- `acousticness` — a 0–1 score reflecting how acoustic (vs. electronic) the song sounds

### UserProfile Features

- `preferred_genre` — the user's favorite musical genre
- `preferred_mood` — the emotional tone the user currently prefers
- `preferred_energy` — the user's preferred energy level (0–1)
- `preferred_tempo` — the user's preferred song speed in BPM
- `preferred_valence` — the user's preferred positivity/mood tone (0–1)
- `preferred_danceability` — the user's preferred danceability level (0–1)
- `preferred_acousticness` — the user's preference for acoustic vs. electronic sound (0–1)

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

## Experiments You Tried

Six user profiles were tested to evaluate how the recommender behaves across different taste types.

The Chill Lofi profile gave the cleanest results. Library Rain ranked first because its energy was a perfect match at 0.35 and its acousticness of 0.86 was very close to the preferred 0.80. Both genre and mood also matched, giving it the full categorical bonus of 3.0 points. Midnight Coding came in second with nearly identical reasoning, just slightly further from the preferred energy and acousticness values. This felt exactly right.

The Conflicted Energy profile was the most revealing. It asked for ambient genre and melancholic mood, but also 0.95 energy and 0.90 danceability. No song in the catalog fits all of those at once. The system ended up recommending high-energy songs that completely ignored the mood preference, essentially falling back to numerical similarity when categorical features found no match. This showed that the system has no way to handle internally contradictory preferences. It just averages everything and picks the survivors.

A weight shift experiment was also reasoned through without changing the code. Doubling the energy weight from 1.0 to 2.0 and halving the genre weight from 2.0 to 1.0 would cause cross-genre songs with similar energy to compete more evenly with genre-matched songs. For a High-Energy Pop user, an EDM song like Neon Babylon would climb the rankings because its energy of 0.95 almost perfectly matches the preference of 0.90, even without a genre match. The tradeoff is that recommendations become less stylistically consistent.

### Terminal Output Screenshots

**High-Energy Pop**
![High-Energy Pop Results](docs/highenergy.png)

**Chill Lofi**
![Chill Lofi Results](docs/chill.png)

**Deep Intense Rock**
![Deep Intense Rock Results](docs/deeprock.png)

**Conflicted Energy (adversarial)**
![Conflicted Energy Results](docs/conflictedenergy.png)

**All-Low / Dark (adversarial)**
![All-Low / Dark Results](docs/alllow.png)

**K-Pop Aggressive (adversarial)**
![K-Pop Aggressive Results](docs/kpop.png)

---

## Limitations and Risks

The genre weight of 2.0 is the single biggest source of bias in the system. Because a genre match automatically adds 2.0 points and no other single feature can match that, songs from a slightly different but similar genre will almost always lose, even if they match the user's actual vibe much better. A pop song and an indie pop song can sound nearly identical, but the system treats them as completely unrelated.

The catalog is too small to serve users with uncommon preferences. With only 20 songs, a user who prefers classical or metal music has at most one matching song in the dataset. The rest of the top five recommendations become whatever is least wrong, not what is actually right.

The system cannot handle internally conflicting user profiles. If a user says they want very high energy but also a melancholic mood, those two preferences fight each other and no song can satisfy both. The system has no way to prioritize one over the other and ends up with mediocre recommendations across the board.

Features are scored independently, so the system misses the meaning that comes from combinations. High energy combined with high acousticness usually means a live performance recording, but the system just sees two separate numbers rather than understanding that relationship.

---

## Reflection

[**Model Card**](model_card.md)

Building this system changed how I think about apps like Spotify. Before this project I assumed those systems were reading my mind somehow. Now I understand they are doing something much more concrete: turning listening behavior and song properties into numbers and doing math. The result feels like magic, but the underlying logic is really just careful feature design and scale.

What surprised me most was how much a single number in the code, the genre weight of 2.0, shaped the entire personality of the recommender. That one value decided which profile types would get great recommendations and which would get mediocre ones. Real systems make those choices constantly in ways users never see, and I now understand that every recommender reflects the values of whoever built it. Weighting genre heavily is saying genre is the most important thing about a song. That is not a neutral choice.

I also discovered how easy it is to accidentally create a filter bubble. My system kept recommending the same few songs to similar profiles, not by design, but just because the scoring math kept rewarding the same winners. Fixing that would mean deliberately introducing diversity and accepting slightly worse average accuracy in return, which is a real tradeoff that production systems have to make consciously.


---

## 7. Model Card

### Model Name

VibeFinder 1.0

---

### Intended Use

VibeFinder 1.0 is a small music recommender designed to suggest songs from a fixed catalog based on a user's taste preferences. It is built for classroom exploration and is not intended for real-world use. The system assumes the user knows their own preferences ahead of time, such as a favorite genre, a preferred mood, and how energetic or acoustic they want their music to feel. It does not learn from listening history or track what you skip. Every recommendation is generated fresh each time you run it, based only on the preferences you provide.

---

### How the Model Works

The system works by comparing a user's preferences to every song in the catalog and giving each song a compatibility score. Think of it like a checklist. If a song's genre matches what you prefer, it gets a big bonus right away. If the mood also matches, it gets another bonus. Then the system looks at numbers, things like how energetic the song is, how upbeat it sounds, how danceable it is, and how acoustic or electronic it feels. For each of those, the closer the song's value is to what the user wants, the higher the score it receives. Songs that are far away from the user's preferences score low on those features. Once every song has a score, the system sorts them from highest to lowest and returns the top five. The key idea is that the system rewards closeness. A song does not get a better score just for being loud or fast. It gets a better score for being close to what you said you like.

---

### Data

The catalog contains 20 songs stored in a CSV file called songs.csv. The original dataset had 10 songs, and 10 more were added to increase genre and mood variety. The catalog now includes pop, lofi, rock, ambient, jazz, synthwave, indie pop, EDM, R&B, metal, country, k-pop, reggae, classical, hip-hop, indie rock, and more. Moods in the dataset include happy, chill, intense, focused, relaxed, moody, euphoric, melancholic, aggressive, nostalgic, romantic, and dark. The dataset is very small, which means users with niche or uncommon tastes will often find that the catalog has few or no songs that genuinely match their preferences. The data also reflects a somewhat Western and English-language bias, since most artist names and song titles follow that style. There is only one k-pop song and one classical song, which means those users will get weaker recommendations than pop or lofi users.

---

### Strengths

The system works best when the user's preferred genre is well represented in the catalog. For example, a lofi listener will almost always receive Library Rain and Midnight Coding at the top, which is exactly what a human would expect. The scoring logic is fully transparent, meaning every recommendation comes with a plain list of reasons explaining exactly why that song was chosen. This makes the system easy to understand and easy to debug. It also works well for users with consistent preferences, where all their feature values point in the same direction, such as wanting high energy, fast tempo, high danceability, and a happy mood all at once. In those cases the system confidently separates good matches from bad ones.

---

### Limitations and Bias

The biggest limitation I discovered is that genre has far too much influence over the final result. Because a genre match adds 2.0 points automatically, a song that perfectly matches the user's energy, mood, tempo, and vibe but belongs to a slightly different genre will almost always lose to a weaker song that just happens to share the same genre label. For example, an indie pop song and a pop song might sound nearly identical, but the system treats them as completely unrelated because their genre strings do not match exactly.

The catalog is also too small to serve users with rare preferences. A user who prefers classical music only has one song to match against, which means the rest of the top five recommendations are filled with songs from completely unrelated genres that just happened to score well on numerical features like energy and acousticness.

The scoring system treats all features as independent of each other. In real music, features interact. A very high energy song that is also very acoustic usually means it is a live performance, which has a completely different feel than a quiet studio recording. The system cannot detect that kind of combination. It scores energy and acousticness separately, so the combined meaning is lost.

Finally, users with conflicting preferences, like wanting very high energy but also a deeply melancholic mood, will always get mediocre scores across the board. No song in the catalog was designed for that combination, so the system ends up recommending songs that partially satisfy one preference while missing the other completely.

---

### Evaluation

I tested six user profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, Conflicted Energy, All-Low or Dark, and K-Pop Aggressive.

The Chill Lofi profile gave the most satisfying results. Library Rain ranked first because its energy value of 0.35 was a perfect match to the user preference of 0.35, and its acousticness of 0.86 was very close to the preferred 0.80. It also matched on both genre and mood, which added the full 3.0 bonus points. The second result was Midnight Coding, which was also a lofi chill song but slightly less close in energy and acousticness. That ordering felt completely right.

The most surprising result came from the Conflicted Energy profile, which asked for ambient genre, melancholic mood, but also 0.95 energy and 0.90 danceability. No song in the catalog fits all of those at once. The top recommendations ended up being songs that scored well on the numerical features like energy and danceability but had no mood or genre match at all. The system essentially gave up on the categorical preferences and fell back to numerical similarity. That was revealing because it showed the system has no way to handle contradictions. It just averages everything out and picks whatever survives.

The K-Pop Aggressive profile was also interesting. The system found the one k-pop song in the catalog and gave it the genre bonus, but no song had an aggressive mood, so the mood bonus was never awarded to anyone. That meant the genre match alone pushed Hangang Evening to the top even though its mood is romantic and the user wanted aggressive. A human would never make that recommendation.

---

### Future Work

The most impactful improvement would be to lower the genre weight and replace strict genre matching with a genre similarity group. For example, pop, indie pop, and k-pop could all be considered close to each other, earning partial credit instead of zero. This would make the system less brittle and more forgiving of small label differences that do not reflect real differences in sound.

Adding more songs to the catalog would also help significantly. With only 20 songs, many user profiles have only one or two real matches, and the rest of the recommendations are just the least-bad options. A catalog of at least 100 songs would allow the scoring differences to actually mean something.

I would also like to add a diversity filter so that the top five recommendations are not all from the same genre or the same artist. Right now if you ask for lofi, you get three or four lofi songs in a row. Real recommenders try to balance familiarity with discovery, and this system currently does not do that at all.

---

### Personal Reflection

Building this system changed how I think about apps like Spotify. Before this project I assumed those systems were just reading my mind somehow. Now I understand that they are doing something much more concrete. They are turning your behavior and the properties of songs into numbers and then doing math. The magic is really just careful feature engineering and scale.

What surprised me most was how much a single design choice, like setting genre weight to 2.0, could shape the entire personality of the recommender. A small number in the code ended up being the most influential decision in the whole system. That made me realize that every recommender system reflects the values and priorities of whoever built it. If you weight genre heavily, you are saying that genre is the most important thing about a song. If you weight energy heavily, you are saying the vibe matters more than the label. Those are not neutral choices, and real systems make them constantly in ways that most users never see.

I also learned that the concept of a filter bubble is very real and easy to create accidentally. My system naturally kept recommending the same few songs to similar profiles, not because I designed it that way, but just because the scoring math rewarded the same winners over and over. Solving that problem in a real system would require deliberately introducing randomness or diversity, which means accepting slightly worse average accuracy in exchange for a wider range of discoveries. That tradeoff felt meaningful to me.
