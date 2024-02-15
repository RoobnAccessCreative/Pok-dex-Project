import matplotlib.pyplot as plt
import pandas as pd
import requests as r
import json


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

def team_display(df, row_index):
  user_df = df.loc[row_index]
  user_team_df = user_df[2:8]
  for i in user_team_df:
    print(i)
  return user_df 

def stats_display(user_df):
   pass

def username_change(user_df, uname):
  n_uname = input(": ")
  change = (f"change username from {uname} to {n_uname}? (y/n) ")
  if change.upper() == 'Y':
    user_df["Name"] = n_uname
  return user_df

def search():
  search = input(": ")
  try:
     data = json.dumps(r.get("https://pokeapi.co/api/v2/pokemon/"+search.lower()).text)
     print(data)
  except:
     print("not found")
  
    
#----------------------------MAIN-PROGRAM--------------------------------------------------------------------


df = pd.read_csv("UserData.csv")

#uname, pword, row_index = login(df)
#user_df = team_display(df, row_index)
#stats_display(user_df)
#user_df = username_change(user_df,uname)
search()
