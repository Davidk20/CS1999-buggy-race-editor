class buggy_validation():

    def __init__(self,new_buggy):
        self.buggy = new_buggy
        self.test1 = self.numerical_test()
        self.test2 = self.comparison_test()

    def passback(self):
        if self.test1 == 'fail' or self.test2 == 'fail':
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



if __name__ == '__main__':
    buggy_validation(None)