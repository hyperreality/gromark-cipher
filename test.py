from gromark import *
import unittest


class TestBasic(unittest.TestCase):
    def test_gronsfeld(self):
        # Testcase from:
        # https://www.cryptogram.org/downloads/aca.info/ciphers/Gronsfeld.pdf
        ct = "CKKTS WGDVG TXNPX IVIIC YNQVZ WRZEL IFRNT NDNQL JDNWU"
        pt = "THISONEUSESTENOFTHETWENTYSIXVIGENEREALPHABETS"

        gronsfeld = Gronsfeld(9321492)
        self.assertEqual(gronsfeld.decrypt(ct), pt)
        gronsfeld = Gronsfeld(9321492)
        self.assertEqual(gronsfeld.encrypt(pt), ct.replace(' ', ''))

    def test_gromark_trans_table(self):
        # Testcase from:
        # https://www.cryptogram.org/downloads/aca.info/ciphers/Gromark.pdf
        key = "ENIGMA"
        self.assertEqual(trans_table(
            key), ("AJRXEBKSYGFPVIDOUMHQWNCLTZ", [1, 5, 3, 2, 4, 0]))

    def test_gromark(self):
        # Testcase from:
        # https://www.cryptogram.org/downloads/aca.info/ciphers/Gromark.pdf
        key = "ENIGMA"
        primer = 23452
        ct = "NFYCKBTIJCNWZYCACJNAYNLQPWWSTWPJQFL"
        pt = "THEREAREUPTOTENSUBSTITUTESPERLETTER"

        gromark = Gromark(key, primer)
        self.assertEqual(gromark.decrypt(ct), pt)
        gromark = Gromark(key, primer)
        self.assertEqual(gromark.encrypt(pt), ct)

    def test_periodic_gromark(self):
        # Testcase from:
        # https://www.cryptogram.org/downloads/aca.info/ciphers/PeriodicGromark.pdf
        key = "ENIGMA"
        ct = "RHNAAX NRUZBN IUARXC RTPATB RLIGDS VCIRCV OYPVRA AZZMUSREQYEV MMURGW TLUD"
        pt = "WINTRYSHOWERSWILLCONTINUEFORTHENEXTFEWDAYSACCORDINGTOTHEFORECAST"

        gromark = PeriodicGromark(key)
        self.assertEqual(gromark.decrypt(ct), pt)
        gromark = PeriodicGromark(key)
        self.assertEqual(gromark.encrypt(pt), ct.replace(' ', ''))


if __name__ == '__main__':
    unittest.main()
