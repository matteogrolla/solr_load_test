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
import solr
from QueriesGen import *

logging.basicConfig(level=logging.INFO)


class QueriesGenFromStoredFields(QueriesGen):
    def __init__(self, collection_url):
        super(QueriesGenFromStoredFields, self).__init__(collection_url)

    def gen_phrase_queries(self, num_queries, id_field_name, field_name, phrase_length, output_path="queries.txt"):
        fun = self.get_gen_phrase_query(field_name, phrase_length)

        self.gen_queries(num_queries, id_field_name, fun, output_path)


    def get_gen_phrase_query(self, field_name, phrase_length):

        def gen_query_denominazione(doc, i_str):
            value = doc[field_name]
            tokens = value.split()
            phrase = " ".join(tokens[0:phrase_length])

            query = 'q=%s:"%s"'%(field_name,phrase)
            return query

        return gen_query_denominazione


    def gen_queries(self, num_queries, id_field_name, fun, output_path="queries.txt"):
        num_docs = self.s.query("*:*").numFound

        out_file = codecs.open(output_path, 'w', encoding='utf-8')
        incr = num_docs / num_queries

        for i in xrange(0, num_queries):

            i_str = str(i*incr).rjust(9, '0')
            response = self.s.query("%s:%s"%(id_field_name, i_str))
            doc = response.results[0]

            query = fun(doc, i_str)
            logging.debug("docid: %s, phrase: %s" % (i_str, query))

            out_file.write('%s\n' % query)

        out_file.close()
