import keyword

import wx
import wx.stc as stc
from wx.lib.embeddedimage import PyEmbeddedImage

if wx.Platform == '__WXMSW__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Courier New',
              'helv' : 'Arial',
              'other': 'Comic Sans MS',
              'size' : 10,
              'size2': 8,
             }
elif wx.Platform == '__WXMAC__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Monaco',
              'helv' : 'Arial',
              'other': 'Comic Sans MS',
              'size' : 12,
              'size2': 10,
             }
else:
    faces = { 'times': 'Times',
              'mono' : 'Courier',
              'helv' : 'Helvetica',
              'other': 'new century schoolbook',
              'size' : 12,
              'size2': 10,
             }

image_smile = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAolJ"
    "REFUOI1tk91Lk2EYxn/vx7OmwyBhVsytmY1cCBFBQWSRlYVGJ51EjajptliH4X/QQeJ5J+ZJ"
    "f0AnIVSWJ0EQQfQhzNG3JkRQILrl3tft6sDNRvnAdfI8z8V939d13Vi2w79IpS4pHt8p17Vk"
    "jK1EIqpcLqPN/to0nWwmrc5IUL29n3jw4Ajl8mVKpYvcv7+frq5HdEZqymauqZljWbYDwOlT"
    "xxSL/eTOnfMY4wElYAWoAhXgI75fIJ/3mJ8/wvST5xaw3kE2k1YsBhMTtzEmCYTqxEaxVaCM"
    "MRYTE1uIxZ6RzVxdf7Rsh2i0XZ5XkPRF0mONjo4KkJSSlBKgcDgsqVVSizwPRTuRZTu42Uxa"
    "XV1rGNMCOECN8fHxpimX6OnpYW5uDmgF1TAEuXG9yuf5lOyZmYcMDUWAReAj8LqJXAEWWVhY"
    "aLqrQaWVoZNtzMxMYRljq1S6iTFtwCrDw9+ZnPQ2hIOFuqB1crUKSx34qw6hXfMNG7264stM"
    "TvrAEvAOKDaRBVpjd2cQ/BbwgwDY8XiEYvEb8AMokky+BF7UK+svGR+qNp+/L0O5jeKcRXxX"
    "GLe//wxTU/fo7Q0AolCAUEiUGoWpAWtQtTi4rw19iUB5K1OPf9F//GTDRkue11K3ad0qBYMK"
    "BAJyXUehoKv93e3S4l6p0Cfv1QlFdwS0EeXBwTT5/Op6mw389qn4Pr5jcTjZweunUVgOw1qA"
    "/K0ig2fOsREky3YYGOjTyAjyPCTVUbWllW3St6T04ZC8N0c1cmGHBo4f0H/LNP3kueU4w3R3"
    "w9gYzM6CX3HwKzaz71cYu/uV7rMvcLb2Mf3srbURi81WNJdLK5HYLuMi46LEng7lMlc2Xec/"
    "xiMt8QU2mDwAAAAASUVORK5CYII=")

html_keywords = (
        "a abbr acronym address applet area b base basefont bdo big blockquote"
        " body br button caption center cite code col colgroup dd del dfn dir"
        " div dl dt em fieldset font form frame frameset h1 h2 h3 h4 h5 h6"
        " head hr html i iframe img input ins isindex kbd label legend li link"
        " map menu meta noframes noscript object ol optgroup option p param"
        " pre q s samp script select small span strike strong style sub sup"
        " table tbody td textarea tfoot th thead title tr tt u ul var xml"
        " xmlns abbr accept-charset accept accesskey action align alink alt"
        " archive axis background bgcolor border cellpadding cellspacing char"
        " charoff charset checked cite class classid clear codebase codetype"
        " color cols colspan compact content coords data datafld dataformatas"
        " datapagesize datasrc datetime declare defer dir disabled enctype"
        " event face for frame frameborder headers height href hreflang hspace"
        " http-equiv id ismap label lang language leftmargin link longdesc"
        " marginwidth marginheight maxlength media method multiple name nohref"
        " noresize noshade nowrap object onblur onchange onclick ondblclick"
        " onfocus onkeydown onkeypress onkeyup onload onmousedown onmousemove"
        " onmouseover onmouseout onmouseup onreset onselect onsubmit onunload"
        " profile prompt readonly rel rev rows rowspan rules scheme scope"
        " selected shape size span src standby start style summary tabindex"
        " target text title topmargin type usemap valign value valuetype"
        " version vlink vspace width text password checkbox radio submit reset"
        " file hidden image public !doctype")

dtml_keywords = (
        "dtml-var dtml-if dtml-unless dtml-in dtml-with dtml-let dtml-call"
        "dtml-raise dtml-try dtml-comment dtml-tree")

