class Caesar():
    key = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPZXCVBNMASDFGHJK1234567890'
    def encrypt(self, n, plaintext):
        """Encrypt the string and return the ciphertext"""
        result = ''

        for l in plaintext:
            try:
                i = (self.key.index(l) + n) % len(self.key)
                result += self.key[i]
            except ValueError:
                result += l
        return result


    def decrypt(self, n, ciphertext):
        """Decrypt the string and return the plaintext"""
        result = ''

        for l in ciphertext:
            try:
                i = (self.key.index(l) - n) % len(self.key)
                result += self.key[i]
            except ValueError:
                result += l

        return result