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
import re
from QueriesGen import *


logging.basicConfig(level=logging.INFO)


class QueriesGenFromPopularTerms(QueriesGen):
    def __init__(self, collection_url):
        super(QueriesGenFromPopularTerms, self).__init__(collection_url)

    def gen_queries(self, field_name, num_queries, num_popular_terms, fun, output_path="queries.txt"):
        terms = self.get_popular_terms(field_name, num_popular_terms)
        out_file = codecs.open(output_path, 'w', encoding='utf-8')
        for i in xrange(num_queries):
            str = fun(terms)
            out_file.write('%s\n' % str)

        out_file.close()

    # Generates num_terms queries from popular terms on field field_name of the collection
    # query_type can be:
    # -wildcard
    # -codes
    # -term
    # -slop
    # -a function fun(term, terms)
    #     term: one of the popular terms
    #     terms: the list of popular get_popular_terms
    #     returns: a string containing the generated query
    def gen_queries_for_field(self, field_name, num_popular_terms, query_type="term", output_path="queries.txt"):

        terms = self.get_popular_terms(field_name, num_popular_terms)
        terms_len = len(terms)
        p = re.compile('^[A-Za-z0-9]+$')
        out_file = codecs.open(output_path, 'w', encoding='utf-8')
        for idx,term in enumerate(terms):

            str = "q=%s:" % field_name
            if query_type == "wildcard":
                #wildcard queries
                if len(term) >= 5 and not(p.match(term) is None):
                    logging.debug(term)
                    term_wild = term[:2]+'*'+term[4:]
                    str += term_wild
                else:
                    continue

            elif query_type == "codes":
                #term queries
                str += term

            elif query_type == "term":
                #term queries
                str += '"%s"' %term

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

            #TODO: generate mandatory terms query

            elif query_type == "slop":
                str += '"%s"~10' %term

            else:
                str = query_type(term, terms)

            out_file.write('%s\n' % str)

        out_file.close()

    def get_popular_terms(self, field_name, num_terms, retrieve_frequencies=False):
        logging.info("get_popular_terms(%s, %i, %s)" % (field_name, num_terms, retrieve_frequencies))
        url = "%s/admin/luke?fl=%s&numTerms=%i" % (self.collection_url, field_name, num_terms)
        tree = ET.parse(urllib.urlopen(url)).getroot()

        terms = []
        for el in self._get_top_terms(tree): #tree.findall('.//lst[@name="topTerms"]/*'):
            term = el.get("name")
            freq = el.text
            logging.debug("%s (%s)" % (term, freq))
            if (retrieve_frequencies):
                terms.append((term, freq))
            else:
                terms.append(term)
        return terms

    #in python 2.6 xpath queries are not available
    def _get_top_terms(self, tree):
        tags = tree.findall("lst")
        for tag in tags:
            if tag.get('name') == 'fields':
                break
        fields = tag
        denominazione = fields.find("lst")
        topTermsParent = denominazione.find("lst")
        topTerms = topTermsParent.findall("int")
        return topTerms

