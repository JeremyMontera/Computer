from typing import List
from .bit import Bit, BitError

class BitString:
    
    def __init__(self, max_length: int):
        self._max_length: int = max_length
        self._bits: List[Bit] = []

    def __len__(self) -> int:
        return sum(1 for bit in self._bits if bit is not None)
    
    @property
    def max_length(self) -> int:
        return self._max_length
    
    def clear(self) -> None:
        self._bits = [None] * self._max_length
    
    def pop_left(self) -> Bit:
        if len(self) == 0:
            raise BitError("This bit string is empty!")
        
        ret: Bit = self._bits[0]
        self._bits = self._bits[1: ]
        return ret
    
    def pop_right(self) -> Bit:
        if len(self) == 0:
            raise BitError("This bit string is empty!")
        
        ret: Bit = self._bits[-1]
        self._bits = self._bits[: -1]
        return ret
    
    def push_left(self, bit: Bit) -> None:
        if len(self) == self._max_length:
            raise BitError("This bit string has the maximum number of bits allowed!")
        
        self._bits = [bit] + self._bits

    def push_right(self, bit: Bit) -> None:
        if len(self) == self._max_length:
            raise BitError("This bit string has the maximum number of bits allowed!")
        
        self._bits += [bit]
