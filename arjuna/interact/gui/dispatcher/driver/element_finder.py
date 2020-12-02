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

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from arjuna.tpi.error import *
from arjuna.core.error import *
from selenium.webdriver.support.relative_locator import RelativeBy

class ElementFinder:
    BY_MAP = {
        "ID": By.ID,
        "NAME": By.NAME,
        "TAG_NAME": By.TAG_NAME,
        "CLASS_NAME": By.CLASS_NAME,
        "LINK_TEXT": By.LINK_TEXT,
        "PARTIAL_LINK_TEXT": By.PARTIAL_LINK_TEXT,
        "CSS_SELECTOR": By.CSS_SELECTOR,
        "XPATH": By.XPATH
    }

    RELATION_MAP = {
        "above": "above",
        "below": "below",
        "right": "to_left_of",
        "left": "to_right_of",
        "near": "near",
    }
    
    @classmethod
    def __create_relative_by(cls, byType, byValue, relations):
        from arjuna import log_debug
        relative_by = RelativeBy({byType: byValue})
        for k,v in relations.items():
            try:
                getattr(relative_by, cls.RELATION_MAP[k.lower()])(v)
            except:
                pass
        log_debug("Root" + str(relative_by.root))
        log_debug("Filters" + str(relative_by.filters))
        return relative_by
        
    @classmethod
    def find_element(cls, container, byType, byValue, *, relations=None):
        from arjuna import log_debug
        log_debug(f"Finding element in container:{container} with wtype:{byType} and wvalue:{byValue} with relations: {relations}")
        try:
            byType = cls.BY_MAP[byType.upper()]
            if not relations:
                return container.find_element(byType, byValue)
            else:
                # Currently Selenium supports Relative locator only for find_elements
                elements = container.find_elements(cls.__create_relative_by(byType, byValue, relations))
                if len(elements) == 0:
                    raise Exception("No elements found.")
                else:
                    return elements[0]
        except Exception as e:
            print(e.__class__, e)
            raise GuiWidgetNotFoundError("By.{}={}".format(byType, byValue))


    @classmethod
    def find_elements(cls, container, byType, byValue, relations=None):
        byType = cls.BY_MAP[byType.upper()]
        if not relations:
            elements = container.find_elements(byType, byValue)
        else:
            elements = container.find_elements(cls.__create_relative_by(byType, byValue, relations))            
        if len(elements) == 0:
            raise GuiWidgetNotFoundError("By.{}={}".format(byType, byValue))
        return elements
