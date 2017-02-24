import sublime, sublime_plugin, re

class IfParentNodeExistCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sels = self.view.sel()
        newRegions = []
        for sel in sels:
            if sel.empty():
                begin = sel.begin() - 1
                end = sel.end()
                notJsonPath = re.compile("[^\w\.'\"\[\]]+")
                while not notJsonPath.match(self.view.substr(sublime.Region(begin, begin + 1))):
                    begin = begin -1
                while not notJsonPath.match(self.view.substr(sublime.Region(end - 1, end))):
                    end = end + 1
                sel = sublime.Region(begin + 1, end);

            path = self.view.substr(sel)
            lastDot = path.rfind('.')
            lastOpenSquareBracket = path.rfind('[')
            last = max(lastDot, lastOpenSquareBracket)
            if last != -1:
                self.view.insert(edit, sel.begin(), path[:last] + ' && ')
                newRegions.append(sublime.Region(sel.begin(), sel.begin() + last))

        self.view.sel().clear()
        for region in newRegions:
            self.view.sel().add(region)
