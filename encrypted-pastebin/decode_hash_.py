import base64
import sys


def rep_chars(h):
    return h.replace('~', '=').replace('!', '/').replace('-', '+')

def b64d(x):
    d = x.encode('utf8')
    return base64.decodestring(d)

title = "algo"
body="algoencriptado"

hashes = [
    "vgFPnyX9F4EvROCgIkIZQFts8msv5huV3-7Zo8VTgVuz2oTBPQ2fLlcFLS0ctvG6obKOxk30cz-SiFIz1dNvyn5mc!0LqQCEkonkgVxEcV4DTrCbE9Syy5Zky!JSnhUznmwExn!rduTYoD8a7CiRcZQMG0mZFCMlTmxFApwheCc0geftwNL2TMh0zLReYbTgpwrAwnPdpQQU5kPt1MLq3Q~~",
    "Qn1KbihNKS7!iW5N6san!7X95cIaHEgEf11UmqQp3tLqA!-F8DLjfdNNP17mM4zIeOCPEbVkMbrJfsreY8SfjrJuF-QGBPDOHCGGGeNYF!e4XA6dbG7PoZLMdL7rKrfmnM!Nit3N0E-Cb!eO3tsvyRfytg3Dw6NxuDR7NzMXC58irwvGzVw1--e81JUZ7HqGYYnzuzVYK9rejB7qYuaHeA~~",
    "Lk6K0piMRNYNX8YtPKSoD2VsafJdqO8eGun6wa8h7sUr!ES2rxnsPP1gaSn6cCOKgg3T!Bs!FrkVU8iRBqf-M648WPjEh8Nx9i4tf8JCMkgpaeo7PzUGPc9JDFNhWjD9n8fBEllFeG3YdQIX835MGoLCVdk17g8B4uw9yMZymAJwDSwosb0zeznq1IDJsg00LBnW2wUI2U5HvntFow-x!Q~~"
]
for i,h in enumerate(hashes):
    print(f'h: {h}')
    print(f'b: {rep_chars(h)}')
    with open(f'h{i}.bin','bw') as f:
        b = b64d(rep_chars(h))
        f.write(b)

