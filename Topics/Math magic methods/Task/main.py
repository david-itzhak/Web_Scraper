class Task:
    def __init__(self, description, team):
        self.description = description
        self.team = team

    def __add__(self, other):
        description = '\n'.join([self.description, other.description])
        team = ', '.join([self.team, other.team])
        return Task(description, team)

