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

import DocsGen as dg
from FieldGen import *

def gen_docs():
    collection_url = "http://localhost:8983/solr/<collection_name>"
    num_docs =  500
    start_id = 0
    num_threads = 8


    dg.runMP(collection_url, num_docs, start_id, num_threads, get_gen_doc())

def get_gen_doc():
    #define word dictionary
    text_gen = FieldGen('../bin/wordlist_wiki.txt')

    #define how solr documents are generated
    def gd(i):
        doc = dict(
            id=i,
            fieldA='constantString',            #field with constant value
            fieldB= text_gen.random(10),     #field with 10 words sampled randomly from dictionary
            fieldC=text_gen.zipf_fast(100),     #field with 10 words sampled from dictionary by zipf law
            fieldD=text_gen.random_code(16),    #field with 16 random characters (letters or numbers)
            fieldE=text_gen.random_code(11, "0123456789"),     #field with 10 random characters (specifies admissible characters)
            fieldF=text_gen.random(1, ["word1", "word2", "word3"]),  #field with 1 word chosen randomly from given sequence
            fieldG=text_gen.random_tuple(4, ["word1", "word2", "word3"])    #multivalue field with 4 word chosen randomly from given sequence
        )
        return doc

    return gd

if __name__ == "__main__":

    #generate documents and add them to a collection
    gen_docs()