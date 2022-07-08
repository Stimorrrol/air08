import psycopg2
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

###################
### БАЗы ДАННЫХ ###
###################

def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT flight_id, flight_no, scheduled_departure, scheduled_arrival, departure_airport, arrival_airport, status, aircraft_code FROM bookings.flights;")


df = pd.DataFrame(rows, columns = ['flight_id', 'flight_no', 'scheduled_departure', 'scheduled_arrival', 'departure_airport', 'arrival_airport', 'status', 'aircraft_code'])


#Наименование Web-сайта
st.title("Авиация")

def get_unique_flight(df):
    """
    Функция преобразует столбец aircraft_code в тип лист,
    с целью далнейшего использования в st.multiselect
    """
    unique_teams = np.unique(df.aircraft_code).tolist()
    return unique_teams

#Виджет множественного выбора самолёта
aircraft_code = st.multiselect( "Вид самолёта: " , get_unique_flight(df))

#Текст под виджетом, считающий количество выбранных позиций
st.write( "Выбрано" , len (aircraft_code))

def get_air (df, aircraft_code):
    """
    Функция, связывающая множественный выбор (выбор самолёта) с датафреймом.
    Т.е. в датафрейме выводятся отфильтрованные по множественному выбору строки
    """
    un = df.loc[df['aircraft_code'].isin(aircraft_code)]
    return un

#Подзаголовок таблицы с данными рейсов
st.subheader("Таблица с данными рейсов")

#Таблица с данными рейсов (датафрейм)
st.dataframe(get_air (df, aircraft_code))


a = pd.DataFrame(get_air (df, aircraft_code)).groupby('aircraft_code').count().reset_index()
ar = a[['aircraft_code','flight_id']]

#Подзаголовок таблицы с данными рейсов
st.subheader("Количество рейсов, выполненное каждым самолётом")

#График
c = alt.Chart(ar).mark_bar().encode(x = 'aircraft_code', y = 'flight_id')
st.altair_chart(c, use_container_width=True)
