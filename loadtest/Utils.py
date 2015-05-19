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

import codecs

class Utils:
    def __init__(self):
        pass

    def load_wordlist(self, path):
        file = codecs.open(path, 'rU', 'utf-8')
        raw = file.read()
        tokens = raw.split()
        #self.ateco_codes = [tokens[i] for i in range(0,len(tokens))]
        file.close()
        return tokens
