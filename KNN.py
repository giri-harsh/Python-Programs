# %%
import pandas as pd
import numpy as np
from collections import Counter

# %%
df = pd.read_csv(r"C:\Work\Programing Language\task4\Game-Recommendation-System\data\raw\rawg_games_20k.csv")

# Keep only required columns
df_clean = df[['id', 'name', 'platforms', 'genres', 'tags']].copy()

# Remove rows with missing values in critical columns
df_clean = df_clean.dropna(subset=['platforms', 'genres', 'tags'])


# %%
print(f"Total games after cleaning: {len(df_clean)}")
print(f"\nFirst 5 rows:")
df_clean.head()


# %%
df_clean['platforms_list'] = df_clean['platforms'].str.split('|')
df_clean['genres_list'] = df_clean['genres'].str.split('|')
df_clean['tags_list'] = df_clean['tags'].str.split('|')

print("\nExample of split values:")
print(f"Game: {df_clean.iloc[0]['name']}")
print(f"Platforms: {df_clean.iloc[0]['platforms_list']}")
print(f"Genres: {df_clean.iloc[0]['genres_list']}")
print(f"Tags (first 5): {df_clean.iloc[0]['tags_list'][:5]}")


# %%
all_genres = []
for genres in df_clean['genres_list']:
    all_genres.extend(genres)
genre_counts = Counter(all_genres)
print(f"\nTotal unique genres: {len(genre_counts)}")
print(f"All genres: {list(genre_counts.keys())}")

# Count all platforms
all_platforms = []
for platforms in df_clean['platforms_list']:
    all_platforms.extend(platforms)
platform_counts = Counter(all_platforms)
print(f"\nTotal unique platforms: {len(platform_counts)}")
print(f"All platforms: {list(platform_counts.keys())}")

# Count all tags and select top 75
all_tags = []
for tags in df_clean['tags_list']:
    all_tags.extend(tags)
tag_counts = Counter(all_tags)

print(f"\nTotal unique tags: {len(tag_counts)}")
print(f"Selecting top 75 most frequent tags...")

# Get top 75 tags
top_75_tags = [tag for tag, count in tag_counts.most_common(75)]

print(f"\nTop 20 most frequent tags:")
for i, (tag, count) in enumerate(tag_counts.most_common(20), 1):
    print(f"{i:2d}. {tag:30s} - appears in {count:4d} games")

# ============================================
# STEP 4: CREATE BINARY COLUMNS

# %%
# ============================================
# STEP 4: CREATE BINARY COLUMNS (OPTIMIZED)
# ============================================
print("\n" + "=" * 60)
print("STEP 4: CREATING BINARY FEATURE COLUMNS")
print("=" * 60)

# Start with id and name
df_encoded = df_clean[['id', 'name']].copy()

# Create all binary columns at once using dictionaries (MUCH FASTER!)
all_binary_cols = {}

# Create binary columns for GENRES
print("\nCreating genre columns...")
for genre in sorted(genre_counts.keys()):
    col_name = f'genre_{genre.replace(" ", "_").replace("-", "_")}'
    all_binary_cols[col_name] = df_clean['genres_list'].apply(
        lambda x: 1 if genre in x else 0
    )

# Create binary columns for PLATFORMS
print("Creating platform columns...")
for platform in sorted(platform_counts.keys()):
    col_name = f'platform_{platform.replace(" ", "_").replace("/", "_").replace("-", "_")}'
    all_binary_cols[col_name] = df_clean['platforms_list'].apply(
        lambda x: 1 if platform in x else 0
    )

# Create binary columns for TOP 75 TAGS
print("Creating tag columns (top 75 only)...")
for tag in sorted(top_75_tags):
    # Clean the tag name for column naming
    col_name = tag.replace(" ", "_").replace("-", "_").replace("'", "").replace("/", "_").replace("&", "and")
    col_name = f'tag_{col_name}'
    all_binary_cols[col_name] = df_clean['tags_list'].apply(
        lambda x: 1 if tag in x else 0
    )

# Concatenate all columns at once (FAST!)
print("\nCombining all feature columns...")
df_binary = pd.DataFrame(all_binary_cols)
df_encoded = pd.concat([df_encoded, df_binary], axis=1)

# %%
# ============================================
# STEP 5: BUILD FINAL DATASET
# ============================================
print("\n" + "=" * 60)
print("STEP 5: FINAL DATASET SUMMARY")
print("=" * 60)

print(f"\nFinal dataset shape: {df_encoded.shape}")
print(f"Total columns: {len(df_encoded.columns)}")
print(f"  - ID and Name: 2 columns")
print(f"  - Genre features: {len([c for c in df_encoded.columns if c.startswith('genre_')])} columns")
print(f"  - Platform features: {len([c for c in df_encoded.columns if c.startswith('platform_')])} columns")
print(f"  - Tag features: {len([c for c in df_encoded.columns if c.startswith('tag_')])} columns")

