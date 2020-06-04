import sqlite3 as sql

class cost_method():
    def __init__(self,buggy):
        self.buggy = buggy
        self.con = sql.connect("database.db")
        self.con.row_factory = sql.Row
        self.cur = self.con.cursor()
        self.cur.execute("SELECT * FROM buggy_costs")
        self.record = self.cur.fetchall()
        self.cost_unit = 0
        self.cost_kg = 0
        self.multiplier = int(self.buggy[0]) - 4
        self.multiplier = 1 + (self.multiplier/10)

    def buggy_cost(self):
        for prop in range(len(self.buggy)):
            for item in range(len(self.record)):
                if self.record[item][0] == self.buggy[prop]:
                    if prop == 11:
                        self.cost_unit += int(self.record[item][1])*self.multiplier
                        self.cost_kg += int(self.record[item][2])*self.multiplier
                        continue
                    else:
                        self.cost_unit = self.cost_unit + (int(self.record[item][1])*int(self.buggy[prop+1]))
                        self.cost_kg = self.cost_kg + (int(self.record[item][2])*int(self.buggy[prop+1]))
            if prop == 5:
                self.cost_unit = self.cost_unit + (int(self.buggy[5]) * int(self.record[0][1]))
            elif prop == 14 and self.buggy[prop]=='true':
                self.cost_unit += int(self.record[1][1])
            elif prop == 15 and self.buggy[prop]=='true':
                self.cost_unit += int(self.record[2][1])
            elif prop == 16 and self.buggy[prop]=='true':
                self.cost_unit += int(self.record[3][1])
            elif prop == 17 and self.buggy[prop]=='true':
                self.cost_unit += int(self.record[4][1])

        return int(self.cost_unit),int(self.cost_kg)


