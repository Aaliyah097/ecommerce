from dataclasses import dataclass


@dataclass
class Category:
    id: int
    name: str
    slug: str
    children: list['Category']
