## Notes

`cast wallet address --account <ACCOUNT-NAME>` to get a saved wallet address

`cast wallet public-key --account <ACCOUNT-NAME>` to get a saved wallet public key

asked chatgpt to turn the public key into x and y components.

`cast keccak "hello"` to generate the hash of the message.
- `0x1c8aff950685c2ed4bc3174f3472287b56d9517b9c948127319a09a7a36deac8`

`cast wallet sign --no-hash 0x1c8aff950685c2ed4bc3174f3472287b56d9517b9c948127319a09a7a36deac8 --account <ACCOUNT-NAME>` to sign the message hash
- `0x2f4de1728da360cbabc3fca322e4cd6e86eea3c29c2dd529ed28c3a2b76a090c1cd57dee13a254ddc2f784a33751e0559fa538cda781adc70e0614815d0570ec1c`

then:
`nargo execute` to generate the circuit's bytecode and solved witness
output:
```
[secp256k_zk_verifier] Circuit witness successfully solved
[secp256k_zk_verifier] Witness saved to target/secp256k_zk_verifier.gz
```
Generate the proof given the circuit bytecode and witness:
```
bb prove \
    -b ./target/secp256k_zk_verifier.json \
    -w ./target/secp256k_zk_verifier.gz \
    -o ./target/
```
output:
```
Scheme is: ultra_honk
Finalized circuit size: 56876
Public inputs saved to "./target/public_inputs"
Proof saved to "./target/proof"
```

Generate verifying key given circuit bytecode:
```
bb write_vk \
    -b ./target/secp256k_zk_verifier.json \
    -o ./target/
```
output:
```
Scheme is: ultra_honk
Finalized circuit size: 56876
VK saved to "./target/vk"
```

verify the proof with the verifying key:
```
bb verify \
    -k ./target/vk \
    -p ./target/proof
```
output:
```
Scheme is: ultra_honk
Proof verified successfully
```

## Generate solidity verifier contract

Need to pass the `--oracle_hash keccak` flag when generating vkey and proving
to instruct `bb` to use keccak as the hash function, which is more optimal in Solidity:
```
bb write_vk \
    --oracle_hash keccak \
    -b ./target/secp256k_zk_verifier.json \
    -o ./target/
```
output:
```
Scheme is: ultra_honk
Finalized circuit size: 56876
VK saved to "./target/vk"
```
Create a directory to store the contracts: `mkdir contracts`
Generate the solidity verifying contract:
```
bb write_solidity_verifier 
    -k ./target/vk \
    -o ./contracts/Verifier.sol
```
output:
```
Scheme is: ultra_honk
Solidity verifier saved to "./contracts/Verifier.sol"
```