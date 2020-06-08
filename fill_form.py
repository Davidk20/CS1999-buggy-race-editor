import _sqlite3 as sql
import random
from form_validation import buggy_validation
from cost_method import cost_method


class fill_form():
    def __init__(self,buggy):
        self.buggy=buggy
        self.value_fills = []
        self.con = sql.connect('database.db')
        self.con.row_factory = sql.Row
        self.cur = self.con.cursor()
        self.parameters = [[4,15],
                           ['none','petrol','fusion','steam','bio','electric','rocket','hamster','thermo','solar','wind'],
                           [0,100],
                           ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'],
                           ['plain','vstripe','hstripe','dstripe','checker','spot'],
                           ["knobbly","slick","steelband","reactive","maglev"],
                           ['none','wood','aluminium','thinsteel','thicksteel','titanium'],
                           ['none', 'spike', 'flame', 'charge', 'biohazard'],
                           ['true','false'],
                           ['steady','defensive','offensive','titfortat','random']
                           ]


    def fill_form(self):
        if type(self.buggy) is list:
            return self.buggy
        elif self.buggy == None:
            self.random_buggy()
            return self.value_fills
        else:
            self.cur.execute(
                "SELECT qty_wheels,power_type,power_units,aux_power_type,aux_power_units,hamster_booster,flag_color_primary,flag_pattern,flag_color_secondary,tyres,qty_tyres,armour,attack,qty_attacks,fireproof,insulated,antibiotic,banging,algo FROM buggies WHERE id=?",
                (self.buggy,))
            self.record = self.cur.fetchone()
            try:
                for data in enumerate(self.record):
                    self.value_fills.append(data[1])
            except:
                self.value_fills = []
        return self.value_fills

    def random_buggy(self):
        self.value_fills = []
        self.value_fills.append(random.randint(self.parameters[0][0], self.parameters[0][1]) * 2)
        self.value_fills.append(self.parameters[1][random.randint(0, 10)])
        self.value_fills.append(random.randint(1, 10))
        self.value_fills.append(self.parameters[1][random.randint(0, 10)])
        self.value_fills.append(random.randint(1, 10))
        if self.value_fills[1] == 'hamster' or self.value_fills[3] == 'hamster':
            self.value_fills.append(random.randint(0, 5))
        else:
            self.value_fills.append(0)
        temp_colour = '#'
        for i in range(6):
            temp_colour += self.parameters[3][random.randint(0,15)]
        self.value_fills.append(temp_colour)
        self.value_fills.append(self.parameters[4][random.randint(0,5)])
        temp_colour = '#'
        for i in range(6):
            temp_colour += self.parameters[3][random.randint(0,15)]
        self.value_fills.append(temp_colour)
        self.value_fills.append(self.parameters[5][random.randint(0,4)])
        self.value_fills.append(random.randint(self.value_fills[0], 30))
        self.value_fills.append(self.parameters[6][random.randint(0,5)])
        self.value_fills.append(self.parameters[7][random.randint(0,4)])
        self.value_fills.append(random.randint(0, 20))
        for i in range(3):
            self.value_fills.append(self.parameters[8][random.randint(0,1)])
        self.value_fills.append(self.parameters[9][random.randint(0,4)])
        result = buggy_validation(self.value_fills)
        if result.passback() == 'error':
            return self.random_buggy()
        else:
            return self.value_fills


if __name__ == '__main__':
    main = fill_form(None)

