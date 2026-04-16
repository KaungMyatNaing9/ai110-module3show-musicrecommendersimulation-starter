# Music Recommender System — Flowchart

```mermaid
flowchart TD
    A([User Profile\npreferred_genre · preferred_mood\npreferred_energy · preferred_tempo\npreferred_valence · preferred_danceability · preferred_acousticness])
    --> B[Load songs.csv catalog]

    B --> C{For each song in catalog}

    C --> D{"genre ==\npreferred_genre?"}
    D -- Yes --> E[+2.0 pts]
    D -- No  --> F[+0.0 pts]
    E & F --> G{"mood ==\npreferred_mood?"}

    G -- Yes --> H[+1.5 pts]
    G -- No  --> I[+0.0 pts]
    H & I --> J["energy similarity\n1 - |song - user| / 1.0\n× weight 1.0"]

    J --> K["valence similarity\n1 - |song - user| / 1.0\n× weight 1.0"]
    K --> L["danceability similarity\n1 - |song - user| / 1.0\n× weight 0.75"]
    L --> M["tempo similarity\n1 - |song - user| / 120\n× weight 0.75"]
    M --> N["acousticness similarity\n1 - |song - user| / 1.0\n× weight 0.5"]

    N --> O["Sum all scores\nnormalize ÷ 7.5\n→ final score 0.0–1.0"]
    O --> P[(Scored Songs List)]

    C -- next song --> D

    P --> Q["Sort by score\ndescending"]
    Q --> R([Return Top K Songs\nas Recommendations])
```

## Notes

- **Max possible score before normalization:** 7.5
- **Categorical features** (genre, mood) are binary: full weight or zero.
- **Numerical features** use distance-based similarity — closer to user preference = higher score.
- **Tempo max range** is 120 (covers the realistic 60–180 BPM span).
- **K** is a configurable parameter (default: top 3 or top 5 recommendations).
