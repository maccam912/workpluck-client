from pydantic import BaseModel 


# Models for Task Submission and Retrieval
class TaskSubmission(BaseModel):
    topic: str
    input: dict


class TaskSubmissionResponse(BaseModel):
    id: str


class TaskRetrievalResponse(BaseModel):
    id: str
    input: dict


# Models for Result Submission and Retrieval
class ResultSubmission(BaseModel):
    id: str
    output: dict


class ResultRetrievalResponse(BaseModel):
    output: dict
