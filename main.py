from bs4 import BeautifulSoup
import pandas as pd

# Read the HTML file
with open('players.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all player rows (assuming each player is in a <tr>)
player_rows = soup.find_all('tr')

# Initialize a list to store player data
players_data = []

# Loop through each player row
for row in player_rows:
    # Extract player name and team
    player_name_div = row.find('div', class_='text-of')
    team_div = row.find('div', class_='stats-player-country')

    # Skip the row if player name or team is not found
    if not player_name_div or not team_div:
        continue

    player_name = player_name_div.text.strip()
    team = team_div.text.strip()

    # Extract agents
    agent_images = row.find_all('img')
    agents = [img['src'].split('/')[-1].replace('.png', '') for img in agent_images]

    # Extract stats
    stats_spans = row.find_all('span')
    stats = [span.text.strip() for span in stats_spans[:4]]

    # Store the data in a dictionary
    player_data = {
        'Player Name': player_name,
        'Team': team,
        'Agents': ", ".join(agents),
        'Stats': ", ".join(stats)
    }

    # Append the player data to the list
    players_data.append(player_data)

# Add players to csv file
df = pd.DataFrame(players_data)

# Define the CSV file name
csv_file = 'player_stats.csv'

# Write the DataFrame to a CSV file
df.to_csv(csv_file, index=False)

print(f"Data has been written to {csv_file}")