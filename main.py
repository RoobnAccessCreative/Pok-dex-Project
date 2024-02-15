import matplotlib.pyplot as plt
import pandas as pd
import requests as r
import json

API_URL = "https://pokeapi.co/api/v2/"

def login(df):
  l_flag = False
  while not l_flag:
      choice = input("1 - login  2 - sign up -- ")
      match choice:
    
          case "2":#new account
              uname = input("Enter New Username —>")
              pword = input("Enter New Password —>")
              if uname not in df["Name"]:
                
                account = {
                  "Name": uname,
                  "Pword": pword,
                  "mon_1": "", "mon_2": "",
                  "mon_3": "", "mon_4": "",
                  "mon_5": "", "mon_6": "", }
                  
                df = pd.concat([df, pd.DataFrame([account])], ignore_index=True)
                df.to_csv("UserData.csv", index=False)
                print("Your account has been registered")
                l_flag = True
                row_index = df.index.get_loc(df[df["Name"] == uname].index[0])
                print(row_index)
              else:
                print("invalid")
                
          case _:#login
            uname = input("Enter Username —>")
            pword = input("Enter password —>")
            row_index = 0
            for i in df["Name"]:
              if uname == i:
                if pword == df.loc[row_index, "Pword"]:
                   l_flag = True
                   break
              else:
                  row_index += 1     
  
            if l_flag is False:
               print("invalid")  
                
  print(f"Welcome, {uname}")
  return uname, pword, row_index

def get_user_row(row_index):
  df = pd.read_csv("UserData.csv")
  user_df = df.loc[row_index]
  return user_df

def team_display(row_index):
  user_df = get_user_row(row_index)
  user_team_df = user_df[2:8]
  party = []
  for i in user_team_df:
    print(i)
    party.append(i)
    stats_display(i)

def stats_display(mon):
   pass

def username_change(uname):
  user_df = get_user_row()
  n_uname = input(": ")
  change = (f"change username from {uname} to {n_uname}? (y/n) ")
  if change.upper() == 'Y':
    user_df["Name"] = n_uname

def search():#fullmatch search from input
  search = input(": ")
  try:
    data = json.loads(r.get(API_URL+"pokemon/"+search.lower()).text)
    image = r.get(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/{data['id']}.png")
    print(data["name"])
  except:
    print("not found")

def search_tag(type):#drop-down filter search
    pokemon_in_type = json.loads(r.get(API_URL+"type/"+type).text)["pokemon"]
    stored_pokemon = []
    for mon in pokemon_in_type:
        if len(stored_pokemon) < 10:
            mon_data = mon["pokemon"]
            stored_pokemon.append(mon_data)
            print(mon_data)
        else:
           break

def team_edit():
  team_display(row_index)
  choice = input("1 - add 2 - remove -- ")
  match choice:
    case '1':
      add_mon()
    case '2':
      delete_mon()
    case _:
        print("pick one of the options bucko or im telling my G money (Sir Gavinsworth III: Duke of Earlesson and cranking 90s in Fortnite) >:(")
    
def add_mon():
  get_user_row()
  search()
  
def delete_mon():
  pass
#----------------------------MAIN-PROGRAM--------------------------------------------------------------------


df = pd.read_csv("UserData.csv")

uname, pword, row_index = login(df)
team_display(row_index)

username_change(uname)
search()
search_tag("ground")
