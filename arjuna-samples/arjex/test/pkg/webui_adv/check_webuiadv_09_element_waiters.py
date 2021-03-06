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
def check_wait_until_absent_nested(request, logged_in_wordpress):
    # Should be validated in root element.
    logged_in_wordpress.element(id="adminmenu").wait_until_absent(id="something")

    try:
        # It is present
        logged_in_wordpress.element(id="adminmenu").wait_until_absent(tags="div")
    except GuiWidgetPresentError as e:
        print("Exception as Expected")
        print(str(e))
    except Exception as e:
        raise Exception("Unexpected exception raise: ", str(e))
    else:
        raise Exception("Exception not raised.")

@test
def check_absent_nested_locator_max_wait(request, logged_in_wordpress):
    try:
        b = time.time()
        logged_in_wordpress.element(id="adminmenu").wait_until_absent(tags="div")
    except GuiWidgetPresentError:
        print(time.time() - b)

    try:
        b = time.time()
        logged_in_wordpress.element(id="adminmenu").wait_until_absent(tags="div", max_wait=10)
    except GuiWidgetPresentError:
        print(time.time() - b)


@test
def check_contains_nested(request, logged_in_wordpress):
    # Should be validated in root element.
    print(logged_in_wordpress.element(id="adminmenu").contains(tags="div"))
    print(logged_in_wordpress.element(id="adminmenu").contains(id="something"))


@test
def check_contains_nested_locator_max_wait(request, logged_in_wordpress):
    b = time.time()
    logged_in_wordpress.element(id="adminmenu").contains(id="something")
    print(time.time() - b)

    b = time.time()
    logged_in_wordpress.element(id="adminmenu").contains(id="something", max_wait=10)
    print(time.time() - b)