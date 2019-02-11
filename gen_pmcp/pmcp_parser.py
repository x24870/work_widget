import xml.etree.ElementTree as ET

class PMCP_Parser():
    def __init__(self):
        self.tree = None

    def read_pmc(self, filename):
        self.tree = ET.parse(filename)

if __name__ == "__main__":
    parser = PMCP_Parser()
    parser.read_pmc('Wolfpass.pmc')
    root = parser.tree.getroot()
    print(root.tag)