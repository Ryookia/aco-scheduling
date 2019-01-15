import FileHelper
from Scheduler import Scheduler
import itertools
import copy
from AntHeuristic import AntHeuristic


def test():
    file_content = FileHelper.load_file(10)
    instance_list_10 = FileHelper.parse_file(file_content)
    for instance in instance_list_10:
        instance.set_deadline_mod(0.8)

    file_content = FileHelper.load_file(50)
    instance_list_50 = FileHelper.parse_file(file_content)
    for instance in instance_list_50:
        instance.set_deadline_mod(0.6)

    file_content = FileHelper.load_file(100)
    instance_list_100 = FileHelper.parse_file(file_content)
    for instance in instance_list_100:
        instance.set_deadline_mod(0.4)

    file_content = FileHelper.load_file(500)
    instance_list_500 = FileHelper.parse_file(file_content)
    for instance in instance_list_500:
        instance.set_deadline_mod(0.2)

    name_t = []
    name_t.append("n = 10")
    name_t.append("n = 50")
    name_t.append("n = 100")
    name_t.append("n = 500")

    list_t = []
    list_t.append(instance_list_10)
    list_t.append(instance_list_50)
    list_t.append(instance_list_100)
    list_t.append(instance_list_500)

    for j in range(0, len(list_t)):
        print(name_t[j])
        instance_list = list_t[j]
        for i in range(0, len(instance_list)):
            print("K = " + str(i + 1))
            print("Result: " + str(instance_list[i].calculate_result()))
            instance = Scheduler.schedule_instance(instance_list[i])
            print("Result sorted: " + str(instance.calculate_result()))
            FileHelper.save_file(instance_list[i].get_file_name(), instance_list[i].format_result())


def check(path):
    FileHelper.parse_file_from_result(path)


def perm():
    smallest = 1000000000
    file = FileHelper.load_file(10)
    inst = FileHelper.parse_file(file)
    inst = inst[0]
    inst.set_deadline_mod(0.8)
    inst.ready_time = 15
    kek = list(itertools.permutations(inst.task_array))
    z = 10 * 9 * 8 * 7 * 6 * 5 * 4 * 3 * 2
    i = 0
    for k in kek:
        inst.task_array = k
        res = inst.calculate_result()
        if res < smallest:
            smallest = res
        # print(str(res) + " " + str(smallest))
        i += 1
        if i % 100000 == 0:
            print(str(i) + " out of " + str(i / z) + " " + str(smallest))
    print(smallest)

def test_meta():
    file_content = FileHelper.load_file(100)
    instance_list_10 = FileHelper.parse_file(file_content)
    for instance in instance_list_10:
        instance.set_deadline_mod(0.8)

    instance_list_10_ant = FileHelper.parse_file(file_content)
    for instance in instance_list_10_ant:
        instance.set_deadline_mod(0.8)

    simple_instance = instance_list_10[0]
    ant_instance = instance_list_10_ant[0]
    print("Result: " + str(instance_list_10[0].calculate_result()))
    simple_instance = Scheduler.schedule_instance(simple_instance)
    print("Result sorted: " + str(simple_instance.calculate_result()))
    ant_instance.ready_time = simple_instance.ready_time
    heuristic = AntHeuristic(1, 350, 500000, 100.0, 1, 0.1, 1)
    result_heu = heuristic.calculate(ant_instance)
    # result_heu = heuristic.calculate(ant_instance, simple_instance.task_array, 1000)
    print("Result Ant: " + str(result_heu.calculate_result()))

    # FileHelper.save_file("n100k1h8.txt", result_heu.format_result())
    # check("./results/n100k1h8.txt")


# test()
# perm()
# check("./results/n500k2h2.txt")

test_meta()



