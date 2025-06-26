import mysql.connector
import pandas as pd

# MySQL Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="valorant_stats"
)
cursor = db.cursor()

# Read CSV file
df = pd.read_csv("player_stats.csv", skiprows=1, header=None, names=["Player Name", "Team", "Agents", "Stats"])

# Insert data into MySQL
for _, row in df.iterrows():
    player_name = row["Player Name"]
    team = row["Team"]
    agents = row["Agents"]
    
    # Split stats into separate values
    stats = row["Stats"].split(", ")
    rating = float(stats[0])
    acs = float(stats[1])
    kdr = float(stats[2])
    hs_percent = float(stats[3].strip('%'))  # Convert "76%" to 76.0

    # Insert into MySQL
    cursor.execute(
        "INSERT INTO players (player_name, team, agents, rating, acs, kdr, hs_percent) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (player_name, team, agents, rating, acs, kdr, hs_percent)
    )

# Commit and close connection
db.commit()
cursor.close()
db.close()

print("CSV data has been inserted into MySQL")
