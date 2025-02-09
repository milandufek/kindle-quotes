# Kindle Quotes

This is a simple Python script that extracts your Kindle highlights from the `My Clippings.txt` file and saves them in a json file.
Then you can search in the json file for a specific book or author, or generate quote of the day.

## Installation

1. Clone the repository
2. Install the requirements

```bash
poetry install
```

## Usage

To extract the quotes from the `My Clippings.txt` file if Kindle is connected on Mac and Linux the file is autodetected. Or specify the path to file. Run the following command:

```bash
python3 kindle_quotes export-kindle-quotes --my-clippings <path-to-my-clippings-file>
```

Quote of the day, shows a random quote from the json file and tracks the quotes that have been shown.

```bash
python3 kindle_quotes show-quote
```

To search for a specific book, author or quote run the command below. The search is case insensitive. Multiple search terms can be used. The format of the output can be `raw` or `simple` (default).

```bash
python3 kindle_quotes find-quote --book <book-name-part>
python3 kindle_quotes find-quote --author <author-name> --format raw
python3 kindle_quotes find-quote --author <author-name> --qoute <quote-part>
python3 kindle_quotes find-quote --help
```
