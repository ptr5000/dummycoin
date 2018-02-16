
class Base64:
    """
    https://tools.ietf.org/html/rfc4648
    """
    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        
    def encode(self, data):
        if len(data) == 0:
            return ""  

        out = ""
        npad = len(data) % 3

        if npad > 0:
            data += '\0' * (3-npad)
      
        for i in range(0, len(data), 3):
            enc = (ord(data[i]) << 16) + (ord(data[i+1]) << 8) + ord(data[i+2])
            
            out += self.alphabet[(enc >> 18) & 63]
            out += self.alphabet[(enc >> 12) & 63]
            out += self.alphabet[(enc >> 6) & 63]
            out += self.alphabet[enc & 63]
        
        if npad > 0:
            out = out[:-(3-npad)] + '=' * (3-npad)

        return out

    def decode(self, data):
        # TODO: replace with own
        return data.decode('base64')
    

