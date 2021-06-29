import unittest
import xml_parser
import xml.etree.ElementTree as ET


class TestSum(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        tree = ET.parse('test_xml.xml')
        self.root = tree.getroot()

    def test_namespace(self):
        self.assertEqual(xml_parser.get_namespace(self.root), 
            '{http://www.abbyy.com/FineReader_xml/FineReader10-schema-v1.xml}', 
            "Should be {http://www.abbyy.com/FineReader_xml/FineReader10-schema-v1.xml}")

    def test_parse_text(self):
        self.assertEqual(len(xml_parser.parse_text(self.root, '{http://www.abbyy.com/FineReader_xml/FineReader10-schema-v1.xml}')), 
            131, "Should be 131")

    def test_find_text(self):
        parsed_text = xml_parser.parse_text(
            self.root, '{http://www.abbyy.com/FineReader_xml/FineReader10-schema-v1.xml}')
        self.assertEqual(xml_parser.find_text(
            parsed_text, 'LAW OFFICES OF C. JOE SAYAS, JR.'), 25, 'Should be 25')

    def test_find_text_reverse(self):
        parsed_text = xml_parser.parse_text(
            self.root, '{http://www.abbyy.com/FineReader_xml/FineReader10-schema-v1.xml}')
        self.assertEqual(xml_parser.find_text_reverse(
            parsed_text, 'LAW OFFICES OF C. JOE SAYAS, JR.', 35), 25, 'Should be 25')


if __name__ == '__main__':
    unittest.main()
