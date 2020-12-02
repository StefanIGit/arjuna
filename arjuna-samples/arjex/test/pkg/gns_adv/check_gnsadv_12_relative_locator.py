# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

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


from arjex.lib.gns_adv.app_page_section.app import WordPress

@for_test
def wordpress(request):
    # Setup
    wordpress = WordPress(section_dir="withx")
    home = wordpress.launch()
    yield home

    # Teadown
    wordpress.quit()

@test
def check_relative_locators_gns_basic_find(request, wordpress):
    e = wordpress.element(tags="input", right=wordpress.gns.user_label)
    print(e.source.content.all)
    e = wordpress.gns.rel_input_1
    print(e.source.content.all)

@test
def check_relative_locators_gns_find_all(request, wordpress):
    user_label = wordpress.multi_element(tags="*", below=wordpress.gns.user_label)
    print(user_label.source.content.all) 
    elems = wordpress.gns.rel_all_1
    for e in elems:
        print(e.source.content.root)  

@test
def check_relative_locators_coded_or(request, wordpress):
    pass_label = wordpress.element(attr=attr(__for="user_pass"))
    e = wordpress.element(name="wrong", id="wrong", tags="input", above=pass_label)
    print(e.source.content.all) 

@test
def check_relative_locators_coded_table_find(request, logged_in_wordpress):
    wordpress = logged_in_wordpress
    wordpress.element(link="Pages").click()

    test1 = wordpress.element(link="Test1")
    date_col = wordpress.element(id="date")
    test1_date = wordpress.element(classes="column-date", left=test1, below=date_col)
    print(test1_date.source.content.all)

    test1 = wordpress.element(link="Test1", right=test1_date)
    print(test1.source.content.all)

    elems = wordpress.multi_element(classes="column-date", right=wordpress.element(link="Sample Page"), below=date_col).elements
    for e in elems:
        print(e.source.content.all)  


@test
def check_relative_locators_coded_nested(request, wordpress):
    raise Exception("Not supported by Selenium and hence in Arjuna yet.")
    # # Locate the form and then all input elements

    # # Level 1 - Element from App
    # form = wordpress.element(id="loginform")

    # e = form.element(classes="button", left=wordpress.element(id="rememberme"))
    # print(e.source.content.all)

    # # Level 2 - MultiElement in Element
    # labels = form.multi_element(tags="label", below=form.element(attr=attr(__for="user_login")))

    # for label in labels:
    #     print(label.text)
    #     print(label.source.content.all)

    #     # Level 3 - Element in Partial Element
    #     i = label.element(tags="input")
    #     print(i.source.content.all)




