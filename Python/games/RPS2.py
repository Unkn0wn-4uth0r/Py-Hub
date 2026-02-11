import random
import sqlite3

# Set up SQLite database
conn = sqlite3.connect('game_scores.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS scores (
    user_score INTEGER,
    computer_score INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Game settings
outcome = ["rock", "paper", "scissors"]
print("Hello.")
print("Welcome to Rock, Paper, Scissors!")
print("Choose either rock, paper, or scissors.")
print("Let's start.")
print("Make sure you type precisely either rock, paper, or scissors.")

user_score = 0
computer_score = 0

# Select difficulty level
difficulty = input("Select difficulty (easy, medium, hard): ").lower()
best_of = int(input("Enter the number of rounds for Best-of Mode (e.g., 3, 5, 7): "))
rounds_to_win = (best_of // 2) + 1

def ai_choice(user_input):
    if difficulty == "easy":
        return random.choice(outcome)
    elif difficulty == "medium":
        # Bias AI to counter user's previous move
        if user_input == "rock":
            return "paper"
        elif user_input == "paper":
            return "scissors"
        elif user_input == "scissors":
            return "rock"
        else:
            return random.choice(outcome)
    elif difficulty == "hard":
        # Predictive logic (simple pattern recognition)
        return random.choice(outcome)  # Add advanced logic here later
    else:
        return random.choice(outcome)

def match_up():
    global user_score, computer_score  # Declare global variables
    user_input = input("Which one do you choose: ").lower()
   
    if user_input not in outcome:
        print(f"{user_input} is not valid, please try again.")
        return
   
    computer_input = ai_choice(user_input)
    print(f"I chose {computer_input}.")
   
    if (user_input == "rock" and computer_input == "scissors") or \
       (user_input == "paper" and computer_input == "rock") or \
       (user_input == "scissors" and computer_input == "paper"):
        print("You won, nice job.")
        user_score += 1
    elif user_input == computer_input:
        print("It's a tie.")
    else:
        print("Sorry you lost, better luck next time.")
        computer_score += 1
   
    print(f"The score is {user_score} for you and {computer_score} for me.")

while True:
    match_up()
   
    # Check Best-of mode winner
    if user_score == rounds_to_win or computer_score == rounds_to_win:
        print(f"{'You' if user_score > computer_score else 'I'} won the best-of-{best_of} match!")
        break
   
    # Continue or exit
    decider = input("If you want to play again, press enter (or type 'exit' to quit): ").lower()
    if decider == "exit":
        break

# Save scores to SQLite database
c.execute('INSERT INTO scores (user_score, computer_score) VALUES (?, ?)', (user_score, computer_score))
conn.commit()

# Retrieve and display top scores
print("Game over! Here are the top scores:")
c.execute('SELECT * FROM scores ORDER BY user_score DESC LIMIT 5')
high_scores = c.fetchall()
for score in high_scores:
    print(score)

conn.close()
