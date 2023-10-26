from argparse import ArgumentParser
import re
import sys

LETTER_TO_NUMBER = {
    'A': '2',
    'B': '2',
    'C': '2',
    'D': '3',
    'E': '3',
    'F': '3',
    'G': '4',
    'H': '4',
    'I': '4',
    'J': '5',
    'K': '5',
    'L': '5',
    'M': '6',
    'N': '6',
    'O': '6',
    'P': '7',
    'Q': '7',
    'R': '7',
    'S': '7',
    'T': '8',
    'U': '8',
    'V': '8',
    'W': '9',
    'X': '9',
    'Y': '9',
    'Z': '9'
}

class PhoneNumber:
    """
    A class representing the phone numbers based on the North American Numbering Plan(NANP) system.

    Attributes:
        area_code(str): The area code.
        exchange_code(str): The exchange code.
        line_number(str): The line's number.
    """

    def __init__(self, number):
        """
        Initializes the attributes with their respective values. The constructor.

        Args:
            number (str or int): A string or integer representing a phone number.
        
        Side Effects:
            Sets the values of the PhoneNumber instance's attributes.

        Raises:
            TypeError: If the argument is not a string or integer.
            ValueError: If the number is not a valid phone number.
        """
        if not isinstance(number, (str, int)):
            raise TypeError("Phone number must be a string or integer.")
        
        reg_exp = r'[^0-9a-zA-Z]'
        number_str = str(number)
        number_str = re.sub(reg_exp, '', number_str)  # Remove all non-alphanumeric characters

        stack = ""
        for char in number_str:
            if char in LETTER_TO_NUMBER:
                stack += LETTER_TO_NUMBER[char]
            else:
                stack += char

        if len(number_str) == 10:
            self.area_code = stack[:3]
            self.exchange_code = stack[3:6]
            self.line_number = stack[6:]
        elif len(number_str) == 11 and number_str[0] == '1':
            self.area_code = stack[1:4]
            self.exchange_code = stack[4:7]
            self.line_number = stack[7:]
        else:
            raise ValueError("Phone number must have exactly 10 or 11 digits.")
        
        if self.area_code[0] in ['0', '1'] or self.exchange_code[0] in ['0', '1'] or self.exchange_code[1:] == '11':
            raise ValueError("Phone number contains an invalid area code or exchange code.")
        
        invalid_codes = ['011', '111', '211', '311', 
                         '411', '511', '611', '711', '811', '911']
        if self.area_code in invalid_codes or self.exchange_code in invalid_codes:
            raise ValueError("Phone number contains an invalid area code or exchange code.")

    def __int__(self):
        """
        Converts the phone number to an integer.

        Returns:
            An integer representation.
        """
        return int(f"{self.area_code}{self.exchange_code}{self.line_number}")
    
    def __str__(self):
        """
        Returns the phone number in standard format.

        Returns:
            A string representation.
        """
        return f"({self.area_code}) {self.exchange_code}-{self.line_number}"

    def __repr__(self):
        """
        Returns a string representation of the PhoneNumber object.

        Returns:
            int: A string representation.
        """
        return f"PhoneNumber('{self.__int__()}')"

    def __lt__(self, other):
        """
        Define the behavior for the < operator.

        Args:
            other (PhoneNumber): The other PhoneNumber instance to compare to.

        Returns:
            bool: True if this PhoneNumber instance is less than the other PhoneNumber instance, False otherwise.

        """
        return int(self) < int(other)

def read_numbers(filepath):
    """
    Opens a file with names and numbers. Sorts them in puts them in a tuple.

    Args:
        filepath (str): the path to the names and the phone numbers file.

    Returns:
        tup_list (list): the list of the tuples with the name, phone number.
    """
    tup_list = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            name, number = line.strip().split("\t")
            try:
                phone_number = PhoneNumber(number)
                tup_list.append((name, phone_number))
            except TypeError:
                pass
            except ValueError:
                pass
        
    tup_list.sort(key=lambda x: x[1])
    return tup_list

def main(path):
    """Read data from path and print results.
    
    Args:
        path (str): path to a text file. Each line in the file should consist of
            a name, a tab character, and a phone number.
    
    Side effects:
        Writes to stdout.
    """
    for name, number in read_numbers(path):
        print(f"{number}\t{name}")

def parse_args(arglist):
    """Parse command-line arguments.
    
    Expects one mandatory command-line argument: a path to a text file where
    each line consists of a name, a tab character, and a phone number.
    
    Args:
        arglist (list of str): a list of command-line arguments to parse.
        
    Returns:
        argparse.Namespace: a namespace object with a file attribute whose value
        is a path to a text file as described above.
    """
    parser = ArgumentParser()
    parser.add_argument("file", help="file of names and numbers")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.file)