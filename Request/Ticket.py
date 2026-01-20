from pydantic import BaseModel


class Ticket(BaseModel):
    subject: str