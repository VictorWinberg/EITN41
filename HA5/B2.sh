function cmsmail {
  echo "-------- Mail $1 --------"
  openssl cms -decrypt -in $2.msg -recip $3 -inkey $4 -out $2.txt
  sed "3q;d" $2.txt
  openssl cms -digest_verify -in $2.txt 2> $2.verify | sed "3q;d"
  sed '1q;d' $2.verify
  echo
  rm $2.txt $2.verify
}

mail1="input/b2/mail1"
mail2="input/b2/mail2"
mail3="input/b2/mail3"
cert="input/b2/certreceiver.pem"
key="input/b2/keyreceiver.pem"

cmsmail 1 $mail1 $cert $key
cmsmail 2 $mail2 $cert $key
cmsmail 3 $mail3 $cert $key
