import sys
import functools
import inspect

def lmap(x, y):
    return list(map(x, y))

# SECTION parse data into a table of floats

file = open('data.csv')
all_lines = file.readlines()
# ignore the header row and trailing whitespace rows
rows = list(filter(lambda line : not line.isspace(), all_lines[1:]))
num_rows = len(rows)

if(num_rows <= 1):
    print("No data provided. All mins, max, avgs are undefined.")
    sys.exit()

# ignore the date/time column
table_strings = lmap(lambda row : row.split(',')[1:], rows)
# blank cells are treated as None and handled carefully
table = lmap(lambda row: lmap(lambda col: float(col) if not col.isspace() and col != '' else None, row), table_strings)
num_cols = len(table[0])

# SECTION calculate aggregations

def min(list):
    return functools.reduce(lambda old, new: new if new != None and new < old else old, list)

def max(list):
    return functools.reduce(lambda old, new: new if new != None and new > old else old, list)

def sum(list):
    return functools.reduce(lambda old, new : (new if new != None else 0) + (old if old != None else 0), list)

def count_empty(list):
    return functools.reduce(lambda sum, new: sum + (1 if new is None else 0), [0] + list)

min_per_host = lmap(min, table)
max_per_host = lmap(max, table)
sum_per_host = lmap(sum, table)
real_cols_per_host = lmap(lambda row: num_cols - count_empty(row), table)
avg_per_host = lmap(lambda tuple : tuple[0] / tuple[1], zip(sum_per_host, real_cols_per_host))

min_total = min(min_per_host)
max_total = max(max_per_host)
sum_total = sum(sum_per_host)
real_cols = sum(real_cols_per_host)
avg_total = sum_total / real_cols

# SECTION format output strings

def format_list(string_list):
    return ', '.join(lmap(lambda str: "{:.2f}".format(str), string_list))

flat_output = inspect.cleandoc("""
min_per_host: {}
max_per_host: {}
avg_per_host: {}

min_total: {:.2f}
max_total: {:.2f}
avg_total: {:.2f}
""").format(
    format_list(min_per_host),
    format_list(max_per_host),
    format_list(avg_per_host),
    min_total,
    max_total,
    avg_total
)

json_output = inspect.cleandoc("""
{{
    "min_per_host": [{}],
    "max_per_host": [{}],
    "avg_per_host": [{}],
    "min_total": {:.2f},
    "max_total": {:.2f},
    "avg_total": {:.2f}
}}
""").format(
    format_list(min_per_host),
    format_list(max_per_host),
    format_list(avg_per_host),
    min_total,
    max_total,
    avg_total
)

with open('output.txt', 'w') as output:
    print("FLAT\n\n" + flat_output + '\n\nJSON\n\n' + json_output, file = output)