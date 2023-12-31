from dataclasses import dataclass


@dataclass
class Category:
    name: str
    slug: str
    file: str
    children: list['Category']
    description: str
    image_link: str
