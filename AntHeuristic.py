import time
import random
import sys
import copy
from AntHolder import AntHolder


class AntHeuristic:
    # p - vaporization 0..1
    # mCount - ant count
    # time - time limit for calculation
    # pher - pheromon count at the beginning
    # sFactor - smoothing factor
    # q - magic number ?
    def __init__(self, p, m_count, time_limit, pheromon, s_factor, best_percent, q):
        self.p = p
        self.mCount = m_count
        self.time = time_limit
        self.pher = pheromon
        self.sFactor = s_factor
        self.bestPercent = best_percent
        self.q = q
        self.matrix = None
        self.firstTaskVector = None
        self.antArray = [None for _ in range(m_count)]
        self.taskCount = 0

    @staticmethod
    def dice_task(position_not_used, task_vector):
        pher_sum = 0
        for position in position_not_used:
            pher_sum += task_vector[position]
        random_value = random.uniform(0, pher_sum)
        pher_sum = 0
        for position in position_not_used:
            pher_sum += task_vector[position]
            if random_value <= pher_sum:
                position_not_used.remove(position)
                return position
        return position_not_used.pop()

    @staticmethod
    def get_current_time():
        return int(round(time.time() * 1000))

    def calculate(self, instance, simple_best=None, best_mod=1):
        start_time = self.get_current_time()
        self.taskCount = len(instance.task_array)
        self.init_matrix(simple_best, best_mod)

        if simple_best is not None:
            best_result = simple_best
        else:
            best_result = [task for task in instance.task_array]
        for i in range(self.mCount):
            self.antArray[i] = AntHolder(i, 0, [task for task in instance.task_array])

        self.shuffle_ant_init(simple_best)
        work_instance = copy.copy(instance)
        work_instance.task_array = best_result
        best_result_value = work_instance.calculate_result()

        # ranking_size = int(self.mCount * self.bestPercent)
        iter = 0
        ant_task_values = [[0] * self.mCount for _ in range(self.taskCount)]
        while self.get_current_time() - start_time < self.time:
            iter += 1
            print("iter " + str(iter))
            iter_best_result = self.perform_iteration(instance, work_instance, best_result, best_result_value)
            work_instance.task_array = iter_best_result
            iter_result_value = work_instance.calculate_result()
            # print("Best in inter:" + (str(iter_result_value)))
            if best_result_value > iter_result_value:
                best_result = iter_best_result
                best_result_value = iter_result_value
                print("Iter: " + str(iter) + ", with value: " + str(best_result_value))

            ant_ranking = sorted(self.antArray, key=lambda ant_sorted: ant_sorted.value, reverse=False)

            for i in range(self.taskCount):
                max_value = 0
                for j in range(self.mCount):
                    value = self.iter_task_in_ant(ant_ranking[j], i, instance)
                    max_value = max(max_value, value)
                    ant_task_values[i][j] = value

                for j in range(self.taskCount):
                    for k in range(self.mCount):
                        self.matrix[ant_ranking[k].task_array[j].task_id][j] \
                            += 1 - (ant_task_values[j][k] / max_value)
                            # += 1 - (ant_task_values[j][k] / max_value) * (best_result_value / ant_ranking[j].value)

            # for i in range(0, ranking_size):
            #     ant = ant_ranking[i]
            #     self.firstTaskVector[ant.task_array[0].task_id] \
            #         += ((ranking_size - i) / float(ranking_size)) * (float(ant.value) / best_result_value)
            #     for j in range(1, self.taskCount):
            #         self.matrix[ant.task_array[j - 1].task_id][ant.task_array[j].task_id] += ((ranking_size - i) / float(ranking_size)) * (float(ant.value) / best_result_value)
            #
            # self.firstTaskVector[best_result[0].task_id] \
            #     += (float(best_result_value) / best_result_value)
            # for j in range(1, self.taskCount):
            #     self.matrix[best_result[j - 1].task_id][best_result[j].task_id] += \
            #         (float(best_result_value) / best_result_value)

            time_penalty = ((self.time - (self.get_current_time() - start_time)) / self.time + 0.05)
            if time_penalty < 0.6:
                time_penalty = 0.6

            for i in range(0, self.taskCount):
                for j in range(0, self.taskCount):
                    self.matrix[i][j] *= self.p * time_penalty

        print("Iter count: " + str(iter))
        work_instance.task_array = best_result
        return work_instance

    def init_matrix(self, simple_best, best_mod):
        self.matrix = [[self.pher for _ in range(self.taskCount)] for _ in range(self.taskCount)]
        self.firstTaskVector = [self.pher for _ in range(self.taskCount)]
        # if simple_best is None:
        #     return
        # for i in range(self.taskCount - 1):
        #     self.matrix[simple_best[i].task_id][simple_best[i + 1].task_id] *= best_mod
        # self.firstTaskVector[simple_best[0].task_id] *= best_mod

    def perform_iteration(self, instance, work_instance, best_result_known, best_result_value_known):
        best_ant = best_result_value_known
        best_result = [x for x in best_result_known]
        for ant in self.antArray:
            self.iter_ant(ant, instance, work_instance)
            if ant.value < best_ant:
                best_ant = ant.value
                best_result = [x for x in ant.task_array]
            work_instance.task_array = instance.task_array
        return best_result

    def iter_ant(self, ant, instance, work_instance):
        ant.proc_time = instance.ready_time
        ant.value = 0
        position_not_used = set([i for i in range(self.taskCount)])
        for i in range(self.taskCount):
            position = self.dice_task(position_not_used, self.matrix[i])
            if position is None:
                raise Exception("returned task as None, correct me please")
            # position_not_used.remove(position)
            ant.task_array[position] = instance.task_array[i]
        to_check = [0] * self.taskCount
        for i in range(self.taskCount):
            t = ant.task_array[i].task_id
            to_check[t] += 1
            if to_check[t] != 1:
                raise Exception("Already failed")
        work_instance.task_array = ant.task_array
        ant.value = work_instance.calculate_result()

    @staticmethod
    def iter_task_in_ant(ant, task_position, instance):
        current_task = ant.task_array[task_position]
        ant.proc_time += current_task.processing_time
        deadline_difference = ant.proc_time - instance.get_deadline()
        value = max(0, deadline_difference * current_task.e_penalty * -1)
        value += max(0, deadline_difference * current_task.d_penalty)
        return value

    def shuffle_ant_init(self, simple_best):
        start_index = 0
        if simple_best is not None:
            for i in range(self.taskCount):
                self.antArray[0].task_array[i] = simple_best[i]
            start_index = 1
        for i in range(start_index, self.mCount):
            random.shuffle(self.antArray[i].task_array)
