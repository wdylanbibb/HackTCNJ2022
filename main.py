import names

class NPC:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        
    def __str__(self) -> str:
        return f'<Person;Name:{self.name},Age{self.age}>'

Vector = list[NPC]


if __name__ == '__main__':
    print(names.get_full_name())

    