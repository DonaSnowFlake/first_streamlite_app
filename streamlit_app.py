import pandas
import streamlit
import snowflake.connector
import requests
from urllib.error import URLError

streamlit.title (' My Parents New Healty Dinner')
streamlit.header ('Breakfast Menu')
streamlit.text ('🐔 Omlet')
streamlit.text ('🥣  Bluberry Oatmeal')
streamlit.text ('🍌🥭🥑 Fruits')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
#streamlit.dataframe(my_fruit_list)

#let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Apple'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page 
#streamlit.dataframe(my_fruit_list)

streamlit.dataframe(fruits_to_show)

#create function 
def get_fruityvice_data(this_fruit_choice):
    #streamlit.write('The user entered ', fruit_choice)
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
            fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
            return fruityvice_normalized
        
streamlit.header("Fruityvice Fruit Advice!") 
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
                        streamlit.error("Please select a fruit to get info. ")
    else:
        back_from_function=get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
        
except URLError as e:
  streamlit.error()

#don't run anithybg past here while we troubleshout
#streamlit.stop()
streamlit.header("The fruit load list contains:")
#snowFlake related functions
def get_fruit_load_list():
     with my_cnx.cursor() as my_cur:
          my_cur.execute("SELECT * FROM fruit_load_list")
     return my_cur.fetchall()
#add button to load the fruit
if streamlit.button ('Get Fruit Load List'):
    # connect to snowflake database
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

fruit_search = streamlit.text_input('What fruit would you like ito add?','bannana')

#Allow the end user to add a fruit to a list 
#my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit');")
