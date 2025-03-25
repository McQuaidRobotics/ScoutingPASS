import csv

def parse_scanner_output(scanner_output):
    data = scanner_output.strip('"').split('""')

    if len(data) < 15:
        print("Error: Input does not have enough fields.")
        return None, None, None


    tele_15 = data[15].strip('"')
    tele_16 = data[16].strip('"')
    tele_15_values = tele_15.split(',')
    tele_16_values = tele_16.split(',')
    teleop_values = []

    for i in range(max(len(tele_15_values), len(tele_16_values))):
        row = data[:6]
        row.append(i)
        if i < len(tele_15_values):
            row.append(tele_15_values[i])
        if i < len(tele_16_values):
            row.append(tele_16_values[i])
        teleop_values.append(row)
    other_values = data[:6]

    return data, teleop_values, other_values

def is_unique_row(filename, row):
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            for existing_row in reader:
                if existing_row[1:6] == row[1:6]:
                    return False
    except FileNotFoundError:
        return True
    return True

def write_to_csv(filename, rows):
    rows = [[value.strip('"') for value in row] for row in rows]
    try:
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
            writer.writerows(rows)
    except Exception as e:
        print(f"Error writing to file {filename}: {e}")

if __name__ == "__main__":
    while True:
        user_input = input("Scan data or type 'exit' to quit: ")
        if user_input.lower() == "exit":
            break

        full_data, teleop_data, other_data = parse_scanner_output(user_input)

        if full_data:
            if is_unique_row("full.csv", full_data):
                write_to_csv("full.csv", [full_data])
                write_to_csv("teleop.csv", teleop_data)
                write_to_csv("other.csv", [other_data])
                print("Data successfully written to CSV files.")
            else:
                print("Duplicate row found, skipping write.")
        else:
            print("Invalid input format. Please try again.")
