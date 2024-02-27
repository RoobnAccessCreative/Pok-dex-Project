import json
import matplotlib.pyplot as plt
import pandas as pd
import requests as r
import sys


API_URL = "https://pokeapi.co/api/v2/"

def menu(df):
  choice = input("1 - login \n2 - sign up\n-> ")
  match choice:
        case "2":
            uname, pword, row_index = new_acc(df)
        case '1':
            uname, pword, row_index = login(df)
        case _:
            print("Invalid choice.")
            menu(df)

  print(f"Welcome, {uname}")
  return uname, pword, row_index

def new_acc(df):
  flag = False
  while not flag:
    uname = input("Enter New Username —>")
    pword = input("Enter New Password —>")
    exist = False
    for i in df["Name"]:
      if uname != i:
        continue
      else:
        exist = True
    if exist is False:
      account = {
        "Name": uname,
        "Pword": pword,
        "mon_1": "", "mon_2": "",
        "mon_3": "", "mon_4": "",
        "mon_5": "", "mon_6": "", }
  
      df = pd.concat([df, pd.DataFrame([account])], ignore_index=True)
      df.to_csv("UserData.csv", index=False)
      print("Your account has been registered")
      row_index = df.index.get_loc(df[df["Name"] == uname].index[0])
      flag = True
    else:
      print("invalid")
  return uname, pword, row_index

def login(df):
  flag = False
  while not flag:
    uname = input("Enter Username —>")
    pword = input("Enter password —>")
    row_index = 0
    for i in df["Name"]:
      if uname == i:
        if pword == df.loc[row_index, "Pword"]:
           flag = True
           break
      else:
          row_index += 1     
  
    if flag is False:
       print("invalid")
  return uname, pword, row_index
  

def get_user_row(row_index):
  df = pd.read_csv('pokedex/UserData.csv')
  user_df = df.loc[row_index]
  return user_df

def team_display(row_index):
  user_df = get_user_row(row_index)
  party_df = user_df[2:8]
  members = []
  for i in party_df:
    if pd.isna(i) is True:
      print("empty")
    else:
      i = int(i)
      mon = json.loads(r.get(API_URL+"pokemon/"+str(i)).text)
      image = r.get(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{i}.png")
      print(mon['name'])
      members.append(mon['name'])
  stats_display(members)
  return None
    
def stats_display(list):
  s_name = ["HP", "Atk", "Def", "Sp.Atk", "Sp.Def", "Spe"]
  colors = ["red" if i ]
  for mon in list:
    data = json.loads(r.get(API_URL+"pokemon/"+mon).text)
    s_val = []
    for i in data['stats']:
      s_val.append(i['base_stat'])
    plt.subplot(1, len(list), list.index(mon)+1)
    plt.bar(s_name, s_val, width=0.5)
    plt.title(mon)
    plt.xticks(rotation=45, ha='right')
  plt.show(block=False)
  
  
  
#fullmatch search from input, repeats if no pokemon is found
def search():
  search_bar = input(": ")
  try:
    data = json.loads(r.get(API_URL+"pokemon/"+search_bar.lower()).text)
    image = r.get(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{data['id']}.png")
    print(data["name"])
    confirm = input("confirm? (y/n)").lower()
    if confirm == 'y':
      return data['id']
    else:
      search()
  except:
    print("try again")
    search()
  
#drop-down filter search: takes a type from drop-down; outputs first 10 results
def search_tag(type):
  pokemon_in_type = json.loads(r.get(API_URL+"type/"+type).text)["pokemon"]
  stored_pokemon = []
  for mon in pokemon_in_type:
      if len(stored_pokemon) < 10:
        mon_data = mon["pokemon"]
        mon_name = mon_data['name']       #MAKWE USE OF THISSRRDSDSTESWDGT
        stored_pokemon.append(mon_name)
        print(mon_name)
        image = r.get(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{mon_data['name']}.png")
      else:
          break
  choice = input("pick one -- ")
  if choice in stored_pokemon:
    return choice
  else:
    search_tag(type)

def menu2():
  team_display(row_index)
  choice = input("1 - add 2 - remove 3 - user settings -- ")
  plt.close()
  match choice:
    case '1':
      add_mon()
    case '2':
      delete_mon()
    case '3':
      menu3()
    case _:
      print("pick one of the options bucko")
      menu2()
      

def add_mon():
  user_df = get_user_row(row_index)
  party = user_df[2:]
  mon_id = search()
  count = 1
  for i in party:
    if pd.isna(i) is False:
      count += 1
      continue
    else:
      user_df.iloc[count+1] = mon_id
      df.iloc[row_index] = user_df
      df.to_csv('pokedex/UserData.csv', index=False)
      break
  if count == 7:
    try:
      replace = int(input("Enter party no. to replace" ))
      if replace < 1 or replace > 6:
        print("not in range")
      else:  
        user_df.iloc[replace+1] = mon_id
        df.iloc[row_index] = user_df
        df.to_csv('pokedex/UserData.csv', index=False)
    except TypeError:
      print("at least do a number")
  menu2() 
  


def delete_mon():
  user_df = get_user_row(row_index)
  delete = int(input("Enter party no. to erase "))
  if delete < 1 or delete > 6:
    print("not in range")
  elif pd.isna(user_df.iloc[delete+1]) is True or delete == 6:
    user_df.iloc[delete+1] = ""
  else:
    print(user_df.iloc[delete+1])
    while delete < 6:
      user_df.iloc[delete+1] = user_df.iloc[delete+2]
      delete += 1
    user_df.iloc[delete+1] = ""
  df.iloc[row_index] = user_df
  df.to_csv('pokedex/UserData.csv', index=False)
  menu2()

def menu3():
  choice = input("1 - change username 2 - delete account 3 - log out  other - back -- ")
  match choice:
    case '1':
      username_change()
    case '2':
      delete()
    case '3':
      sys.exit("--Goodbye!--")
    case _:
      menu2()

def username_change():
  user_df = get_user_row(row_index)
  uname = user_df["Name"]
  n_uname = input(": ")
  change = input(f"change username from {uname} to {n_uname}? (y/n) ")
  if change.upper() == 'Y':
    user_df["Name"] = n_uname
    df.iloc[row_index] = user_df
    df.to_csv('pokedex/UserData.csv', index=False)
  menu2()

def delete():
  print("account details cannot be recovered")
  check = input("are you sure? (y/n)").lower()
  if check == 'y':
    df.drop(df.index[row_index], inplace=True)
    df.to_csv('pokedex/UserData.csv', index=False)


#----------------------------MAIN-PROGRAM--------------------------------------------------------------------


df = pd.read_csv('pokedex/UserData.csv')

uname, pword, row_index = menu(df)
menu2()
