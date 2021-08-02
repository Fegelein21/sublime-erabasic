import sublime
import sublime_plugin
import os
import re

def plugin_loaded():
    global settings
    settings = sublime.load_settings('CTagsAutoComplete.sublime-settings')

last_modify_time = 0
ctags_rows = []

class CTagsAutoComplete(sublime_plugin.EventListener):


    def on_query_completions(self, view, prefix, locations):
        if is_disabled_in(view.scope_name(locations[0])):
            return []

        ctags_paths = [folder + '\.tags_sorted_by_file' for folder in view.window().folders()]

        if not (ctags_paths and is_file_exist(view, ctags_paths[0])):
            return []

        global last_modify_time
        global ctags_rows

        current_modify_time = os.path.getmtime(ctags_paths[0])
        if last_modify_time != current_modify_time:
            last_modify_time = current_modify_time
            ctags_file = open(str(ctags_paths[0]), encoding = 'utf-8')
            ctags_rows = ctags_file.readlines()
            ctags_file.close()

        results = []
        for rows in ctags_rows:
            if len(rows) < 3 or rows[0] == '!':
                continue

            if re.findall('.*' + prefix + '.*', rows, re.I):
                matched = rows.replace('\n', '').split('\t')
                trigger = matched[0] + ('\t%s' % matched[3])

                if matched[3] == 'M' and settings.get("parameter_auto_complete", False):
                    contents = re.findall(matched[0] + r'(?:(?:\(.*\))|(?:,.*\b))?', str(matched[2]))
                    if contents:
                        results.append((trigger, contents[0]))
                        continue
                results.append((trigger, matched[0]))

        results = list(set(results))
        results.sort()

        return (results, sublime.INHIBIT_WORD_COMPLETIONS & sublime.INHIBIT_EXPLICIT_COMPLETIONS)

def is_disabled_in(scope):
    excluded_scopes = settings.get("exclude_scopes", [])
    for excluded_scope in excluded_scopes:
        if scope.find(excluded_scope) != -1:
            return True
    return False

def is_file_exist(view, file):
    if (not view.window().folders() or not os.path.exists(file)):
        return False
    return True

plugin_loaded()
