from preswald import connect, get_df, query, table, text, slider, plotly, selectbox, checkbox
import plotly.express as px

# Connect to the data source and load the Pokémon dataset
connect()
df = get_df('Pokemon_csv')

# Define strengths and weaknesses for each Pokémon type
pokemon_type_strengths_weaknesses = pokemon_type_strengths_weaknesses = {
    "Bug": {
        "strong_against": "Psychic, Dark",
        "weak_against": "Fire, Flying, Rock"
    },
    "Dark": {
        "strong_against": "Psychic, Ghost",
        "weak_against": "Fighting, Fairy, Bug"
    },
    "Dragon": {
        "strong_against": "Dragon",
        "weak_against": "Ice, Fairy, Steel"
    },
    "Electric": {
        "strong_against": "Water, Flying",
        "weak_against": "Ground, Dragon"
    },
    "Fairy": {
        "strong_against": "Dragon, Dark, Fighting",
        "weak_against": "Steel, Poison"
    },
    "Fighting": {
        "strong_against": "Normal, Rock, Steel, Ice, Dark",
        "weak_against": "Psychic, Flying, Fairy"
    },
    "Fire": {
        "strong_against": "Bug, Grass, Ice, Steel",
        "weak_against": "Water, Rock, Ground"
    },
    "Flying": {
        "strong_against": "Bug, Fighting, Grass",
        "weak_against": "Electric, Ice, Rock"
    },
    "Ghost": {
        "strong_against": "Psychic, Ghost",
        "weak_against": "Dark, Normal"
    },
    "Grass": {
        "strong_against": "Water, Ground, Rock",
        "weak_against": "Fire, Flying, Bug, Ice"
    },
    "Ground": {
        "strong_against": "Fire, Electric, Poison, Rock, Steel",
        "weak_against": "Water, Ice, Grass"
    },
    "Ice": {
        "strong_against": "Dragon, Flying, Grass, Ground",
        "weak_against": "Fire, Fighting, Rock, Steel"
    },
    "Normal": {
        "strong_against": "",
        "weak_against": "Fighting"
    },
    "Poison": {
        "strong_against": "Fairy, Grass",
        "weak_against": "Ground, Psychic"
    },
    "Psychic": {
        "strong_against": "Fighting, Poison",
        "weak_against": "Bug, Ghost, Dark"
    },
    "Rock": {
        "strong_against": "Bug, Flying, Fire, Ice",
        "weak_against": "Water, Ground, Steel"
    },
    "Steel": {
        "strong_against": "Fairy, Ice, Rock",
        "weak_against": "Fire, Fighting, Ground"
    },
    "Water": {
        "strong_against": "Fire, Ground, Rock",
        "weak_against": "Electric, Grass"
    }
}

# 🔷 Header and type selector
text(f"# Learn about Pokemon by Types")
text(f"## Choose the Pokemon Type you want to learn about: ")

# 🎯 Let the user choose a Pokémon type to explore
choice = selectbox(
    label="Choose Pokemon Type",
    options = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"]
)

# 🔍 Filter the dataset to include Pokémon with the selected type
pokemons_with_type = df[(df["Type 1"] == choice) | (df["Type 2"] == choice)]

# 📊 Calculate average base stats and count values
avg_hp = pokemons_with_type["HP"].mean()
avg_attack = pokemons_with_type["Attack"].mean()
avg_defense = pokemons_with_type["Defense"].mean()
avg_sp_atk = pokemons_with_type["Sp. Atk"].mean()
avg_sp_def = pokemons_with_type["Sp. Def"].mean()
avg_speed = pokemons_with_type["Speed"].mean()
avg_total = pokemons_with_type["Total"].mean()
count = pokemons_with_type.shape[0]
count_lengendary = pokemons_with_type[(pokemons_with_type['Legendary'] == True)].shape[0]

