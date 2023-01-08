import re
from keras_preprocessing.sequence import pad_sequences

class Preprocess:

    def __init__(self):
        self.vocab = {'PAD': 0, '!': 1, '"': 2, '$': 3, '(': 4, ')': 5, '*': 6, '+': 7, '-': 8, '.': 9, '/': 10, ':': 11, '=': 12, '[': 13, ']': 14, '^': 15, '_': 16, '{': 17, '}': 18, '~': 19, '،': 20, '؟': 21, 'ء': 22, 'أ': 23, 'إ': 24, 'ا': 25, 'ب': 26, 'ة': 27, 'ت': 28, 'ث': 29, 'ج': 30, 'ح': 31, 'خ': 32, 'د': 33, 'ذ': 34, 'ر': 35, 'ز': 36, 'س': 37, 'ش': 38, 'ص': 39, 'ض': 40, 'ط': 41, 'ظ': 42, 'ع': 43, 'غ': 44, 'ف': 45, 'ق': 46, 'ك': 47, 'ل': 48, 'م': 49, 'ن': 50, 'ه': 51, 'و': 52, 'ى': 53, 'ي': 54, '–': 55, '‘': 56, '’': 57, '“': 58, 'UNK': 59}

        self.harakat = {'PAD': 0, '#': 1, 'A': 2, 'B': 3, 'C': 4, '_': 5, 'ً': 6, 'َ': 7, 'ُ': 8, 'ِ': 9, 'ّ': 10, 'ْ': 11, 'UNK': 12, 'D': 13, 'E': 14, 'F': 15}



        self.ALPHABET = [chr(n) for n in list(range(0x0621, 0x063B)) + list(range(0x0641, 0x064B))]
        self.DIACRITICS = [chr(w) for w in range(0x064B, 0x0653)]
        self.DIACRITICS_joined = "".join(self.DIACRITICS)
        self.DIACRITICS_NO_SHADAH = self.DIACRITICS[:]
        self.DIACRITICS_NO_SHADAH.remove(chr(0x0651))
        self.ALPHADIAC = self.ALPHABET + self.DIACRITICS
        self.ALPHADIACSTR = "".join(self.ALPHADIAC)

        self.tremoveStartingDiacritics    =   re.compile('^[' + ''.join(self.DIACRITICS) + ']+?')
        self.tremoveLeadingDiacritics     =   re.compile(' [' + ''.join(self.DIACRITICS) + ']+?')
        self.tSpreating = re.compile(fr'([{self.ALPHADIACSTR}])([^{self.ALPHADIACSTR}\s]+?)')
        self.tmultispaces = re.compile('(\s)\s+')
        self.tSpreating2 = re.compile(fr'([^{self.ALPHADIACSTR}\s]+?)([{self.ALPHADIACSTR}])')
        self.tmultidiacitics = re.compile(fr'[{"".join(self.DIACRITICS_NO_SHADAH)}]+?([{"".join(self.DIACRITICS)}])')
        #del_dic = re.compile(rf'[{"".join(DIACRITICS)}]+')


    def tremoveaa(self, text):
        text = self.tSpreating2.sub(r"\1 \2", text)
        text = self.tSpreating.sub(r"\1 \2", text)
        text = self.tremoveLeadingDiacritics.sub(' ', text)
        text = self.tremoveStartingDiacritics.sub('', text) #remove diactrics at the begin of word
        #handles the separation of punctuation
        text = self.tmultispaces.sub(r'\1', text) #handles multispaces and empty lines
        text = self.tmultidiacitics.sub(r'\1', text)
        return text

    def clean_and_reformat(self, txt : str) -> None:
        txt = self.tremoveaa(txt)
        output = []
        lines = txt.split('\n')
        for line in lines:
            if line.isspace():
                continue
            output.append(
                line.replace(" ", "_")
            )
        return  "\n".join(output)


    """
    splitting a text to X and Y
    X: the phrases without diacritization
    Y: the diacritization with out the letters
    """

    def split(self, txt : str) -> None:
        self.pattern = re.compile(f'[^{self.DIACRITICS_joined}][{self.DIACRITICS_joined}]*')
        self.from_to = {
                        "َّ" : "A",
                        "ِّ" : "B",
                        "ُّ" : "C",
                        "ًّ" : "D",
                        "ٍّ" : "E",
                        "ٌّ" : "F"
                        }


        matches = self.pattern.findall(txt)

        output_X = ''
        output_y = ''
        for match in matches:
            output_X += match[:1]
            hrkah = match[1:]
            output_y += hrkah if hrkah else "#"

        for from_, to_ in self.from_to.items():
            output_y = output_y.replace(from_, to_)


        return output_X, output_y


    def encode_seq(self, seq, mapping):
        sequences = list()
        for line in seq:
            # integer encode line
            #add a line for unseen chars !!!!
            encoded_seq = [mapping.get(char) for char in line]
            # store
            encoded_seq = [a if a else mapping.get("UNK") for a in encoded_seq]

            sequences.append(encoded_seq)
        return sequences

    #mapping should be either "X" or "Y"
    def encode_and_pad(self, data, mapping):
        if mapping == "X":
            map = self.vocab
        else:
            map = self.harakat

        sequences = self.encode_seq(data.split("\n"),map) # param is a list of all phrases to be encoded
        #padding
        pad_corp= pad_sequences(sequences,maxlen=125,padding='post',value=0)
        return(pad_corp)

    def prepare_text(self, txt: str) -> str :
        output = self.clean_and_reformat(txt)
        X = self.encode_and_pad(output, "X")

        return X
