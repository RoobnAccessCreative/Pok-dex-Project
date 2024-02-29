import json
import matplotlib.pyplot as plt
import pandas as pd
import requests as r
import sys


API_URL = "https://pokeapi.co/api/v2/"

def menu(df):
  
  choice = input("1 - login \n2 - sign up\n-- ")
  match choice:
        case "2":
            uname, pword, row_index = new_acc(df)
        case '1':
            uname, pword, row_index = login(df)
        case _:
            print("Sorry, I didn't quite catch that.")
            menu(df)

  print(f"Welcome, {uname}")
  return uname, pword, row_index

def new_acc(df):
  flag = False
  while not flag:
    print()
    uname = input("Enter New Username \n-- ")
    pword = input("Enter New Password \n-- ")
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
      print()
      print("Your account has been registered.")
      row_index = df.index.get_loc(df[df["Name"] == uname].index[0])
      flag = True
    else:
      print()
      print("Sorry, another trainer's already used that name.")
  return uname, pword, row_index

def login(df):
  flag = False
  while not flag:
    print()
    uname = input("Enter Username \n-- ")
    pword = input("Enter password \n-- ")
    row_index = 0
    for i in df["Name"]:
      if uname == i:
        if pword == df.loc[row_index, "Pword"]:
           flag = True
           break
      else:
          row_index += 1     

    if flag is False:
      print()
      print("I don't know anyone like that..")
  return uname, pword, row_index


def get_user_row(row_index):
  df = pd.read_csv('UserData.csv')
  user_df = df.loc[row_index]
  return user_df

