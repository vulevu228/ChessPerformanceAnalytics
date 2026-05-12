import pandas as pd
import chess.pgn
import os

def analyze_chess_data(pgn_file, target_user):
    games = []
    
    if not os.path.exists(pgn_file):
        print(f"Error: File {pgn_file} not found.")
        return None

    with open(pgn_file) as f:
        while True:
            try:
                game = chess.pgn.read_game(f)
                if game is None: break
                
                h = game.headers
                is_white = h.get("White") == target_user
                result = h.get("Result")
                
                # Logic: Use Opening Name, fallback to ECO
                opening_name = h.get("Opening") or h.get("ECO") or "Unknown"

                # Score calculation
                score = 0.5
                if result == "1-0":
                    score = 1 if is_white else 0
                elif result == "0-1":
                    score = 0 if is_white else 1
                
                games.append({
                    "Date": h.get("UTCDate"),
                    "Result": result,
                    "Color": "White" if is_white else "Black",
                    "Your_Rating": int(h.get("WhiteElo" if is_white else "BlackElo", 0)),
                    "Opponent_Rating": int(h.get("BlackElo" if is_white else "WhiteElo", 0)),
                    "ECO": h.get("ECO"),
                    "Opening": opening_name,
                    "Score": score
                })
            except Exception as e:
                continue

    df = pd.DataFrame(games)
    
    # --- FEATURE ENGINEERING FOR VISUALIZATION ---
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month_Year'] = df['Date'].dt.strftime('%Y-%m')
    df['Opponent_Bracket'] = (df['Opponent_Rating'] // 100) * 100
    
    # Save the processed data
    df.to_csv("processed_chess_data.csv", index=False)
    print(f"Success! Processed {len(df)} games into processed_chess_data.csv")
    return df

# --- CONFIGURATION ---
# Redacted: Enter your username here before running
MY_USERNAME = "Spanish_dOc" 
FILE_NAME = "full_history_30k.pgn"

if __name__ == "__main__":
    analyze_chess_data(FILE_NAME, MY_USERNAME)