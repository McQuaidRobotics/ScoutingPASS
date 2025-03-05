import csv

def parse_scanner_output(scanner_output):
    data = scanner_output.strip('"').split('""')

    if len(data) < 14:
        print("Error: Input does not have enough fields.")
        return None, None, None


    tele_12 = data[12].strip('"')
    tele_13 = data[13].strip('"')
    tele_12_values = tele_12.split(',')
    tele_13_values = tele_13.split(',')
    teleop_values = []

    for i in range(max(len(tele_12_values), len(tele_13_values))):
        row = data[:6]
        if i < len(tele_12_values):
            row.append(tele_12_values[i])
        if i < len(tele_13_values):
            row.append(tele_13_values[i])
        teleop_values.append(row)
    other_values = data[:6] + [data[7]] + data[7:12] + data[14:]

    return data, teleop_values, other_values

def write_to_csv(filename, rows):
    rows = [[value.strip('"') for value in row] for row in rows]
    try:
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
            writer.writerows(rows)
            file.close()
    except Exception as e:
        print(f"Error writing to file {filename}: {e}")

if __name__ == "__main__":
    while True:
        user_input = input("Scan data or type 'exit' to quit: ")
        if user_input.lower() == "exit":
            break

        full_data, teleop_data, other_data = parse_scanner_output(user_input)

        if full_data:
            write_to_csv("full.csv", [full_data])
            write_to_csv("teleop.csv", teleop_data)
            write_to_csv("other.csv", [other_data])
            print("Data successfully written to CSV files.")
        else:
            print("Invalid input format. Please try again.")
