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

import solr
import logging
import time

logging.basicConfig(level=logging.DEBUG)

class DocsGen:
    def __init__(self, collection_url, threadId=0, fun=None):
        self.s = solr.Solr(collection_url)
        self.avgNumChar = 0
        self.batch_size = 100
        self.threadId = threadId
        self._gen_doc = fun

    def add_docs(self,n=3, start=0):
        start_time = time.time()
        self.avgNumChar = 0
        batch = []
        for i in xrange(start,start+n):
            doc = self.gen_doc(i)
            batch.append(doc)
            if i % self.batch_size == 0:
                self.s.add_many(batch)
                batch = []
            if i % 10000 == 0:
                logging.debug(("threadId: %i time: %s seconds, added docs: %i" % (self.threadId, time.time() - start_time, i-start)))
        self.s.add_many(batch)
        self.s.commit()
        self.avgNumChar /= n
        logging.info("startId: %i" % start)
        logging.info("average num char: %s" % self.avgNumChar)
        logging.info("time: %s seconds, added docs: %i" % (time.time() - start_time, n))

    def gen_doc(self, i):
        assert not(self.text_gen is None)

        #TODO: compute avg numchars for every field
        doc = self._gen_doc(i)

        return doc

    def wipe_collection(self):
        self.s.delete_query("*:*")
        self.s.commit()

from FieldGen import *


def run(threadID, collection_url, startDocID, numDocs, fun):
    text_gen = FieldGen('../bin/wordlist_wiki.txt')

    dg = DocsGen(collection_url, threadID, fun)
    dg.text_gen = text_gen

    dg.add_docs(numDocs, startDocID)


def runMP(collection_url, num_docs, start_id, num_threads, gen_doc):
    import multiprocessing


    dg = DocsGen(collection_url)
    dg.wipe_collection()

    docs_per_thread = num_docs / num_threads
    dgmts = []
    for i in xrange(0,num_threads):
        p = multiprocessing.Process(target = run, args=(i, collection_url, start_id+docs_per_thread*i, docs_per_thread,
                                                        gen_doc))
        p.start()

def _profile():
    collection_url = "http://localhost:8983/solr/race_posizione"
    num_docs =  1000
    start_id = 0

    text_gen = FieldGen('../bin/wordlist_wiki.txt')

    dg = DocsGen(collection_url, 0)
    dg.text_gen = text_gen

    dg.wipe_collection()
    dg.add_docs(num_docs, start_id)

def get_gen_doc():
    text_gen = FieldGen('../bin/wordlist_wiki.txt')

    def gd(i):
        denominazione = text_gen.random(10)
        text = text_gen.zipf_fast(400)
        doc = dict(
            id=i,
            type='posizione',
            denominazione= denominazione,
            oggetto_sociale=text,
            c_fiscale=text_gen.random_code(16),
            partita_iva=text_gen.random_code(11, "0123456789"),
            n_rea=text_gen.random_code(6, "0123456789"),
            provincia=text_gen.random(1, ["AG", "AL", "AN", "AO", "AQ", "AR", "AP", "AT", "AV", "BA", "BT", "BL",
                                          "BN", "BG", "BI", "BO", "BZ", "BS", "BR", "CA", "CL", "CB", "CI", "CE", "CT", "CZ", "CH", "CO", "CS",
                                          "CR", "KR", "CN", "EN", "FM", "AG", "AL", "AN", "AO", "AQ", "AR", "AP", "AT", "AV", "BA", "BT", "BL",
                                          "BN", "BG", "BI", "BO", "BZ", "BS", "BR", "CA", "CL", "CB", "CI", "CE", "CT", "CZ", "CH", "CO", "CS",
                                          "CR", "KR", "CN", "EN", "FM", "FE", "FI", "FG", "FC", "FR", "GE", "GO", "GR", "IM", "IS", "SP", "LT",
                                          "LE", "LC", "LI", "LO", "LU", "MC", "MN", "MS", "MT", "VS", "ME", "MI", "MO", "MB", "NA", "NO", "NU",
                                          "OG", "OT", "OR", "PD", "PA", "PR", "PV", "PG", "PU", "PE", "PC", "PI", "PT", "PN", "PZ", "PO", "RG",
                                          "RA", "RC", "RE", "RI", "RN", "Roma", "RO", "SA", "SS", "SV", "SI", "SR", "SO", "TA", "TE", "TR", "TO",
                                          "TP", "TN", "TV", "TS", "UD", "VA", "VE", "VB", "VC", "VR", "VV", "VI", "VT"]),
            c_ateco_secondaria=text_gen.random_tuple(4, text_gen.ateco_codes)
        )
        return doc

    return gd

if __name__ == "__main__":

    collection_url = "http://localhost:8983/solr/race_posizione"
    num_docs =  500
    start_id = 0
    num_threads = 8

    '''
    text_gen = FieldGen('../bin/wordlist_wiki.txt')

    dg = DocsGen(collection_url, 0)
    dg.text_gen = text_gen

    dg.wipe_collection()
    dg.add_docs(num_docs, start_id)
    '''

    '''
    import multiprocessing


    dg = DocsGen(collection_url)
    dg.wipe_collection()


    docs_per_thread = num_docs / num_threads
    dgmts = []
    for i in xrange(0,num_threads):
        p = multiprocessing.Process(target = run, args=(i, collection_url, start_id+docs_per_thread*i, docs_per_thread, gd) )
        p.start()
    '''

    runMP(collection_url, num_docs, start_id, num_threads, get_gen_doc())

