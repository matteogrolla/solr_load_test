# Copyright 2015 Matteo Grolla
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import codecs
from random import randint
import numpy as np
import logging
from random import choice
import time

logging.basicConfig(level=logging.DEBUG)

class FieldGen:
    def __init__(self, wordlist_path):
        self.last_zipf_indexes = None

        file = codecs.open(wordlist_path, 'rU', 'utf-8')
        raw = file.read()
        tokens = raw.split()

        #Swap comments if file contains frequencies after words
        #self.wf = [(tokens[i], tokens[i+1]) for i in range(0,len(tokens),2)]
        #self.w = [tokens[i] for i in range(0,len(tokens),2)]
        self.w = [tokens[i] for i in range(0,len(tokens))]
        self.wnp = np.array(self.w)
        logging.info("numTerms: %s" % len(self.w))
        file.close()

        file = codecs.open("../bin/ateco_codes.txt", 'rU', 'utf-8')
        raw = file.read()
        tokens = raw.split()
        self.ateco_codes = [tokens[i] for i in range(0,len(tokens))]
        file.close()

    def random(self, num_words=50, word_source = None):
        if word_source == None:
            word_source = self.w
        words = []
        text = " "
        for i in xrange(0,num_words):
            word = word_source[randint(0,len(word_source)-1)]
            words.append(word)
            #text += " " + word

        return text.join(words)

    def zipf(self, num_words=50):
        words = []
        text = " "
        emitted = 0
        len_w = len(self.w)
        while True:
            indexes = np.random.zipf(1.2, num_words)
            filtered = indexes[indexes < len_w]
            for i in filtered:
                words.append(self.w[i])
                emitted += 1
                if emitted >= num_words:
                    #return text
                    return text.join(words)

    def zipf_fast(self, num_words=50):
        if self.last_zipf_indexes is None:
            self.last_zipf_indexes = np.array(self._zipf_indexes(num_words))

        len_w = len(self.w)

        indexes = np.random.zipf(1.2, num_words)
        indexes[indexes >= len_w] = self.last_zipf_indexes

        #words = self.wnp[indexes]
        '''
            TODO: improve performance
            currently it's a bit faster than normal zipf but:
            lot of time is spent conversion of words from ndarray to list
            if not even more time is spent joining words in ndarray
            this doesn't work
            np.core.defchararray.join("-", np.array(["1", "2"]))
array(['1', '2'],
      dtype='|S1')

        '''
        #words_list = words.tolist()
        words_list = [self.w[i] for i in indexes]
        return " ".join(words_list)


    def _zipf_indexes(self, num_words):
        emitted = 0
        len_w = len(self.w)
        res = []

        while True:
            indexes = np.random.zipf(1.1, num_words)
            filtered = indexes[indexes < len_w]
            for i in filtered:
                res.append(i)
                emitted += 1
                if emitted >= num_words:
                    #return text
                    return res

    def random_code(self, num_chars, letters="abcdefghilmnopqrstuvz1234567890"):
        code = ''.join([choice(letters) for i in xrange(0,num_chars)])
        return code

    def random_tuple(self, num_el, el_source):
        res = [choice(el_source) for i in xrange(0, num_el)]
        return res

def go():
    tg = FieldGen('../bin/wordlist_wiki.txt')
    for i in xrange(0, 10000):
        value = tg.zipf_fast(400)

if __name__ == "__main__":
    start_time = time.time()

    tg = FieldGen('../bin/wordlist_wiki.txt')
    for i in xrange(0, 10000):
        value = tg.zipf_fast(400)
    #value = tg.random_tuple(5, tg.ateco_codes)

    print("%f seconds" % (time.time() - start_time))
    #print value


