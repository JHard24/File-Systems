import pathlib, shutil, os, datetime

def valid_first_input(user_input: str) -> bool:
    '''Return True if user_input conforms to the specified format and includes a valid
    path. Otherwise, return False.
    '''
    if len(user_input) < 3:
        return False
    if user_input[:2] != 'D ' and user_input[:2] != 'R ':
        return False
    path = pathlib.Path(user_input[2:])
    return path.exists()

def get_search_info(user_input: str) -> (pathlib.Path, bool):
    '''Return whether or not the search will be recursive (True or False) and the path
    based on user_input.
    '''
    path = pathlib.Path(user_input[2:])
    if user_input[0] == 'D':
        return path, False
    if user_input[0] == 'R':
        return path, True

def get_files_in_directory(directory: pathlib.Path, recursive_search: bool) -> list[pathlib.Path]:
    '''Return the paths of all the files in the directory. If recursive_search
    is True, recursively call get_files_in_directory on any subdirectories in
    directory.
    '''
    contents = sorted(list(directory.iterdir()))
    files = []
    for item in contents:
        if item.is_file():
            files.append(item)
    if recursive_search:
        for item in contents:
            if item.is_dir():
                files += get_files_in_directory(item, recursive_search)
    return files

def valid_second_input(user_input: str) -> bool:
    '''Return True if user_input conforms to the specified format. Otherwise, return
    False.
    '''
    if user_input == 'A':
        return True
    if len(user_input) > 2:
        if user_input[:2] == 'N ' or user_input[:2] == 'E ' or user_input[:2] == 'T ':
            return True
        if user_input[:2] == '< ' or user_input[:2] == '> ':
            if user_input[2:].isdigit():
                return True
    return False

def get_search_characteristics(user_input: str) -> (str, str):
    '''Return the type of search to be executed and the relevant value for this type of
    search based on user_input.
    '''
    search_type = user_input[0]
    if search_type == 'A':
        return search_type, ''
    else:
        return search_type, user_input[2:]

def execute_search(files: list[pathlib.Path], search_type: str, search_value: str) -> list[pathlib.Path]:
    '''Return a list of file paths that were found in files after executing the
    appropriate search_type with the corresponding search_value.
    '''
    if search_type == 'A':
        return files
    elif search_type == 'N':
        return name_search(files, search_value)
    elif search_type == 'E':
        return extension_search(files, search_value)
    elif search_type == 'T':
        return text_search(files, search_value)
    elif search_type == '<':
        return size_less_than_search(files, search_value)
    elif search_type == '>':
        return size_greater_than_search(files, search_value)

def name_search(files: list[pathlib.Path], name: str) -> list[pathlib.Path]:
    '''Return a list of file paths from files with the matching name.
    '''
    files_found = []
    for item in files:
        if item.name == name:
            files_found.append(item)
    return files_found

def extension_search(files: list[pathlib.Path], extension: str) -> list[pathlib.Path]:
    '''Return a list of file paths from files with the matching extension.
    '''
    if extension[0] != '.':
        extension = '.' + extension
    files_found = []
    for item in files:
        if item.suffix == extension:
            files_found.append(item)
    return files_found

def text_search(files: list[pathlib.Path], text: str) -> list[pathlib.Path]:
    '''Return a list of file paths from text files containing the specified text.
    '''
    files_found = []
    for item in files:
        try:
            r_file = item.open('r')
            file_text = r_file.read()
            if text in file_text:
                files_found.append(item)
        except UnicodeDecodeError:
            pass
        else:
            r_file.close()
    return files_found

def size_less_than_search(files: list[pathlib.Path], size: str) -> list[pathlib.Path]:
    '''Return a list of file paths from files that are less than size bytes.
    '''
    size = int(size)
    files_found = []
    for item in files:
        if item.stat().st_size < size:
            files_found.append(item)
    return files_found

def size_greater_than_search(files: list[pathlib.Path], size: str) -> list[pathlib.Path]:
    '''Return a list of file paths from files that are greater than size bytes.
    '''
    size = int(size)
    files_found = []
    for item in files:
        if item.stat().st_size > size:
            files_found.append(item)
    return files_found

def valid_third_input(user_input: str) -> bool:
    '''Return True if user_input conforms to the specified format. Otherwise, return
    False.
    '''
    if user_input == 'F' or user_input == 'D' or user_input == 'T':
        return True
    return False

def take_action(files: list[pathlib.Path], action: str) -> None:
    '''Perform the specified action on each of the files.
    '''
    if action == 'F':
        print_first_line(files)
    elif action == 'D':
        duplicate_files(files)
    elif action == 'T':
        touch_files(files)

def print_first_line(files: list[pathlib.Path]) -> None:
    '''Print the first line of text of each file in files. If a file is not a text
    file, instead print "NOT TEXT".
    '''
    for item in files:
        try:
            r_file = item.open('r')
            first_line = r_file.readline().strip()
            print(first_line)
        except UnicodeDecodeError:
            print('NOT TEXT')
        else:
            r_file.close()

def duplicate_files(files: list[pathlib.Path]) -> None:
    '''Create a duplicate of each file in files, but with ".dup" appended to the end of
    each file name.
    '''
    for item in files:
        new_name = str(item) + '.dup'
        new_path = pathlib.Path(new_name)
        shutil.copyfile(item, new_path)

def touch_files(files: list[pathlib.Path]) -> None:
    '''Change the last modified timestamp of each file in files to the current
    date/time.
    '''
    for item in files:
        current_time = datetime.datetime.now().timestamp()
        os.utime(item, (current_time, current_time))

if __name__ == '__main__':
    while True:
        first_input = input()
        if valid_first_input(first_input):
            break
        print('ERROR')
    directory, recursive_search = get_search_info(first_input)
    files = get_files_in_directory(directory, recursive_search)
    for item in files:
        print(item)
    while True:
        second_input = input()
        if valid_second_input(second_input):
            break
        print('ERROR')
    search_type, search_value = get_search_characteristics(second_input)
    files_found = execute_search(files, search_type, search_value)
    for item in files_found:
        print(item)
    if len(files_found) > 0:
        while True:
            third_input = input()
            if valid_third_input(third_input):
                break
            print('ERROR')
        take_action(files_found, third_input)
