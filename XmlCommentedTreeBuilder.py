from xml.etree import ElementTree


class XmlCommentedTreeBuilder(ElementTree.XMLTreeBuilder):
    def __init__(self, html=0, target=None):
        ElementTree.XMLTreeBuilder.__init__(self, html, target)
        self._parser.CommentHandler = self.handle_comment
        # self._target.start("document", {})

    def handle_comment(self, data):
        self._target.start(ElementTree.Comment, {})
        self._target.data(data)
        self._target.end(ElementTree.Comment)

    def close(self):
        # self._target.end("document")
        return ElementTree.XMLTreeBuilder.close(self)


# TEST.
"""
with open('../config.xml', 'r') as f:
    xml = ElementTree.parse(f, parser=XmlCommentedTreeBuilder())
    ElementTree.dump(xml)
"""


