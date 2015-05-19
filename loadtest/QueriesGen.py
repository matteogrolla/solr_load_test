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
        self.wl_province = self._load_wordlist("../bin/province.txt")

    def _load_wordlist(self, path):
        file = codecs.open(path, 'rU', 'utf-8')
        raw = file.read()
        tokens = raw.split()
        #self.ateco_codes = [tokens[i] for i in range(0,len(tokens))]
        file.close()
        return tokens

    def gen_queries(self, field_name, num_terms, query_type="term"):

        terms = self.get_popular_terms(field_name, num_terms)
        #out_files = ["queries_hf.txt", "queries_mf.txt", "queries_lf.txt"]
        #out_file_idx = -1
        p = re.compile('^[A-Za-z0-9]+$')
        out_file = codecs.open("queries.txt", 'w', encoding='utf-8')
        for idx,term in enumerate(terms):
            '''
            if idx < len(terms)/3:
                if out_file_idx != 0:
                    out_file_idx = 0
                    out_file = codecs.open(out_files[out_file_idx], 'w', encoding='utf-8')
            elif idx < 2*len(terms)/3:
                if out_file_idx != 1:
                    out_file.close()
                    out_file_idx = 1
                    out_file = codecs.open(out_files[out_file_idx], 'w', encoding='utf-8')
            else:
                if out_file_idx != 2:
                    out_file_idx = 2
                    out_file = codecs.open(out_files[out_file_idx], 'w', encoding='utf-8')
            '''
            plain_term = term[0]
            if query_type == "wildcard":
                #wildcard queries
                if len(plain_term) >= 5 and not(p.match(plain_term) is None):
                    logging.debug(plain_term)
                    term_wild = plain_term[:2]+'*'+plain_term[2:]
                    out_file.write('%s\n' % term_wild)

            elif query_type == "codes":
                #term queries
                out_file.write('%s\n' % plain_term)

            elif query_type == "term":
                #term queries
                out_file.write('"%s"\n' % plain_term)

            elif query_type == "phrase":
                out_file.write('"%s"\n' % plain_term)

            elif query_type == "slop":
                out_file.write('"%s"~10\n' % plain_term)

            elif query_type =="ateco":
                prov_words = [self.wl_province[i] for i in random.sample(xrange(len(self.wl_province)), 3)]
                prov_words = " ".join(prov_words)
                descr_words = [terms[i][0] for i in random.sample(xrange(len(terms)), 3)]
                descr_str = "+"+" +".join(descr_words)
                out_file.write("q=+type:posizione +provincia:("+prov_words+")"
                    "&fq={!join fromIndex=ateco from=ateco_cod_attivita to=c_ateco_secondaria}"
                    "(+ateco_descrizione:("+descr_str+") +ateco_tipo_codifica:(+07))\n")
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


if __name__ == "__main__":
    #"http://192.168.1.3:8983/solr/race_posizione_aux"
    qg = QueriesGen("http://192.168.1.3:8983/solr/ateco")
    qg.gen_queries("ateco_descrizione", 20000, "ateco")