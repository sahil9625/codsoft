import random

options = ['Rock', 'Paper', 'Scissors']

def play_game():
    userOption = input('Press 1 for Rock, 2 for Paper, 3 for Scissors, or "q" to quit: ').strip().lower()

    if userOption == 'q':
        print("Exiting game.")
        return False

    if userOption not in ['1', '2', '3']:
        print("Invalid input. Please enter 1, 2, 3, or 'q' to quit.")
        return True

    userOption = int(userOption)
    userChoice = options[userOption - 1]

    computerChoice = options[random.randint(0, 2)]

    print(f'You chose: {userChoice}')
    print(f'Computer chose: {computerChoice}')

    result = "It's a tie!"

    if userChoice == computerChoice:
        result = "It's a tie!"
    elif (userChoice == 'Rock' and computerChoice == 'Scissors') or \
         (userChoice == 'Paper' and computerChoice == 'Rock') or \
         (userChoice == 'Scissors' and computerChoice == 'Paper'):
        result = "You Won!"
    else:
        result = "Computer Won!"

    print(result)
    return True

while play_game():
    pass