# 📘 Display strengths, weaknesses, and stat summaries
text(f"## {choice} Type's General Data")
text(f"### 🔥 {choice} Type is strong against: {pokemon_type_strengths_weaknesses[choice]['strong_against']}")
text(f"### 🧊 {choice} Type is weak against: {pokemon_type_strengths_weaknesses[choice]['weak_against']}")
text(f"### ❤️ Average HP: {avg_hp:.2f}")
text(f"### 💪 Average Attack: {avg_attack:.2f}")
text(f"### 🛡️ Average Defense: {avg_defense:.2f}")
text(f"### 🔮 Average Special Attack: {avg_sp_atk:.2f}")
text(f"### 🧠 Average Special Defense: {avg_sp_def:.2f}")
text(f"### ⚡ Average Speed: {avg_speed:.2f}")
text(f"### 📊 Average Total Stats: {avg_total:.2f}")

# 🥇 Show count of legendary Pokémon for this type
text(f"### Out of {count} pokemons with type {choice}, there are {count_lengendary} legendary pokemons.")
legendary_counts = pokemons_with_type["Legendary"].value_counts().reset_index()
legendary_counts.columns = ["Legendary", "Count"]
fig_pie = px.pie(legendary_counts, names="Legendary", values="Count", title="Legendary vs Non-Legendary")
plotly(fig_pie)

# 📈 Scatter plot for total stat distribution
text(f"## {choice} Pokemon Total Stat's distribution")
fig = px.scatter(pokemons_with_type, x="Name", y="Total", labels={"x": "X-axis", "y": "Y-axis"})
plotly(fig)

# 📊 Bar chart for most common secondary typings
text(f"## {choice} Pokemons' Most Common Secondary Types")

# Get secondary types when the selected type is primary
secondary_types = pokemons_with_type[
    (pokemons_with_type["Type 1"] == choice)
]["Type 2"].dropna().value_counts()

# Get secondary types when the selected type is secondary
secondary_types_alt = pokemons_with_type[
    (pokemons_with_type["Type 2"] == choice)
]["Type 1"].dropna().value_counts()

# 🔄 Combine counts from both primary and secondary slots
combined_secondary_types = secondary_types.add(secondary_types_alt, fill_value=0).astype(int)
combined_secondary_types = combined_secondary_types.sort_values(ascending=False)

# Format the data for plotting
chart_data = combined_secondary_types.reset_index()
chart_data.columns = ["Secondary Type", "Count"]

# 📊 Bar chart of common type combinations
fig_chart = px.bar(
    chart_data,
    x="Secondary Type",
    y="Count",
    title=f"Common Secondary Types with {choice}",
    color="Count",
    text="Count"
)
plotly(fig_chart)

# 📋 Display a table of all Pokémon with this type
text(f"## All {choice} Pokemons")

# 🧰 Filter options for generation
text(f"Filter {choice} Pokemons by Generation")
generation = selectbox(
    label = "Filter Pokemons by Generation",
    options = ["show all generations",1, 2, 3, 4, 5, 6]
)

# ⭐ Option to show only legendary Pokémon
text(f"Filter {choice} Pokemons by Legendary Status")
legendary = checkbox(label="Show only lengendary pokemons")

# 🔢 Stat-based filtering using a slider
text(f"Filter {choice} Pokemons by Total Stats")
threshold_total = slider("Threshold for Total Stats", min_val=0, max_val=600, default=0)

# Apply filters based on generation and total stats
if generation != "show all generations":
    filtered_pokemons = pokemons_with_type[(pokemons_with_type["Total"] > threshold_total) & (pokemons_with_type["Generation"] == generation)]
else:
    filtered_pokemons = pokemons_with_type[pokemons_with_type["Total"] > threshold_total]

# Apply filter for legendary Pokémon
if legendary:
    filtered_pokemons = filtered_pokemons[filtered_pokemons["Legendary"] == True]

# 📋 Show filtered Pokémon in a table
table(filtered_pokemons, title=f"Pokemons with type {choice}")
