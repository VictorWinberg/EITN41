# Optional. Check whats wrong
openssl rsa -check -in input/censored.pem -noout

# Parse censored private key to asn1 and 
# create a asn1 structured rsa_key with p, q and e
echo
echo " === Please insert and calculate values needed into asn1 stucture input/asn.cnf === "
openssl asn1parse -in input/censored.pem | while ((i++)); read line; do
  if [[ ($i == 4) || ($i == 6) || ($i == 7) ]]; then
    IFS=':' read -ra keys <<< "$line"
    for j in "${!keys[@]}"; do
      if [[ $j == 3 ]]; then
        if [[ $i == 4 ]]; then
          echo "e (hex): ${keys[$j]}"
        elif [[ $i == 6 ]]; then
          echo "q (hex): ${keys[$j]}"
        elif [[ $i == 7 ]]; then
          echo "q (hex): ${keys[$j]}"
        fi
      fi
    done
  fi
done
echo " === End of values === "
echo

# Parse the generated asn1 rsa_key to der encoding
mkdir -p output
openssl asn1parse -genconf input/asn.cnf -out output/asn.der -noout

# Parse the der encoded rsa_key to pem format
openssl rsa -in output/asn.der -inform der -out output/key.pem

# Decode the base64 encoded message
openssl base64 -d -in input/message.b64 > output/message.txt

printf "\nDecrypted message: "

# Decrypt the encrypted message with rsa private key
openssl rsautl -decrypt -in output/message.txt -inkey output/key.pem
