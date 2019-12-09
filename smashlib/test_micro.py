import io
import unittest
from unittest.mock import Mock, patch
from smashlib.micro import Micro
from smashlib.micro import  HexDispData, HexBlankCheck, ProtoError
from smashlib.micro import IspChecksumError, IspProgError, IspTimeoutError


class HexTestCase(unittest.TestCase):

    def test_dispdata(self):
        hex_disp = HexDispData(0x20, 0x8)
        expected_value = b":050000040020000800cf"
        self.assertEqual(hex_disp.hex, expected_value)

    def test_blank_check(self):
        hex_blank = HexBlankCheck(0x20, 0x8)
        expected_value = b":050000040020000801ce"
        self.assertEqual(hex_blank.hex, expected_value)

    def test_hex_dip(self):
        self.assertRaisesRegex(ValueError, "data start address 0x54321 out of range",
                               HexDispData, 0x54321, 0x4321)
        self.assertRaisesRegex(ValueError, "data end address 0x43266 out of range",
                               HexDispData, 0x5432, 0x43266)

    def test_hex_dip_error(self):
        self.assertRaisesRegex(ValueError, "check start address 0x54321 out of range",
                               HexBlankCheck, 0x54321, 0x4321)
        self.assertRaisesRegex(ValueError, "check end address 0x43266 out of range",
                               HexBlankCheck, 0x5432, 0x43266)

class MockTestCase(unittest.TestCase):
    def setUp(self):
        self.serial = Mock()
        self.micro_obj = Micro("P89V51RD2", 12, self.serial)

    def data(self):
        string = io.BytesIO(b":0300610002000397\n:0300610002000397")
        m_open = Mock(return_value=string)
        return m_open

    def test_sync_baudrate(self):
        self.micro_obj.sync_baudrate()
        self.assertEqual(self.micro_obj.serial.write.called, True)
        self.assertEqual(self.micro_obj.serial.wait_for.called, True)
        self.serial.wait_for.assert_called_with(b"U")

    def test_sync_baudrate_error(self):
        self.serial.wait_for.side_effect = IspTimeoutError('')
        self.assertRaises(IspTimeoutError, self.micro_obj.sync_baudrate)

    def test_program_file(self):
        self.serial.wait_for.return_value = b"."
        with patch('builtins.open', self.data()):
            self.micro_obj.prog_file("", Mock())
        self.assertEqual(self.micro_obj.serial.write.called, True)
        self.assertEqual(self.micro_obj.serial.wait_for.called, True)

    def test_send_cmd_checksum(self):
        self.serial.wait_for.return_value = b"X"
        with patch('builtins.open', self.data()):
            self.assertRaises(IspChecksumError, self.micro_obj.prog_file, "")

    def test_send_cmd_progem_error(self):
        self.serial.wait_for.return_value = b"R"
        string = io.BytesIO(b":03000000020008")
        m_open = Mock(return_value=string)
        with patch('builtins.open', m_open):
            self.assertRaises(IspProgError, self.micro_obj.prog_file, "")   
    def test_send_cmd_progem_error_3(self):
        self.serial.wait_for.return_value = b"P"
        string = io.BytesIO(b":03000000020008")
        m_open = Mock(return_value=string)        
        with patch('builtins.open', m_open):
            self.assertRaises(IspProgError, self.micro_obj.prog_file, "")

    def test__getitem__(self):
        data = [b":", b"\r", b"0x0000=0E", b""]
        self.micro_obj.serial.read_timeo.side_effect = data
        self.assertEqual(self.micro_obj[0x0000], 14)
        self.assertEqual(self.micro_obj.serial.write.called, True)

    def test__update_cache_with_line_error(self):
        data = [b'0x0000', b''] * 8
        self.micro_obj.serial.read_timeo.side_effect = data
        self.assertRaises(ProtoError, lambda: self.micro_obj[0xffff])
    
    def test__update_cache_with_line_addr_error(self):
        data = [b'0xghgj=pp', b''] * 8
        self.micro_obj.serial.read_timeo.side_effect = data
        self.assertRaises(ProtoError, lambda: self.micro_obj[0x0000])

    def test__update_cache_with_line_data_error(self):
        data = [b'0xghgj=7', b''] * 8
        self.micro_obj.serial.read_timeo.side_effect = data
        self.assertRaises(ProtoError, lambda: self.micro_obj[0x0000])

    def test_getitem_error(self):
        data = [b'0x0001=0E', b''] * 8
        self.micro_obj.serial.read_timeo.side_effect = data
        self.assertRaises(ProtoError, lambda: self.micro_obj[0x0000])


if __name__ == '__main__':
    unittest.main()

