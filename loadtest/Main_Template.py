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
import QueriesGenFromPopularTerms as qGenPT
import Utils
import random

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

def get_gen_query_A():
    utils = Utils.Utils()
    #variables accessible from gen_query_A()
    wl_province = utils.load_wordlist("../bin/province.txt")

    #term: an element of terms chosen randomly
    #terms: ordered (from most popular) list of terms from chosen field
    #output: a string containing the query (ex: "q=fieldA:<term>")
            #can return complex queries using pseudo join or other features
    def gen_query_A(term, terms):

        return "query"

    return gen_query_A

if __name__ == "__main__":

    solr_url = "http://localhost:8983/solr"
    out_dir = "../output/dev/"
    #Generate docs Posizione

    collection_url = solr_url+"/race_posizione"
    num_docs =  500
    start_id = 0
    num_threads = 8

    #Note: execution proceeds right after spawning processes
    #dGen.runMP(collection_url, num_docs, start_id, num_threads, get_gen_doc())

    #Generate term queries denominazione
    qg = qGenPT.QueriesGenFromPopularTerms(solr_url+"/<collection_name>")
    qg.gen_queries_for_field("<source_field>", 20000, "term", out_dir+"queries_term_1.txt")

    #Generate term queries denominazione
    qg = qGenPT.QueriesGenFromPopularTerms(solr_url+"/<collection_name>")
    qg.gen_queries_for_field("<source_field>", 20000, "wildcard", out_dir+"queries_wildcard_1.txt")

    #Generate queries Posizione ateco
    qg = qGenPT.QueriesGenFromPopularTerms(solr_url+"/<collection_name>")
    qg.gen_queries_for_field("fieldA", 20000, get_gen_query_A(), out_dir+"queries_A.txt")