import pathlib

def validate_first_input(user_input: str) -> bool:
    '''Return True if user_input conforms to the specified format and includes a valid
    path. Otherwise, return False.
    '''
    if len(user_input) < 3:
        return False
    if user_input[:2] != 'D ' and user_input[:2] != 'R ':
        return False
    path = pathlib.Path(user_input[2:])
    return path.exists()

def get_search_info(user_input: str) -> (bool, pathlib.Path):
    '''Return whether or not the search will be recursive (True or False) and the path
    based on user_input.
    '''
    path = pathlib.Path(user_input[2:])
    if user_input[0] == 'D':
        return path, False
    if user_input[0] == 'R':
        return path, True

def print_files(directory: pathlib.Path, recursive_search: bool) -> None:
    '''Print the paths of all the files in the directory. If recursive_search is True,
    recursively call print_files to print all the files in any subdirectories in directory.
    '''
    contents = list(directory.iterdir())
    contents.sort()
    for item in contents:
        if item.is_file():
            print(item)
    if recursive_search:
        for item in contents:
            if item.is_dir():
                print_files(item, recursive_search)

if __name__ == '__main__':
    while True:
        first_input = input()
        if validate_first_input(first_input):
            break
        print('ERROR')
    path, recursive_search = get_search_info(first_input)
    print_files(path, recursive_search)
