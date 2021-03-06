# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from arjuna import *

@test
def check_coded_diff_locator_or(request, wordpress):
    e = wordpress.element(classes="nonexisting", attr=attr(type="submit"))
    print(e.source.content.root)

@test
def check_same_locator_or_coded(request, wordpress):
    e = wordpress.element(name=oneof("nonexisting", "log"))
    print(e.source.content.root)
