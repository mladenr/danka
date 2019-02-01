class Potrazivanje:
    def __init__(self, projectId, createdDate, deadlineDate, amount, isplaceno, kasnioSaIsplatom, brojDanaKasnjenja, dug, pretplata, uplataList):
        self.projectId = projectId
        self.createdDate = createdDate
        self.deadlineDate = deadlineDate
        self.amount = amount
        self.isplaceno = isplaceno
        self.kasnioSaIsplatom = kasnioSaIsplatom
        self.brojDanaKasnjenja = brojDanaKasnjenja
        self.dug = dug
        self.pretplata = pretplata
        self.uplataList = uplataList

    def __repr__(self):
        return str(self.__dict__)

    def __getitem__(self, i):
        return self
