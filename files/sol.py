import re
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

def parse_hocr(path):
    with open(path, 'r', encoding='utf-8') as file:
        return BeautifulSoup(file, 'html.parser')

def extract_text_positions(soup):
    data = []
    for span in soup.find_all(class_=['ocrx_word']):
        title = span.get('title', '')
        coords = re.findall(r'bbox (\d+) (\d+) (\d+) (\d+)', title)
        if coords:
            x1, y1, x2, y2 = map(int, coords[0])
            text = span.get_text().strip()
            if text:
                data.append({'text': text, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})
    return data

def order_data(data):
    return sorted(data, key=lambda item: (item['y1'], item['x1']))

def group_into_rows(data, y_tolerance=10):
    rows = []
    current_row = []
    last_y = None

    for item in data:
        if last_y is None or abs(item['y1'] - last_y) <= y_tolerance:
            current_row.append(item)
        else:
            rows.append(current_row)
            current_row = [item]
        last_y = item['y1']
    if current_row:
        rows.append(current_row)
    return rows

def detect_columns(rows, x_tolerance=30):
    """Encuentra las posiciones de columna más comunes."""
    x_positions = []
    for row in rows:
        for cell in row:
            x_positions.append(cell['x1'])
    x_positions = sorted(x_positions)
    
    # Agrupamos valores cercanos en rangos
    columns = []
    current_group = [x_positions[0]]
    for x in x_positions[1:]:
        if abs(x - np.mean(current_group)) <= x_tolerance:
            current_group.append(x)
        else:
            columns.append(int(np.mean(current_group)))
            current_group = [x]
    columns.append(int(np.mean(current_group)))
    return columns

def clean_and_normalize_table(table):
    # Elimina filas vacías o casi vacías
    cleaned = [row for row in table if sum(1 for cell in row if cell.strip()) > 1]
    # Encuentra el máximo número de columnas
    max_cols = max(len(row) for row in cleaned)
    # Normaliza el número de columnas
    normalized = [row + [''] * (max_cols - len(row)) for row in cleaned]
    return normalized

def build_csv(rows, output_path='output.csv', x_tolerance=30):
    columns = detect_columns(rows, x_tolerance)
    table = []

    for row in rows:
        line = [''] * len(columns)
        for cell in row:
            x = cell['x1']
            idx = min(range(len(columns)), key=lambda i: abs(columns[i] - x))
            if line[idx]:
                line[idx] += ' ' + cell['text']
            else:
                line[idx] = cell['text']
        table.append(line)

    # Limpieza y normalización
    table = clean_and_normalize_table(table)

    df = pd.DataFrame(table)
    df.to_csv(output_path, index=False, header=False)
    print(f"CSV generado: {output_path}")

def hocr_to_csv(input_path, output_path='output.csv'):
    soup = parse_hocr(input_path)
    data = extract_text_positions(soup)
    ordered = order_data(data)
    rows = group_into_rows(ordered)
    build_csv(rows, output_path)

if __name__ == '__main__':
    names = ['1C_5.hocr', '1E_1.hocr', '3T_4.hocr']
    for name in names:
        hocr_input = './hocr_files/' + name
        csv_output = './csv_files/' + name + '.csv'
        hocr_to_csv(hocr_input, csv_output)
