#float arithemtic is inaccurate due to binary precision so need to use decimal and convert after
from decimal import Decimal
from typing import Dict, List, Set
import string

"""
for me personally the credit calculation is incredibly tricky
it is not tricky because of the complexity of the rules
but because of the edge cases that could potentially exist due to lack of clarity of what exactly a word is
and this affects the unique words rule and character length rule
(Note: A “word” is defined as any continual sequence of letters, plus ‘ and -)

for example are these words?
dog---
cats'''
dog'-

dog-cat'frog-cow
---------
dog78 in this case maybe the length would be 0 or 3 or 5
dog78cat

long-term in a hyphenated word
but is long- valid?

These are just some examples, so I've decided to make the assumption (based on the API) that a word is a normal english word
delimited by a space and if there is punctuation on at the end of the word discount it (. , !, ?) etc
"""

class TextToCredits:
    def __init__(self, text: str):
        self.text: int = text
        self.character_length: int = len(text)
        self.total_credits: Decimal = Decimal()
        self.words: Dict[str, int] = dict()
        self.counter: Dict[str, int] = dict()
    
    def get_total_credits(self):
        self.__calculate_total_credit()
        return float(self.total_credits)
    
    def __calculate_total_credit(self):
        self.__set_base_cost()
        self.__character_count()
        self.__word_multipliers()
        self.__third_vowel()
        self.__length_penalty()
        self.__unique_character_bonus()
        self.__palindrome()

    def __set_base_cost(self):
        self.total_credits = Decimal(1)
    
    def __character_count(self):
        character_cost: Decimal = Decimal('0.05')
        total_character_cost: Decimal = character_cost * self.character_length
        self.total_credits += total_character_cost
    
    def __word_multipliers(self):
        small_word_cost: Decimal = Decimal('0.1')
        medium_word_cost: Decimal = Decimal('0.2')
        large_word_cost: Decimal = Decimal('0.3')
        
        temp: List[str] = self.text.split(" ")
        
        for word in temp:
            word_length: int = self.__helper(word)
            
            if 1 <= word_length <= 3:
                self.total_credits += small_word_cost
            
            elif 4 <= word_length <= 7:
                self.total_credits += medium_word_cost
            
            elif word_length >= 8:
                self.total_credits += large_word_cost
    
    def __third_vowel(self):
        third_vowel_cost: Decimal = Decimal('0.3')
        total_vowel_cost: Decimal = Decimal()
        vowels: Set[str] = {'a', 'e', 'i', 'o', 'u'
                            'A', 'E', 'I', 'O', 'U'}
        
        for i in range(self.character_length):
            character: str = self.text[i]

            #the third character will have a remainder of 2 if 0-based indexing is used
            #a, b, c = 0, 1, 2... 2 % 3 = 2
            if character in vowels and i % 2 == 2:
                total_vowel_cost += third_vowel_cost

        self.total_credits += total_vowel_cost
    
    def __length_penalty(self):
        length_penatly: Decimal = Decimal('5')
        
        if self.character_length > 100:
            self.total_credits += length_penatly

    def __unique_character_bonus(self):
        unique_bonus: Decimal = Decimal('2')
        temp: List[str] = self.text.split(" ")
        
        for word in temp:
            word_length: int = self.__helper(word)
            check_word: str = word[: word_length] #removes punctuation if it exists
            
            self.counter[check_word] = self.counter.get(check_word, 0) + 1
        
        for word in self.counter:
            count: int = self.counter[word]
            
            if count > 1:
                return

        self.total_credits = max(self.total_credits - unique_bonus, Decimal('1'))
        
    
    def __palindrome(self):
        is_palindrome: bool = self.__is_palindrome()
        
        if is_palindrome:
            self.total_credits *= 2
    
    #helper function to see something is a word or not
    def __helper(self, word: str) -> bool:
        word_length: int = len(word)
        last_character: str = word[-1]
        
        if last_character not in string.ascii_letters or last_character not in "'-":
            word_length -= 1
        
        return word_length
    
    def __is_palindrome(self) -> bool:
        is_palindrome: bool = True
        left: int = 0
        right: int = self.character_length - 1
        
        """
        Palindromes: If the entire message is a palindrome 
        (that is to say, after converting all uppercase letters into lowercase letters 
        and removing all non-alphanumeric characters, it reads the same forward and backward), 
        double the total cost after all other rules have been applied.
        
        based on the rules I am going to include numbers as abc....123456789 are alphanumeric so I'll remove everything else
        """
        while left < right:
            left_character: str = self.text[left]
            right_character: str = self.text[right]
            
            if not left_character.isalnum():
                left += 1
                continue
            
            if not right_character.isalnum():
                right -= 1
            
            if left_character != right_character:
                is_palindrome = False
                break
            
            left += 1
            right -= 1
            
        return is_palindrome
