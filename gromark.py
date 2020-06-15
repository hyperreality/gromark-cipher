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




key = 9321492
test_gronsfeld = Gronsfeld(key)
ct = "CKKTS WGDVG TXNPX IVIIC YNQVZ WRZEL IFRNT NDNQL JDNWU"
decrypted = test_gronsfeld.decrypt(ct)
assert decrypted == "THISONEUSESTENOFTHETWENTYSIXVIGENEREALPHABETS"
test_gronsfeld = Gronsfeld(key)
encrypted = test_gronsfeld.encrypt(decrypted)
assert encrypted == ct.replace(' ', '')


