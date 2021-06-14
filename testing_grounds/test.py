form scapy.all impot utils

hex = """0000   ff ff ff ff ff ff c0 ee fb df 58 08 08 00 45 00
0010   00 3c 4a b2 40 00 40 11 2e 83 c0 a8 00 d4 ff ff
0020   ff ff a0 f0 d4 31 00 28 a7 ae 21 31 00 20 ff ff
0030   ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
0040   ff ff ff ff ff ff ff ff ff ff
"""

scapy.utils.hexedit(hex)
