import json
import csv
from collections import defaultdict

# Function to read CSV files and aggregate player kills
def aggregate_player_kills(csv_files):
    player_kills_count = defaultdict(lambda: [[], []])  # Initialize defaultdict with lists to hold kill counts for each map range
    
    # Iterate through each CSV file
    for csv_file in csv_files:
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            # Iterate through each row in the CSV file
            for row in reader:
                map_number = int(row['Map'].split()[1])  # Extract the map number
                if 1 <= map_number <= 4:
                    player_kills_count[row['Player Name']][0].append(int(row['Player Kills']))  # Add kills to maps 1-4
                elif 5 <= map_number <= 6:
                    player_kills_count[row['Player Name']][1].append(int(row['Player Kills']))  # Add kills to maps 5-6
    
    # Calculate the average kills for each player for maps 1-4 and 5-6
    player_kills_average = {}
    for player_name, kills in player_kills_count.items():
        kills_avg_map1_4 = sum(kills[0]) / len(kills[0]) if kills[0] else 0
        kills_avg_map5_6 = sum(kills[1]) / len(kills[1]) if kills[1] else 0
        player_kills_average[player_name] = [kills_avg_map1_4, kills_avg_map5_6]
    
    return player_kills_average

# Main function
def main():
    json_files = ['data.json', 'data2.json']  # Add more JSON files if needed
    csv_files = []

    for json_file in json_files:
        # Opening JSON file and loading the data
        with open(json_file) as f:
            data = json.load(f)
        
        # Define the CSV file header for the initial data
        header = ["Map", "Team Name", "Player Name", "Player Kills"]
        out_put_csv = json_file.split('.')[0] + '.csv' 
        
        # Open the CSV file for writing the initial data
        with open(out_put_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)  # Write the header
    
            map_counter = 1

            # Iterate through all games in the data
            for game in data['games']:
                game_map = f"Map {map_counter}"
                
                # Iterate through all results in each game
                for result in game['results']:
                    team_info = [game_map, result['name']]
                    
                    # Iterate through all players in each result
                    for player in result['players']:
                        player_info = [player['name'], player['kills']]
                        writer.writerow(team_info + player_info)
                
                # Increment map counter for the next game
                map_counter += 1
        
        csv_files.append(out_put_csv)

    # Aggregate player kills from the CSV files
    player_kills = aggregate_player_kills(csv_files)
    
    # Write the aggregated data to a new CSV file
    output_file = 'aggregated_output.csv'
    agg_header = ["Player Name", "Kills (Maps 1-4)", "Kills (Maps 5-6)"]
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(agg_header)  # Write the header
        for player_name, kills in player_kills.items():
            writer.writerow([player_name, kills[0], kills[1]])  # Write the aggregated data for each player
    
    print("Aggregated data has been written to:", output_file)

if __name__ == "__main__":
    main()