print(f"\nFirst 3 games with their encoded features:")
print(df_encoded.head(3))

# Save the processed dataset
output_file = 'games_encoded_for_knn.csv'
df_encoded.to_csv(output_file, index=False)
print(f"\n✓ Encoded dataset saved to: {output_file}")

# ============================================
# BONUS: FEATURE STATISTICS
# ============================================
print("\n" + "=" * 60)
print("FEATURE STATISTICS")
print("=" * 60)

# Get feature columns only (exclude id and name)
feature_cols = [col for col in df_encoded.columns if col not in ['id', 'name']]

# Calculate statistics
feature_sums = df_encoded[feature_cols].sum()
print(f"\nMost common features across all games:")
print(feature_sums.sort_values(ascending=False).head(10))

# Example: Show encoding for a specific game
print("\n" + "=" * 60)
print("EXAMPLE: ENCODED FEATURES FOR 'Grand Theft Auto V'")
print("=" * 60)

gta_row = df_encoded[df_encoded['name'] == 'Grand Theft Auto V']
if not gta_row.empty:
    active_features = []
    for col in feature_cols:
        if gta_row[col].values[0] == 1:
            active_features.append(col)

    print(f"\nActive features (value = 1) for GTA V:")
    for feat in active_features:
        print(f"  • {feat}")

print("\n" + "=" * 60)
print("✓ PREPROCESSING COMPLETE!")
print("=" * 60)
print(f"\nYour dataset is ready for KNN training!")
print(f"Next steps:")
print(f"1. Load '{output_file}'")
print(f"2. Separate features (all columns except 'id' and 'name')")
print(f"3. Train KNN model using these binary features")
print(f"4. Use game 'name' or 'id' for recommendations")

# %%
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import normalize

# ============================================
# STEP 1: LOAD THE ENCODED DATASET
# ============================================
print("=" * 60)
print("LOADING ENCODED DATASET FOR KNN TRAINING")
print("=" * 60)

# Load the preprocessed data
df = pd.read_csv('games_encoded_for_knn.csv')

print(f"\nDataset loaded successfully!")
print(f"Total games: {len(df)}")
print(f"Total columns: {len(df.columns)}")



# %%
# ============================================
# STEP 2: PREPARE FEATURES FOR KNN
# ============================================
print("\n" + "=" * 60)
print("PREPARING FEATURES FOR KNN")
print("=" * 60)

# Separate features from game info
game_info = df[['id', 'name']].copy()
feature_columns = [col for col in df.columns if col not in ['id', 'name']]

# Extract feature matrix
X = df[feature_columns].values

print(f"\nFeature matrix shape: {X.shape}")
print(f"Features being used: {len(feature_columns)}")
print(f"\nFeature breakdown:")
print(f"  - Genre features: {len([c for c in feature_columns if c.startswith('genre_')])}")
print(f"  - Platform features: {len([c for c in feature_columns if c.startswith('platform_')])}")
print(f"  - Tag features: {len([c for c in feature_columns if c.startswith('tag_')])}")

# Normalize features for better cosine similarity
# (optional but recommended for binary features)
X_normalized = normalize(X, norm='l2')

print("\n✓ Features normalized for cosine similarity")


# %%
# STEP 3: TRAIN KNN MODEL
# ============================================
print("\n" + "=" * 60)
print("TRAINING KNN MODEL WITH COSINE SIMILARITY")
print("=" * 60)

# Initialize KNN with cosine similarity
# n_neighbors = number of similar games to find + 1 (the game itself)
knn_model = NearestNeighbors(
    n_neighbors=11,  # Find 10 similar games + the query game itself
    metric='cosine',
    algorithm='brute',  # Best for cosine similarity
    n_jobs=-1  # Use all CPU cores
)

# Fit the model
print("\nTraining KNN model...")
knn_model.fit(X_normalized)

print("✓ KNN model trained successfully!")

# %%
# ============================================
# STEP 4: RECOMMENDATION FUNCTION
# ============================================
print("\n" + "=" * 60)
print("CREATING RECOMMENDATION FUNCTION")
print("=" * 60)

