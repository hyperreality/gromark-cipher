from gromark import *
from attack_gromark import *
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

    def test_ractf_06(self):
        pattern = [1,4,3,5,2,6]

        possible_keys = find_gromark_key(pattern)
        key = possible_keys[0].upper()
        ct = """BFPNU DXTEA IDDTK VDSSY NJCYC
HETNS YDWVP ZWHBA FCMAN CDWOV
IZJOB VTNLT NFPKM XIODY UMCJR
XDPAZ QZFRB UXZLZ ZTLVD JJVAK
EYMRT YTMHW XAMPX TWEKC WNSYH
REYBG AZFRQ SMJNN XRBJM UVDZI
CUFJX YIQSH JMXCV ABIDY SMQLN
OPZGJ JFLUC SPPKS AYZMX OQYOS
SNJLD CNJAM BLXYN BFLXC UAKOH
HCBER IAWXE VXCGL BQONI LXWYA
TYHMH GSOMF LEZMG EFCRQ TKWMF
VWNGH XZZPX RWYWN NATZT GYAKV
BKGLF BYBCZ IWOTK BEQJI LXONL
TCYET BUDGJ FBTHT EVKCH XVEDX
XPBXE NZEYG INKNM KYWXT XNEMO
AOCRG XBGXQ XYWHQ IYXBO BEVDG
ADNXT DFDYD GCFZN KGHHD WQKXY
CFJII GSDJV FREIW QMNYP MXMKZ
IZRBO BHDRB EASHY NXZXS GEHPE
PMVLK WXEUU KAOMW OWJFD LBKHE"""
        pt = "AGENTIMSOGLADYOUWEREABLETOABLETODECRYPTTHATLASTMESSAGEFORUSTHATWASJUSTWHATWENEEDEDTOSENDAGROUPOFOUROWNMENTOINTERCEPTDONNIEANDROCCOITAPPEARSTHEYWEREOPERATINGONBEHALFOFALARGERINTERNATIONALORGANIZATIONBUTWEWERENTABLETOFINDANYLEADSITLOOKSLIKEMOSTOFTHECRYPTOLOGISTSARERETURNINGFROMTHEIRHOLIDAYSSOTHISWILLPROBABLYBETHELASTEMAILFROMMEWELLHAVETOBECAREFULINFURTURETOMAKESURETHEIRLEAVENEVERLINESUPLIKETHATAGAINAGENTBPSIFYOUEVERWANTTOTRANSFERTOTHECIPHERDEPARTMENTIDBEHAPPYTOPUTANAMEINFORYOUPPSTHESECRETCODEISORG"

        gromark = PeriodicGromark(key)
        self.assertEqual(gromark.decrypt(ct), pt)


if __name__ == '__main__':
    unittest.main()
