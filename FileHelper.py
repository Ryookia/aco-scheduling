import re
import numpy
from InstanceHolder import InstanceHolder
FILE_DIRECTORY = "./instances/"
RESULT_DIRECTORY = "./results/"
RESULT_N_REGEX = "[n][0-9]+"
RESULT_K_REGEX = "[k][0-9]+"
RESULT_H_REGEX = "[h][0-9]+"
# RESULT_H_REGEX = "[h][0-9]*\.?[0-9]+$"
RESULT_FILE_REGEX = "[n][0-9]+[k][0-9]+[h][0-9]*\.?[0-9]+$"


# Returns file in form of a list, in which every next entry is a new line
def load_file(instance_size):
    file_name = get_file_directory() + get_file_by_size(instance_size)
    with open(file_name, "r") as file:
        content = file.readlines()
        content = [x.strip() for x in content]
        return content


def load_file_from_name(file_path):
    with open(file_path, "r") as file:
        content = file.readlines()
        content = [x.strip() for x in content]
        content = [float(s) for s in content[0].split(' ')]
        return content


# Returns file name based on instance size (requires predefined size)
def get_file_by_size(size):
    switcher = {
        10: "sch10.txt",
        20: "sch20.txt",
        50: "sch50.txt",
        100: "sch100.txt",
        200: "sch200.txt",
        500: "sch500.txt",
        1000: "sch1000.txt"
    }
    result = switcher.get(size, None)
    if result is None:
        raise Exception("Unknown file for given instance size")
    return result


def get_file_directory():
    return FILE_DIRECTORY


def parse_file(file_content):
    instance_count = int(file_content[0])
    instance_list = []
    current_line = 1
    for i in range(0, instance_count):
        size = int(file_content[current_line])
        current_line += 1
        task_list = []
        for j in range(0, size):
            task_list.append(re.split('\s+', file_content[current_line]))
            for k in range(0, 3):
                task_list[j][k] = int(task_list[j][k])
            current_line += 1
        instance_list.append(InstanceHolder((i + 1), size, task_list))
    return instance_list


def save_file(file_name, file_content):
    with open(RESULT_DIRECTORY + file_name, 'w+') as file:
        file.truncate(0)
        file.write(file_content)


def parse_file_from_result(file_name):
    content = load_file_from_name(file_name)
    k_regex = re.compile(RESULT_K_REGEX)
    print(file_name)
    print(content)
    k = k_regex.search(file_name)
    if k is None:
        raise Exception("K is wrong in format")
    k = int(file_name[k.start() + 1: k.end()])

    n_regex = re.compile(RESULT_N_REGEX)
    n = n_regex.search(file_name)
    if n is None:
        raise Exception("N is wrong in format")
    n = int(file_name[n.start() + 1:n.end()])

    h_regex = re.compile(RESULT_H_REGEX)
    h = h_regex.search(file_name)
    if h is None:
        raise Exception("H is wrong in format")
    h = float(file_name[h.start() + 1:h.end()])
    while h > 1:
        h /= 10

    f = content[0]
    ready = content[2]
    task_id_list = content[3:]

    file_content = load_file(n)
    instance_list = parse_file(file_content)
    instance = instance_list[k - 1]
    instance.set_deadline_mod(h)
    instance.ready_time = int(ready)

    # kek = ""
    # for ins in instance.task_array:
    #     kek += " " + str(ins.task_id)
    # print(kek)
    new_task_array = []
    for task_id in task_id_list:
        new_task_array.append(instance.task_array[int(task_id)])
    instance.task_array = new_task_array

    check = numpy.zeros(len(new_task_array), dtype=bool)
    for task in instance.task_array:
        check[int(task.task_id)] = True
    for ch in check:
        if not ch:
            raise Exception("Not all!!!")
    # print(instance)
    print("Calculated: " + str(instance.calculate_result()))
    print("Given:" + str(f))
    # kek = ""
    # for ins in instance.task_array:
    #     kek += " " + str(ins.task_id)
    # print(kek)
