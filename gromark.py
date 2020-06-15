import string


class GronsfeldKey:
  def __init__(self, primer):
    self.primer = primer
    self.i = 0

  def __next__(self):
    next_num = self.primer[self.i]
    self.i = (self.i + 1) % len(self.primer)
    return next_num


class Gronsfeld:
    def __init__(self, key, key_type=GronsfeldKey, alphabet=string.ascii_uppercase):
        self.alphabet = alphabet
        if type(key) is int:
            key = list([int(i) for i in str(key)])
        self.key = key_type(key)

    def __encDec(self, text, isEncrypt):
        ans = ""
        for i, char in enumerate(text):
            try:
                alphIndex = (self.alphabet.index(char) +
                         isEncrypt * next(self.key)) % len(self.alphabet)
                ans += self.alphabet[alphIndex]
            except ValueError as e:
                print(f"Can't find char {char} in alphabet, skipping")
        return ans

    def encrypt(self, plaintext):
        return self.__encDec(plaintext, 1)

    def decrypt(self, ciphertext):
        return self.__encDec(ciphertext, -1)


def trans_table(orig_key, alphabet=string.ascii_uppercase):
    # Remove dups
    key = ""
    for i, k in enumerate(orig_key):
        if orig_key.index(k) == i:
            key += k

    # Create x*x block of remaining letters of alphabet
    rest = "".join([c for c in alphabet if c not in key])
    block = [key] + [rest[i:i+len(key)]
                     for i in range(0, len(rest), len(key))]

    # key column positions from key letters
    column_orders = [sorted(key).index(k) for k in key]

    # take columns in correct order
    out = ""
    for i, _ in enumerate(column_orders):
        col = column_orders.index(i)

        for bl in block:
            try:
                out += bl[col]
            except IndexError:
                pass

    return out, column_orders


class GromarkKey:
  def __init__(self, primer):
    self.primer = primer

  def __next__(self):
    next_num = (self.primer[0] + self.primer[1]) % 10
    self.primer.append(next_num)
    return self.primer.pop(0)


class Gromark:
    def __init__(self, keyword, primer, key_type=GromarkKey, alphabet=string.ascii_uppercase):
        self.alphabet = alphabet
        self.trans, _ = trans_table(keyword, alphabet)
        self.gronsfeld = Gronsfeld(
            key=primer,
            key_type=key_type,
            alphabet=alphabet,
        )

    def encrypt(self, plaintext):
        intermediate = self.gronsfeld.encrypt(plaintext)
        translated = "".join([self.trans[self.alphabet.index(c)] for c in intermediate])
        return translated

    def decrypt(self, ciphertext):
        translated = "".join([self.alphabet[self.trans.index(c)] for c in ciphertext if c in self.alphabet])
        return self.gronsfeld.decrypt(translated)


class PeriodicGromarkKey:
  def __init__(self, keyword, alphabet=string.ascii_uppercase):
    self.trans, self.numerical_key = trans_table(keyword, alphabet)
    self.key_shifts = [self.trans.index(k) for k in keyword]
    self.primer = [n+1 for n in self.numerical_key]
    self.i = 0

  def __next__(self):
    next_num = (self.primer[0] + self.primer[1]) % 10
    self.primer.append(next_num)
    initial_shift = self.primer.pop(0)

    periodic_shift = (self.i % (len(self.numerical_key)**2)) // len(self.numerical_key)
    self.i += 1
    return initial_shift + self.key_shifts[periodic_shift]


class PeriodicGromark:
    def __new__(self, keyword, alphabet=string.ascii_uppercase):
        return Gromark(
            keyword=keyword,
            primer=keyword,
            key_type=PeriodicGromarkKey,
            alphabet=alphabet,
        )


key = 9321492
test_gronsfeld = Gronsfeld(key)
ct = "CKKTS WGDVG TXNPX IVIIC YNQVZ WRZEL IFRNT NDNQL JDNWU"
decrypted = test_gronsfeld.decrypt(ct)
assert decrypted == "THISONEUSESTENOFTHETWENTYSIXVIGENEREALPHABETS"
test_gronsfeld = Gronsfeld(key)
encrypted = test_gronsfeld.encrypt(decrypted)
assert encrypted == ct.replace(' ', '')


key = "ENIGMA"
primer = 23452
ct = "NFYCKBTIJCNWZYCACJNAYNLQPWWSTWPJQFL"

test_gromark = Gromark(key, primer)
assert test_gromark.trans == "AJRXEBKSYGFPVIDOUMHQWNCLTZ"

decrypted = test_gromark.decrypt(ct)
assert decrypted == "THEREAREUPTOTENSUBSTITUTESPERLETTER"

test_gromark = Gromark(key, primer)
assert test_gromark.trans == "AJRXEBKSYGFPVIDOUMHQWNCLTZ"
encrypted = test_gromark.encrypt(decrypted)
assert encrypted == ct


key = "ENIGMA"
ct = "RHNAAX NRUZBN IUARXC RTPATB RLIGDS VCIRCV OYPVRA AZZMUSREQYEV MMURGW TLUD"

test_periodic_gromark = PeriodicGromark(key)
decrypted = test_periodic_gromark.decrypt(ct)
assert decrypted == "WINTRYSHOWERSWILLCONTINUEFORTHENEXTFEWDAYSACCORDINGTOTHEFORECAST"

test_periodic_gromark = PeriodicGromark(key)
encrypted = test_periodic_gromark.encrypt(decrypted)
assert encrypted == ct.replace(' ', '')


key = "AGENCY"
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

test_periodic_gromark = PeriodicGromark(key)
decrypted = test_periodic_gromark.decrypt(ct)
print(decrypted)

