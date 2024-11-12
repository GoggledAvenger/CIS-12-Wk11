# Main Program of Lab09 - Book Cipher App

import json, os, random, re

BOOKS = 3
LINE = 120
PAGE = 64
pages = {}
line_window = {}
line_number = 0
char_window = []
page_number = 0

def clean_line(line):
    return line.strip().replace('-',' ') + ' '

def process_page(line, line_num):
    global line_window, pages, page_number
    line_window[line_num] = line
    if len(line_window) == PAGE:
        add_page()

def add_page():
    global line_window, pages, page_number, line_number
    page_number += 1
    pages[page_number] = dict(line_window)
    line_number = 0
    line_window.clear()

def process_char(char):
    global char_window
    char_window.append(char)
    if len(char_window) == LINE:
        add_line()

def add_line():
    global char_window, line_number
    line_number += 1
    process_page(''.join(char_window),line_number)
    char_window.clear()

def read_book(file_path):
    global char_window
    with open(file_path, 'r', encoding = 'utf-8-sig') as fp:
        for line in fp:
            line = clean_line(line)
            if line.strip():
                for c in line:
                    process_char(c)
    if len(char_window) > 0:
        add_line()

def generate_codebook():
    global pages
    code_book = {}
    for page, lines in pages.items():
        for num, line in lines.items():
            for pos, char in enumerate(line):
                if char in code_book:
                    code_book[char].append(f'{page}-{num}-{pos}')
                else:
                    code_book[char] = [f'{page}-{num}-{pos}']
    return code_book

def save_codebook(file_path, book):
    with open(file_path, 'w', encoding = 'utf-8-sig') as fp:
        json.dump(book, fp, indent=4)

def load(file_path, *key_books, reverse=False):
    if os.path.exists(file_path):
        with open(file_path, 'r') as fp:
            return json.load(fp)
    else:
        process_books(*key_books)
        if reverse:
            save_codebook(file_path, pages)
            return pages
        else:
            code_book = generate_codebook()
            save_codebook(file_path, code_book)
            return code_book

def process_books(*paths):
    for path in paths:
        read_book(path)

def encrypt(codebook, message):
    cipher_text = []
    for char in message:
        index = random.randint(0,len(codebook[char]) - 1)
        cipher_text.append(codebook[char].pop(index))
    return '-'.join(cipher_text)

def decrypt(rev_codebook, ciphertext):
    plaintext = []
    for cc in re.findall(r'\d+-\d+-\d+', ciphertext):
        page, line, char = cc.split('-')
        plaintext.append(rev_codebook[page][line][int(char)])
    return ''.join(plaintext)

def main_menu():
    print(f"""
    1) Encrypt
    2) Decrypt
    3) Quit
    """)
    return int(input(f"Make a selection [1,2,3]\n"))

def main():
    key_books = ('books/completeworksofwilliamshakespeare.txt','books/drjekyllandmrhyde.txt','books/warandpeace.txt')
    code_book_path = 'codebooks/real_deal.json'
    rev_code_book_path = 'codebooks/real_deal_r.json'
    while True:
        try:
            choice = main_menu()
            match choice:
                case 1:
                    codebook = load(code_book_path, *key_books)
                    message = input(f"Please enter your secret message:\n")
                    print(encrypt(codebook,message))
                    continue
                case 2:
                    rev_codebook = load(rev_code_book_path, *key_books, reverse=True)
                    message = input(f"Please enter your cipher text:\n")
                    print(decrypt(rev_codebook, message))
                    continue
                case 3:
                    break
        except ValueError as ve:
            print(f"Improper Selection.\n")

if __name__ == '__main__':
    main()