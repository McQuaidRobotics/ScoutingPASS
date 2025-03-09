import csv

def parse_scanner_output(scanner_output):
    data = scanner_output.strip('"').split('\t')
    print (data)
    # if len(data) < 14:
    #     print("Error: Input does not have enough fields.")
    #     return None, None, None

    return data

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

        data = parse_scanner_output(user_input)

        if data:
            write_to_csv("pitScouting.csv", [data])
            print("Data successfully written to CSV files.")
        else:
            print("Invalid input format. Please try again.")
