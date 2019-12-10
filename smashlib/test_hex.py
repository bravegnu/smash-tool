import io
import unittest
from unittest.mock import Mock, patch
from .hexfile import Hex, HexFile, HexError

class HexTest(unittest.TestCase):

    def setUp(self):
        self.hex_data = Hex(b":03000000020008")
        string = io.BytesIO(b":03000000020008f3")
        self.m_open = Mock(return_value=string)

    def test_checksum(self):
        expected_value = b":03000000020008f3"
        result = self.hex_data.append_checksum(b":03000000020008")
        self.assertEqual(result, expected_value)

    def test_get_type(self):
        self.assertEqual(self.hex_data.get_type(), b"00")

    def test_is_data(self):
        self.assertEqual(self.hex_data.is_data(), 1)

    def test_is_eof(self):
        self.assertEqual(self.hex_data.is_eof(), 0)

    def test_addr(self):
        self.assertEqual(self.hex_data.addr(), 0000)

    def test_data(self):
        expected_value = (2, 0, 8)
        result = self.hex_data.data()
        self.assertEqual(result, expected_value)

    def test_datalen(self):
        self.assertEqual(self.hex_data.datalen(), 3)

    def test_get_hex(self):
        expected_value = b":03000000020008"
        self.assertEqual(self.hex_data.get_hex(), expected_value)

    def test__bytes__(self):
        expected_value = b":03000000020008"
        self.assertEqual(self.hex_data.__bytes__(), expected_value)

    def test_block_from_addr(self):
        expected_value = 0
        addr = 1010
        addr_range = [(0000, 1111)]
        with patch('builtins.open', self.m_open):
            hex_read = HexFile('')
        result = hex_read.block_from_addr(addr, addr_range)
        self.assertEqual(result, expected_value)

    def test_iter(self):
        with patch('builtins.open', self.m_open):
            hex_read = HexFile('')
        self.assertEqual(hex_read.rewind(), None)

    def test_data_bytes(self):
        with patch('builtins.open', self.m_open):
            hex_read = HexFile('')
        self.assertEqual(hex_read.count_data_bytes(), 3)

    def test_data_data(self):
        expected_value = [(0, 2), (1, 0), (2, 8)]
        with patch('builtins.open', self.m_open):
            hex_read = HexFile('')
        data = hex_read.data_bytes()
        self.assertEqual(list(data), expected_value)

    def test_used_blocks(self):
        addr_range = [(0000, 1111)]
        with patch('builtins.open', self.m_open):
            hex_read = HexFile('')
        result = hex_read.used_blocks(addr_range)
        self.assertEqual(result, [0])

    def test_hex_error(self):
        result = self.hex_data.append_checksum
        self.assertRaises(HexError, result, 'N/A')

    def test_hexfile_error(self):
        self.assertRaises(HexError, Hex(":dfgh").data)

    def test_addr_error(self):
        self.assertRaises(HexError, Hex(":dfgh").addr)

    def test_datalen_error(self):
        self.assertRaises(HexError, Hex(":ggg").datalen)

class HexfileTest(unittest.TestCase):

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
        expected_value = [(0000, 1111)]
        with patch('builtins.open', m_open):
            hex_read = HexFile('')
        self.assertRaises(HexError, hex_read.used_blocks, expected_value)

    def test_block_data_error(self):
        string = io.BytesIO(b":03000000020008F3")
        m_open = Mock(return_value=string)
        string.name = ''
        expected_value = [(-111, -222)]
        with patch('builtins.open', m_open):
            hex_read = HexFile('')
        self.assertRaises(HexError, hex_read.used_blocks, expected_value)

    def test_data_bytes_error(self):
        string = io.BytesIO(b":03000000")
        m_open = Mock(return_value=string)
        string.name = ''
        with patch('builtins.open', m_open):
            hex_read = HexFile('')
        self.assertRaises(HexError, next, hex_read.data_bytes())

if __name__ == '__main__':
    unittest.main()
