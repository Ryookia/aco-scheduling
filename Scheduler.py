import time

class Scheduler:


    @staticmethod
    def schedule_instance(instance):

        # e_sum = 0
        # d_sum = 0
        #
        # for task in instance.task_array:
        #     e_sum += task.e_penalty * task.processing_time
        #     d_sum += task.d_penalty * task.processing_time
        #
        # e_in = e_sum / (e_sum + d_sum)
        # if e_in * instance.h > 0.5:
        #     instance.ready_time = int(instance.h * 0.5 * instance.deadline)

        # print("e_Sun:" + str(e_sum) +", d_sun:" + str(d_sum))

        k = time.time()

        instance.deadline = 0
        for task in instance.task_array:
            instance.deadline += task.processing_time
        instance.deadline = int(instance.h * instance.deadline)

        if instance.h >= 0.5:
            instance.ready_time = int(instance.deadline * (instance.h - 0.5))
        else:
            instance.ready_time = 0
        print("REady: "  + str(instance.ready_time))

        instance.task_array = sorted(instance.task_array, key=lambda x: x.d_penalty / x.processing_time, reverse=True)
        i = 0
        sum_time = instance.ready_time
        while sum_time < instance.deadline and i < len(instance.task_array):
            sum_time += instance.task_array[i].processing_time
            i += 1
        instance.task_array[:i] = sorted(instance.task_array[:i], key=lambda x: x.e_penalty / x.processing_time,
                                         reverse=False)

        # instance.task_array[i:] = sorted(instance.task_array[i:], key=lambda x: x.d_penalty * x.processing_time,
        #                                  reverse=True)
        # instance.task_array[:i] = sorted(instance.task_array[:i], key=lambda x: x.e_penalty * x.processing_time,
        #                                  reverse=True)
        # instance.ready_time = int(instance.deadline * 0.5)
        print("TIME = " + str(time.time() - k))
        return instance

    @staticmethod
    def get_comparator():
        def compare(o1, o2):
            if o1.e_penalty < o2.e_penalty:
                return -1
            else:
                return 1
        return compare
