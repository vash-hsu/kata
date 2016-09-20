#!/usr/bin/env python

import json
import codecs


def string_ex(input_string):
    if isinstance(input_string, str):
        return input_string
    elif isinstance(input_string, unicode):
        try:
            return input_string.decode("utf-8").encode("ascii")
        except BaseException as err:
            return repr(input_string)
    else:
        return repr(input_string)


def recurse_print_json(json_dict, indent=0):
    if not isinstance(json_dict, dict):
        return recurse_print_json(json.loads(json_dict), indent+1)
    for key in json_dict.keys():
        print("\t"*indent + string_ex(key))
        content = json_dict[key]
        if isinstance(content, dict):
            recurse_print_json(content, indent+1)
        elif isinstance(content, list):
            for child_node in content:
                if isinstance(child_node, dict):
                    recurse_print_json(child_node, indent+1)
                else:
                    print '\t' * (indent + 1) + string_ex(child_node)
        else:
            print '\t'*(indent+1) + string_ex(json_dict[key])


def recurse_find_json_by_keyword(json_dict, keyword):
    '''
    :param json_dict: dict or string
    :param keyword: string
    :return: list candidates
    '''
    candidates = list()
    if isinstance(json_dict, str):
        candidates.extend(recurse_find_json_by_keyword(json.loads(json_dict),
                                                       keyword))
    elif isinstance(json_dict, dict):
        for key in json_dict.keys():
            content = json_dict[key]
            if key == keyword:
                # candidates.append(str(content))
                candidates.append(content)
            else:
                if isinstance(content, dict):
                    candidates.extend(recurse_find_json_by_keyword(content,
                                                                   keyword))
                elif isinstance(content, list):
                    for child_node in content:
                        if isinstance(child_node, dict):
                            candidates.extend(
                                recurse_find_json_by_keyword(child_node,
                                                             keyword))
    return candidates
