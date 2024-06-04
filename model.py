import argparse
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Function to parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Predict kills for a player in maps 1-4.')
    parser.add_argument('player_name', type=str, help='Name of the player')
    parser.add_argument('kills_maps_1_4', type=int, help='Number of kills in maps 1-4')
    parser.add_argument('kills_maps_5_6', type=int, help='Number of kills in maps 5-6')
    return parser.parse_args()

# Step 1: Load and prepare data
data = pd.read_csv('aggregated_output.csv')  

# Step 2: Model Training
models = {}  

# Train a separate model for each player
for player_name in data['Player Name'].unique():
    player_data = data[data['Player Name'] == player_name]
    X = player_data[['Kills (Maps 1-4)', 'Kills (Maps 5-6)']]
    y = player_data['Kills (Maps 1-4)']  
    model = RandomForestRegressor()  #this is actually basic so idk
    model.fit(X, y)
    models[player_name] = model

# Step 3: Prediction
def predict_kills(player_name, kills_maps_1_4, kills_maps_5_6):
    model = models.get(player_name)
    if model:
        prediction = model.predict([[kills_maps_1_4, kills_maps_5_6]])
        return prediction[0]
    else:
        return None  # Return None if model for the player doesn't exist

# Example usage - just pass in the name and the kills, rn it doesnt matter it just tells u how many kills it thinks its gonna have lol
def main():
    args = parse_arguments()
    player_name = args.player_name
    kills_maps_1_4 = args.kills_maps_1_4
    kills_maps_5_6 = args.kills_maps_5_6

    predicted_kills = predict_kills(player_name, kills_maps_1_4, kills_maps_5_6)
    if predicted_kills is not None:
        print(f"The predicted kills for {player_name} in maps 1-4 is approximately: {predicted_kills:.2f}")
    else:
        print(f"No model found for {player_name}")

if __name__ == "__main__":
    main()
