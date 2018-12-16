# BattleFortune
Dominons 5 Montecarlo Simulation: You can't cheat fate, but you can predict the future.

# Vision
Allow the user to simulate hundreds of Dominions battles. BattleFortune aims to help players to both predict battle results, and improve their scripting by providing useful statistical information about battles outcomes.

# Current Sate
In the current state, BattleFortune will run the same battle as many times as the user wants, and ouput a distribution chart with the expected gold loss for each nation. Mods are not supported. Only tested on Windows. 

To run BattleFortuner you will need to follow these steps:
1. Script a Battle on Dominions 5, ending the turn for both nations.
2. Save the turn without hosting the battle.
3. Run the function battlefortune on battlefortune.py with the following inputs:
    1. Number of turns to be simulated.
    2. Name of the Game to be simulated.
    3. Number of the province where the battle is happening.
    4. Dominions 5 executable path.
    5. Dominions 5 game folder path.

# Sample Outputs
Here are a few examples of the current output capabilities of BattleFortune.

#### Expected Gold Loss for each army
![Expected Gold Loss](https://media.discordapp.net/attachments/480242947015573504/521898564771643392/unknown.png)

#### Expected Return on Investment
![Army Return on Investment](https://media.discordapp.net/attachments/480242947015573504/521900656861380608/unknown.png)


##### credits
This project would not be possible without Illwinter, the Dominions Discord community, and the help of yet to be named awesome developers.
