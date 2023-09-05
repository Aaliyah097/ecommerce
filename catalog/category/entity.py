from dataclasses import dataclass


@dataclass
class Category:
    name: str
    slug: str
    file: str | None
    children: list['Category']
