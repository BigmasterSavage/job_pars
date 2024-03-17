import streamlit as st
from src.func import fetch_and_parse_hh_ru_cities, table


col_1, col_2 = st.columns([3, 1])
with col_1:
    st.title("Парсер вакансий")
with col_2:
    st.image("style/sky_logo_new.png", width=100)

st.sidebar.header("Фильтры")

# ----------------- Фильтр города ----------------
location_list = ["Не выбрано"] + sorted(fetch_and_parse_hh_ru_cities())
toggle_location = st.sidebar.toggle("Город, регион")
if toggle_location:
    location_choice = st.sidebar.selectbox("Город, регион",
                                           location_list,
                                           index=location_list.index("Не выбрано"),
                                           placeholder="Не выбрано"
                                           )
    st.session_state.selection = location_choice
    location = st.session_state.selection
else:
    location = "Не выбрано"

if location is not None:
    st.write("Город:", location)
else:
    st.write("Город:", "Не выбрано")

# ----------------- Фильтр зарплаты ----------------
toggle_salary = st.sidebar.toggle("Зарплата (от)")
if toggle_salary:
    salary_in = st.sidebar.number_input("Зарплата (от)", value=None, placeholder="Введите зарплату...")
    st.session_state.selection = salary_in
    salary = st.session_state.selection
else:
    salary = None

if salary is not None:
    st.write("Желаемая зарплата от:", salary)
else:
    st.write("Желаемая зарплата от:", "Не выбрано")

# ----------------- Фильтр график работы ----------------
toggle_experience = st.sidebar.toggle("Опыт работы")
if toggle_experience:
    experience_in = st.sidebar.radio("График работы",
                                   ["Нет опыта", "От 1 года до 3 лет", "От 3 до 6 лет", "Более 6 лет"],
                                   index=None)
    st.session_state.selection = experience_in
    experience = st.session_state.selection
else:
    experience = None

if experience is not None:
    st.write("Опыт работы:", experience)
else:
    st.write("Опыт работы:", "Не выбрано")


query = st.text_input("Введите запрос")
if query:
    try:
        df = table(query=query, location=location, salary=salary, experience=experience)
        st.write(df)
    except Exception as e:
        st.write(f"По вашему запросу нет вакансий!")




# Пока без отдельного файла CSS
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)