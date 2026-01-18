import string
import random
import itertools
from typing import List, Set, Iterator, Tuple, Optional

class PasswordGeneratorLogic:
    """
    Handles the core logic for generating password lists.
    
    This class manages data storage (word/number/symbol lists) and 
    implements the algorithms for generating password combinations 
    and character injection.
    """

    def __init__(self):
        self.words: List[str] = []
        self.numbers: List[str] = []
        self.symbols: List[str] = []

    def load_list_from_file(self, file_path: str) -> List[str]:
        """
        Reads a text file and returns a list of non-empty lines.

        Args:
            file_path (str): Path to the input file.

        Returns:
            List[str]: Cleaned list of lines from the file.

        Raises:
            IOError: If the file cannot be read.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]

    def set_lists(self, words: List[str], numbers: List[str], symbols: List[str]):
        """Updates the internal lists used for generation."""
        self.words = words
        self.numbers = numbers
        self.symbols = symbols

    def get_list_counts(self) -> int:
        """Returns the number of non-empty loaded lists."""
        return sum([bool(self.words), bool(self.numbers), bool(self.symbols)])

    def get_insertion_characters(self, choice: str) -> List[str]:
        """
        Returns a list of characters based on user selection.
        
        Args:
            choice (str): "Numbers", "Special Characters", or "Both".
        """
        if choice == "Numbers":
            return list(string.digits)
        elif choice == "Special Characters":
            return list(string.punctuation)
        elif choice == "Both":
            return list(string.digits + string.punctuation)
        return []

    def calculate_total_combinations(self, order: List[str]) -> int:
        """Calculates the theoretical maximum number of combinations based on list sizes."""
        total = 1
        for elem in order:
            if elem == 'word' and self.words:
                total *= len(self.words)
            elif elem == 'number' and self.numbers:
                total *= len(self.numbers)
            elif elem == 'symbol' and self.symbols:
                total *= len(self.symbols)
        return total

    def inject_characters(self, word: str, chars: List[str], num_insertions: int) -> str:
        """
        Randomly inserts characters into a specific word.

        Args:
            word (str): The target word.
            chars (List[str]): Pool of characters to insert.
            num_insertions (int): How many characters to insert.

        Returns:
            str: The modified word.
        """
        for _ in range(num_insertions):
            if len(word) == 0:
                break
            pos = random.randint(0, len(word))
            char = random.choice(chars)
            word = word[:pos] + char + word[pos:]
        return word

    def construct_password_with_injection(self, order: List[str], insert_chars_list: List[str], num_insertions: int) -> str:
        """
        Reconstructs a password by picking random elements and injecting characters into words.
        
        Note: This logic mirrors the original 'insert_chars_in_password' behavior where
        random elements are re-selected during the injection phase.
        """
        components = []
        for elem in order:
            if elem == 'word' and self.words:
                word = self.words[random.randint(0, len(self.words) - 1)]
                word = self.inject_characters(word, insert_chars_list, num_insertions)
                components.append(word)
            elif elem == 'number' and self.numbers:
                number = self.numbers[random.randint(0, len(self.numbers) - 1)]
                components.append(number)
            elif elem == 'symbol' and self.symbols:
                symbol = self.symbols[random.randint(0, len(self.symbols) - 1)]
                components.append(symbol)
        
        return ''.join(components)

    def generate_random_password(self, order: List[str], insert_option: bool, 
                                 insert_chars_list: List[str], num_insertions: int,
                                 min_len: int, max_len: float) -> Optional[str]:
        """
        Generates a single random password based on criteria.
        
        Returns:
            str: The password if it meets length criteria, else None.
        """
        components = []
        for elem in order:
            if elem == 'word' and self.words:
                word = random.choice(self.words)
                if insert_option and insert_chars_list:
                    word = self.inject_characters(word, insert_chars_list, num_insertions)
                components.append(word)
            elif elem == 'number' and self.numbers:
                components.append(random.choice(self.numbers))
            elif elem == 'symbol' and self.symbols:
                components.append(random.choice(self.symbols))
        
        password = ''.join(components)
        
        if min_len <= len(password) <= max_len:
            return password
        return None

    def get_combinations_iterator(self, order: List[str]) -> Iterator[Tuple]:
        """Returns an iterator for all cartesian products of the lists."""
        lists = []
        for elem in order:
            if elem == 'word' and self.words:
                lists.append(self.words)
            elif elem == 'number' and self.numbers:
                lists.append(self.numbers)
            elif elem == 'symbol' and self.symbols:
                lists.append(self.symbols)
        
        return itertools.product(*lists)
