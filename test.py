import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import xml.etree.ElementTree as ET

class ESFMDecryptor:
    def __init__(self):
        # Trophy key from dev wiki
        self.trophy_key = bytes([
            0x21, 0xF4, 0x1A, 0x6B, 0xAD, 0x8A, 0x1D, 0x3E, 
            0xCA, 0x7A, 0xD5, 0x86, 0xC1, 0x01, 0xB7, 0xA9
        ])
    
    def generate_data_key(self, np_communication_id):
        """
        Generate the data encryption key by encrypting NP communication ID
        with the trophy key using AES-CBC-128.
        
        Args:
            np_communication_id (str): NP communication ID string
            
        Returns:
            bytes: Generated data encryption key (16 bytes)
        """
        # Pad the NP communication ID with zeros to 16 bytes
        np_id_bytes = np_communication_id.encode('utf-8')
        padded_np_id = np_id_bytes.ljust(16, b'\x00')[:16]
        
        # Encrypt with trophy key using AES-ECB (since IV is zeros for key generation)
        cipher = AES.new(self.trophy_key, AES.MODE_CBC, bytes.fromhex("00000000000000000000000000000000"))
        data_key = cipher.encrypt(padded_np_id)
        
        return data_key
    
    def decrypt_esfm(self, esfm_data, np_communication_id):
        """
        Decrypt ESFM data.
        
        Args:
            esfm_data (bytes): Raw ESFM file data
            np_communication_id (str): NP communication ID
            
        Returns:
            str: Decrypted XML content
        """
        # Extract IV (first 16 bytes)
        iv = esfm_data[:16]
        encrypted_data = esfm_data[16:]
        
        # Generate the data key
        data_key = self.generate_data_key(np_communication_id)
        
        # Decrypt the data using AES-CBC
        cipher = AES.new(data_key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(encrypted_data)
        
        # Remove padding
        unpadded_data = unpad(decrypted_data, AES.block_size)
        
        return unpadded_data.decode('utf-8')
    
    def decrypt_esfm_file(self, input_file, output_file, np_communication_id):
        """
        Decrypt an ESFM file and save the decrypted XML.
        
        Args:
            input_file (str): Path to input ESFM file
            output_file (str): Path to output XML file
            np_communication_id (str): NP communication ID
        """
        # Read the ESFM file
        with open(input_file, 'rb') as f:
            esfm_data = f.read()
        
        # Decrypt the data
        decrypted_xml = self.decrypt_esfm(esfm_data, np_communication_id)
        
        # Save the decrypted XML
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(decrypted_xml)
        
        print(f"Successfully decrypted {input_file} to {output_file}")
        
        # Try to parse the XML to verify it's valid
        try:
            ET.fromstring(decrypted_xml)
            print("XML validation: OK")
        except ET.ParseError as e:
            print(f"XML validation warning: {e}")
        
        return decrypted_xml

# Example usage
def main():
    decryptor = ESFMDecryptor()
    
    # Example NP communication ID (replace with actual ID)
    np_communication_id = "NPWR32931_00"  # Example format
    
    # Example file paths (replace with actual paths)
    input_esfm_file = "NPWR32931_00/TROP.ESFM"
    output_xml_file = "out.esfm.xml"
    
    try:
        # Decrypt the file
        decrypted_xml = decryptor.decrypt_esfm_file(
            input_esfm_file, 
            output_xml_file, 
            np_communication_id
        )
        
        # Print first few lines of decrypted XML
        print("\nFirst 200 characters of decrypted XML:")
        print(decrypted_xml[:200] + "..." if len(decrypted_xml) > 200 else decrypted_xml)
        
    except FileNotFoundError:
        print(f"Error: File {input_esfm_file} not found.")
    except Exception as e:
        print(f"Error during decryption: {e}")

# Utility function to detect NP communication ID from common patterns
def find_np_communication_id(possible_ids, esfm_file_path):
    """
    Try to decrypt with multiple possible NP communication IDs.
    
    Args:
        possible_ids (list): List of possible NP communication IDs to try
        esfm_file_path (str): Path to ESFM file
        
    Returns:
        str: Successful NP communication ID, or None if none worked
    """
    decryptor = ESFMDecryptor()
    
    with open(esfm_file_path, 'rb') as f:
        esfm_data = f.read()
    
    for np_id in possible_ids:
        try:
            decrypted = decryptor.decrypt_esfm(esfm_data, np_id)
            # Try to parse as XML to verify it's valid
            ET.fromstring(decrypted)
            print(f"Success with NP ID: {np_id}")
            return np_id
        except:
            continue
    
    print("No valid NP communication ID found from the provided list.")
    return None

if __name__ == "__main__":
    main()