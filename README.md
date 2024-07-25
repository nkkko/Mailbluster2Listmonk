# Mailbluster2Listmonk

## Overview

The `Mailbluster2Listmonk` project is a powerful script designed to consolidate multiple CSV files from Mailbluster, filter critical information, clean data, and prepare it for import into [Listmonk](https://github.com/knadh/listmonk).

Listmonk is a high performance, self-hosted, newsletter and mailing list manager with a modern dashboard. Single binary app.

This script not only merges and filters data but also provides options to split the resulting file into multiple chunks, ensuring manageability and ease of use.

## Features

- **CSV File Consolidation**: Merges multiple CSV files into a single, cohesive file.
- **Subscription Filter**: Only includes rows where the subscription status is `TRUE`.
- **Data Cleaning**: Handles edge cases in data, ensuring names are correctly parsed and attribute fields are not inserted with `NaN` values.
- **Progress Tracking**: Implements a progress bar using `tqdm` to track the processing of files.
- **File Splitting**: Optionally splits the resulting CSV into multiple smaller files based on user input.

## Requirements

- Python 3.x
- Pandas
- Tqdm
- Numpy
- Json

Install the required Python libraries using:
```sh
pip install pandas tqdm numpy
```

## File Structure

```
Mailbluster2Listmonk/
│
├── export/                     # Directory containing input CSV files
│   ├── exported-leads_1.csv
│   ├── exported-leads_2.csv
│   └── ...
├── combined-exported-leads.csv # Output consolidated CSV file (if split is not used)
├── script.py                   # Main script file
└── README.md                   # Project documentation
```

## Usage

1. **Directory Setup**:
    - Ensure your input CSV files are placed in the `export` directory.

2. **Running the Script**:
    - Navigate to the directory containing `script.py`.
    - Run the script using Python:

    ```sh
    python script.py [--split <number_of_files>]
    ```

    - **Arguments**:
      - `--split`: Optional argument to specify the number of resulting CSV files. If omitted, the script will produce a single consolidated file.

    **Example**:
    ```sh
    python script.py --split 3
    ```

## Script Explanation

### Libraries

- **os**: For directory and path handling.
- **pandas**: For CSV file manipulation.
- **json**: For creating JSON attribute structures.
- **tqdm**: For displaying progress bars.
- **argparse**: For parsing command-line arguments.
- **numpy**: For handling NaN values.

### Key Functions

1. **`clean_name(first_name, last_name, full_name)`**:
    - Cleans and parses names ensuring no '0' values for last names and correctly handles full names in the first name field.

2. **`generate_attributes(row)`**:
    - Generates a JSON structure for the attributes while excluding any fields that contain `NaN` values.

3. **`split_dataframe(df, num_splits)`**:
    - Splits a DataFrame into the specified number of smaller DataFrames.

4. **`save_splitted_files(dfs, base_filename)`**:
    - Saves the smaller DataFrames into individual CSV files.

5. **`process_files(directory, split=None)`**:
    - Main function to process files in the `export` directory, perform filtering and data cleaning, and generate the consolidated CSV file. Handles file splitting if the `split` argument is provided.

### Main Execution

The script's entry point parses command-line arguments, specifies the directory containing CSV files, and calls the `process_files` function.

```python
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and combine CSV files.")
    parser.add_argument("--split", type=int, default=None,
                        help="Number of files to split the combined CSV into.")
    args = parser.parse_args()
    export_directory = "export"
    process_files(export_directory, args.split)
```

## Contributing

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new features'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
