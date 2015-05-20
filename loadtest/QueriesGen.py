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

import urllib
import xml.etree.ElementTree as ET
import logging
import codecs
import re
import random
import numpy as np

logging.basicConfig(level=logging.INFO)

class QueriesGen:
    def __init__(self, collection_url):
        self.collection_url = collection_url

    def _load_wordlist(self, path):
        file = codecs.open(path, 'rU', 'utf-8')
        raw = file.read()
        tokens = raw.split()
        file.close()
        return tokens

    def gen_queries(self, field_name, num_terms, query_type="term", output_path="queries.txt"):

        terms = self.get_popular_terms(field_name, num_terms)
        terms_len = len(terms)
        p = re.compile('^[A-Za-z0-9]+$')
        out_file = codecs.open(output_path, 'w', encoding='utf-8')
        for idx,term in enumerate(terms):

            str = "q=%s:" % field_name
            plain_term = term[0]
            if query_type == "wildcard":
                #wildcard queries
                if len(plain_term) >= 5 and not(p.match(plain_term) is None):
                    logging.debug(plain_term)
                    term_wild = plain_term[:2]+'*'+plain_term[4:]
                    str += term_wild

            elif query_type == "codes":
                #term queries
                str += plain_term

            elif query_type == "term":
                #term queries
                str += '"%s"' %plain_term

            #     phrases generated this way on average find 0 results
            #     possibilities are:
            #     1)  generate a shingled index from the generated collection
            #         Read docs from generated collection and index them in another collection where the desired field
            #         is shingled. Now run GenerateQueries on this field with query_type="term"
            #     2)  initialize the random seed when running DocsGen
            #         initialize the same random seed when running QueriesGen
            #             make random.zipf produce the same integers as when running DocsGen
            #             use these as dictionary indexes to produce small phrases
            #         (More involved but avoid shingle index generation
            #         idea: seed could be every x documents to ease the alignment between DocsGen and QueriesGen)
            #
            # elif query_type == "phrase":
            #     #words = [terms[i][0] for i in random.sample(xrange(len(terms)), 3)]
            #     words_idx = np.random.zipf(2, 3)
            #     filtered_idx = words_idx[words_idx < terms_len]
            #     words = [terms[i][0] for i in filtered_idx]
            #     str += '"%s"' % " ".join(words)

            elif query_type == "slop":
                str += '"%s"~10' %plain_term

            else:
                str += query_type(term, terms)

            out_file.write('%s\n' % str)

        out_file.close()

    def get_popular_terms(self, field_name, num_terms):
        url = "%s/admin/luke?fl=%s&numTerms=%i" % (self.collection_url, field_name, num_terms)
        tree = ET.parse(urllib.urlopen(url)).getroot()

        terms = []
        for el in tree.findall('.//lst[@name="topTerms"]/*'):
            term = el.get("name")
            freq = el.text
            logging.debug("%s (%s)" % (term, freq))
            terms.append((term, freq))
        return terms
