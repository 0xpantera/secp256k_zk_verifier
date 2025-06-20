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
`bb prove 