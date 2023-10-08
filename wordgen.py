import requests
import sys
import random
import time

def progress_bar(completed, total, length=50):
    filled = int(completed * length / total)
    bar = '|' + '#' * filled + '-' * (length - filled) + '|'
    percent = f"{100 * completed // total}%"
    sys.stdout.write("\r" + bar + " " + percent)
    sys.stdout.flush()

def transform_word(word):
    transform_dict = {
        'a': '4',
        'e': '3',
        'i': '1',
        'o': '0',
        's': '5',
        'h': '#'
    }
    return ''.join([transform_dict.get(c, c) for c in word])

def get_synonyms(word):
    response = requests.get(f"https://api.datamuse.com/words?rel_syn={word}")
    words = response.json()
    return [item['word'] for item in words[:2]]

def add_special_chars(word):
    char_list = ['!', '@', '#', '$', '%', '^', '&', '*']

    total_chars = random.randint(1, 4)  # Total number of special characters (front + back) is between 1 and 4
    front_chars_count = random.randint(0, total_chars)  # Randomly select number of special characters for the front
    back_chars_count = total_chars - front_chars_count  # Remaining characters are for the back

    front_chars = ''.join(random.choices(char_list, k=front_chars_count))
    back_chars = ''.join(random.choices(char_list, k=back_chars_count))

    return front_chars + word + back_chars

def generate_passwords(inputs, special_chars, transform, use_synonyms, max_length, max_count=10000):
    base_passwords = inputs.copy()

    while len(base_passwords) < max_count:
        if use_synonyms:
            for word in other_words:
                base_passwords.extend(get_synonyms(word))

        if transform:
            transformed_passwords = [transform_word(word) for word in base_passwords]
            base_passwords += transformed_passwords

        if special_chars:
            special_char_passwords = [add_special_chars(word) for word in base_passwords]
            base_passwords += special_char_passwords

        for num in particular_numbers:
            base_passwords.extend([word + num for word in base_passwords])

        base_passwords = list(set(base_passwords))
        base_passwords = [pwd for pwd in base_passwords if len(pwd) <= max_length]
        random.shuffle(base_passwords)
        progress_bar(len(base_passwords), max_count)

    return base_passwords[:max_count]

if __name__ == "__main__":
    name = input("Enter name: ")
    lastname = input("Enter lastname: ")
    dob = input("Enter date of birth (e.g. 01Jan1990): ")
    spouse_name = input("Enter spouse's name: ")
    hometown = input("Enter hometown: ")
    phonenumber = input("Enter phone number: ")
    fathers_name = input("Enter father's name: ")
    first_born_name = input("Enter first born's name: ")
    other_words = input("Enter other related words (comma separated): ").split(',')
    particular_numbers = input("Any particular numbers? (separated by comma): ").split(',')

    inputs = [name, lastname, dob, spouse_name, hometown, phonenumber, fathers_name, first_born_name] + other_words

    special_chars = input("Include special characters? (yes/no): ").lower() == 'yes'
    transform = input("Use number-letter transformations? (yes/no): ").lower() == 'yes'
    use_synonyms = input("Include synonyms for other words? (yes/no): ").lower() == 'yes'
    max_length = int(input("Enter maximum password length: "))

    passwords = generate_passwords(inputs, special_chars, transform, use_synonyms, max_length)

    with open("list.txt", "w") as file:
        for password in passwords:
            file.write(password + "\n")

    print(f"\n\nGenerated and saved {len(passwords)} passwords to list.txt.")
