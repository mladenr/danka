class Uplata:
    def __init__(self, projectId, date, amount, processed):
        self.projectId = projectId
        self.date = date
        self.amount = amount
        self.processed = processed

    def __repr__(self):
        return str(self.__dict__)

