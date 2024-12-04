def text_to_binary(text):#This defines a function that is named text_to_binary that takes an input parameter text which is supposed to be a string
    return ''.join(format(ord(char), '08b') for char in text)
# you need to convert each character to its ASCII code, then to a 8-bit binary string and after you join them together

def binary_to_text(binary):#onvert a binary string back to text
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]# Split the binary data in to pieces of 8 bits representing the characters
    return ''.join(chr(int(char, 2)) for char in chars)#Convert each binary piece to an integer and then convert it to its corresponding character

def encode_message(image_path, message, output_image_path):# create a function to put the message in the image and hide a message in the image
    with open(image_path, 'rb') as img:#Open the image file in binary read mode
        data = bytearray(img.read())#Read the image data into a bytearray for modification.
    
    binary_message = text_to_binary(message) + '1111111111111110'   # Convert the message to binary and append a special end delimiter ('1111111111111110').
    
   
    if len(binary_message) > len(data):# Check if the binary message is larger than the image data
        raise ValueError("The image does not have enough space to hide the message.")# Raise an error if the image does not have enough space to store the entire binary message

    
    
    for i in range(len(binary_message)):#this code loops in between each index of the binary message string; from zero to its length - 1, to process each character 
        data[i] = (data[i] & 0b11111110) | int(binary_message[i])#Replaces the least significant bit of the current byte in the image data with the corresponding bit from the binary message, keeping all other bits in the byte intact.
    
   
    with open(output_image_path, 'wb') as output_img:#This opens the file where the modified image will be saved. The 'wb' mode ensures we’re writing in binary format, which is necessary for images.
        output_img.write(data)#Here, changed binary data with the hidden message is written to a new image file. In other words, this step saves the modified image as an output file with the hidden information.
 
def decode_message(image_path):#takes out the hidden message from the image 
    with open(image_path, 'rb') as img:#It opens an image file in read mode. In other words, it reads the contents of a file as raw bytes, not text; that's how it keeps all the data.
        data = bytearray(img.read())#it reads the entire contents of the image file as a mutable bytearray, so it does allow modifications to be made to the binary data.
    
    binary_message = ''#Builds a string to contain a binary message that is extracted from the image.
    for byte in data:#loop through every byte of the data.
        binary_message += str(byte & 1)#pulls the least significant bit from every byte.
        if binary_message.endswith('1111111111111110'):# It checks whether the delimiter finishes off the binary message.
            break
    
    # Check if no hidden message was found
    if not binary_message.endswith('1111111111111110'):
        raise ValueError("No hidden message found in the image.")
    
    # Return the binary message without the end delimiter
    return binary_to_text(binary_message[:-16])

def main():
    # Main function It handles user interaction
    choice = input("Enter 1 to encode a message, 2 to decode a message: ")#choose between encoding or decoding a message
    if choice == '1':#if user enters 1 means he wants to encode
       
        image_path = input("Enter the path of the image: ")#asks user the put the path of the image 
        output_image_path = input("Enter the path for the output image: ")#asks user to enter the path of the output image 
        message = input("Enter the message to hide: ")#tells user to enter the message he wants to hide
        try:
            encode_message(image_path, message, output_image_path)#call the function to hide the message within the image
            print("message saved and encoded to", output_image_path)#print to the user that message is saved and encoded 
        except Exception as e:
            print("Error:", e)
    elif choice == '2': #means user wants to decode
       
        image_path = input("Enter the path of the image to decode: ")#tells the user to enter the path of the image he wants to decode 
        try:
            message = decode_message(image_path)#Call the function to extract a hidden message from the image file.
            print("Decoded message:", message)
        except Exception as e:
            print("Error:", e)
    else:
        # if user enter anything besides 1 or 2 then it will print invalid choice
        print("Invalid choice.")

# makes sure the script runs the main function when executed directly
if __name__ == "__main__":
    main()
