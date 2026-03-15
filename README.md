# Tetis
A modern pastel-themed version of the classic Tetris game built with Python and Pygame. The project features smooth gameplay, rounded blocks, soft pastel colors, scoring, record tracking, and a polished UI layout.

📸 Preview

Classic falling block gameplay with a soft pastel aesthetic and clean interface.

✨ Features

🎨 Soft pastel color palette

🧩 Classic 7 Tetris pieces

📈 Score system with line clear bonuses

🏆 High score (record) saving

🔄 Piece rotation

⬅️➡️ Movement controls

⏬ Soft drop

🎯 Next piece preview

🟦 Rounded block rendering

🎮 Smooth 60 FPS gameplay

🧱 Dynamic difficulty (speed increases)

🕹 Controls
Key	Action
⬅️ Left Arrow / A	Move Left
➡️ Right Arrow / D	Move Right
⬇️ Down Arrow / S	Soft Drop
⬆️ Up Arrow / W	Rotate Piece
❌ Close Window	Quit Game
🧠 Game Rules

Blocks fall from the top of the board.

Arrange them to complete horizontal lines.

Completed lines disappear and award points.

Clearing multiple lines grants bonus points.

The game ends when blocks reach the top of the board.

🏆 Scoring System
Lines Cleared	Points
1	100
2	300
3	700
4	1500
📂 Project Structure
Tetris/
│
├── main.py
├── record
│
├── font.ttf
├── bg.jpg
└── bg2.jpg
⚙️ Requirements

Python 3.8+

Pygame

Install dependencies:

pip install pygame
▶️ Run the Game
python main.py
💡 How It Works

The game uses:

Pygame surfaces for rendering

Grid-based collision detection

Random piece generation

Deep copy piece cloning

Persistent file storage for the high score

🛠 Technologies

Python 🐍

Pygame 🎮

📜 License

This project is open-source and free to use for learning and modification.
