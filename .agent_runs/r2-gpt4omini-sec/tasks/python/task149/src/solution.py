# src/solution.py

def number_to_words(n: int) -> str:
    if not isinstance(n, int):
        raise TypeError("Input must be an integer.")
    if n < -999999999999 or n > 999999999999:
        raise ValueError("Input must be in the range -999999999999 to 999999999999.")

    if n == 0:
        return "zero"
    
    def one(num):
        switcher = {
            1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
            6: "six", 7: "seven", 8: "eight", 9: "nine"
        }
        return switcher.get(num, "")
    
    def two_less_20(num):
        switcher = {
            10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen",
            14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen",
            18: "eighteen", 19: "nineteen"
        }
        return switcher.get(num, "")
    
    def ten(num):
        switcher = {
            2: "twenty", 3: "thirty", 4: "forty", 5: "fifty",
            6: "sixty", 7: "seventy", 8: "eighty", 9: "ninety"
        }
        return switcher.get(num, "")
    
    def two(num):
        if num == 0:
            return ""
        elif num < 10:
            return one(num)
        elif num < 20:
            return two_less_20(num)
        else:
            tenner = ten(num // 10)
            rest = one(num % 10)
            return tenner + ("-" + rest if rest else "")
    
    def three(num):
        hundred = num // 100
        rest = num % 100
        if hundred and rest:
            return one(hundred) + " hundred " + two(rest)
        elif hundred:
            return one(hundred) + " hundred"
        else:
            return two(rest)
    
    def words(num):
        billion = num // 1000000000
        million = (num // 1000000) % 1000
        thousand = (num // 1000) % 1000
        remainder = num % 1000
        
        parts = []
        if billion:
            parts.append(three(billion) + " billion")
        if million:
            parts.append(three(million) + " million")
        if thousand:
            parts.append(three(thousand) + " thousand")
        if remainder:
            parts.append(three(remainder))
        
        return " ".join(parts)
    
    result = words(abs(n))
    if n < 0:
        return "negative " + result
    return result
