import sublime
import sublime_plugin
import os
import re

class GlobalVar():
    disabled = False
    ctags_file_path = ''
    modify_time = 0
    all_keyword = []
    settings = None
    settings_changed = False
    func_show_param = False
    func_show_param_count = False
    func_auto_add_param = False
    func_auto_add_bracket = False
    global_show_data_type = False
    global_show_declare = False
    global_show_defvalue = False
    global_show_dimension = False
    global_add_colon = False

Global = GlobalVar()

def plugin_loaded():
    Global.settings = sublime.load_settings('EraBasic.sublime-settings')
    ctags_settings = sublime.load_settings('CTags.sublime-settings')
    if Global.settings and ctags_settings:
        Global.settings.clear_on_change('EraBasicSettingsOnChange')
        Global.settings.add_on_change('EraBasicSettingsOnChange', settings_on_change)
        settings_on_change()
        disabled = False
    else:
        disabled = True

def settings_on_change():
    Global.settings_changed = True

    Global.func_show_param = Global.settings.get('erabasic_func_show_param', False)
    Global.func_show_param_count = Global.settings.get('erabasic_func_show_param_count', False)
    Global.func_auto_add_param = Global.settings.get('erabasic_func_auto_add_param', False)
    Global.func_auto_add_bracket = Global.settings.get('erabasic_func_auto_add_bracket', False)

    Global.global_show_data_type = Global.settings.get('erabasic_global_show_data_type', False)
    Global.global_show_declare = Global.settings.get('erabasic_global_show_declare', False)
    Global.global_show_defvalue = Global.settings.get('erabasic_global_show_defvalue', False)
    Global.global_show_dimension = Global.settings.get('erabasic_global_show_dimension', False)
    Global.global_add_colon = Global.settings.get('erabasic_global_add_colon', False)


class EraBasic(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):

        if Global.disabled:
            return []

        if 'source.erabasic' not in view.scope_name(locations[0]):
            return []

        if not view.window().folders():
            return []

        if not os.path.exists(Global.ctags_file_path):
            for folder in view.window().folders():
                ctags_paths = folder + r'\.tags_sorted_by_file'
                if os.path.exists(ctags_paths):
                    Global.ctags_file_path = ctags_paths
                    break
            if not os.path.exists(Global.ctags_file_path):
                return []

        need_regen_all_keyword = False

        modify_time = os.path.getmtime(Global.ctags_file_path)
        if Global.modify_time != modify_time:
            Global.modify_time = modify_time
            need_regen_all_keyword = True

        if Global.settings_changed:
            Global.settings_changed = False
            need_regen_all_keyword = True

        if need_regen_all_keyword:
            regen_all_keyword(view)

        results = []
        for key,value in Global.all_keyword:
            if re.search('.*' + prefix + '.*', key, re.I):
                results.append((key, value))
        results = list(set(results))
        results.sort()

        return results

def regen_all_keyword(view):

    ctags_file = open(Global.ctags_file_path, encoding = 'utf-8')
    ctags_rows = ctags_file.readlines()
    ctags_file.close()

    Global.all_keyword.clear()

    for rows in ctags_rows:
        if len(rows) < 3 or rows[0] == '!':
            continue

        matched = rows.replace('\n', '').split('\t')
        contents = None
        if matched[3] == 'f':
            contents = func_process(matched)
        elif matched[3] == 'g':
            contents = global_process(matched)
        else:
            trigger = '%s\t%s' % (matched[0], matched[3])
            contents = (trigger, matched[0])

        if contents:
            Global.all_keyword.append(contents)

def func_process(matched):

    trigger = matched[0]
    trigger_R = matched[3]
    strings = matched[0]
    contents = func_search_param(matched)

    exec_func_add_param = Global.func_show_param or Global.func_auto_add_param

    if exec_func_add_param:
        if Global.func_show_param and not Global.func_show_param_count:
            trigger = func_add_param(matched, contents, False)
        if Global.func_auto_add_param:
            strings = func_add_param(matched, contents, True)

    if Global.func_auto_add_bracket:
        if not Global.func_auto_add_param and contents[0] != 0:
            strings += '(${1})${0}'

    if Global.func_show_param_count and not Global.func_show_param:
        trigger_R = '%s-A' % len(contents[1])

    trigger = '%s\t%s' % (trigger, trigger_R)

    return (trigger, strings)

