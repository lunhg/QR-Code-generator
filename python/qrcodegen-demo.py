# 
# QR Code generator demo (Python 2, 3)
# 
# Run this command-line program with no arguments. The program computes a bunch of demonstration
# QR Codes and prints them to the console. Also, the SVG code for one QR Code is printed as a sample.
# 
# Copyright (c) Project Nayuki. (MIT License)
# https://www.nayuki.io/page/qr-code-generator-library
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# - The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
# - The Software is provided "as is", without warranty of any kind, express or
#   implied, including but not limited to the warranties of merchantability,
#   fitness for a particular purpose and noninfringement. In no event shall the
#   authors or copyright holders be liable for any claim, damages or other
#   liability, whether in an action of contract, tort or otherwise, arising from,
#   out of or in connection with the Software or the use or other dealings in the
#   Software.
#
# Modified by lunhg
# 

from __future__ import print_function
from qrcodegen import QrCode, QrSegment
import argparse
import uuid
import datetime

def main(args):
    do_basic_demo(inputText=args.inputText,
                  eccLvl=args.eccLvl,
                  tokenize=args.tokenize,
                  token_type=args.token_type,
                  token_expires=args.token_expires,
                  token_notbefore=args.token_notbefore,
                  token_subject=args.token_subject,
                  token_audience=args.token_audience,
                  token_signature=args.token_signature)

# ---- argparser ---
def argument_parser():
    inputHelp = "the text be encoded (data itself)"
    eccHelp = "the error correct level (LOW, MEDIUM, QUARTILE, HIGH)"
    tokenizeHelp = "the data will be tokenized (only JWT at time, algorithm is HS256)"
    tokenTypeHelp = "the data will be tokenized to (requires --tokenize. Defaults to JWT at time)"
    tokenExpiresTimeHelp = "the data tokenized expires time in timedelta minutes (defaults to 1000)"
    tokenNotBeforeHelp = "the data tokenized will not be validate before defined timedelta minutes from now  (defaults to 0)"
    tokenIssuerHelp = "the issuer of data"
    tokenSubjectHelp = "the subject of data"
    tokenAudienceHelp = "the audience of data"
    tokenSignatureHelp = "the signature of data"
    printHelp = "the output will be printed as svg"

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputText', help=inputHelp)
    parser.add_argument('-e', '--eccLvl', help=eccHelp)
    parser.add_argument('-t', '--tokenize', action='store_true', help=tokenizeHelp)
    parser.add_argument('-T', '--token-type', help=tokenTypeHelp)
    parser.add_argument('-E', '--token-expires', help=tokenExpiresTimeHelp)
    parser.add_argument('-B', '--token-notbefore', help=tokenNotBeforeHelp)
    parser.add_argument('-I', '--token-issuer', help=tokenIssuerHelp)
    parser.add_argument('-S', '--token-subject', help=tokenSubjectHelp)
    parser.add_argument('-A', '--token-audience', help=tokenAudienceHelp)
    parser.add_argument('-G', '--token-signature', help=tokenSignatureHelp)
    parser.add_argument('-p', '--print', help=printHelp)
    return parser.parse_args()

# ---- Demo suite ----

def do_basic_demo(**kwargs):
    inputText = kwargs.get('inputText') if kwargs.get('inputText') else 'Hello World'
    eccLvl = kwargs.get('eccLvl') if kwargs.get('eccLvl') else 'LOW'
    tokenize = kwargs.get('tokenize') if kwargs.get('tokenize') else False
    token_type = kwargs.get('token_type') if kwargs.get('token_type') else 'jwt'
    token_expires = kwargs.get('token_expires') if kwargs.get('token_expires') else 1000
    token_notbefore = kwargs.get('token_notbefore') if kwargs.get('token_notbefore') else 0
    token_issuer = kwargs.get('token_issuer') if kwargs.get('token_issuer') else 'qrcodegen'
    token_subject = kwargs.get('token_subject') if kwargs.get('token_subject') else 'qrcodegen block'
    token_audience = kwargs.get('token_audience') if kwargs.get('token_audience') else 'qrcodegen' 
    token_signature = kwargs.get('token_signature') if kwargs.get('token_signature') else uuid.uuid4().hex
    ecc = None

    #print("%s=%s" % ('inputText', inputText))
    #print("%s=%s" % ('eccLvl', eccLvl))
    #print("%s=%s" % ('tokenize', tokenize))
    #print("%s=%s" % ('token_type', token_type))
    #print("%s=%s" % ('token_expires', token_expires))
    #print("%s=%s" % ('token_notbefore', token_notbefore))
    #print("%s=%s" % ('token_issuer', token_issuer))
    #print("%s=%s" % ('token_subject', token_subject))
    #print("%s=%s" % ('token_audience', token_audience))
    #print("%s=%s" % ('token_signature', token_signature))

    if (eccLvl == "LOW"):
        ecc = QrCode.Ecc.LOW

    if (eccLvl == "MEDIUM"):
        ecc = QrCode.Ecc.MEDIUM

    if (eccLvl == "QUARTILE"):
        ecc = QrCode.Ecc.QUARTILE

    if (eccLvl == "HIGH"):
        ecc = QrCode.Ecc.HIGH

    if (tokenize and (token_type == 'JWT' or token_type == 'jwt')):
        from jwcrypto import jwt, jwk
        #print("Tokenizing...")
        key = jwk.JWK.generate(kty='oct', size=256)
        priv_key = key.export(private_key=True)
        dt_now = datetime.datetime.now()
        header = {
            'alg': 'HS256',
            'type': 'JWT'
        }
        payload = {
            'msg': u""+inputText,
            'iss': token_issuer,
            'sub': token_subject,
            'aud': token_audience,
            'exp': str(dt_now + datetime.timedelta(minutes=token_expires)),
            'nbf': str(dt_now + datetime.timedelta(minutes=token_notbefore)),
            'iat': str(dt_now),
            'sig': token_signature
        }

        Token = jwt.JWT(header=header, claims=payload)
        Token.make_signed_token(key)
        text = u""+Token.serialize()
        #print(text)
        svg_qrcode(text, ecc)

    else:
        text = u""+inputText
        svg_qrcode(text, ecc)


def print_qrcode(text, ecc):
    # Make public QR Code symbol
    qr = QrCode.encode_text(text, ecc)
    print_qr(qr)

def svg_qrcode(text, ecc):
    qr = QrCode.encode_text(text, ecc)
    print(qr.to_svg_str(4))
# ---- Utilities ----

def print_qr(qrcode):
	"""Prints the given QrCode object to the console."""
	border = 4
	for y in range(-border, qrcode.get_size() + border):
		for x in range(-border, qrcode.get_size() + border):
			print(u"\u2588 "[1 if qrcode.get_module(x,y) else 0] * 2, end="")
		print()
	print()

	
# Run the main program
if __name__ == "__main__":
    args = argument_parser()
    main(args)