def recommend_games(game_name, n_recommendations=10):
    """
    Recommend similar games based on a game name

    Parameters:
    - game_name: Name of the game (case-insensitive, partial match supported)
    - n_recommendations: Number of games to recommend (default: 10)

    Returns:
    - DataFrame with recommended games and similarity scores
    """

    # Find the game in the dataset (case-insensitive, partial match)
    game_matches = game_info[game_info['name'].str.contains(game_name, case=False, na=False)]

    if len(game_matches) == 0:
        print(f"❌ Game '{game_name}' not found in dataset!")
        print("\nDid you mean one of these?")
        # Show similar game names
        similar_names = game_info[game_info['name'].str.contains(game_name.split()[0], case=False, na=False)]['name'].head(5)
        for name in similar_names:
            print(f"  - {name}")
        return None

    # If multiple matches, use the first one
    if len(game_matches) > 1:
        print(f"⚠ Multiple matches found. Using: '{game_matches.iloc[0]['name']}'")
        print(f"Other matches: {list(game_matches['name'].values[1:])}\n")

    game_idx = game_matches.index[0]
    game_name_exact = game_matches.iloc[0]['name']

    # Get the feature vector for this game
    game_features = X_normalized[game_idx].reshape(1, -1)

    # Find nearest neighbors
    distances, indices = knn_model.kneighbors(game_features, n_neighbors=n_recommendations+1)

    # Prepare results (exclude the game itself)
    results = []
    for i in range(1, len(indices[0])):  # Skip index 0 (the game itself)
        idx = indices[0][i]
        distance = distances[0][i]
        similarity = 1 - distance  # Convert distance to similarity score

        results.append({
            'Rank': i,
            'Game': game_info.iloc[idx]['name'],
            'Similarity': round(similarity * 100, 2)  # Convert to percentage
        })

    results_df = pd.DataFrame(results)

    # Display results
    print("=" * 80)
    print(f"🎮 GAMES SIMILAR TO: {game_name_exact}")
    print("=" * 80)
    print(results_df.to_string(index=False))
    print("=" * 80)

    return results_df


def recommend_by_features(platforms=None, genres=None, tags=None, n_recommendations=10):
    """
    Recommend games based on desired features (platforms, genres, tags)

    Parameters:
    - platforms: List of platforms (e.g., ['PC', 'PlayStation 5'])
    - genres: List of genres (e.g., ['Action', 'RPG'])
    - tags: List of tags (e.g., ['Singleplayer', 'Open World'])
    - n_recommendations: Number of games to recommend

    Returns:
    - DataFrame with recommended games
    """

    # Create a custom feature vector
    custom_features = np.zeros(X.shape[1])

    if platforms:
        for platform in platforms:
            col_name = f'platform_{platform.replace(" ", "_").replace("/", "_").replace("-", "_")}'
            if col_name in feature_columns:
                col_idx = feature_columns.index(col_name)
                custom_features[col_idx] = 1

    if genres:
        for genre in genres:
            col_name = f'genre_{genre.replace(" ", "_").replace("-", "_")}'
            if col_name in feature_columns:
                col_idx = feature_columns.index(col_name)
                custom_features[col_idx] = 1

    if tags:
        for tag in tags:
            # Clean tag name for column matching
            clean_tag = tag.replace(" ", "_").replace("-", "_").replace("'", "").replace("/", "_").replace("&", "and")
            col_name = f'tag_{clean_tag}'
            if col_name in feature_columns:
                col_idx = feature_columns.index(col_name)
                custom_features[col_idx] = 1

    # Normalize the custom feature vector
    custom_features_normalized = normalize(custom_features.reshape(1, -1), norm='l2')

    # Find nearest neighbors
    distances, indices = knn_model.kneighbors(custom_features_normalized, n_neighbors=n_recommendations)

    # Prepare results
    results = []
    for i in range(len(indices[0])):
        idx = indices[0][i]
        distance = distances[0][i]
        similarity = 1 - distance

        results.append({
            'Rank': i + 1,
            'Game': game_info.iloc[idx]['name'],
            'Similarity': round(similarity * 100, 2)
        })

    results_df = pd.DataFrame(results)

    # Display results
    print("=" * 80)
    print(f"🎮 RECOMMENDED GAMES FOR YOUR PREFERENCES")
    print("=" * 80)
    if platforms:
        print(f"Platforms: {', '.join(platforms)}")
    if genres:
        print(f"Genres: {', '.join(genres)}")
    if tags:
        print(f"Tags: {', '.join(tags)}")
    print("-" * 80)
    print(results_df.to_string(index=False))
    print("=" * 80)

    return results_df

print("✓ Recommendation functions created successfully!")


# %%
# ============================================
# STEP 5: TEST THE RECOMMENDER
# ============================================
print("\n" + "=" * 60)
print("TESTING THE RECOMMENDATION SYSTEM")
print("=" * 60)

# Test 1: Recommend games similar to GTA V
print("\n🎮 TEST 1: Find games similar to 'Grand Theft Auto V'")
print("-" * 60)
recommendations = recommend_games('Grand Theft Auto V', n_recommendations=10)

# Test 2: Recommend games similar to The Witcher 3
print("\n\n🎮 TEST 2: Find games similar to 'The Witcher 3'")
print("-" * 60)
recommendations = recommend_games('Witcher 3', n_recommendations=10)

# Test 3: Recommend games by features
print("\n\n🎮 TEST 3: Recommend PC RPG games with Open World and Singleplayer")
print("-" * 60)
recommendations = recommend_by_features(
    platforms=['PC'],
    genres=['RPG', 'Action'],
    tags=['Singleplayer', 'Open World'],
    n_recommendations=10
)

# %%



