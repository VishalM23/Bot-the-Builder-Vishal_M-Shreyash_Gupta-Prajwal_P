import tkinter as tk
import discord
from discord import player
from discord.ext import commands
from discord.ext.commands import bot
from SnL_generator import SnL_generator
import random
import CAP
import os
import datetime as dt
import random
import time
import game_logic
# from time import sleep
# from random import randint

root = tk.Tk()
root.attributes('-topmost',True)

# LabelGrid = []

# def updateGrid():
#   global players
#   global players_clrs
#   global LabelGrid
#   global Grid
#   for i in LabelGrid:
#     i.grid_forget()
#   for i in range(10):
#     for j in range(10):
#       root.grid_rowconfigure(i,weight=1,minsize=60)
#       root.grid_columnconfigure(j,weight=1,minsize=60)
#       Label = tk.Label(root)
#       Label.grid(column=j,row=i,sticky="nsew")
#       LabelGrid.append(Label)
#       if (i+j)%2 == 0:
#         Label.configure(bg="Black")
#       if Grid[i][j] == "Empty":
#         Label.configure(text="")
#       elif Grid[i][j] == "Start":
#         Label.configure(text="Start",bg="Sky Blue")
#       elif Grid[i][j] == "End":
#         Label.configure(text="End",bg="Gold")
#       else:
#         LabelText = "Leads to\nCollumn "+str(Grid[i][j][1])+"\nRow "+str(Grid[i][j][0])
#         Label.configure(text=LabelText,bg="Red" if Grid[i][j][2] == "S" else "Green")
  
#   for i in range(3):
#     p= tk.Label(root,text="Player"+str(i+1),bg=players_clrs[i])
#     p.grid(column=players[i][1],row=players[i][0],sticky="n")
#     LabelGrid.append(p)  
#   # p2 = tk.Label(root,text="Player 2",bg="Blue")
#   # p2.grid(column=player2[1],row=player2[0],sticky="s")
#   # LabelGrid.append(p2)
#   root.update()

# def movePlayer(player,spaces):
#   global Grid
#   endSpace = player
#   for i in range(spaces):
#     if endSpace == [0,0]:
#       return endSpace
#     if endSpace[0]%2 == 1:
#       if endSpace[1] == 9:
#         endSpace[0] -= 1
#       else:
#         endSpace[1] += 1
#     else:
#       if endSpace[1] == 0:
#         endSpace[0] -= 1
#       else:
#         endSpace[1] -= 1
#   if type(Grid[endSpace[0]][endSpace[1]])==list:
#     print("here")
#     return [Grid[endSpace[0]][endSpace[1]][0],Grid[endSpace[0]][endSpace[1]][1]]
#   return endSpace

# Turn = 0
# Winner = ""

# Text = tk.Label(root,text="Loading")
# WaitVariable = tk.IntVar()
# Button = tk.Button(root,text="Roll",command=lambda: WaitVariable.set(1))
# Text.grid(column=0,row=10,columnspan=10,sticky="nsew")
# Button.grid(column=0,row=11,columnspan=10,sticky="nsew")

# root.grid_rowconfigure(10,weight=1,minsize=32)
# root.grid_rowconfigure(11,weight=1,minsize=32)

# updateGrid()
# while True:
#   Text.configure(text="Player " +str(Turn+1)+"s turn")
#   Button.wait_variable(WaitVariable)
#   roll = randint(1,6)
#   Text.configure(text="Rolled a "+str(roll))

#   players[Turn]= movePlayer(players[Turn],roll)
#   if (players[Turn] == [0,0]):
#     Winner = "Player "+str(Turn)
#     break;
#   # if Turn%2 == 1:
#   #   player1 = movePlayer(player1,roll)
#   #   if player1 == [0,0]:
#   #     Winner = "Player 1"
#   #     break
#   # else:
#   #   player2 = movePlayer(player2,roll)
#   #   if player2 == [0,0]:
#   #     Winner = "Player 1"
#   #     break
#   Turn = (1+Turn)%3
#   updateGrid()
#   sleep(1)

# Text.configure(text=Winner+" wins!")
# updateGrid()



bot = commands.Bot(command_prefix="!")
players =[]
colors=[ "yellow", "magenta","red", "green", "blue", "cyan"]
players_clrs=[]
players_pos=[]
turn = 0
new_board=True
game = True
Grid=[]
Label_Grid=[]

# Things to run when the bot connects to Discord

@bot.event
async def on_ready():
    print("Connected!")
    global players,player_clrs,turn,new_board, game,Grid
    players = []
    player_clrs= []
    turn = 0
    new_board=True
    game = True

@bot.command(pass_context=True)
async def new(ctx, *player_args):
    # print(new_board)
    global players,players_clrs,turn,new_board, game, Grid, players_pos,colors
    if new_board:

        players=[]
        players_pos =[]
        players_clrs=[]
        game=True
        for player in player_args:
          print(player)
          await ctx.send("Starting a new Game Between "+ player+" ")
        for i in player_args:
          str=i.replace('!','')
          players.append(str)
        random.shuffle(players)

        if(len(players)<=1):
          await ctx.send("Please Select a player to play against!")
        else:
          time.sleep(1)
          await ctx.send("Its {}'s turn".format(players[0]))
          new_board=False
          Grid=SnL_generator()
          for i in range(len(players)):
            players_pos.append([9,0])
            players_clrs.append(colors[i])
    else:
        await ctx.send("You already have a game running")


@bot.command(pass_context=True)
async def roll(ctx):
    global players,player_clrs,turn,new_board, game, Grid, players_pos, Label_Grid, root
    
    if(not game):
      await ctx.send("Game Ended !!!")
      new_board=True
      return;
    print(ctx.message.author.mention,players[turn])
    
    if str(ctx.message.author.mention) == players[turn] and game:
        game_logic.refresh_grid(root, players, players_pos, players_clrs, Label_Grid, Grid)
        await ctx.send("Rolling the dice :game_die:")
        roll_val=random.randint(1,6)
        await ctx.send("{} rolled {}".format(ctx.message.author.mention,roll_val))
        players_pos[turn]=game_logic.move_player(Grid, players_pos[turn], roll_val)
            
        game_logic.refresh_grid(root, players, players_pos, players_clrs, Label_Grid, Grid)
        cap = CAP.CAP(root) 
        cap.capture("File11.jpg", overwrite=True)
        await ctx.send(file=discord.File("File11.jpg"))
        if(players_pos[turn]==[0,0]):
            await ctx.send("{} Won !!!".format(players[turn]))
            game=False
        else:
          turn = (turn+1)%len(players)
          await ctx.send("Its {}'s turn".format(players[turn]))
          time.sleep(1)
    else:
        await ctx.send("It is not Your Chance, {} play your chance!!".format(players[turn]))

bot.run("ODYxODYzMTkwOTIxMDg0OTM5.YOP-pQ.NPdVQZG07BxLeN8KCXqSz5GpSzg")