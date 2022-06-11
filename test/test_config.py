from audiorename.config import read_config_file
import unittest


class TestConfig(unittest.TestCase):

    def test_read_config(self):
        args = read_config_file('example-config.ini')
        self.assertEquals(args.backup_folder, '/tmp/backup')


if __name__ == '__main__':
    unittest.main()