js_keywords = ("abstract break boolean byte case const continue catch "
                  "class char debugger default delete do double default "
                  "export false else enum export extend final finally "
                  "float for function goto if implements import in "
                  "instanceof int interface long native new null "
                  "package private protected public return short static "
                  "synchronized switch super this throw throws transient "
                  "try true typeof var void volatile with while")


class SourceTextCtrl(stc.StyledTextCtrl):

    fold_symbols = 3

    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        stc.StyledTextCtrl.__init__(self, parent, ID, pos, size, style)
        self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(1, 50)

        self.EmptyUndoBuffer()

        self.set_source_lexer("")

        self.SetProperty("tab.timmy.whinge.level", "1")
        self.SetMargins(2, 2)

        self.SetViewWhiteSpace(False)

        # Setup a margin to hold fold markers
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)

        self.SetIndent(4)  # Proscribed indent size for wx
        self.SetIndentationGuides(True)  # Show indent guides
        self.SetBackSpaceUnIndents(True)  # Backspace unindents rather than delete 1 space
        self.SetTabIndents(True)  # Tab key indents
        self.SetTabWidth(4)  # Proscribed tab size for wx
        self.SetUseTabs(False)  # Use spaces rather than tabs, or

        if self.fold_symbols == 0:
            # Arrow pointing right for contracted folders, arrow pointing down for expanded
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_ARROWDOWN, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_ARROW, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_EMPTY, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_EMPTY, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_EMPTY,     "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY,     "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY,     "white", "black")

        elif self.fold_symbols == 1:
            # Plus for contracted folders, minus for expanded
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_MINUS, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_PLUS,  "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")

        elif self.fold_symbols == 2:
            # Like a flattened tree control using circular headers and curved joins
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_CIRCLEMINUS,          "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_CIRCLEPLUS,           "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,                "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNERCURVE,         "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_CIRCLEPLUSCONNECTED,  "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_CIRCLEMINUSCONNECTED, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNERCURVE,         "white", "#404040")

        elif self.fold_symbols == 3:
            # Like a flattened tree control using square headers
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_BOXMINUS,          "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_BOXPLUS,           "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,             "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNER,           "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_BOXPLUSCONNECTED,  "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER,           "white", "#808080")

        self.Bind(stc.EVT_STC_UPDATEUI, self.on_update_ui)
        self.Bind(stc.EVT_STC_MARGINCLICK, self.on_margin_click)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_pressed)

        self.find_data = wx.FindReplaceData()
        self.find_data.SetFlags(wx.FR_DOWN)

        find_at_id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.on_key_find, id=find_at_id)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL,  ord('F'), find_at_id )])
        self.SetAcceleratorTable(accel_tbl)

        self.encoding = None

        # register some images for use in the AutoComplete box.
        self.RegisterImage(1, image_smile.GetBitmap())
        self.RegisterImage(2,
                           wx.ArtProvider.GetBitmap(wx.ART_NEW, size=(16, 16)))
        self.RegisterImage(3,
                           wx.ArtProvider.GetBitmap(wx.ART_COPY, size=(16, 16)))

    def set_detail_style_spec(self, ext):
        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
        self.StyleClearAll()  # Reset all to be like the default

        # Global default styles for all languages

        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER,  "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")

        # styles
        # Default
        self.StyleSetSpec(stc.STC_P_DEFAULT, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # Comments
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#007F00,face:%(other)s,size:%(size)d" % faces)
        # Number
        self.StyleSetSpec(stc.STC_P_NUMBER, "fore:#007F7F,size:%(size)d" % faces)
        # String
        self.StyleSetSpec(stc.STC_P_STRING, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        # Single quoted string
        self.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        # Keyword
        self.StyleSetSpec(stc.STC_P_WORD, "fore:#00007F,bold,size:%(size)d" % faces)
        # Triple quotes
        self.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#7F0000,size:%(size)d" % faces)
        # Triple double quotes
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%(size)d" % faces)
        # Class name definition
        self.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%(size)d" % faces)
        # Function or method name definition
        self.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % faces)
        # Operators
        self.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces)
        # Identifiers
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # Comment-blocks
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%(size)d" % faces)
        # End of line where string is not closed
        self.StyleSetSpec(stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)

        self.SetCaretForeground("BLUE")

    def set_source_lexer(self, ext):
        if ext == ".html":
            self.SetLexer(stc.STC_LEX_HTML)
            keywords = html_keywords + ' ' + dtml_keywords
            self.SetKeyWords(0, keywords)
        elif ext == ".css":
            self.SetLexer(stc.STC_LEX_CSS)
            self.SetKeyWords(0, "")
        elif ext == ".xml":
            self.SetLexer(stc.STC_LEX_XML)
            self.SetKeyWords(0, "")
        elif ext == ".py":
            self.SetLexer(stc.STC_LEX_PYTHON)
            self.SetKeyWords(0, " ".join(keyword.kwlist))
        elif ext == ".js":
            self.SetLexer(stc.STC_LEX_CPP)
            self.SetKeyWords(0, js_keywords)
        else:
            self.SetLexer(stc.STC_LEX_TEX)
            self.SetKeyWords(0, "")

        self.SetProperty("fold", "1")

        self.set_detail_style_spec(ext)

    def fold_all(self):
        line_count = self.GetLineCount()
        expanding = True

        # find out if we are folding or unfolding
        for line_num in range(line_count):
            if self.GetFoldLevel(line_num) & stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(line_num)
                break

        line_num = 0

        while line_num < line_count:
            level = self.GetFoldLevel(line_num)
            if level & stc.STC_FOLDLEVELHEADERFLAG and \
               (level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:

                if expanding:
                    self.SetFoldExpanded(line_num, True)
                    line_num = self.expand(line_num, True)
                    line_num = line_num - 1
                else:
                    lastChild = self.GetLastChild(line_num, -1)
                    self.SetFoldExpanded(line_num, False)

                    if lastChild > line_num:
                        self.HideLines(line_num+1, lastChild)

            line_num += 1

    def expand(self, line, do_expand, vis_levels=0, level=-1):
        last_child = self.GetLastChild(line, level)
        line += 1

        while line <= last_child:
            if vis_levels > 0:
                self.ShowLines(line, line)
            else:
                self.HideLines(line, line)

            if level == -1:
                level = self.GetFoldLevel(line)

            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if vis_levels > 1:
                    self.SetFoldExpanded(line, True)
                else:
                    self.SetFoldExpanded(line, False)

                line = self.expand(line, do_expand, vis_levels - 1)
            else:
                line += 1

        return line

    def go_line(self, line):
        # print("line: %d" % line)
        self.GotoLine(line)

    def highlight_line(self, line_number):
        line_number -= 1
        # line = self.GetLine(lineno)
        end = self.GetLineEndPosition(line_number)
        indent = self.GetLineIndentPosition(line_number)
        # start = end - len(line) + indent
        start = indent
        # start = self.GetLineEndPosition(lineno-1)
        self.SetSelection(start, end)
        self.SetFocus()

    def find_string(self, find_string):
        text = self.GetValue()
        csel = self.GetSelection()
        if csel[0] != csel[1]:
            cpos = max(csel)
        else:
            cpos = self.GetInsertionPoint()
        if cpos == self.GetLastPosition():
            cpos = 0

        # Simple case insensitive search
        text = text.upper()
        find_string = find_string.upper()
        found = text.find(find_string, cpos)
        if found != -1:
            end = found + len(find_string)
            self.SetSelection(found, end)
            self.SetFocus()
            return True
        return False

    def on_key_find(self, event):
        # self.DisableButtons()
        self.find_dlg = wx.FindReplaceDialog(self, self.find_data, "Find")
        self.find_dlg.Bind(wx.EVT_FIND, self.on_find)
        self.find_dlg.Bind(wx.EVT_FIND_NEXT, self.on_find)
        # self.finddlg.Bind(wx.EVT_FIND_REPLACE, self.OnFind)
        # self.finddlg.Bind(wx.EVT_FIND_REPLACE_ALL, self.OnFind)
        self.find_dlg.Bind(wx.EVT_FIND_CLOSE, self.on_find_close)
        self.find_dlg.Show(True)

    def on_find(self, evt):
        """
        #print repr(evt.GetFindString()), repr(self.findData.GetFindString())
        map = {
            wx.wxEVT_COMMAND_FIND : "FIND",
            wx.wxEVT_COMMAND_FIND_NEXT : "FIND_NEXT",
            wx.wxEVT_COMMAND_FIND_REPLACE : "REPLACE",
            wx.wxEVT_COMMAND_FIND_REPLACE_ALL : "REPLACE_ALL",
            }

        et = evt.GetEventType()

        if et in map:
            evtType = map[et]
        else:
            evtType = "**Unknown Event Type**"


        if et in [wx.wxEVT_COMMAND_FIND_REPLACE, wx.wxEVT_COMMAND_FIND_REPLACE_ALL]:
            replaceTxt = "Replace text: %s" % evt.GetReplaceString()
        else:
            replaceTxt = ""

        self.log.write("%s -- Find text: %s  %s  Flags: %d  \n" %
                       (evtType, evt.GetFindString(), replaceTxt, evt.GetFlags()))

        """


        # self.SetSelection(1)
        end = self.GetLastPosition()

        # StyledTextControl is in UTF-8 encoding
        # textstring = self.GetRange(0, end).encode("utf-8")
        text_string = self.GetText().encode("utf-8")
        find_string = self.find_data.GetFindString().encode("utf-8")
        if not (self.find_data.GetFlags() & wx.FR_MATCHCASE):
            text_string = text_string.lower()
            find_string = find_string.lower()

        backward = not (self.find_data.GetFlags() & wx.FR_DOWN)
        if backward:
            start = self.GetSelection()[0]
            loc = text_string.rfind(find_string, 0, start)
        else:
            start = self.GetSelection()[1]
            loc = text_string.find(find_string, start)
        if loc == -1 and start != 0:
            # string not found, start at beginning
            if backward:
                start = end
                loc = text_string.rfind(find_string, 0, start)
            else:
                start = 0
                loc = text_string.find(find_string, start)

        if loc == -1:
            dlg = wx.MessageDialog(self, 'Find String Not Found',
                          'Find String Not Found',
                          wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        if self.find_dlg:
            if loc == -1:
                self.find_dlg.SetFocus()
                return
            else:
                self.find_dlg.Destroy()
                self.find_dlg = None
        self.ShowPosition(loc)
        self.SetSelection(loc, loc + len(find_string))

    def on_find_close(self, evt):
        # self.log.write("FindReplaceDialog closing...\n")
        evt.GetDialog().Destroy()
        # self.EnableButtons()

    def on_key_pressed(self, event):
        if self.CallTipActive():
            self.CallTipCancel()

        if event.ControlDown() and event.GetKeyCode() == wx.WXK_SPACE:
            pos = self.GetCurrentPos()

            # Tips
            if event.ShiftDown():
                self.CallTipSetBackground("yellow")
                self.CallTipShow(pos, 'lots of of text: blah, blah, blah\n\n'
                                 'show some suff, maybe parameters..\n\n'
                                 'fubar(param1, param2)')
            # Code completion
            else:
                # lst = []
                # for x in range(50000):
                #    lst.append('%05d' % x)
                # st = " ".join(lst)
                # print len(st)
                # self.AutoCompShow(0, st)

                kw = keyword.kwlist[:]
                kw.append("zzzzzz?2")
                kw.append("aaaaa?2")
                kw.append("__init__?3")
                kw.append("zzaaaaa?2")
                kw.append("zzbaaaa?2")
                kw.append("this_is_a_longer_value")
                # kw.append("this_is_a_much_much_much_much_much_much_much_longer_value")

                kw.sort()  # Python sorts are case sensitive
                self.AutoCompSetIgnoreCase(False)  # so this needs to match

                # Images are specified with a appended "?type"
                for i in range(len(kw)):
                    if kw[i] in keyword.kwlist:
                        kw[i] = kw[i] + "?1"

                self.AutoCompShow(0, " ".join(kw))
        else:
            event.Skip()

    def on_update_ui(self, evt):
        # check for matching braces
        brace_at_caret = -1
        brace_opposite = -1
        char_before = None
        caret_pos = self.GetCurrentPos()
        style_before = stc.STC_P_DEFAULT

        if caret_pos > 0:
            char_before = self.GetCharAt(caret_pos - 1)
            style_before = self.GetStyleAt(caret_pos - 1)

        # check before
        if char_before and chr(char_before) in "[]{}()" and style_before == stc.STC_P_OPERATOR:
            brace_at_caret = caret_pos - 1

        # check after
        if brace_at_caret < 0:
            char_after = self.GetCharAt(caret_pos)
            style_after = self.GetStyleAt(caret_pos)

            if char_after and chr(char_after) in "[]{}()" and style_after == stc.STC_P_OPERATOR:
                brace_at_caret = caret_pos

        if brace_at_caret >= 0:
            brace_opposite = self.BraceMatch(brace_at_caret)

        if brace_at_caret != -1  and brace_opposite == -1:
            self.BraceBadLight(brace_at_caret)
        else:
            self.BraceHighlight(brace_at_caret, brace_opposite)
            # pt = self.PointFromPosition(braceOpposite)
            # self.Refresh(True, wxRect(pt.x, pt.y, 5,5))
            # print pt
            # self.Refresh(False)

    def on_margin_click(self, evt):
        # fold and unfold as needed
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.fold_all()
            else:
                line_clicked = self.LineFromPosition(evt.GetPosition())

                if self.GetFoldLevel(line_clicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(line_clicked, True)
                        self.expand(line_clicked, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(line_clicked):
                            self.SetFoldExpanded(line_clicked, False)
                            self.expand(line_clicked, False, 0)
                        else:
                            self.SetFoldExpanded(line_clicked, True)
                            self.expand(line_clicked, True, 100)
                    else:
                        self.ToggleFold(line_clicked)