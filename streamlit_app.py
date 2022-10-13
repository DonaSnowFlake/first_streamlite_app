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

streamlit.header("Fruityvice Fruit Advice!") 
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
                        streamlite.error("Please select a fruit to get info. ")
    else:
      
            #streamlit.write('The user entered ', fruit_choice)
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
            #streamlit.text(fruityvice_response.json()) #wites data to screen as a json
            # wtakes the json and normalise it 
            fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
            # output the data as table
            streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlite.error()

#don't run anithybg past here while we troubleshout
streamlite.stop()

# connect to snowflake database
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

fruit_search = streamlit.text_input('What fruit would you like ito add?','bannana')

#Allow the end user to add a fruit to a list 
#my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlite');")
