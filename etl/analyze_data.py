"""
Data analysis script to understand cleaning requirements
"""
import pandas as pd
import os

# Load data
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(script_dir, 'data', 'raw', 'NBA_Player_Totals.csv')
df = pd.read_csv(csv_path)

print("="*70)
print("NBA DATA ANALYSIS")
print("="*70)

# Basic info
print(f"\nTotal rows: {len(df):,}")
print(f"Total columns: {len(df.columns)}")
print(f"Date range: {df['season'].min()} - {df['season'].max()}")

# 1. PLAYER NAME DUPLICATES
print("\n" + "="*70)
print("1. PLAYER NAME DUPLICATES (Top 10)")
print("="*70)
dupes = df.groupby('player')['player_id'].nunique()
dupes_multi = dupes[dupes > 1].sort_values(ascending=False).head(10)
print(dupes_multi)
print(f"\nPlayers with multiple IDs: {(dupes > 1).sum()}")

# Show example
if len(dupes_multi) > 0:
    example_player = dupes_multi.index[0]
    print(f"\nExample: {example_player}")
    print(df[df['player'] == example_player][['player', 'player_id', 'season', 'tm']].head(10))

# 2. POSITION ANALYSIS
print("\n" + "="*70)
print("2. POSITION ANALYSIS")
print("="*70)
pos_counts = df['pos'].value_counts().sort_index()
print(f"\nTotal unique positions: {df['pos'].nunique()}")
print("\nPosition breakdown:")
print(pos_counts)

# Categorize positions
print("\nPosition categories:")
guards = pos_counts[pos_counts.index.str.contains('G', na=False)]
forwards = pos_counts[pos_counts.index.str.contains('F', na=False)]
centers = pos_counts[pos_counts.index.str.contains('C', na=False)]
print(f"  Guard-related: {len(guards)} variations, {guards.sum():,} players")
print(f"  Forward-related: {len(forwards)} variations, {forwards.sum():,} players")
print(f"  Center-related: {len(centers)} variations, {centers.sum():,} players")

# 3. TEAM 'TOT' ANALYSIS
print("\n" + "="*70)
print("3. TEAM 'TOT' ANALYSIS")
print("="*70)
tot_count = (df['tm'] == 'TOT').sum()
print(f"Rows with TOT: {tot_count:,}")
print(f"Percentage of data: {tot_count/len(df)*100:.1f}%")

# Show example of traded player
tot_players = df[df['tm'] == 'TOT']['player'].unique()[:3]
print(f"\nExample traded players:")
for player in tot_players:
    player_data = df[df['player'] == player].sort_values('season').tail(5)
    print(f"\n{player}:")
    print(player_data[['season', 'tm', 'g', 'pts']].to_string(index=False))

# 4. MISSING VALUES
print("\n" + "="*70)
print("4. MISSING VALUES")
print("="*70)
missing = df.isnull().sum()
missing = missing[missing > 0].sort_values(ascending=False)
if len(missing) > 0:
    print(missing)
else:
    print("No NULL values found")

# Check for 'NA' strings
na_strings = (df == 'NA').sum()
na_strings = na_strings[na_strings > 0].sort_values(ascending=False)
if len(na_strings) > 0:
    print("\n'NA' string values:")
    print(na_strings)

print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)
