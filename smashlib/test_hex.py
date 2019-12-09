import io
import unittest
from unittest.mock import Mock, patch
from hexfile import Hex, HexFile, HexError

class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.hex_data = Hex(b":03000000020008")
        string = io.BytesIO(b":03000000020008f3")
        m_open = Mock(return_value=string)
        with patch('builtins.open', m_open):
            self.hex_read = HexFile('')
    def test_checksum(self):
        self.assertEqual(self.hex_data.append_checksum(b":03000000020008"), b":03000000020008f3")

    def test_get_type(self):
        self.assertEqual(self.hex_data.get_type(), b"00")

    def test_is_data(self):
        self.assertEqual(self.hex_data.is_data(), 1)

    def test_is_eof(self):
        self.assertEqual(self.hex_data.is_eof(), 0)

    def test_addr(self):
        self.assertEqual(self.hex_data.addr(), 0000)

    def test_data(self):
        self.assertEqual(self.hex_data.data(), (2, 0, 8))

    def test_datalen(self):
        self.assertEqual(self.hex_data.datalen(), 3)

    def test_get_hex(self):
        self.assertEqual(self.hex_data.get_hex(), b":03000000020008")

    def test__bytes__(self):
        self.assertEqual(self.hex_data.__bytes__(), b":03000000020008")

    def test_block_from_addr(self):
        self.assertEqual(self.hex_read.block_from_addr(1010, [(0000, 1111)]), 0)

    def test_iter(self):
        self.assertEqual(self.hex_read.rewind(), None)

    def test_data_bytes(self):
        self.assertEqual(self.hex_read.count_data_bytes(), 3)

    def test_data_data(self):
        data = self.hex_read.data_bytes()
        data_list = []
        for i in data:
            data_list.append(i)
        self.assertEqual(data_list, [(0, 2), (1, 0), (2, 8)])

    def test_used_blocks(self):
        self.assertEqual(self.hex_read.used_blocks([(0000, 1111)]), [0])

    def test_hex_error(self):
        self.assertRaises(HexError, self.hex_data.append_checksum, 'N/A')

    def test_hexfile_error(self):
        self.assertRaises(HexError, Hex(":dfgh").data)

    def test_addr_error(self):
        self.assertRaises(HexError, Hex(":dfgh").addr)

    def test_datalen_error(self):
        self.assertRaises(HexError, Hex(":ggg").datalen)

class SecondTest(unittest.TestCase):

    def test_count_error(self):
        string = io.BytesIO(b":03000000")
        m_open = Mock(return_value=string)
        string.name = ''
        with patch('builtins.open', m_open):
            hex_read = HexFile('')
        self.assertRaises(HexError, hex_read.count_data_bytes)

    def test_file_error(self):
        string = io.BytesIO(b":03000001020008F3")
        m_open = Mock(return_value=string)
        with patch('builtins.open', m_open):
            hex_read = HexFile('')
        self.assertRaises(StopIteration, next, hex_read)

    def test_block_error(self):
        string = io.BytesIO(b":03gggg00020008F3")
        m_open = Mock(return_value=string)
        string.name = ''
        with patch('builtins.open', m_open):
            hex_read = HexFile('')
        self.assertRaises(HexError, hex_read.used_blocks, [(0000, 1111)])

    def test_block_data_error(self):
        string = io.BytesIO(b":03000000020008F3")
        m_open = Mock(return_value=string)
        string.name = ''
        with patch('builtins.open', m_open):
            hex_read = HexFile('')
        self.assertRaises(HexError, hex_read.used_blocks, [(-111, -222)])


    def test_data_bytes_error(self):
        string = io.BytesIO(b":03000000")
        m_open = Mock(return_value=string)
        string.name = ''
        with patch('builtins.open', m_open):
            hex_read = HexFile('')
        self.assertRaises(HexError, next, hex_read.data_bytes())



if __name__ == '__main__':
    unittest.main()

