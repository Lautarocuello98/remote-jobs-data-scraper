from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class JobRecord:
    title: str
    company: str
    location: str
    tags: str
    salary: Optional[str]
    date_posted: Optional[str]
    job_url: str
    source: str

    def to_dict(self) -> dict:
        return asdict(self)