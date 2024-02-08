import pandas as pd
import matplotlib.pyplot as plt

def login(df):
    l_flag = False
    while not l_flag:
        choice = input("a ")
        match choice:
            case 'new':
                uname = input('Enter Username —>')
                pword = input('Enter password —>')
                if uname not in df['Name']:
                    account = {'Name': uname, 'Pword': pword, 'mon_1': '', 'mon_2': '', 'mon_3': '', 'mon_4': '', 'mon_5': '', 'mon_6': '', }
                    df = pd.concat([df, pd.DataFrame([account])], ignore_index=True)
                    df.to_csv('UserData.csv', index=False)
                    print('Your account has been registered')
                    l_flag = True
                else:
                    print('invalid')
            case _:
                uname = input('Enter Username —>')
                pword = input('Enter password —>')
                if uname not in df['Name']:
                    print('Invalid')
                else:
                    row_index = df.index.get_loc(df[df['Name'] == uname].index[0])
                    if df.loc['Pword', row_index] != pword:
                        print("That's invalid")
                    else:
                        l_flag = True
    print(f'Welcome, {uname}')
    return uname, pword, row_index

def team_display(row_index):
    n_df = df.loc[row_index]
    n_df = n_df.iloc[2:8]
    team = list()
    for mon in n_df:
        team.append(mon)
    print(team)

#----------------------------MAIN-PROGRAM--------------------------------------------------------------------


df = pd.read_csv('UserData.csv')

uname, pword, row_index = login(df)
team_display(row_index)
