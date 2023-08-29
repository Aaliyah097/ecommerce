from dataclasses import dataclass


@dataclass
class Category:
    name: str
    slug: str
    children: list['Category']
