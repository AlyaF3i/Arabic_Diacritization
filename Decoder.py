
import numpy as np

class Decoder:
    def __init__(self):
        self.rev_harakat = {0: '', 1: '', 2: 'َّ', 3: 'ِّ', 4: 'ُّ', 5: '', 6: 'ً', 7: 'َ', 8: 'ُ', 9: 'ِ', 10: 'ّ', 11: 'ْ', 12: '', 13: 'ًّ', 14: 'ٌّ', 15: 'ٍّ'}
        self.rev_vocab = {0: '', 1: '!', 2: '"', 3: '$', 4: '(', 5: ')', 6: '*', 7: '+', 8: '-', 9: '.', 10: '/', 11: ':', 12: '=', 13: '[', 14: ']', 15: '^', 16: ' ', 17: '{', 18: '}', 19: '~', 20: '،', 21: '؟', 22: 'ء', 23: 'أ', 24: 'إ', 25: 'ا', 26: 'ب', 27: 'ة', 28: 'ت', 29: 'ث', 30: 'ج', 31: 'ح', 32: 'خ', 33: 'د', 34: 'ذ', 35: 'ر', 36: 'ز', 37: 'س', 38: 'ش', 39: 'ص', 40: 'ض', 41: 'ط', 42: 'ظ', 43: 'ع', 44: 'غ', 45: 'ف', 46: 'ق', 47: 'ك', 48: 'ل', 49: 'م', 50: 'ن', 51: 'ه', 52: 'و', 53: 'ى', 54: 'ي', 55: '–', 56: '‘', 57: '’', 58: '“', 59: '#'}


    def decode(self, input : np.array, prediction : np.array) -> str:
      """
        input is the characters [vocab]
        prediction is the harakat [harakat]
      """
      output = ""
      for char_line, hrkah_line in zip(input, prediction):
        for char, hrkah in zip(char_line, hrkah_line):
          decoded_char = self.rev_vocab[char]
          if decoded_char:
            output += decoded_char + self.rev_harakat[hrkah]
        #output += "\n"
      return output #del_doublicated_spaces.sub(r'\1', output)
