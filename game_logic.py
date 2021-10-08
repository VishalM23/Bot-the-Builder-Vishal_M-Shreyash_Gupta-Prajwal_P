import tkinter as tk
def move_player(Grid, player_pos, places):

    if(player_pos[0]==0):
        if(places>(player_pos[1])):
            return player_pos
    for i in range(places):
        if player_pos == [0,0]:
            return player_pos
        if player_pos[0]%2 == 1:
            if player_pos[1] == 9:
                player_pos[0] -= 1
            else:
                player_pos[1] += 1
        else:
            if player_pos[1] == 0:
                player_pos[0] -= 1
            else:
                player_pos[1] -= 1

    if type(Grid[player_pos[0]][player_pos[1]])==list:
        print("here")
        return [Grid[player_pos[0]][player_pos[1]][0],Grid[player_pos[0]][player_pos[1]][1]]
    return player_pos


def refresh_grid(root, players, players_pos, players_clrs, LabelGrid, Grid):
    for i in LabelGrid:
        i.grid_forget()
    for i in range(10):
        for j in range(10):
            root.grid_rowconfigure(i,weight=1,minsize=60)
            root.grid_columnconfigure(j,weight=1,minsize=60)
            Label = tk.Label(root)
            Label.grid(column=j,row=i,sticky="nsew")
            LabelGrid.append(Label)
            if (i+j)%2 == 0:
                Label.configure(bg="#355C70")
            if Grid[i][j] == "Empty":
                Label.configure(text="")
            elif Grid[i][j] == "Start":
                Label.configure(text="Start",bg="Sky Blue")
            elif Grid[i][j] == "End":
                Label.configure(text="End",bg="Gold")
            else:
                LabelText = "Leads to\nColumn "+str(Grid[i][j][1])+"\nRow "+str(Grid[i][j][0])
                Label.configure(text=LabelText,bg="#f96262" if Grid[i][j][2] == "S" else "#52f488")
  
    for i in range(len(players)):
        p= tk.Label(root,text="Player"+str(i+1),bg=players_clrs[i])
        # p= tk.Label(root,text="{}".format(players[i].username),bg=players_clrs[i])
        p.grid(column=players_pos[i][1],row=players_pos[i][0],sticky="n")
        LabelGrid.append(p)  
  # p2 = tk.Label(root,text="Player 2",bg="Blue")
  # p2.grid(column=player2[1],row=player2[0],sticky="s")
  # LabelGrid.append(p2)
    root.update()