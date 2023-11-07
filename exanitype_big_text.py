from PIL import Image

image_path = './big_text/big_text_sheet.png'
image = Image.open(image_path).convert('RGBA')

characterLayout = [
    ["ð", "ñ", "ò", "ó", "õ", "õ", "ö", "÷", "ø", "ù", "ú", "û", "ü", "ý", "þ", "ÿ"],
    ["à", "á", "â", "ã", "ä", "å", "æ", "ç", "è", "é", "ê", "ë", "ì", "í", "î", "ï"],
    ["Ð", "Ñ", "Ò", "Ó", "Ô", "Õ", "Ö", "×", "Ø", "Ù", "Ú", "Û", "Ü", "Ý", "Þ", "ß"],
    ["À", "Á", "Â", "Ã", "Ä", "Å", "Æ", "Ç", "È", "É", "Ê", "Ë", "Ì", "Í", "Î", "Ï"],
    ["°", "±", "²", "³", "´", "µ", "¶", "·", "¸", "¹", "º", "»", "¼", "½", "¾", "¿"],
    [" ", "¡", "¢", "£", "¤", "¥", "¦", "§", "̈", "©", "ᵃ", "«", "¬", "–", "®", "̄"],
    ["|", "`", "´", "“", "”", "•", "–", "—", "‾", "™", "š", ">", "œ", "□", " ", "Ÿ"],
    ["€", "□", "‚", "ƒ", "„", "…", "†", "‡", "^", "‰", "Š", "<", "Œ", "□", "Ž", "□"],
    ["p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "□"],
    ["`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o"],
    ["P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_"],
    ["@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"],
    ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?"],
    [" ", "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/"],
    ["̿"]
]

user_input = input("Enter text: ")

result_image = Image.new('RGBA', (len(user_input) * 16 + user_input.count(" ") * 16, 32))

x_position = 0
for char in user_input:
    found = False
    if char == " ":
        x_position += 4
    else:
        for y, row in enumerate(characterLayout):
            if char in row:
                x = row.index(char)
                segment = image.crop((x * 16, y * 32, x * 16 + 16, y * 32 + 32))

                bbox = segment.getbbox()
                if bbox is not None:
                    left, upper, right, lower = bbox
                    segment = segment.crop((left, 0, right, 32))

                    result_image.paste(segment, (x_position, 0))
                    x_position += segment.width
                found = True
                break

        if not found:
            print(f"Character '{char}' not found in characterLayout.")

left, upper, right, lower = result_image.getbbox()
result_image = result_image.crop((left, upper, right, lower))

result_image.save('exanitype_big_text.png')
