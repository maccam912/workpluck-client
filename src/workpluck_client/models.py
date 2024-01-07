from pydantic import BaseModel, UUID4


# Models for Task Submission and Retrieval
class TaskSubmission(BaseModel):
    topic: str
    input: dict


class TaskSubmissionResponse(BaseModel):
    id: UUID4


class TaskRetrievalResponse(BaseModel):
    id: UUID4
    input: dict


# Models for Result Submission and Retrieval
class ResultSubmission(BaseModel):
    id: UUID4
    output: dict


class ResultRetrievalResponse(BaseModel):
    output: dict
