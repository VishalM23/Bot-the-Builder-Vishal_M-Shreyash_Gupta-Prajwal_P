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
from leaderboard import update_leaderboard
import pandas as pd
# from time import sleep
# from random import randint

root = tk.Tk()
root.attributes('-topmost',True)
root.attributes("-alpha", 0.9)

bot = commands.Bot(command_prefix="!")
players =[]
colors=[ "yellow", "magenta", "green", "blue", "cyan"]
players_clrs=[]
players_pos=[]
turn = 0
new_board=True
game = True
Grid=[]
Label_Grid=[]
difficulty=2
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
async def get_leaderboard(ctx):

    dataset=pd.read_csv('./leaderboard.csv')
    dataset.drop(dataset.filter(regex="Unnamed"),axis=1, inplace=True)
    s = ['Player     Wins   Losses']
    # This needs to be adjusted based on expected range of values or   calculated dynamically
    for index, data in dataset.iterrows():
        s.append('   '.join([str(item).center(7, ' ') for item in data.values]))
        # Joining up scores into a line
    d = '```'+'\n'.join(s) + '```'
    # Joining all lines togethor! 
    embed = discord.Embed(title = 'Quotient Results', description = d)
    await ctx.send(embed = embed)




@bot.command(pass_context=True)
async def new(ctx, *player_args_):
    # print(new_board)
    global players,players_clrs,turn,new_board, game, Grid, players_pos,colors,difficulty
    if new_board:
        if(len(player_args_[-1])==1):
            difficulty=int(player_args_[-1])
            player_args=player_args_[:len(player_args_)-1]
        else:
          player_args=player_args_


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
          Grid=SnL_generator(difficulty)
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
        # cap = CAP.CAP(root) 
        # cap.capture("File11.jpg", overwrite=True)
        # await ctx.send(file=discord.File("File11.jpg"))
        if(players_pos[turn]==[0,0]):
            await ctx.send("{} Won !!!".format(players[turn]))
            game=False
            update_leaderboard(players, turn)
        else:
          turn = (turn+1)%len(players)
          await ctx.send("Its {}'s turn".format(players[turn]))
          time.sleep(1)
    else:
        await ctx.send("It is not Your Chance, {} play your chance!!".format(players[turn]))

bot.run("ODYxODYzMTkwOTIxMDg0OTM5.YOP-pQ.NPdVQZG07BxLeN8KCXqSz5GpSzg")