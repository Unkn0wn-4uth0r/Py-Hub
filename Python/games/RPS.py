import random
choices = ["Rock", "Paper", "Scissors"]

comp_choice = choice.random()

print("Rock, Paper, or Scissors")

user_choice = input("Enter a choice")
if( (user_choice == "Rock" and comp_choice == "Paper") or (user_choice == "Paper" and comp_choice == "Scissors") or (user_choice == "Scissors" and comp_choice == "Rock"):

