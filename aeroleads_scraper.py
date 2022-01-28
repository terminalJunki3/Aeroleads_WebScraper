from bs4 import BeautifulSoup
import pandas as pd
import requests
import time



USERNAME = 'xxxxx' # put correct usename here
PASSWORD = 'xxxxx' # put correct password here
authenticity_token = "xxxx"
LOGINURL = 'https://aeroleads.com/users/login'

session = requests.session()

req_header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Windows OS X 10.15; rv:80.0) Gecko/20100101 Firefox/90.0',
    'Cookie': '_lead_session=xxxx--xxxxx'
}

formdata = {
    'utf8': '✓',
    'authenticity_token': authenticity_token,
    'user[email]': USERNAME,
    'user{password]': PASSWORD,
    'user[remember_me]': '0',
    'commit': 'Log+in'
}

# Authenticate
r = session.post(LOGINURL, headers=req_header, data=formdata, allow_redirects=False)


# Extract Data

company = input("Company Search: ")
table_name = "tableout.xlsx"
print(" ")
print(f"[+] Scraping site for {company}")
print(" ")

dataframe_collection = {}
for i in range(1, 41):
    DATAURL = f'https://aeroleads.com//search?profile_company%5B%5D={company}&page={i}'
    x = session.get(DATAURL)
    soup = BeautifulSoup(x.content, 'html.parser')
    df_list = pd.read_html(x.text)  # this parses all the tables in webpages to a list
    df = df_list[0]
    dataframe_collection[i] = df
    print(f' [+]{DATAURL}')
    time.sleep(1)



final = pd.DataFrame() # create final DataFrame
print(" ")
print(" ")
print("----Combining Data(s)----")
for key, sub_df in dataframe_collection.items(): # Combines all Dataframes
    final = final.append(sub_df, ignore_index=False)  # Add your sub_df one by one

final.drop(['Actions', 'Contacts'], axis=1, inplace=True)
final.to_excel(f'{company}.xlsx', sheet_name='Employee Info')
print(f"[+] File Complete! Name:{company}.xlsx")

test = input("Press ENTER to exit.")