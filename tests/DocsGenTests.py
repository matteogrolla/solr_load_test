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

from loadtest.DocsGen import *
from loadtest.TextGen import *

def test_add_doc():
    text_gen = FieldGen('../bin/wordlist1.txt')

    dg = DocsGen("http://localhost:8983/solr/collection1")
    dg.text_gen = text_gen

    dg.wipe_collection()
    dg.add_docs(100)

if __name__ == "__main__":
    test_add_doc()
