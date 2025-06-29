from pydantic import BaseModel, StrictInt, StrictStr

class Task(BaseModel):
    task_id: StrictStr
    file_path: StrictStr

class TaskResult(BaseModel):
    benign_thread: StrictInt
    attack_thread: StrictInt

