class TaskHolder:
    task_id = None
    processing_time = None
    e_penalty = None
    d_penalty = None

    def __init__(self, task_id, processing_time, e_penalty, d_penalty):
        self.task_id = task_id
        self.processing_time = processing_time
        self.e_penalty = e_penalty
        self.d_penalty = d_penalty

    def __repr__(self):
        return "Id: " + str(self.task_id) + ", P: " + str(self.processing_time) + ", E: " \
               + str(self.e_penalty) + ", D: " + str(self.d_penalty)