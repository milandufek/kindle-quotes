import os
from kindle_quotes.__main__ import parse_quote, get_quotes


def test_get_quotes() -> None:
    test_file = 'files/test_clippings.txt'
    os.chdir(os.path.dirname(__file__))
    expected_quotes = [
        [
            "John Wick (John Wick;Baba Yaga)",
            "- Your Highlight on Page 17 | Location 311-313 | Added on Saturday, February 8, 2024 10:41:17 PM",
            "Est adipisci eius tempora aliquam amet. Sed labore aliquam sit labore. Aliquam quisquam sed magnam ipsum etincidunt non amet. Porro ut aliquam etincidunt etincidunt. Porro ut modi consectetur numquam dolore voluptatem tempora. Non dolor dolorem ut. Eius neque quaerat adipisci quisquam ipsum modi quiquia. Sed etincidunt sit dolor etincidunt adipisci aliquam sit. Adipisci quisquam ipsum aliquam."
        ],
        [
            "Lorem Ipsum (1st edition) (Špaček, Karel)",
            "- Your Highlight on Page 18 | Location 322-324 | Added on Saturday, February 8, 2024 10:45:05 PM",
            "Consectetur neque adipisci tempora modi magnam numquam. Dolore porro etincidunt dolor dolor modi non tempora. Ipsum ipsum est numquam \"etincidunt\" sit. Velit aliquam etincidunt numquam. Sit dolorem quiquia quisquam. Etincidunt dolorem modi sit tempora dolore tempora ipsum."
        ]
    ]
    assert get_quotes(test_file) == expected_quotes


def test_parse_quote() -> None:
    quote = [
        "Factfulness Illustrated: Ten Reasons We're Wrong About the World - Why Things are Better than You Think (Rosling, Hans;Rosling, Ola;Rosling Rönnlund, Anna)",
        "- Your Highlight on Location 2251-2252 | Added on Sunday, January 7, 2024 9:28:14 AM",
        "To control the destiny instinct, stay open to new data and be prepared to keep freshening up your knowledge."
    ]
    expected = {
        'title': 'Factfulness Illustrated: Ten Reasons We\'re Wrong About the World - Why Things are Better than You Think',
        'quote': 'To control the destiny instinct, stay open to new data and be prepared to keep freshening up your knowledge.',
        'added_on': '2024-01-07 09:28:14',
        'authors': ['Rosling, Hans', 'Rosling, Ola', 'Rosling Rönnlund, Anna'],
        'location': 'Location 2251-2252',
    }
    assert parse_quote(quote) == expected
