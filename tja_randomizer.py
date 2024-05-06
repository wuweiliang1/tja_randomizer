import argparse
import re
import random


def randomize_tja_and_save(file_path, use_seed=100, random_level=0):
    if use_seed:
        random.seed(use_seed)
    randomize_threshold = 0.5
    random_level_name = "crazy"
    if random_level == 1:
        randomize_threshold = 0.75
        random_level_name = "mild"
    with open(file_path, 'r', encoding='shift-jis') as fd:
        lines = fd.readlines()
        file_name = fd.name

    title = ""
    title_line_idx = -1
    for idx in range(len(lines)):
        if lines[idx].startswith('TITLE:'):
            title = lines[idx].split(':')[1].strip()
            title_line_idx = idx
            break

    new_lines = lines.copy()
    scan_offset = 0
    line_to_replace = []
    while True:
        start_idx, end_idx, new_line_to_replace = find_course_idx(lines, scan_offset)
        scan_offset = end_idx
        if not new_line_to_replace:
            break
        line_to_replace.extend(new_line_to_replace)

    for line_info in line_to_replace:
        line_idx, line_data = line_info
        # reverse 1 to 2, 2 to 1, 3 to 4, 4 to 3 by 50% chance
        target_line_data = ''
        for char in line_data:
            target_char = char
            if random.random() > randomize_threshold:
                if char == '1':
                    target_char = '2'
                elif char == '2':
                    target_char = '1'
                elif char == '3':
                    target_char = '4'
                elif char == '4':
                    target_char = '3'
            target_line_data += target_char
        new_lines[line_idx] = target_line_data

    if title and title_line_idx >= 0:
        new_lines[title_line_idx] = f'TITLE:{title} ({random_level_name},seed{seed})\n'

    new_file_name = file_name.replace(".tja", f"_{random_level_name}_seed_{seed}.tja")
    with open(new_file_name, 'w', encoding='shift-jis') as f:
        f.writelines(new_lines)


def find_course_idx(tja_lines, start_offset=0):
    line_count = len(tja_lines)
    lines = tja_lines
    course_idx = 0
    start_idx = 0
    end_idx = 0

    for idx in range(start_offset, line_count):
        if lines[idx].startswith('COURSE:'):
            course_level = lines[idx].split(':')[1].strip()
            print(f"replacing tja file with course:{course_level}")
            course_idx = idx
            break

    if course_idx == 0:
        return -1, -1, None

    for idx in range(course_idx, line_count):
        if lines[idx].startswith('#START'):
            start_idx = idx
            break
    for idx in range(start_idx, line_count):
        if lines[idx].startswith('#END'):
            end_idx = idx
            break

    line_to_replace = []
    for course_line_idx in range(start_idx, end_idx):
        if lines[course_line_idx].startswith('#'):
            continue
        if re.search(r"^\d+,", lines[course_line_idx]):
            line_to_replace.append((course_line_idx, lines[course_line_idx]))
    return start_idx, end_idx, line_to_replace


if __name__ == '__main__':
    seed = 100
    arg_parser = argparse.ArgumentParser(description='Randomize tja file. 用于生成稳定预期的随机化次郎谱面.'
                                                     'Example: tja_randomizer.exe --seed 100 --random-level 0 some_file.tja')
    arg_parser.add_argument('--seed', type=int, help='Random seed for random generator. Default as 100. 随机数发生器指定的随机种子，用于控制随机序列。默认为100。', default=100)
    arg_parser.add_argument('--random-level', type=int, help='Random level. 0: crazy, 1: mild. default as 0. 随机级别，0为大随机，1为小随机。默认为0。', default=0)
    arg_parser.add_argument('file', type=str, help='TJA file. 指定的TJA文件')
    args = arg_parser.parse_args()
    if args.seed:
        seed = args.seed
    randomize_tja_and_save(args.file, seed, args.random_level)
