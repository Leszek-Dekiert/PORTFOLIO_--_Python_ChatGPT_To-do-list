# -*- coding: utf-8 -*-


###

#To-do list simulator

###


#Description of the program: "To-do list simulator" is a program for writing 
#down notes, and assingnig a level of importance (or priority) to those 
#notes. The program also allowes to viewing the list (with priorities and 
#dates of entry), changing entries and/or priority levels, removing entries
#and sorting entries by level of importance. Every time an entry is removed
#it is being transferred to the archive file "To-do-list_archive". Enjoy.


###

#Code of the program:
    
###
    
    
#Importing used libraries
from datetime import datetime
import re
import roman
import os


#Creating empty txt files if they haven't existed before. This needs to happen
#after user turns on the program (made with help from ChatGPT)
files = ['To-do-list_archive.txt', 'To-do-list.txt']
for file in files:
    file_full_path = os.path.join(os.getcwd(), file)
    if not os.path.exists(file_full_path):
        with open(file_full_path, 'w') as f:
            pass
print('Files have been created.')


#Connecting the script folder path to the file names 
#(made with help from ChatGPT)
file_path = os.path.join(os.getcwd(), 'To-do-list.txt')
file_path_archive = os.path.join(os.getcwd(), 'To-do-list_archive.txt')


