SUPERSCRIPT = "⁰¹²³⁴⁵⁶⁷⁸⁹"
import random

class Polynomial:
    def __init__(self, *data):
        self.poly = list(data)
    
    def sort(self):
        '''Sorts the polynomial from greatest to smallest exponent. This isn't necessary for any operations'''
        self.poly = sorted(self.poly, key=lambda d: d[1], reverse=True)

    def evaluate(self, x):
        '''Plugs in the value of x for each part of the polynomial and solves the opperation'''
        answer = 0

        for data in self.poly:
            coeff, exp = data
            answer += coeff * (x**exp)

        return answer

    def strip(self):
        '''Gets rid of any monomial inside the polynomial data who's **coefficient is 0**, as they are essentially useless.'''
        new_poly = []
        for data in self.poly:
            if data[0]:
                new_poly.append(data)

        self.poly = new_poly

    def degree(self):
        '''Returns the highest exponent (degree) of the polynomial'''
        highest = 0
        for data in self.poly:
            if data[1] > highest:
                highest = data[1]
        return highest
    
    def simplify(self):
        '''Combines all like terms and compresses the polynomial'''

        poly_dict = {}
        for data in self.poly:
            coeff, exp = data
            existing_value = poly_dict.get(exp) or 0
            poly_dict[exp] = existing_value + coeff
        
        self.poly = [(coeff, exp) for exp,coeff in poly_dict.items()]
    
    def benchmark(self):
        '''Returns a string of information about the polynomial. May be useful for benchmarking or analytics.'''
        length = len(self)
        degree = self.degree()
        return f"/// Polynomial Information ///\n - Length: {length}\n - Degree: {degree}\n - Equation: ({self})"
    
    def to_dict(self):
        '''Returns the polynomial as a dictionary with "key-value pairs". The keys are exponents and the values are the coefficients.\n 
        **It's HIGHLY recommended to *simplify* the polynomial before using this method!**'''
        return dict([(data[1], data[0]) for data in self.poly])
    
    def shuffle(self):
        '''randomly suffles all the pieces of the polynomial'''
        random.shuffle(self.poly)
    
    def join(self, other_poly):
        '''Joins both polynomials together into 1 bigger polynomial'''
        #self.poly = list(set(self.poly).union(set(other_poly.poly)))
        #for other_data in other_poly.poly:
        self.poly.extend(other_poly.poly)

    def __add__(self, other_poly):
        self.join(other_poly)
        self.simplify()
        self.sort()
        self.strip()
        #addsub_operation(self, other_poly, 1)
        return self

    def __sub__(self, other_poly):
        self.join(-other_poly)
        self.simplify()
        self.sort()
        self.strip()
        #addsub_operation(self, other_poly, -1)
        return self
    
    def __mul__(self, other_poly):
        new_poly = Polynomial()

        for data in self.poly:
            for other_data in other_poly.poly:
                new_poly.poly.append((data[0] * other_data[0], data[1] + other_data[1]))

        new_poly.simplify()
        new_poly.sort()
        new_poly.strip()

        return new_poly

    def __neg__(self):
        return Polynomial(*[(data[0] * -1, data[1]) for data in self.poly])

    def __str__(self):
        if not len(self):
            return "0"
        
        first = True
        all = []
        for data in self.poly:            
            coeff, exp = data

            if not coeff:
                continue

            negative = coeff < 0

            # simplify the coefficient text as much as possible
            num_str = str(coeff)
            num_str = num_str[1:] if negative else num_str # remove negative symbol in the number (its used bellow)
            num_str = num_str[1:] if abs(coeff) == 1 else num_str # remove coefficent number if equal to 1
            
            # how the add/sub symbols should be spaced or removed based on its position in the polynomial
            symbol_str = "-" if (first and negative) else (" - " if negative else (" + " if not first else ""))
            first = False

            x_str, exp_str = "x" if exp else "", get_superscript(exp)

            all.append(f"{symbol_str}{num_str}{x_str}{exp_str}")

        return "".join(all).strip()
    
    def __len__(self):
        return len(self.poly)
    
    def __getitem__(self, n):
        if type(n) == slice:
            return Polynomial(*self.poly[n])
        else:
            return Polynomial(self.poly[n])
    
def addsub_operation(p1: Polynomial, p2: Polynomial, negative):
    poly_dict = {}
    for data in p1.poly:
        coeff, exp = data
        poly_dict[exp] = coeff

    for data in p2.poly:
        coeff, exp = data

        existing_value = poly_dict.get(exp) or 0
        poly_dict[exp] = existing_value + (coeff * negative)

    p1.poly = [(coeff, exp) for exp,coeff in poly_dict.items()]
    p1.strip()

def multiply_operation(p1: Polynomial, p2: Polynomial):
    pass

def get_superscript(exp):
    if exp <= 1:
        return ""
    
    string = ""
    for n in str(exp):
        string = f"{string}{SUPERSCRIPT[int(n)]}"

    return string
