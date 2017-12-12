censored_key=${1-'input/b1/censored.pem'}
secret_msg=${2-'input/b1/message.b64'}

# Make output folder
mkdir -p output

# Optional. Check whats wrong
echo "0. [Optional] RSA check censored key: "
openssl rsa -check -in $censored_key -noout

# Parse censored private key to asn1 and 
# create a asn1 structured rsa_key with p, q and e
echo "1. asn1parse censored key to python"
openssl asn1parse -in $censored_key | python3 asncreate.py

# Parse the generated asn1 rsa_key to der encoding
echo "3. generate encoded RSA key with der encoding"
openssl asn1parse -genconf output/asn.cnf -out output/asn.der -noout

# Parse the der encoded rsa_key to pem encoding
echo "4. parse the der encoded RSA key to pem encoding"
openssl rsa -in output/asn.der -inform der -out output/key.pem

# Decode the base64 encoded message
echo "5. decode the base64 encoded message"
openssl base64 -d -in $secret_msg > output/message.txt

# Decrypt the encrypted message with rsa private key
echo "6. decrypt the encrypted message"
openssl rsautl -decrypt -in output/message.txt -inkey output/key.pem

# Remove output folder
rm -rf output
