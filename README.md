# Chess Game Performance Analysis ♟️📊

An Information Engineering approach to analyzing personal chess history. This project processes raw PGN data from Lichess into a structured format to identify strategic strengths, rating growth, and skill plateaus.

## 🚀 Overview
This repository contains a Python-based pipeline that transforms thousands of chess games into actionable insights. By extracting metadata from PGN files, we can visualize performance across different opening systems and rating brackets.

## 🛠️ Tech Stack
- **Language:** Python 3.12
- **Libraries:** Pandas (data manipulation), python-chess (PGN parsing)
- **Visualization:** Power BI (in progress)

## 📁 Repository Structure
- `analyze_games.py`: Parses raw PGN data into `processed_chess_data.csv`.
- `processed_chess_data.csv`: The cleaned, feature-engineered dataset — opening, color, rating, opponent bracket, and score per game.

## 🔧 How to Use
1. `pip install -r requirements.txt`
2. Download your PGN file from Lichess, then set `MY_USERNAME` and `FILE_NAME` in `analyze_games.py`.
3. `python analyze_games.py` — parses the PGN into `processed_chess_data.csv`.

## 📊 Dashboard
A Power BI report (opening volume, repertoire strength, ELO progression, skill-ceiling and color-performance breakdowns, all via DAX measures over `processed_chess_data.csv`) is in progress.
