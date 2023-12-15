from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import pandas as pd
import time
import sqlalchemy as db
import openai
import streamlit as st


openai.api_key = st.secrets["api_key"]

def appInfo():
    st.set_page_config(
        page_title="TP Final",
        page_icon="🧊",
        layout="wide",
    )

    st.sidebar.title("Edison MASSENA")

    st.sidebar.write("L'application permet de collecter des données sur les jeux vidéos de la plateforme Steam et de les stocker dans une base de données. Les données sont ensuite affichées dans une page de visualisation. Vous avez également la possibilité de faire une recherche sur un jeu en particulier. Selenium est utilisé pour le scraping car il était nécessaire de scroller la page pour charger les données supplémentaire. /// Lien scraping: https://store.steampowered.com/search/?term=action /// Streamlit Cloud: https://tpfinalwebscraping-2naa9gpyaq7vccm9fvqufa.streamlit.app/")


class DataBase():
    def __init__(self, name_database='database'):
        self.name = name_database
        self.url = f"sqlite:///{name_database}.db"
        self.engine = db.create_engine(self.url)
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.table = self.engine.table_names()


    def create_table(self, name_table, **kwargs):
        colums = [db.Column(k, v, primary_key = True) if 'id_' in k else db.Column(k, v) for k,v in kwargs.items()]
        db.Table(name_table, self.metadata, *colums)
        self.metadata.create_all(self.engine)
        print(f"Table : '{name_table}' are created succesfully")

    def read_table(self, name_table, return_keys=False):
        table = db.Table(name_table, self.metadata, autoload=True, autoload_with=self.engine)
        if return_keys:
            table.columns.keys()
        else : 
            return table


    def add_row(self, name_table, **kwarrgs):
        name_table = self.read_table(name_table)

        stmt = (
            db.insert(name_table).
            values(kwarrgs)
        )
        self.connection.execute(stmt)
        print(f'Row id added')


    def delete_row_by_id(self, table, id_):
        name_table = self.read_table(name_table)

        stmt = (
            db.delete(name_table).
            where(students.c.id_ == id_)
            )
        self.connection.execute(stmt)
        print(f'Row id {id_} deleted')

    def select_table(self, name_table):
        name_table = self.read_table(name_table)
        stm = db.select([name_table])
        return self.connection.execute(stm).fetchall()
    
    def get_tables(self):
        return self.engine.table_names()
    

def dataToDB(df):
    database = DataBase('games')
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    database.create_table(f'games_{date}', title = db.String, release = db.String, price = db.String, image = db.String, note = db.String)

    for i in range(len(df)):
        database.add_row(f'games_{date}', title=df.title[i], release=df.release[i], price=df.price[i], image=df.image[i], note=df.note[i])



def steam_scrap():
    
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    BASE_URL = "https://store.steampowered.com/search/?term=action"    

    driver.get(BASE_URL)

    for i in range(41):
        ActionChains(driver).scroll_by_amount(0, 3000).perform()
        time.sleep(0.8)

    list_games = driver.find_elements(By.ID, "search_resultsRows")
    
    list_games = list_games[0].find_elements(By.TAG_NAME, "a")

    json_list = [] 

    for i in range(len(list_games)):

        try:
            title = list_games[i].find_element(By.CLASS_NAME, "title").text
        except:
            title = ''
        try:
            release = list_games[i].find_element(By.CLASS_NAME, "search_released").text
        except:
            release = ''
        try:
            price = list_games[i].find_element(By.CLASS_NAME, "discount_final_price").text
        except:
            price = ''
        try:
            image = list_games[i].find_element(By.TAG_NAME, "img").get_attribute("src")
        except:
            image = ''
        try:
            note = list_games[i].find_element(By.CLASS_NAME, "search_review_summary").get_attribute("data-tooltip-html")
        except:
            note = ''

        json_list.append({"title":title, "release":release, "price":price, "image":image, "note":note})

    driver.quit()

    df_games = pd.DataFrame(json_list)

    return df_games



def assistant(text):
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": "Tu es maintenant un expert jeux vidéo, je te donnerais un nom de jeux et tu me diras ses informations et également ses différents prix dans le passé."
            },
            {
            "role": "user",
            "content": text
            }
        ],
        temperature=0.3,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        return response['choices'][0]['message']["content"]