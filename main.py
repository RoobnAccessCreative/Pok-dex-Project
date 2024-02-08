import pandas as pd
import matplotlib.pyplot as plt

def login(choice, df):
    match choice:
        case 'new':
            uname = input('Enter Username —>')
            pword = input('Enter password —>')
            if uname not in df['Name']:
                account = {'Name': uname, 'Pword': pword, 'mon_1': '', 'mon_2': '', 'mon_3': '', 'mon_4': '', 'mon_5': '', 'mon_6': '', }
                df = pd.concat([df, pd.DataFrame([account])], ignore_index=True)
                df.to_csv('UserData.csv', index=False)
                print('Your account has been registered')
        case _:
            uname = input('Enter Username —>')
            pword = input('Enter password —>')





#----------------------------MAIN-PROGRAM--------------------------------------------------------------------


df = pd.read_csv('UserData.csv')

choice = input("a ")
login(choice, df)
