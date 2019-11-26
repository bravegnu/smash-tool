import unittest
from unittest.mock import Mock
from smashlib.hexfile import Hex, HexFile, HexError
from smashlib.smash import Serial
from smashlib.micro import Micro
import errno 
import builtins
import io
from smashlib.micro import micro_info, HexDispData, HexBlankCheck, ProtoError, IspTimeoutError, IspChecksumError, IspProgError


class MockTestCase(unittest.TestCase):

	def setUp(self):
		self.serial = Mock()
		self.micro_obj = Micro("P89V51RD2", 12, self.serial)

	def test_dispdata(self):
		hex_disp = HexDispData(0x20, 0x8)
		expected_value = b":050000040020000800cf"
		self.assertEqual(hex_disp.hex, expected_value)

	def test_blank_check(self):
		hex_blank = HexBlankCheck(0x20, 0x8)
		expected_value = b":050000040020000801ce"
		self.assertEqual(hex_blank.hex, expected_value)

	def test_sync_baudrate(self):
		self.micro_obj.sync_baudrate()
		self.assertEqual(self.micro_obj.serial.write.called, True)
		self.assertEqual(self.micro_obj.serial.wait_for.called, True)
		self.serial.wait_for.assert_called_with(b"U")


	def test_send_cmd(self):
		v = self.micro_obj._send_cmd(b"U", 2)
		self.assertEqual(self.micro_obj.serial.write.called, True)
		self.assertEqual(self.micro_obj.serial.wait_for.called, True)
		self.assertEqual(v,  None)

	def test_send_cmd_none(self):
		self.serial.wait_for.return_value = b"."
		v = self.micro_obj._send_cmd(b"U", None)
		self.assertEqual(v,  None)

	def test_send_cmd_checksum(self):
		self.serial.wait_for.return_value = b"X"
		self.assertRaises(IspChecksumError,  self.micro_obj._send_cmd, b"U", None)	


	def test_send_cmd_progem_error(self):
		self.serial.wait_for.return_value = b"R"
		self.assertRaises(IspProgError,  self.micro_obj._send_cmd, b"U", None)

	def test_send_cmd_progem_error_3(self):
		self.serial.wait_for.return_value = b"P"
		self.assertRaises(IspProgError,  self.micro_obj._send_cmd, b"U", None)

	def test_send_cmd_progem_error_2(self):
		self.serial.wait_for.return_value = b"P"
		self.assertRaises(IspProgError,  self.micro_obj._send_cmd, b"U", None)

	def test_program_file(self):
		self.micro_obj._send_cmd = Mock()
		byte = io.BytesIO(b":03000000020008f3")
		builtins.open = Mock(return_value=byte)
		data = 0
		self.micro_obj.prog_file(byte, data)
		self.micro_obj._send_cmd.assert_called_with(b':03000000020008f3')

	def test_hex_dip(self):
		self.assertRaisesRegex(ValueError, "data start address 0x54321 out of range", HexDispData, 0x54321, 0x4321)
		self.assertRaisesRegex(ValueError, "data end address 0x43266 out of range", HexDispData, 0x5432, 0x43266)

	def test_hex_dip_error(self):
		self.assertRaisesRegex(ValueError, "check start address 0x54321 out of range", HexBlankCheck, 0x54321, 0x4321)
		self.assertRaisesRegex(ValueError, "check end address 0x43266 out of range", HexBlankCheck, 0x5432, 0x43266)

	def test__getitem__(self):
		data = [b'0x0000=0E', b'']
		self.micro_obj.serial.read_timeo = Mock(side_effect = data)
		self.micro_obj.__getitem__(0x0000)
		self.assertEqual(self.micro_obj.serial.write.called, True)	

	def test_update_cache_with_data(self):
		self.micro_obj._update_cache_with_line = Mock()
		v = self.micro_obj._update_cache_with_data(b'0x0000=0E')
		self.micro_obj._update_cache_with_line.assert_called_with(b'0x0000=0E')
		self.assertEqual(v, None)

	def test_update_line(self):
		v = self.micro_obj._update_cache_with_line(b'0x0000=0E')
		self.assertEqual(v, None)

	def test_update_cache(self):
		data = [b'0x0000=0E', b'']
		self.micro_obj._update_cache_with_data = Mock()
		self.micro_obj.serial.read_timeo = Mock(side_effect = data)
		self.micro_obj._update_cache(0x0000)
		self.assertEqual(self.micro_obj.serial.write.called, True)
		self.micro_obj._update_cache_with_data.assert_called_with(b'0x0000=0E')
		
	def test_getitem(self):
		data = [b'0x0000=0E', b'']
		self.micro_obj.serial.read_timeo = Mock(side_effect = data)
		self.assertEqual(self.micro_obj._getitem(0x0000), 14)
		self.assertEqual(self.micro_obj.serial.write.called, True)

	def test__update_cache_with_line_error(self):
		self.assertRaises(ProtoError, self.micro_obj._update_cache_with_line, b'0x0000+0E')

	def test__update_cache_with_line_addr_error(self):
		self.assertRaises(ProtoError, self.micro_obj._update_cache_with_line, b'0xghgj=0E')	

	def test_getitem_error(self):
		data = [b'0x0001=0E', b'']
		self.micro_obj.serial.read_timeo = Mock(side_effect = data)
		self.assertRaises(ProtoError, self.micro_obj._getitem, 0x0001)
	


if __name__ == '__main__':
	unittest.main()
