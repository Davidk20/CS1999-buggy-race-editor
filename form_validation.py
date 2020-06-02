import _sqlite3 as sql

class buggy_validation():
    def __init__(self,new_buggy):
        self.buggy = new_buggy
        self.test1 = self.numerical_test()
        self.test2 = self.comparison_test()
        self.test3 = self.hamster_test()
        self.test4 = self.consumable_test()

    def passback(self):
        if self.test1 == 'fail' or self.test2 == 'fail' or self.test3 == 'fail' or self.test4 == 'fail':
            return 'error'
        else:
            return 'success'


    def numerical_test(self):
        if int(self.buggy[0])%2 != 0:
            return 'fail'
        elif int(self.buggy[10])<int(self.buggy[0]):
            return 'fail'
        else:
            return 'success'

    def comparison_test(self):
        if self.buggy[1]==self.buggy[3]:
            return 'fail'
        elif self.buggy[3]!='none' and self.buggy[4]==0:
            return 'fail'
        elif self.buggy[6] == self.buggy[8] and self.buggy[7]!='plain':
            return 'fail'
        else:
            return 'success'

    def hamster_test(self):
        if self.buggy[1]!='hamster' and self.buggy[3]!='hamster' and int(self.buggy[5])>0:
            return 'fail'
        else:
            return 'success'

    def consumable_test(self):
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT Item,consumable FROM buggy_costs")
            consumables = cur.fetchall()
            for item in range(len(consumables)):
                if self.buggy[1] == consumables[item][0]:
                    if consumables[item][1] == "False":
                        if int(self.buggy[2])>1:
                            return 'fail'
                    else:
                        pass
                elif self.buggy[3] == consumables[item][0]:
                    if int(self.buggy[4])>1:
                        return 'fail'
                    else:
                        pass
            return 'success'
if __name__ == '__main__':
    buggy_validation(None)