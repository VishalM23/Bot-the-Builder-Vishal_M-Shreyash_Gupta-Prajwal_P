from numpy import NaN
import pandas as pd


# data = pd.DataFrame(columns = ['Player', 'Wins', 'Losses'])
# data.to_csv('leaderboard.csv')


def update_leaderboard(player_ids,winner):

    winner_id=player_ids[winner]

    data=pd.read_csv('./leaderboard.csv')

    for i in range(len(player_ids)):
        # print(player_ids[i] in data['Player'].values())
        if((player_ids[i] in data['Player'].values) == False):
            df2 = {'Player': player_ids[i], 'Wins': 0, 'Losses': 0}
            data = data.append(df2, ignore_index = True)
            
    data.loc[data['Player']!=winner_id,'Losses']+=1
    data.loc[data['Player']==winner_id,'Wins']+=1


    data.drop(data.filter(regex="Unnamed"),axis=1, inplace=True)
    data.to_csv('leaderboard.csv')

# update_leaderboard(["Shreyash","Vishal"],1)
# update_leaderboard(["Vishal","Prajwal"],1)
# update_leaderboard(["Shreyash","Vishal","Prajwal"],1)

# @bot.command(pass_context=True)
# async def get_leaderboard(ctx, *player_args):

#     data=pd.read_csv('./leaderboard.csv')
#     await ctx.send('Player' , 'Wins', 'Losses')
#     for index, row in data.iterrows():
#         await ctx.send(row['Player'] , row['Wins'], row['Losses'])