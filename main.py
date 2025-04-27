from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
from collections import defaultdict
from pprint import pprint


excel_data_df = pandas.read_excel('wine.xlsx', sheet_name='Лист1', na_values='', keep_default_na=False)
excel_data_df = excel_data_df.fillna('')
categorized_wine = defaultdict(list)


def process_row(row):
    category = row['Категория']
    wine_info = {
        'Название': row['Название'],
        'Цена': row['Цена'],
        'Картинка': row['Картинка'],
        'Акция': row['Акция']
    }
    categorized_wine[category].append(wine_info)


excel_data_df.apply(process_row, axis=1)


event1 = datetime.date.today()
event2 = datetime.date(year=1920, month=1, day=1)
delta = event1-event2
years = delta.days // 365


def get_years_label(years):
    if years % 100 in (11, 12, 13, 14):
        return "лет"
    last_digit = years % 10
    if last_digit == 1:
        return "год"
    elif last_digit in (2, 3, 4):
        return "года"
    else:
        return "лет"
    

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)


template = env.get_template('template.html')


rendered_page = template.render(
    date1_text=years,
    year_form1_text=get_years_label(years),
    categorized_wine=categorized_wine
)


with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)


server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
