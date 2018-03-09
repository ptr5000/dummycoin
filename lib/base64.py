
class Base64:
    """
    https://tools.ietf.org/html/rfc4648
    """

    def __init__(self):
        self.alphabet = \
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    def encode(self, data):
        """
        Encode a string using Base64

        Args:
            data: string to be encoded

        Returns:
            encoded string
        """
        if len(data) == 0:
            return ""

        out = ""
        npad = len(data) % 3

        if npad > 0:
            data += '\0' * (3-npad)

        for i in xrange(0, len(data), 3):
            enc = (ord(data[i]) << 16) + (ord(data[i+1]) << 8) + ord(data[i+2])

            out += self.alphabet[(enc >> 18) & 63]
            out += self.alphabet[(enc >> 12) & 63]
            out += self.alphabet[(enc >> 6) & 63]
            out += self.alphabet[enc & 63]

        if npad > 0:
            out = out[:-(3-npad)] + '=' * (3-npad)

        return out

    def decode(self, data):
        """
        Decode base64 encoded string

        Args:
            data: base64 encoded string

        Returns:
            Decoded string
        """
        out = ""

        npad = data.count('=')
        data = data.replace('=', 'A')

        for i in xrange(0, len(data), 4):
            ch = (self.alphabet.index(data[i]) << 18) + \
                 (self.alphabet.index(data[i+1]) << 12) + \
                 (self.alphabet.index(data[i+2]) << 6) + \
                self.alphabet.index(data[i+3])

            out += chr((ch >> 16) & 255)
            out += chr((ch >> 8) & 255)
            out += chr(ch & 255)

        if npad > 0:
            out = out[:-npad]

        return out
