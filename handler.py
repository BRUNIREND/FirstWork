import hashlib
import os
import sys
import collections

def handle_arg():
    args = sys.argv
    if len(args) == 1:
        return 'Directory is not specified', False
    else:
        path = args[1]
        return path, True
def print_derictori(path):
    file_format, size_sort = file_size_ret()
    walk_dir = os.walk(path)
    path_arr = collections.defaultdict(list)
    for root, dirs, files in walk_dir:
        for name in files:
            current_path = os.path.join(root, name)
            size_path = os.path.getsize(current_path)
            if file_format != '':
                check_format = name.split('.')[1] == file_format
                if check_format:
                    path_arr[size_path].append(current_path)
                    # path_arr.append((current_path, size_path))
            else:
                path_arr[size_path].append(current_path)
                # path_arr.append((current_path, size_path))
    sorted_keys = sorted(path_arr.keys(), reverse=size_sort)
    for key in sorted_keys:
        print(str(key) + ' bytes')
        for path_in_arr in path_arr[key]:
            print(path_in_arr)
        print()

    hash_arr = get_hashes(sorted_keys, path_arr)
    if hash_arr != False:
        hash_dict_with_count, pos_arr = check_duplicates(hash_arr, sorted_keys)
        delete_them(hash_dict_with_count, pos_arr)

def delete_them(hash_arr, pos_arr):
    print('Delete files?\n')
    user_input = input()
    free_space = 0
    while True:
        if user_input not in ['yes', 'no']:
            print('Wrong option')
        else:
            break
        user_input = input()
    if user_input == 'no':
        return
    while True:
        delete_files_position, flag = testing_values(pos_arr)

        if flag:
            for k, v in hash_arr.items():
                for i in hash_arr[k]:
                    for j in delete_files_position:
                        if j == i[2]:
                            free_space += os.path.getsize(i[0])
                            os.remove(i[0])

            break
        else:
            print('Wrong option')
    print(f"Total freed up space: {free_space} bytes")




def testing_values(pos_arr):
    user_input = input('Enter file numbers to delete:\n')
    # if user_input == '':
    #     return None, False
    try:
        delete_files_position = list(map(int, user_input.split(' ')))
    except:
        print('Wrong option')
        return '', False
    for position in delete_files_position:
        if position not in pos_arr:
            print('Wrong option')
            return None, False
    return delete_files_position, True


def check_duplicates(hash_dict, size_arr):
    count = 1
    pos_arr = []
    for size in size_arr:
        print(f"\n{size} bytes")
        for k, v in hash_dict.items():
            print(f"Hash: {k}")
            for b,i in enumerate(hash_dict[k]):
                # print(hash_dict)
                if i[1] == size:
                    print(f"{count}. {i[0]}")
                    hash_dict[k][b] = [i[0], i[1], count]
                    pos_arr.append(count)
                    count += 1
    return hash_dict, pos_arr


def get_hashes(keys_bytes, dict_arr):
    user_input = input('Check dor duplicates?\n')
    files_with_hashes = {}
    while True:
        if user_input not in ['yes', 'no']:
            print('Wrong option')
        else:
            break
        user_input = input()
    if user_input == 'no':
        return False
    else:
        for byte_size in keys_bytes:
            for path in dict_arr[byte_size]:
                with open(path, 'rb') as current_file:
                    files_with_hashes.setdefault(hashlib.md5(current_file.read()).hexdigest(),
                                                 []).append((path, byte_size))
        return {k: v for k, v in files_with_hashes.items() if len(v) > 1}



def file_size_ret():
    file_format_input = input("Enter file format:\n")
    print("""
Size sorting options:
1. Descending
2. Ascending
""")
    size_sorting_input = input('Enter a sorting option:\n')
    while True:
        if size_sorting_input == '2' or size_sorting_input == '1':
            break
        print('Wrong option')
        size_sorting_input = input('Enter a sorting option:\n')
    return file_format_input, [True, False][int(size_sorting_input) - 1]



hash = hashlib.md5()
path_derictory, flag = handle_arg()
if flag:

    print_derictori(path_derictory)
else:
    print(path_derictory)