#Defining function for removing all empty lines from txt file 
#(made with help from ChatGPT)
def remove_empty_paragraphs(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    cleaned_lines = [line for line in lines if line.strip()]   
    with open(file_path, 'w') as f:
        f.writelines(cleaned_lines)


#Defining function for index finding for chosen entries 
#(made with help from ChatGPT)
def find_entry_index(entry_number):
    pattern = rf'^{entry_number}\.'  
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for index, line in enumerate(lines):
        if re.match(pattern, line.strip()):
            return index
    return None


#Defining function for extracting all entry Id's (made with help from ChatGPT)
def extract_leading_digits(texts):
    all_numbers = []
    for text in texts:
        match = re.match(r'^\d+', text)
        if match:
            all_numbers.append(int(match.group(0)))
    return all_numbers


#Defining function for looking for a number at the beginning of a line 
#that ends with a dot (made with help from ChatGPT)
def get_number(line):
    matching = re.match(r'(\d+)\.', line)
    return matching.group(1) if matching else None


#Defining function for data extraction (made with help from ChatGPT)
def parse_entry(line):
    match = re.match(r'(\d+)\.\s*(.*)\s*-\s*(\d{2}\.\d{2}\.\d{4})\s*-\s*'
                     '([IVXLCDM]+)$', line.strip())
    if match:
        unique_number = int(match.group(1))
        text = match.group(2).strip()
        date = datetime.strptime(match.group(3), '%d.%m.%Y')
        roman_number = roman.fromRoman(match.group(4))
        return (roman_number, unique_number, date, text, line.strip())
    return None


#Defining function for removing and moving an entry to archive file 
#(made with help from ChatGPT)
def move_task(number_remove, source_file=file_path, 
              archive_file=file_path_archive):
    with open(source_file, 'r') as src:
        lines = src.readlines()
    with open(file_path_archive, 'a') as archive, open(file_path, 'w') as src:
        task_found = False
        for line in lines:
            if line.startswith(str(number_remove)):
                archive.write(line)
                task_found = True
            else:
                src.write(line)
        if not task_found:
            print(f'Could not find an entry with the number: {number_remove}')


#Defining function for checking if txt file is empty 
#(made with help from ChatGPT)
def is_file_empty(file_path):
    return (os.path.exists(file_path) 
            and os.path.getsize(file_path) == 0
            or os.path.getsize(file_path) == 1
            or os.path.getsize(file_path) == 2)


#Defining function for changing an entry (made with help from ChatGPT)
def update_entry_in_file(file_path, number_change, new_entry, new_today, 
                         new_priority_choice):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    pattern = re.compile(rf'^{number_change}\. .* - .* - [IVXLCDM]+$', 
                         re.MULTILINE)
    new_line = f'{number_change}. {new_entry} - {new_today} - {new_priority}\n'
    for i, line in enumerate(lines):
        if pattern.match(line.strip()):
            lines[i] = new_line
            break
    with open(file_path, 'w') as file:
        file.writelines(lines)


###


#To-do-list program


###


#User introduction and input
remove_empty_paragraphs(file_path)
opening = ''
while opening != '6':
    opening = input('\nWelcome to Your personal To-do-list!\n'
                    'Press "1" if You would like do see the list of entries of'
                    ' Your list.\n'
                    'Press "2" if You would like do add an entry to Your list.'
                    '\nPress "3" if You would like do remove an entry '
                    'from Your list, and move it to archive file.\n'
                    'Press "4" if You would like to change an entry and'
                    ' priority in Your list.\n'
                    'Press "5" if You would like do see sorted list of entries'
                    ' by priority/Id/date/entry.\n'
                    'Or press "6" if You would like to exit the program.\n')


#Instruction for listing entries
    if opening == '1':
        file = open(file_path, 'r')
        print('\nHere is a list of all Your entries:\n')
        for line in file:
            print(f'{line}', end='')


#Instruction for adding an entry
    elif opening == '2':
        with open(file_path, 'r') as file:
            if is_file_empty(file_path):
                number_of_entry = 1
            else:
                for line in reversed(file.readlines()):
                    line = line.strip()
                    if line:
                        number_of_entry = get_number(line)
                        number_of_entry = int(number_of_entry) + 1
                        break
        entry = input('Write Your entry here: ')
        priority_choice = input('Set a priority for Your entry:\n'
                         'For highest (I) priority, press 1\n'
                         'For medium (II) priority, press 2\n'
                         'For lowest (III) priority, press 3\n')   
        if priority_choice == '1':
            priority = 'I'
        elif priority_choice == '2':
            priority = 'II'
        elif priority_choice == '3':
            priority = 'III'
        else:
            'Error. You need to set the priority between 1 and 3'
        today = datetime.today().strftime('%d.%m.%Y')
        with open(file_path, 'a') as file:
            file.write(f'\n{number_of_entry}. {entry} - {today} - {priority}')
            print('\nEntry has been added to the list.')


#Instruction for removeing/moving an entry to the archive file
    elif opening == '3':
        with open (file_path, 'r') as file:
            all_numbers = extract_leading_digits(file)
        number_remove = int(input('Pick the number of entry that You would'
                              ' like to remove: '))
        if number_remove in all_numbers:
            move_task(number_remove)
            print('Entry has been removed from the list and moved to archive.')
        else:
            print('This number has no entries attached')


#Instruction for changing an entry on the list
    elif opening == '4':
        print('\n')
        file = open(file_path, 'r')
        for line in file:
            print(f'{line}')
        try:
            number_change = (input('\nAbove You have a list of entries. '
                        'Choose which entry You would like to change: '))
            new_entry = input('Write a new entry You would like to replace the'
                              ' old one with: ')
            index_change = find_entry_index(f'{number_change}')
            new_today = datetime.today().strftime('%d.%m.%Y')
            new_priority_choice = input('Set a priority for Your new entry:\n'
                             'For highest (I) priority, press 1\n'
                             'For medium (II) priority, press 2\n'
                             'For lowest (III) priority, press 3\n')   
            if new_priority_choice == '1':
                new_priority = 'I'
            elif new_priority_choice == '2':
                new_priority = 'II'
            elif new_priority_choice == '3':
                new_priority = 'III'
            else:
                'Error. You need to set the priority between 1 and 3'
            update_entry_in_file(file_path, number_change, new_entry, 
                                     new_today, new_priority)
            print('Entry and priority have been changed.')
        except Exception as e:
             print('An error occurred. Please try again. Make sure that entry'
                   ' You are trying to change is on the list of entries')


#Instruction for sorting the list by priority/Id/date/entry
    elif opening == '5':
        print('\nHere is a sorted list:\n')
        with open(file_path, 'r') as file:
            lines = file.readlines()
        entries = ([parse_entry(line) for line in lines if parse_entry(line) 
                    is not None])
        entries.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
        for entry in entries:
            print(entry[4])

#Instruction for exiting the program
    elif opening == '6':
        print('\nExiting the program...')


#Instruction for wrong input
    else:
        print('\nWrong instruction. Exiting the program.')