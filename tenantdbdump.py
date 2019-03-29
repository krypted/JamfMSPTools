#
#
# Exports the contents of a flat sql dump to csv files with the name of the table.csv and a xls representation of the database
# Requires Python 3.7 (from a Mac, first - brew install python3)
#      Prior to running python3 -m pip install pandas
#      Prior to running python3 -m pip install openpyxl
# Usage python3 sqlcsvxlsexport.py <sql dump file> <target directory>
# Send accolades for the script to krypted@me.com or hatemail to <devnull>
#
#
import re
import csv
import sys
import os.path
import argparse
import pandas as pd

PATTERN = '_binary.*?\',\''


# allow large content in the dump
csv.field_size_limit(sys.maxsize)

def is_insert(line):
    return 'INSERT INTO' in line or False


def get_values(line):
    return line.partition(' VALUES ')[2]

def get_table_name(line):
    match = re.search('INSERT INTO `([0-9_a-zA-Z]+)`', line)
    if match:
        return match.group(1)
    else:
        print(line)

def get_columns(line):
    match = re.search('INSERT INTO `.*` \(([^\)]+)\)', line)
    if match:
        return list(map(lambda x: x.replace('`', '').strip(), match.group(1).split(',')))

def values_sanity_check(values):
    assert values
    assert values[0] == '('
    # Assertions have not been raised
    return True

def parse_values_2(values):
    rows = []
    latest_row = []

    reader = csv.reader([values], delimiter=',',
                        doublequote=False,
                        escapechar='\\',
                        quotechar="'",
                        strict=True
    )

    for reader_row in reader:
        for column in reader_row:
            if ',' not in column:
                return [column[1:-1]]
            if len(column) == 0 or column == 'NULL':
                latest_row.append(chr(0))
                continue
            if column[0] == "(":
                new_row = False
                if len(latest_row) > 0:
                    if latest_row[-1][-1] == ")":
                        latest_row[-1] = latest_row[-1][:-1]
                        new_row = True
                if new_row:
                    latest_row = ['' if field == '\x00' else field for field in latest_row]
                    rows.append(latest_row)
                    latest_row = []
                if len(latest_row) == 0:
                    column = column[1:]
            latest_row.append(column)
        if latest_row[-1][-2:] == ");":
            latest_row[-1] = latest_row[-1][:-2]
            latest_row = ['' if field == '\x00' else field for field in latest_row]

            rows.append(latest_row)

        return rows

def parse_values(values):
    rows = []
    latest_row = []

    reader = csv.reader([values], delimiter=',',
                        doublequote=False,
                        escapechar='\\',
                        quotechar="'",
                        strict=True
    )

    for reader_row in reader:
        for column in reader_row:
            if len(column) == 0 or column == 'NULL':
                latest_row.append(chr(0))
                continue
            if column[0] == "(":
                new_row = False
                if len(latest_row) > 0:
                    if latest_row[-1][-1] == ")":
                        latest_row[-1] = latest_row[-1][:-1]
                        new_row = True
                if new_row:
                    latest_row = ['' if field == '\x00' else field for field in latest_row]

                    rows.append(latest_row)
                    latest_row = []
                if len(latest_row) == 0:
                    column = column[1:]
            latest_row.append(column)
        if latest_row[-1][-2:] == ");":
            latest_row[-1] = latest_row[-1][:-2]
            latest_row = ['' if field == '\x00' else field for field in latest_row]

            rows.append(latest_row)

        return rows




def main(filepath, output_folder):
    dataframes = {}

    with open(filepath, 'rb') as f:
        #with codecs.open(file_name, "r", encoding='utf-8', errors='ignore') as
        for line in f.readlines():
            try:
                line = line.decode('utf8')



                if is_insert(line):
                    table_name = get_table_name(line)
                    columns = get_columns(line)
                    values = get_values(line)
                    if values_sanity_check(values):
                        rows = parse_values(values)
                        if rows and len(rows[0]) != len(columns):
                            print(str(len(rows[0])) + ' - ' + str(len(columns)) + ' : ' + table_name)

                    if table_name not in dataframes.keys():
                        df_to_add = pd.DataFrame(rows, columns=columns)
                        dataframes[table_name] = df_to_add
                    else:
                        df_to_add = pd.DataFrame(rows, columns=columns)
                        dataframes[table_name] = dataframes[table_name].append(df_to_add, ignore_index=True)

                    if not os.path.isfile(output_folder + table_name + '.csv'):
                        with open(output_folder + table_name + '.csv', 'w') as outcsv:
                            writer = csv.writer(outcsv, quoting=csv.QUOTE_ALL)
                            writer.writerow(columns)
                            for row in rows:
                                writer.writerow(row)
                    else:
                        with open(output_folder + table_name + '.csv', 'a') as outcsv:
                            writer = csv.writer(outcsv, quoting=csv.QUOTE_ALL)
                            for row in rows:
                                writer.writerow(row)
            except UnicodeDecodeError:
                line = str(line)
                table_name = get_table_name(line)
                columns = get_columns(line)
                line = line.split('VALUES ')[1].strip()

                line = line[:-3]
                values = line[1:-3].split('),(')

                for value in values:
                    tmp_value = value
                    start_idx = 0
                    tmp_fields = []
                    quitted = False
                    binary_end = len(value)
                    while 'binary' in tmp_value:

                        first_binary = re.search(PATTERN, tmp_value[start_idx:])
                        if not first_binary:
                            tmp_fields.append(tmp_value)
                            quitted = True
                            break
                        binary_start, binary_end = first_binary.span()

                        tmp_fields += parse_values_2('(' + tmp_value[start_idx:binary_start - 1] + ')')
                        tmp_fields.append(first_binary.group()[:-5])
                        start_idx = binary_end
                        tmp_value = tmp_value[binary_end:]

                    if binary_end != len(value) and not quitted:
                        splitted = tmp_value.split("','")
                        tmp_fields += splitted

    writer = pd.ExcelWriter(output_folder + 'database.xls', engine='openpyxl')
    for table in dataframes.keys():
        dataframes[table].to_excel(writer, table[:30], index=False)
    writer.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert sqldump to csv')

    parser.add_argument('sql_filepath', action="store", type=str)
    parser.add_argument('output_dir', action="store", default='.', type=str)

    args = parser.parse_args()

    file_path = args.sql_filepath
    out_dir = args.output_dir if args.output_dir.endswith('/') else args.output_dir + '/'

    main(file_path, out_dir)
