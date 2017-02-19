from html.parser import HTMLParser as HP
from xml.etree import ElementTree as ET

class HTMLParser (HP):

    # oveeride base class init
    def __init__(self, convert_charrefs=True):
        HP.__init__(self, convert_charrefs=convert_charrefs)

        # tree structure for element
        self.__tree = []
        self.__root = None

    def feed(self, data):
        # clear three and root
        self.__tree.clear()
        self.__root = None

        # new feed
        HP.feed(self, data)
        return self.__root

    def handle_starttag(self, tag, attrs):
        if len(self.__tree) == 0:
            element = ET.Element(tag, dict(self.__filter_attrs(attrs)))
            self.__tree.append(element)
            self.__root = element
        
        else:
            element = ET.SubElement(self.__tree[-1], tag, dict(self.__filter_attrs(attrs)))
            self.__tree.append(element)

    def handle_endtag(self, tag):
        self.__tree.pop()

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data):
        if len(self.__tree) != 0:
            self.__tree[-1].text = data

    def handle_entityref(self, name):
        pass

    def handle_charref(self, name):
        pass

    def handle_comment(self, data):
        pass

    def handle_decl(self, decl):
        pass

    def handle_pi(self, data):
        pass

    def unknown_decl(self, data):
        pass

    def get_root_element(self):
        return self.__root

    def __filter_attrs(self, attrs):
        return filter(lambda x: x[0] and x[1], attrs) if attrs else []

# example usage data
# support xpath but limited depend on python library xpath
'''parser = HTMLParser()
root = parser.feed(html)
parser.close()

panels = root.findall(".//div[@class='panel']/div[@class='panel-content']")
for panel in panels:
    span = panel.find("a[@class='refinement-header']/h3/span[@class='facet-name']")
    if span != None:
        if span.text in ("kollektion", "farbe", "grösse", "marke"):
            print(span.text)
            panelsOpt = panel.findall("div/ul/li")
            if len(panelsOpt) != 0:
                for li in panelsOpt:
                    print("==")
                    print("data-id: {}".format(li.get("data-id")))
                    print("data-name: {}".format(li.get("data-name")))
                    a = li.find("a")
                    print("query-string: {}".format(a.get("href")))

        if span.text == "preisrahmen":
            print("==")
            print(span.text)
            userMin = panel.find("div/div[@class='price-tip']/span[@id='userMin']")
            userMax = panel.find("div/div[@class='price-tip']/span[@id='userMax']")
            print("min-price: {}".format(userMin.text.split(" ")[0].strip()))
            print("max-price: {}".format(userMax.text.split(" ")[0].strip()))'''