def func_search_param(matched):

    param_type = 0

    contents = re.search(r'\@.*?\((.*)\)\s*\;*\$', matched[2].replace(' ', ''))
    if contents and len(contents.group(1)):
        param_type = 1

    if param_type == 0:
        contents = re.search(r'\@.*?\,(.*)\s*\;*\$', matched[2].replace(' ', ''))
        if contents:
            param_type = 2

    if param_type == 0:
        return (param_type, ())

    return (param_type, contents.group(1).split(','))

def func_add_param(matched, contents, format_arg):

    if contents[0] == 0:
        return matched[0]

    strings = ''
    for index,string in enumerate(contents[1]):
        if len(strings) > 0:
            strings += ', '
        if format_arg:
            if contents[0] == 1:
                strings += '${%s:%s}' % (str(index + 1), string)
            else:
                strings += '${%s:%s}' % (str(index + 1 if index < len(contents[1]) - 1 else 0), string)
        else:
            strings += string

    if contents[0] == 1:
        strings = '%s(%s)' % (matched[0], strings)
        if format_arg:
            strings += '${0}'
    else:
        strings = '%s, %s' % (matched[0], strings)

    return strings

def global_process(matched):

    contents = re.search(r'.*?\s+((?:(?:CONST|CHARADATA|SAVEDATA)\s+)*)(%s\s*.*)\s*\;*.*\$' % matched[0], matched[2], re.I)
    if not contents:
        return None

    trigger = ''
    trigger_R = ''
    strings = matched[0]

    declares = None
    if Global.global_show_declare or Global.global_add_colon:
        declares = global_declare_check(contents.group(1))

    type_contents = None
    if Global.global_show_defvalue or Global.global_show_dimension or Global.global_add_colon:
        type_contents = global_type_check(matched[0], contents.group(2))

    for i in range(0, 4):
        string = ''
        if i == 0 and Global.global_show_data_type:
            string = global_datatype_check(matched[2])

        elif i == 1 and Global.global_show_declare:
            if declares and declares.find('CONST') == -1:
                string = declares

        elif i == 2 and Global.global_show_defvalue:
            if type_contents and type_contents[0] == 1 and len(type_contents[1]):
                string = "= %s" % type_contents[1]

        elif i == 3 and Global.global_show_dimension:
            if type_contents and type_contents[0] == 2:
                string = "%s-D" % max(len(type_contents[1].split(',')), 1)

        if len(string):
            if len(trigger_R):
                trigger_R += ','
            trigger_R += string

    if not len(trigger_R):
        trigger_R = matched[3]

    trigger = '%s\t%s' % (matched[0], trigger_R)

    if Global.global_add_colon:
        if type_contents and declares:
            colons = 0
            if type_contents[0] == 2:
                colons += max(len(type_contents[1].split(',')), 1)
            if declares.find('_C') != -1:
                colons += 1
            for i in range(0, colons):
                strings += ':${%s}' % str(i + 1 if i < colons - 1 else 0)

    return (trigger, strings)

def global_datatype_check(strings):

    contents = re.search(r'\^\#(DIM(?:S)?)', strings, re.I)
    if contents and len(contents.group(1)):
        return 'I' if contents.group(1).upper() == 'DIM' else 'S'
    return ''

def global_declare_check(strings):

    if len(strings):
        declares = ''
        for i in range(0, 3):
            string = ''
            if i == 0 and strings.upper().find('CONST') != -1:
                string = 'CONST'
            elif i == 1 and strings.upper().find('CHARADATA') != -1:
                string = '_C'
            elif i == 2 and strings.upper().find('SAVEDATA') != -1:
                string = '_S'
            if len(string):
                declares += string
        return declares
    return ''

def global_type_check(matched, strings):

    contents = re.search(r'%s\s*\=\s*(.*)\s*\;*.*' % matched, strings)
    if contents:
        return (1, contents.group(1))

    contents = re.search(r'%s\s*\,(.*)\s*\;*.*' % matched, strings)
    if contents:
        return (2, contents.group(1))

    return (0, None)
