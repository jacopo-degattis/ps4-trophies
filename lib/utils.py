import hmac
import hashlib
from Crypto.Cipher import AES

KEYSET_HASHES = {
    1: bytes.fromhex("8707960A53468D6C843B3DC9624E22AF"),
    2: bytes.fromhex("A6D6583D3217E87D9BE9BCFC4436BE4F"),
    3: bytes.fromhex("FFF9BDEA803B14824C61850EBB084EE9"),
    4: bytes.fromhex("5DC6B8D1A3A0741852A7D44268714824"),
    5: bytes.fromhex("2DE8DE4DE6628BB62DD5C170F565B62C"),
    6: bytes.fromhex("FD44A32D8BC8AC189C1BD096402966CF"),
    7: bytes.fromhex("BC4C9F0FE5D356A05752024CBDEEE8E4"),
    8: bytes.fromhex("F6F9D82182CCC2227B7D33A3B71EADE3"),
}

KEYSET_KEYS = {
    1: bytes.fromhex("B5DAEFFF39E6D90ECA7DC5B029A8153E"),
    2: bytes.fromhex("EC0D347E2A7657471F1FC33E9E916FD4"),
    3: bytes.fromhex("51D8BFB4E387FB4120F081FE33E4BE9A"),
    4: bytes.fromhex("346B5D231332AC428A44A708B1138F6D"),
    5: bytes.fromhex("20D043852530C404D16869E07908D5E6"),
    6: bytes.fromhex("93B7270DF0D3731060079066655D8D07"),
    7: bytes.fromhex("4C7844836937508B9233DF7CD7D65165"),
    8: bytes.fromhex("3A32EECF749939871C3D7BF8C01C7D1F"),
}


# TODO: replace print with debug statements
# TODO: improve code to make it more PYTHON friendly
def sce_sbl_ss_decrypt_sealed_key(enc, dec):
    """
    Python implementation of sceSblSsDecryptSealedKey
    """
    error_code = -2146499562

    if enc is not None and dec is not None:
        error_code = -2146499532

        # Check magic bytes "pfsSKKey"
        error_code = -2146499538

        # Get key version
        key_version = enc[8]
        # print(f"Using Keyset Version {key_version}")

        # Get HMAC key based on version
        sha256hmac_key = KEYSET_HASHES.get(key_version)
        if sha256hmac_key is None:
            # print(f"Error: No HMAC key found for version {key_version}")
            return error_code

        # Calculate HMAC-SHA256 of first 0x40 bytes
        hmac_calculated = hmac.new(sha256hmac_key, enc[:0x40], hashlib.sha256).digest()

        error_code = -2146499531
        # Compare with stored HMAC (bytes 64-95)
        if hmac.compare_digest(hmac_calculated, enc[64:96]):
            # print("HMAC Check... Success!")

            # Extract IV (bytes 16-31)
            iv = enc[16:32]
            # print("IV", iv.hex())

            # Extract encrypted key (bytes 32-63)
            encrypted_key = enc[32:64]

            # Get AES key based on version
            aes_key = KEYSET_KEYS.get(key_version)
            if aes_key is None:
                # print(f"Error: No AES key found for version {key_version}")
                return error_code

            # Decrypt using AES-CBC with no padding
            cipher = AES.new(aes_key, AES.MODE_CBC, iv)
            decrypted_key = cipher.decrypt(encrypted_key)

            # Copy decrypted key to output
            dec[:] = decrypted_key[:32]

            error_code = 0
        else:
            exit(-1)
            # print("HMAC Check... Failure!")
            # print(f"Expected: {enc[64:96].hex().upper()}")
            # print(f"Calculated: {hmac_calculated.hex().upper()}")

    return error_code
