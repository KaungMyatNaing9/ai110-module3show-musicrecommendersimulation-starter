# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeFinder 1.0

---

## 2. Intended Use

VibeFinder 1.0 is a small music recommender designed to suggest songs from a fixed catalog based on a user's taste preferences. It is built for classroom exploration and is not intended for real-world use. The system assumes the user knows their own preferences ahead of time, such as a favorite genre, a preferred mood, and how energetic or acoustic they want their music to feel. It does not learn from listening history or track what you skip. Every recommendation is generated fresh each time you run it, based only on the preferences you provide.

---

## 3. How the Model Works

The system works by comparing a user's preferences to every song in the catalog and giving each song a compatibility score. Think of it like a checklist. If a song's genre matches what you prefer, it gets a big bonus right away. If the mood also matches, it gets another bonus. Then the system looks at numbers, things like how energetic the song is, how upbeat it sounds, how danceable it is, and how acoustic or electronic it feels. For each of those, the closer the song's value is to what the user wants, the higher the score it receives. Songs that are far away from the user's preferences score low on those features. Once every song has a score, the system sorts them from highest to lowest and returns the top five. The key idea is that the system rewards closeness. A song does not get a better score just for being loud or fast. It gets a better score for being close to what you said you like.

---

## 4. Data

The catalog contains 20 songs stored in a CSV file called songs.csv. The original dataset had 10 songs, and 10 more were added to increase genre and mood variety. The catalog now includes pop, lofi, rock, ambient, jazz, synthwave, indie pop, EDM, R&B, metal, country, k-pop, reggae, classical, hip-hop, indie rock, and more. Moods in the dataset include happy, chill, intense, focused, relaxed, moody, euphoric, melancholic, aggressive, nostalgic, romantic, and dark. The dataset is very small, which means users with niche or uncommon tastes will often find that the catalog has few or no songs that genuinely match their preferences. The data also reflects a somewhat Western and English-language bias, since most artist names and song titles follow that style. There is only one k-pop song and one classical song, which means those users will get weaker recommendations than pop or lofi users.

---

## 5. Strengths

The system works best when the user's preferred genre is well represented in the catalog. For example, a lofi listener will almost always receive Library Rain and Midnight Coding at the top, which is exactly what a human would expect. The scoring logic is fully transparent, meaning every recommendation comes with a plain list of reasons explaining exactly why that song was chosen. This makes the system easy to understand and easy to debug. It also works well for users with consistent preferences, where all their feature values point in the same direction, such as wanting high energy, fast tempo, high danceability, and a happy mood all at once. In those cases the system confidently separates good matches from bad ones.

---

## 6. Limitations and Bias

The biggest limitation I discovered is that genre has far too much influence over the final result. Because a genre match adds 2.0 points automatically, a song that perfectly matches the user's energy, mood, tempo, and vibe but belongs to a slightly different genre will almost always lose to a weaker song that just happens to share the same genre label. For example, an indie pop song and a pop song might sound nearly identical, but the system treats them as completely unrelated because their genre strings do not match exactly.

The catalog is also too small to serve users with rare preferences. A user who prefers classical music only has one song to match against, which means the rest of the top five recommendations are filled with songs from completely unrelated genres that just happened to score well on numerical features like energy and acousticness.

The scoring system treats all features as independent of each other. In real music, features interact. A very high energy song that is also very acoustic usually means it is a live performance, which has a completely different feel than a quiet studio recording. The system cannot detect that kind of combination. It scores energy and acousticness separately, so the combined meaning is lost.

Finally, users with conflicting preferences, like wanting very high energy but also a deeply melancholic mood, will always get mediocre scores across the board. No song in the catalog was designed for that combination, so the system ends up recommending songs that partially satisfy one preference while missing the other completely.

---

## 7. Evaluation

I tested six user profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, Conflicted Energy, All-Low or Dark, and K-Pop Aggressive.

The Chill Lofi profile gave the most satisfying results. Library Rain ranked first because its energy value of 0.35 was a perfect match to the user preference of 0.35, and its acousticness of 0.86 was very close to the preferred 0.80. It also matched on both genre and mood, which added the full 3.0 bonus points. The second result was Midnight Coding, which was also a lofi chill song but slightly less close in energy and acousticness. That ordering felt completely right.

The most surprising result came from the Conflicted Energy profile, which asked for ambient genre, melancholic mood, but also 0.95 energy and 0.90 danceability. No song in the catalog fits all of those at once. The top recommendations ended up being songs that scored well on the numerical features like energy and danceability but had no mood or genre match at all. The system essentially gave up on the categorical preferences and fell back to numerical similarity. That was revealing because it showed the system has no way to handle contradictions. It just averages everything out and picks whatever survives.

The K-Pop Aggressive profile was also interesting. The system found the one k-pop song in the catalog and gave it the genre bonus, but no song had an aggressive mood, so the mood bonus was never awarded to anyone. That meant the genre match alone pushed Hangang Evening to the top even though its mood is romantic and the user wanted aggressive. A human would never make that recommendation.

I also ran an informal weight shift experiment. I reasoned through what would happen if the genre weight was halved from 2.0 to 1.0 and the energy weight was doubled from 1.0 to 2.0. In that scenario, a song with near-perfect energy alignment would gain as much as a genre match, which would help cross-genre recommendations rise in the rankings. For a High-Energy Pop user, songs like Neon Babylon from EDM and Gym Hero from pop would compete more evenly, since both have very high energy. The tradeoff is that the system becomes less sure about style, since energy alone does not tell you very much about whether a song actually sounds like pop or not.

---

## 8. Future Work

The most impactful improvement would be to lower the genre weight and replace strict genre matching with a genre similarity group. For example, pop, indie pop, and k-pop could all be considered close to each other, earning partial credit instead of zero. This would make the system less brittle and more forgiving of small label differences that do not reflect real differences in sound.

Adding more songs to the catalog would also help significantly. With only 20 songs, many user profiles have only one or two real matches, and the rest of the recommendations are just the least-bad options. A catalog of at least 100 songs would allow the scoring differences to actually mean something.

I would also like to add a diversity filter so that the top five recommendations are not all from the same genre or the same artist. Right now if you ask for lofi, you get three or four lofi songs in a row. Real recommenders try to balance familiarity with discovery, and this system currently does not do that at all.

---

## 9. Personal Reflection

Building this system changed how I think about apps like Spotify. Before this project I assumed those systems were just reading my mind somehow. Now I understand that they are doing something much more concrete. They are turning your behavior and the properties of songs into numbers and then doing math. The magic is really just careful feature engineering and scale.

What surprised me most was how much a single design choice, like setting genre weight to 2.0, could shape the entire personality of the recommender. A small number in the code ended up being the most influential decision in the whole system. That made me realize that every recommender system reflects the values and priorities of whoever built it. If you weight genre heavily, you are saying that genre is the most important thing about a song. If you weight energy heavily, you are saying the vibe matters more than the label. Those are not neutral choices, and real systems make them constantly in ways that most users never see.

I also learned that the concept of a filter bubble is very real and easy to create accidentally. My system naturally kept recommending the same few songs to similar profiles, not because I designed it that way, but just because the scoring math rewarded the same winners over and over. Solving that problem in a real system would require deliberately introducing randomness or diversity, which means accepting slightly worse average accuracy in exchange for a wider range of discoveries. That tradeoff felt meaningful to me.
