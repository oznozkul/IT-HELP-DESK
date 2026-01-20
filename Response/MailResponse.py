from pydantic import BaseModel


class MailResponse(BaseModel):
    id: int
    label: str