def team_display(row_index):
  print()
  print("======================================")
  print("           Y O U R  T E A M          ")
  print("--------------------------------------")
  user_df = get_user_row(row_index)
  party_df = user_df[2:8]
  members = []
  for i in party_df:
    if pd.isna(i) is True:
      print("Empty")
    else:
      i = str(i).replace(".0", "")
      mon = json.loads(r.get(API_URL+"pokemon/"+str(i)).text)
      image = r.get(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{i}.png")
      print("#"+str(mon['id'])+" — "+mon['name'])
      members.append(mon['name'])
  stats_display(members)
  print("======================================")
  return None

def stats_display(list):
  s_name = ["HP", "Atk", "Def", "Sp.Atk", "Sp.Def", "Spe"]
  mon_dict = {

  }
  index = 1
  for mon in list:
    if mon not in mon_dict.keys():
      mon_dict[mon] = 1
    else:
      mon_dict[mon] = mon_dict[mon] + 1
    data = json.loads(r.get(API_URL+"pokemon/"+mon).text)
    s_val = []
    colours = []
    for i in data['stats']:
      stat = i['base_stat']
      s_val.append(stat)
      if stat >= 150:#determines the colour of the bar based on stat value
        colours.append('c')
      elif stat >= 90:
        colours.append('limegreen')
      elif stat >= 40:
        colours.append('gold')
      else:
        colours.append('tab:red')
        
    plt.subplot(1, len(list), index)
    plt.bar(s_name, s_val, width=0.5, color=colours)
    if mon_dict[mon] == 1:
      plt.title(mon)
    else:
      plt.title(f"{mon} {mon_dict[mon]}")
    plt.xticks(rotation=45, ha='right')
    index = index + 1
  plt.show(block=False)



#fullmatch search from input, repeats if no pokemon is found
def search():
  print("---------------------------------------")
  search_bar = input("Enter a Pokémon name or Pokédex number\n--  ")
  try:
    data = json.loads(r.get(API_URL+"pokemon/"+search_bar.lower()).text)
    image = r.get(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{data['id']}.png")
    print(data["name"])
    confirm = input("confirm? (y/n) -- ").lower()
    if confirm == 'y':
      return data['id']
    else:
      search()
  except:
    print("I've never heard of that Pokémon.")
    search()

#drop-down filter search: takes a type from drop-down; outputs first 10 results
def search_tag():
  print()
  print("-----------------------------------------------------------")
  types = ['normal','fighting','flying','poison','ground','rock','bug','ghost','steel'] 
  types_c = ['fire', 'water','grass','electric','ice','dragon','fairy','dark','psychic']
  print(*types)
  print(*types_c)
  print("-----------------------------------------------------------")
  flag = False
  while not flag:
    print()
    type = input("Enter one of the above types\n-- ")
    if type in types or type in types_c:
      flag = True
  pokemon_in_type = json.loads(r.get(API_URL+"type/"+type).text)["pokemon"]
  stored_pokemon = []
  print("---------------------------------------")
  for mon in pokemon_in_type:
      if len(stored_pokemon) < 10:
        mon_data = mon["pokemon"]
        mon_name = mon_data['name']  
        stored_pokemon.append(mon_name)
        print(mon_name)
        print()
        image = r.get(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{mon_data['name']}.png")
      else:
          break
  print("---------------------------------------")
  while True:
    print()
    choice = input("Choose one of the above Pokémon to add.\n-- ")
    if choice in stored_pokemon:
      break
    else:
      print()
      print("Sorry, I didn't quite catch that.")
  pokemon = json.loads(r.get(API_URL+"pokemon/"+choice).text)
  mon_id = pokemon['id']
  return mon_id


def menu2():#main menu
  team_display(row_index)
  while True:
    print("---------------------------------------")
    choice = input("1 - Add Pokémon \n2 - Remove Pokémon \n3 - User Settings \n-- ")
    plt.close()
    match choice:
      case '1':
        add_mon()
      case '2':
        delete_mon()
      case '3':
        menu3()
      case _:
        print()
        print("Sorry, I didn't quite catch that.")
        


def add_mon():
  user_df = get_user_row(row_index)
  party = user_df[2:]
  print("---------------------------------------")
  choice = input("Search by:\n  1 - Type\n  2 - Name/National Dex No.\n-- ")
  match choice:
    case '1':
      mon_id = search_tag()
    case '2':
      mon_id = search()
    case _:
      print("Sorry, I didn't quite catch that.")
      add_mon()
  count = 1
  for i in party:
    if pd.isna(i) is False:
      count += 1
      continue
    else:
      user_df.iloc[count+1] = mon_id
      df.iloc[row_index] = user_df
      df.to_csv('UserData.csv', index=False)
      break
  if count == 7:
    try:
      replace = int(input("Enter party no. to replace\n-- " ))
      if replace < 1 or replace > 6:
        print()
        print("Remember! You can only have 1-6 Pokémon on your team.")
      else:  
        user_df.iloc[replace+1] = mon_id
        df.iloc[row_index] = user_df
        df.to_csv('UserData.csv', index=False)
    except TypeError:
      print()
      print("Remember! You can only have 1-6 Pokémon on your team.")
  menu2() 



def delete_mon():
  user_df = get_user_row(row_index)
  print("---------------------------------------")
  try:
    delete = int(input("Enter number of party member to delete\n-- "))
  except TypeError:
    print()
    print("Sorry, I didn't quite catch that.")
    delete_mon()
  if delete < 1 or delete > 6:
    print("Remember! You can only have 1-6 Pokémon on your team.")
  elif pd.isna(user_df.iloc[delete+1]) is True or delete == 6:
    user_df.iloc[delete+1] = ""
  else:
    print(user_df.iloc[delete+1])
    while delete < 6:
      user_df.iloc[delete+1] = user_df.iloc[delete+2]
      delete += 1
    user_df.iloc[delete+1] = ""
  df.iloc[row_index] = user_df
  df.to_csv('UserData.csv', index=False)
  menu2()

def menu3():
  print("---------------------------------------")
  choice = input("1 - Change Username \n2 - Log Out \n3 - Delete Account  \nOther - back\n-- ")
  match choice:
    case '1':
      username_change()
    case '2':
      print()
      sys.exit("---GOODBYE---")
    case '3':
      delete()
    case _:
      menu2()

def username_change():
  user_df = get_user_row(row_index)
  uname = user_df["Name"]
  print("---------------------------------------")
  n_uname = input("Enter your new username\n-- ")
  change = input(f"Change username from {uname} to {n_uname}? (y/n) ")
  if change.upper() == 'Y':
    exist = False
    for i in df["Name"]:
      if n_uname == i:
        exist = True
        break
    if exist is False:
      user_df["Name"] = n_uname
      df.iloc[row_index] = user_df
      df.to_csv('UserData.csv', index=False)
    else:
      print()
      print("Sorry, another trainer's already used that name.")
      username_change()
  menu2()

def delete():
  print("ACCOUNT DETAILS CANNOT BE RECOVERED ONCE DELETED")
  check = input("ARE YOU SURE? (y/n)").lower()
  if check == 'y':
    df.drop(df.index[row_index], inplace=True)
    df.to_csv('UserData.csv', index=False)


#----------------------------MAIN-PROGRAM--------------------------------------------------------------------


df = pd.read_csv('UserData.csv')

print("""
   ___   ____ _  __ ______ ____ ___     ___ 
  / _ \ / __/| |/_//_  __// __// _ \   |_  |
 / // // _/ _>  <   / /  / _/ / , _/  / __/ 
/____//___//_/|_|  /_/  /___//_/|_|  /____/ 
                                            """)
print()

uname, pword, row_index = menu(df)
menu2()


