from TaskHolder import TaskHolder


class InstanceHolder:
    instance_id = None
    # amount of task in given instance
    size = None
    # array of tasks
    task_array = None
    h = 1
    deadline = None

    ready_time = 0

    def __init__(self, instance_id, size, task_list):
        self.instance_id = instance_id
        self.size = size
        self.task_array = []
        self.parse_task_list(task_list)

    def set_deadline_mod(self, h):
        self.h = h
        self.deadline = self.get_deadline()

    def parse_task_list(self, task_list):
        for j in range(0, self.size):
            self.task_array.append(TaskHolder(j, task_list[j][0], task_list[j][1], task_list[j][2]))

    def __repr__(self):
        result = "Size: " + str(self.size)
        for i in range(0, self.size):
            result += "\n" + repr(self.task_array[i])
        return result

    def get_deadline(self):
        sum_time = 0
        for i in range(0, self.size):
            sum_time += self.task_array[i].processing_time
        return int(sum_time * self.h)

    def calculate_result(self):
        current_time = self.ready_time
        deadline_time = self.get_deadline()
        penalty_sum = 0
        for i in range(0, self.size):
            current_time += self.task_array[i].processing_time
            difference = deadline_time - current_time
            if difference < 0:
                penalty_sum += (difference * -1) * self.task_array[i].d_penalty
            else:
                penalty_sum += difference * self.task_array[i].e_penalty
        return penalty_sum

    def format_result(self):
        result = ''
        result += str(self.calculate_result())
        result += " "
        result += str(self.h)
        result += " "
        result += str(self.ready_time)
        for i in range(0, self.size):
            result += " "
            result += str(self.task_array[i].task_id)
        return result

    def get_file_name(self):
        res = None
        if self.h == 1:
            res = str(self.h)
        else:
            res = str(self.h)[2:]
        return 'n' + str(self.size) + 'k' + str(self.instance_id) + 'h' + res + '.txt'
