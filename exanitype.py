from PIL import Image
import os

os.system('cls' if os.name == 'nt' else 'clear')
cont = False
answer = None

#Options Menu/Input stuffs.
while(cont == False):
	try:
		print("Input number for option: ")
		print("0.) Quit")
		print("1.) Title Font")
		print("2.) Large Text")
		#print("3.) Small Text")
		answer = input("Selection: ")
	except KeyboardInterrupt:
		print("Quitting...")
		quit()
	if(answer == "0"):
		print("Quitting...")
		quit()
	elif(answer != "1" and answer != "2"):
		os.system('cls' if os.name == 'nt' else 'clear')
		print("Invalid Input!")
	else:
		cont = True

character_layout, image_path, crop_x, crop_y, space_size, vertical_buffer = None, None, None, None, None, None

#While I considered making config files of sorts for fonts, hardcoding is fine for my purposes.
match answer:
	case "0": #failsafe ig.
		print("Quitting...")
		quit()
	case "1":
		image_path = './fonts/title_font.png'
		characterLayout = [
			["A", "B", "C", "D"],
			["E", "F", "G", "H"],
			["I", "J", "K", "L"],
			["M", "N", "O", "P"],
			["Q", "R", "S", "T"],
			["U", "V", "W", "X"],
			["Y", "Z", " ", "" ]
		]
		crop_x = 128
		crop_y = 128
		space_size = 32
		letter_spacing = 0
		vertical_buffer = 2
		line_spacing = 0
	case "2":
		image_path = './fonts/big_text.png'
		characterLayout = [
			["ð", "ñ", "ò", "ó", "õ", "õ", "ö", "÷", "ø", "ù", "ú", "û", "ü", "ý", "þ", "ÿ" ],
			["à", "á", "â", "ã", "ä", "å", "æ", "ç", "è", "é", "ê", "ë", "ì", "í", "î", "ï" ],
			["Ð", "Ñ", "Ò", "Ó", "Ô", "Õ", "Ö", "×", "Ø", "Ù", "Ú", "Û", "Ü", "Ý", "Þ", "ß" ],
			["À", "Á", "Â", "Ã", "Ä", "Å", "Æ", "Ç", "È", "É", "Ê", "Ë", "Ì", "Í", "Î", "Ï" ],
			["°", "±", "²", "³", "´", "µ", "¶", "·", "¸", "¹", "º", "»", "¼", "½", "¾", "¿" ],
			[" ", "¡", "¢", "£", "¤", "¥", "¦", "§", "̈",  "©", "ᵃ", "«", "¬", "–", "®", "̄"  ],
			["|", "`", "´", "“", "”", "•", "–", "—", "‾", "™", "š", ">", "œ", "□", " ", "Ÿ" ],
			["€", "□", "‚", "ƒ", "„", "…", "†", "‡", "^", "‰", "Š", "<", "Œ", "□", "Ž", "□" ],
			["p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "□" ],
			["`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o" ],
			["P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_"],
			["@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O" ],
			["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?" ],
			[" ", "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/"],
			["̿"]
		]
		crop_x = 16
		crop_y = 32
		space_size = 4
		letter_spacing = 0
		vertical_buffer = 0
		line_spacing = 2

image = Image.open(image_path).convert('RGBA')

image_list = []

print("################################")
print("# TYPE! Input nothing to quit! #")
print("################################")
while True:
	try:
		user_input = input("")
	except KeyboardInterrupt:
		print("Quitting...")
		quit()
	if user_input == "":
		print('\033[F', end='', flush=True)
		print("################################")
		break
	#We need to pre-make the image with the appropriate width. If there is extra it doesn't matter because we crop it anyway.
	result_image = Image.new('RGBA', (len(user_input) * crop_x + user_input.count(" ") * crop_x, crop_y))

	x_position = 0
	#Iterate through the input, cropping source image for character via referencing character_layout, concatinate them together.
	for char in user_input:
		found = False
		if char == " ":
			x_position += space_size
		else:
			for y, row in enumerate(characterLayout):
				if char in row:
					x = row.index(char)
					segment = image.crop((x * crop_x, y * crop_y, x * crop_x + crop_x, y * crop_y + crop_y))

					bbox = segment.getbbox()
					if bbox is not None:
						left, upper, right, lower = bbox
						#width = right - left  #Calculate the width of the bounding box
						right = right + letter_spacing
						segment = segment.crop((left, 0, right, crop_y))
						result_image.paste(segment, (x_position, 0))
						x_position += segment.width
					found = True
					break

			if not found:
				print(f"Character '{char}' not found in characterLayout.")
				
	#vertical_buffer exists just for title_font, as J overlaps below.
	if vertical_buffer != 0:
		left, upper, right, lower = result_image.getbbox()
		upper+=vertical_buffer
		result_image = result_image.crop((left, upper, right, lower))
		
	left, upper, right, lower = result_image.getbbox()
	result_image = result_image.crop((left, upper, right, lower))
	
	#Add to the list.
	image_list.append(result_image)
if not image_list:
	print("Quitting...")
	quit()
#Get the total height of all the images combined, and the widest image.
total_height = sum(img.size[1] + line_spacing for img in image_list) - line_spacing
max_width = max(img.size[0] for img in image_list)

#Create a new image of this size.
result_image = Image.new('RGBA', (max_width, total_height), (255, 255, 255, 0))

#Append all the images together.
current_height = 0
for img in image_list:
	#This would center the text.
	#result_image.paste(img, ((max_width - img.size[0]) // 2, current_height))
	result_image.paste(img, (0, current_height))
	current_height += img.size[1] + line_spacing

#Save ^-^
try:
	result_image.save((input("Save as: ") or "exanitype") + ".png")
except KeyboardInterrupt:
	print("Save Image Aborted!")
	quit()
	
	
#This is for turning a character_layout into a string, for testing.
'''
		with open("test_characters.txt", "w", encoding="utf-8") as file:
			for row in characterLayout:
				for char in row:
					file.write(char)
'''