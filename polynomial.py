from copy import deepcopy


class Polynomial(object):
    def __init__(self, *coeff):
        if len(coeff) == 1:
            coeff = coeff[0]
        if type(coeff) == int or type(coeff) == float:
            self.coeff = [coeff]
        elif type(coeff) == str:
            self.coeff = list(map(Polynomial.num, coeff.split()))
        elif type(coeff) == Polynomial:
            self.coeff = deepcopy(coeff.coeff)
        elif type(coeff) == dict:
            self.coeff = [0] * (sorted(coeff)[-1] + 1)
            for key in coeff:
                self.coeff[key] = coeff[key]
        else:
            self.coeff = deepcopy(list(coeff))
        if self.coeff == []:
            self.coeff = [0]
        n = len(self.coeff) - 1
        while n != 0 and self.coeff[n] == 0:
            n -= 1
        if n != 0:
            self.coeff = self.coeff[:(n + 1)]
        else:
            self.coeff = [self.coeff[0]]
        self.counter = -1
        
    def __repr__(self):
        return ('Polynomial '+ str(self.coeff))
    
    def __str__(self):
        n = len(self.coeff) - 1
        if n == 0:
            return str(self.coeff[0])
        elif n == 1:
            a = ''
            if self.coeff[1] == -1:
                a += '-x'
            elif self.coeff[1] == 1:
                a += 'x'
            else:
                a += str(self.coeff[1]) + 'x'
            if self.coeff[0] < 0:
                a += ' - ' + str(abs(self.coeff[0]))
            elif self.coeff[0] > 0:
                a += ' + ' + str(self.coeff[0])
            return a              
        else:
            a = ''
            if self.coeff[-1] == 1:
                a += 'x' + Polynomial.degr(n)
            elif self.coeff[-1] == -1:
                a += '-x' + Polynomial.degr(n)
            else:
                a = str(self.coeff[-1]) + 'x' + Polynomial.degr(n)
            for i in range(n - 1, 1, -1):
                if self.coeff[i] < 0:
                    if self.coeff[i] != -1:
                        a += ' - ' + str(abs(self.coeff[i])) + 'x' + Polynomial.degr(i)
                    else:
                        a += ' - ' + 'x' + Polynomial.degr(i)
                elif self.coeff[i] > 0:
                    if self.coeff[i] != 1:
                        a += ' + ' + str(self.coeff[i]) + 'x' + Polynomial.degr(i)
                    else:
                        a += ' + ' + 'x' + Polynomial.degr(i)
            if self.coeff[1] < 0:
                if self.coeff[1] != -1:
                    a += ' - ' + str(abs(self.coeff[1])) + 'x'
                else:
                    a += ' - ' + 'x'
            elif self.coeff[1] > 0:
                if self.coeff[1] != 1:
                    a += ' + ' + str(self.coeff[1]) + 'x'
                else:
                    a += ' + ' + 'x'
            if self.coeff[0] < 0:
                a += ' - ' + str(abs(self.coeff[0]))
            elif self.coeff[0] > 0:
                a += ' + ' + str(self.coeff[0])
            return a                        


    def num(a):
        if int(float(a)) == float(a):
            return int(a)
        else:
            return float(a)

    def degr(m):
        return '^' + str(m)
        #A = list(map(int, list(str(m))))
        #line = ''
        #for i in range(len(A)):
            #if A[i] == 0:
                #line += chr(8304)
            #elif A[i] == 1:
                #line += chr(185)
            #elif A[i] == 2 or A[i] == 3:
                #line += chr(178 + (A[i] - 2))
            #else:
                #line += chr(8308 + (A[i] - 4))
        #return line
    
    def __eq__(self, other):
        return self.coeff == Polynomial(other).coeff
    
    def __ne__(self, other):
        return self.coeff != Polynomial(other).coeff
    
    def __neg__(self):
        return Polynomial(list(map(lambda x: x * (-1), self.coeff)))
    
    def __pos__(self):
        return self
    
    def __bool__(self):
        return self.coeff != [0]
                
    def __add__(self, other):
        A = Polynomial(self).coeff
        B = Polynomial(other).coeff
        if len(A) < len(B):
            A += [0] * (len(B) - len(A))
        for i in range(len(B)):
            A[i] += B[i]
        return Polynomial(A)
    
    def __iadd__(self, other):
        self = self + other
        return self
    
    def __radd__(self, other):
        return Polynomial(self) + Polynomial(other)
    
    def __sub__(self, other):
        return Polynomial(self) + (-Polynomial(other))
    
    def __rsub__(self, other):
        return (-Polynomial(self)) + Polynomial(other)
    
    def __isub__(self, other):
        self = self - other
        return self
    
    def __mul__(self, other):
        A = Polynomial(self).coeff
        B = Polynomial(other).coeff
        C = Polynomial()
        for j in range(len(B)):
            C += Polynomial([0] * j + [A[i] *  B[j] for i in range(len(A))])
        return C
    
    def __rmul__(self, other):
        return Polynomial(self) * Polynomial(other)
    
    def __imul__(self, other):
        self = self * other
        return self    
    
    def __call__(self, other):
        a = 0
        B = self.coeff
        for i in range(len(B)):
            a += (((other) ** i) * B[i])
        return a
    
    def __iter__(self):
        return iter([(i, self.coeff[i]) for i in range(len(self.coeff))])
    
    def __next__(self):
        self.counter += 1
        if self.counter <= len(self.coeff):
            return list(A.__iter__())[self.counter]
        else:
            raise StopIteration

    def degree(self):
        return len(self.coeff) - 1
    
    def __divmod__(self, other):
        A = Polynomial(self)
        B = Polynomial(other)
        if A.degree() >= B.degree():
            C = [0] * (A.degree() - B.degree() + 1)
            for i in range(1, len(C) + 1):
                C[-i] += Polynomial.num(A.coeff[-1] / B.coeff[-1])
                A -= (B * Polynomial(C[:len(C) - i + 1]))
            return (Polynomial(C), Polynomial(self) - B * Polynomial(C))
        else:
            return (Polynomial(), A)
        
    def __mod__(self, other):
        return (self.__divmod__(other))[1]
    
    def __imod__(self, other):
        self = (self.__divmod__(other))[1]
        return self

    def __floordiv__(self, other):
        return (self.__divmod__(other))[0]

    def __ifloordiv__(self, other):
        self = (self.__divmod__(other))[0]
        return self
    
    def gcd(self, other):
        A = Polynomial(self)
        B = Polynomial(other)
        print(A, B)
        while B != 0:
            A, B = B, A % B
            print(A, B)
        return A
