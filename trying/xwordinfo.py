import json
from bs4 import BeautifulSoup

html_content = ""
with open("example-crossword.html") as f:
    html_content = f.read()

def parse_crossword(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    crossword = {}

    # Parse grid
    grid_table = soup.find('table', {'id': 'PuzTable'})
    grid = []
    cell_numbers = {}  # Map of (row, col) to cell number
    for i, tr in enumerate(grid_table.find_all('tr')):
        row = []
        for j, td in enumerate(tr.find_all('td')):
            cell = {}
            if 'black' in td.get('class', []):
                cell['type'] = 'black'
            else:
                num_div = td.find('div', class_='num')
                letter_div = td.find('div', class_='letter')
                cell['type'] = 'white'
                cell['number'] = num_div.text if num_div else ''
                cell['letter'] = letter_div.text if letter_div else ''
                if cell['number']:
                    cell_numbers[(i, j)] = cell['number']
            row.append(cell)
        grid.append(row)

    num_rows = len(grid)
    num_cols = len(grid[0]) if grid else 0

    # Map clues to grid positions
    # First, we need to identify all the clues and their starting positions
    clue_numbers = {}  # Map of clue number to clue data
    clue_cells = {}    # Map of clue labels to list of cells

    # Initialize clue_cells for across and down clues
    for i in range(num_rows):
        for j in range(num_cols):
            cell = grid[i][j]
            if cell['type'] == 'white' and cell['number']:
                num = cell['number']
                # Check for across clue
                if j + 1 < num_cols and grid[i][j + 1]['type'] == 'white':
                    label = f"{num}A"
                    clue_cells[label] = []
                    x, y = i, j
                    while y < num_cols and grid[x][y]['type'] == 'white':
                        clue_cells[label].append((x, y))
                        y += 1
                # Check for down clue
                if i + 1 < num_rows and grid[i + 1][j]['type'] == 'white':
                    label = f"{num}D"
                    clue_cells[label] = []
                    x, y = i, j
                    while x < num_rows and grid[x][y]['type'] == 'white':
                        clue_cells[label].append((x, y))
                        x += 1

    # Parse clues
    def parse_clues(clue_section, direction):
        clues = []
        for numclue in clue_section.find_all('div', class_='numclue'):
            nums_and_texts = numclue.find_all('div')
            for idx in range(0, len(nums_and_texts), 2):
                num_div = nums_and_texts[idx]
                text_div = nums_and_texts[idx + 1]
                clue_number = num_div.text.strip()
                clue_text = text_div.text.strip()

                # Extract answer from clue_text
                if ':' in clue_text:
                    clue_part, answer_part = clue_text.split(':', 1)
                    clue_text_clean = clue_part.strip()
                    answer = answer_part.strip()
                else:
                    clue_text_clean = clue_text
                    answer = ''

                label = f"{clue_number}{direction}"
                cells = [(row + 1, col + 1) for row, col in clue_cells.get(label, [])]  # 1-based indexing
                clues.append({
                    "label": label,
                    "cells": cells,
                    "clue": clue_text_clean,
                    "answer": answer
                })
        return clues

    across_section = soup.find('div', {'id': 'ACluesPan'})
    down_section = soup.find('div', {'id': 'DCluesPan'})

    across_clues = parse_clues(across_section, 'A')
    down_clues = parse_clues(down_section, 'D')

    # Build the final JSON structure
    crossword['grid'] = grid
    crossword['across_clues'] = across_clues
    crossword['down_clues'] = down_clues

    # Output as JSON
    return json.dumps(crossword, indent=2)

# Call the function and print the JSON
crossword_json = parse_crossword(html_content)
print(crossword_json)
