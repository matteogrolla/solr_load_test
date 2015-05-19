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
        p = re.compile('^[A-Za-z0-9]+$')
        out_file = codecs.open(output_path, 'w', encoding='utf-8')
        for idx,term in enumerate(terms):

            str = None
            plain_term = term[0]
            if query_type == "wildcard":
                #wildcard queries
                if len(plain_term) >= 5 and not(p.match(plain_term) is None):
                    logging.debug(plain_term)
                    term_wild = plain_term[:2]+'*'+plain_term[2:]
                    str = term_wild

            elif query_type == "codes":
                #term queries
                str = plain_term

            elif query_type == "term":
                #term queries
                str = '"%s"' %plain_term

            elif query_type == "phrase":
                str = '"%s"' %plain_term

            elif query_type == "slop":
                str = '"%s"~10' %plain_term

            else:
                str = query_type(term, terms)

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
