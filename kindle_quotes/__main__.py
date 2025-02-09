import json
import logging
import os
import platform
import random
import textwrap
import sys
from datetime import datetime
import click


MY_CLIPPINGS = 'My Clippings.txt'
HISTORY_FILE = 'data/quotes_history.txt'
QUOTE_FILE = 'data/quotes.json'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger(__name__)


def get_quotes(clippings_path: str) -> list[list[str]]:
    if not os.path.exists(clippings_path):
        log.error(f'File not found: {clippings_path}')
        sys.exit(1)

    with open(clippings_path, encoding='utf-8') as f:
        content = '\n'.join(line for line in f.read().strip().split('\n')[:-1] if line)

    content = content.split('==========\n')
    quotes = [item.strip().split('\n') for item in content
              if '- Your Highlight on ' in item]

    return quotes


def parse_quote(item: list[str]) -> dict:
    quote = {}
    book = item[0].split(' (')
    quote['title'] = ' ('.join(book[:-1])
    quote['authors'] = book[-1].strip(')').split(';')
    info = item[1].split(' | ')
    quote['location'] = ' '.join(info[0].split(' ')[-2:])
    quote['added_on'] = datetime.strptime(
        info[-1].replace('Added on ', ''),
        '%A, %B %d, %Y %I:%M:%S %p').strftime(DATE_FORMAT)
    quote['quote'] = item[2].replace('\xa0', ' ')

    return quote


def dump_quotes(data: list[dict], file_path: str = QUOTE_FILE) -> None:
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=True, indent=2)
    log.info(f'Quotes exported to {file_path}')


def load_quotes(file_path: str = QUOTE_FILE) -> list[dict]:
    if not os.path.exists(file_path):
        log.error(f'File not found: \"{file_path}\"')
        sys.exit(1)

    with open(file_path, encoding='utf-8') as f:
        try:
            quotes = json.load(f)
        except json.JSONDecodeError:
            log.error(f'Invalid JSON file: \"{file_path}\"')
            sys.exit(1)

    if not quotes:
        log.warning('No quotes found.')
        sys.exit(0)

    return quotes


def get_history(history_file_path: str = HISTORY_FILE) -> list[tuple[datetime, int]]:
    history = []
    if os.path.exists(history_file_path):
        with open(history_file_path, encoding='utf-8') as f:
            for line in f:
                date_str, index = line.strip().split(', ')
                date = datetime.strptime(date_str, DATE_FORMAT)
                history.append((date, int(index)))

    return history


def append_index_to_history(index: int) -> None:
    with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
        f.write(f'{datetime.now().strftime(DATE_FORMAT)}, {index}\n')


def reset_history() -> None:
    if not os.path.exists(HISTORY_FILE):
        return

    import shutil
    shutil.copy(HISTORY_FILE, f'{HISTORY_FILE}.bak')
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        f.write('')
    log.info('History reset.')


def get_random_quote(quotes: list[dict]) -> dict:
    history = get_history()
    if len(quotes) == len(history):
        log.warning('All quotes have been shown.')
        reset_history()

    for _ in range(len(quotes)):
        index = random.randint(0, len(quotes) - 1)
        if index in history:
            continue

        append_index_to_history(index)
        return quotes[index]

    return {}


def simple_quote(item: dict) -> str:
    return '\n\n'.join(
        [textwrap.fill(paragraph, width=90)
        for paragraph in item['quote'].split('\n\n')]
    ) + '\n\n' + item['title'] + ' (' + ', '.join(item['authors']) + ')'


def get_clippings_path() -> str:
    user = os.environ.get('USER')
    MAC_PATH = f'/Volumes/Kindle/documents/{MY_CLIPPINGS}'
    LINUX_PATH = f'/run/media/{user}/Kindle/documents/{MY_CLIPPINGS}'

    match platform.system():
        case 'Darwin':
            return MAC_PATH
        case 'Linux':
            return LINUX_PATH
        case _:
            current_dir = os.getcwd()
            log.error('Cannot autodetect Kindle clippings path.' \
                      f'Using current directory \"{current_dir}/{MY_CLIPPINGS}\"')
            return MY_CLIPPINGS


def validate_query_key(key: str) -> str:
    if key == 'author':
        key = 'authors'
    elif key == 'book':
        key = 'title'

    valid_keys = ['title', 'authors', 'quote']
    if key not in valid_keys:
        log.error(f"Invalid key. Choose from: {', '.join(valid_keys)}")
        sys.exit(1)

    return key


@click.command()
@click.option('--my-clippings', default='', help='Path to My Clippings file')
def export_kindle_quotes(my_clippings: str = '', export_file: str = '') -> None:
    if not my_clippings:
        my_clippings = get_clippings_path()
    dump_quotes([parse_quote(quote) for quote in get_quotes(my_clippings)],
              file_path=export_file)


@click.command()
@click.option('--format', default='simple', help='Output format: "simple" or "raw"')
def show_quote(format: str = 'simple') -> None:
    quotes = load_quotes()
    quote = get_random_quote(quotes)
    if format == 'simple':
        print(simple_quote(quote))
        return

    print(quote)


@click.command
@click.option('--author', default='', help='Author name')
@click.option('--book', default='', help='Book title')
@click.option('--quote', default='', help='Quote text')
@click.option('--format', default='simple', help='Output format: "simple" or "raw"')
def find_quote(format: str = 'simple', author: str = '', book: str = '', quote: str = '') -> None:
    if not any([author, book, quote]):
        log.error('No query parameters provided.')
        log.info('At least one of the following is required: author, book, quote')
        sys.exit(1)

    author = author.strip().lower()
    book = book.strip().lower()
    quote = quote.strip().lower()

    quotes = load_quotes()
    filtered_quotes = [
        item for item in quotes if (
            (not author or author in ' '.join(item['authors']).lower()) and
            (not book or book in item['title'].lower()) and
            (not quote or quote in item['quote'].lower())
        )
    ]

    if not filtered_quotes:
        log.info('No quotes found.')
        sys.exit(0)

    if format == 'simple':
        for item in filtered_quotes:
            print('---')
            print(simple_quote(item), end='\n\n')
        return

    print(filtered_quotes)


@click.group()
def cli() -> None:
    pass


cli.add_command(export_kindle_quotes)
cli.add_command(find_quote)
cli.add_command(show_quote)


if __name__ == '__main__':
    cli()
