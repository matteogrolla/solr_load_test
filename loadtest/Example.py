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

from FieldGen import *
import DocsGen as dGen
import QueriesGen as qGen
import Utils
import random

def get_gen_doc():
    #define word dictionary
    text_gen = FieldGen('../bin/wordlist_wiki.txt')

    #define how solr documents are generated
    def gd(i):
        doc = dict(
            id=i,
            content_type='film',            #field with constant value
            title= text_gen.zipf_fast(10),     #field with 10 words sampled randomly from dictionary
            description=text_gen.zipf_fast(100),     #field with 10 words sampled from dictionary by zipf law
            sku=text_gen.random_code(16),    #field with 16 random characters (letters or numbers)
            category=text_gen.random(1, ["cat1", "cat2", "cat3"]),  #field with 1 word chosen randomly from given sequence
            features=text_gen.random_tuple(4, ["feat1", "feat2", "feat3"])    #multivalue field with 4 word chosen randomly from given sequence
        )
        return doc

    return gd

if __name__ == "__main__":

    solr_url = "http://localhost:8983/solr"
    out_dir = "../output/example/"
    collection_url = solr_url+"/collection1"

    #Generate docs
    num_docs =  500
    start_id = 0
    num_threads = 8
    #Note: execution proceeds right after spawning processes
    dGen.runMP(collection_url, num_docs, start_id, num_threads, get_gen_doc())

    #Generate term queries denominazione
    qg = qGen.QueriesGen(collection_url)
    #qg.gen_queries("description", 20000, "term", out_dir+"queries_term_description.txt")

    #Generate term queries denominazione
    qg = qGen.QueriesGen(collection_url)
    #qg.gen_queries("description", 20000, "wildcard", out_dir+"queries_wildcard_description.txt")
