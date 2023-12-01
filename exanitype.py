from PIL import Image, ImageFont, ImageDraw
import select
import sys
import os

os.system('cls' if os.name == 'nt' else 'clear')

programMode	= 0	#Changes the state of the program to different menus/modes.

class textData:		#Stores data about an imageFont.
	def __init__(self):
		self.character_layout	= None
		self.image_path			= None
		self.crop_x				= None
		self.crop_y				= None
		self.space_size			= None
		self.force_crop_top		= None
		self.force_crop_width	= None
		self.flip_vertical		= None
		self.center_letters		= None

def mainMenu():
	global programMode
	cont = False	#Used to exit the menu loop.
	answer = None	#Tracks the menu option.
	#Options Menu/Input stuffs.
	while(cont == False):
		try:
			title = "MAIN MENU" if programMode == 0 else "FONT TO IMAGEFONT MENU"
			zeroOption = "Quit" if programMode == 0 else "Back"
			print(title)
			print("Input number for option: ")
			print("0.) "+zeroOption)
			print("1.) Title Font" )
			print("2.) fontbase24r (May take a hot minute on slow PCs)")
			print("3.) Small Text" )
			print("4.) Medium Text")
			#print("5.) Large Text")
			if programMode == 0:
				print("5.) Font to ImageFont")
			answer = input("Selection: ")
		except KeyboardInterrupt:
			print("Quitting...")
			quit()
		if(answer == "0"):
			if programMode == 0:
				print("Quitting...")
				quit()
			else:
				os.system('cls' if os.name == 'nt' else 'clear')
				programMode = 0
		elif(answer == "5" and programMode == 0):
			os.system('cls' if os.name == 'nt' else 'clear')
			programMode = 1
		elif(answer == "1" or answer == "2" or answer == "3" or answer == "4"):	#This is terrible.
			cont = True	
			if programMode == 0:
				textToFont(answerReply(answer))
			else:
				fontToImage(answer) 
		else:
			os.system('cls' if os.name == 'nt' else 'clear')
			print("Invalid Input!")

def answerReply(answer):
	os.system('cls' if os.name == 'nt' else 'clear')
	atd = textData()	#Active Text Data.
	#While I considered making config files of sorts for fonts, hardcoding is fine for my purposes.
	match answer:
		case "0": #failsafe ig.
			print("Quitting...")
			quit()
		case "1":
			atd.image_path = './fonts/titlefont.png' 	#This is the image path, obviously.
			atd.character_layout = [					#Match this to the image. Blank spots can just be empty "" or " ".
				["A", "B", "C", "D"],
				["E", "F", "G", "H"],
				["I", "J", "K", "L"],
				["M", "N", "O", "P"],
				["Q", "R", "S", "T"],
				["U", "V", "W", "X"],
				["Y", "Z", " ", "" ]
			]
			atd.crop_x = 128							#The width of each character's section. Image-fonts are grids after all.
			atd.crop_y = 128							#The height of what's described on the line above.
			atd.space_size = 32							#This is how many pixels to jump if a space is input.
			atd.letter_spacing = 0						#Add pixels to the end of characters.
			atd.line_spacing = 0						#When typing multiline, how many pixels of space betwix them.
			atd.force_crop_width = 0					#Shifts the right edge of a character's space. (small_font has trailing pixel overlap(s), and thus this). 
			atd.force_crop_top = 2						#Same as above, but the top edge of the space. (J in title_font dips into the character below, so this.).
			atd.flip_vertical = True					#Flips the image vertically before doing anything else. Exanima files are naturally upside down.
			atd.snick = False							#Because fontbase24r is an encoded rfi, it came out with black background. This fixes it, perfectly. (Basically if you have a grayscale font with a black background, use this.)
			atd.center_letters = True					#titlefont letters are actually centered in their "cells", so this is a fix for that when using FontToImageFont.
		case "2":
			atd.image_path = './fonts/fontbase24r.png'
			atd.character_layout = [
				["ð", "ñ", "ò", "ó", "õ", "õ", "ö", "÷", "ø", "ù", "ú", "û", "ü", "ý", "þ", "ÿ" ],
				["à", "á", "â", "ã", "ä", "å", "æ", "ç", "è", "é", "ê", "ë", "ì", "í", "î", "ï" ],
				["Ð", "Ñ", "Ò", "Ó", "Ô", "Õ", "Ö", "×", "Ø", "Ù", "Ú", "Û", "Ü", "Ý", "Þ", "ß" ],
				["À", "Á", "Â", "Ã", "Ä", "Å", "Æ", "Ç", "È", "É", "Ê", "Ë", "Ì", "Í", "Î", "Ï" ],
				["°", "±", "²", "³", "´", "µ", "¶", "·", "̧",  "¹", "º", "»", "¼", "½", "¾", "¿" ], #This has a Combining Cedilla, not a blank space.
				["ﬂ", "¡", "¢", "£", "¤", "¥", "¦", "§", "̈",  "©", "ᵃ", "«", "¬", "–", "®", "̄"	], #Two dots diacritic, Combining Macron
				["|", "`", "´", "“", "”", "•", "–", "—", "‾", "™", "š", ">", "œ", " ", "□", "Ÿ" ],
				["□", " ", "‚", "ƒ", "„", "…", "†", "‡", "^", "‰", "Š", "<", "Œ", " ", "□", " " ],
				["p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "Ž" ],
				["`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o" ],
				["P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_"],
				["@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O" ],
				["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?" ],
				[" ", "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/"]
			]
			atd.crop_x = 64
			atd.crop_y = 64
			atd.space_size = 12
			atd.letter_spacing = 1
			atd.line_spacing = 2
			atd.force_crop_width = 0
			atd.force_crop_top = 0
			atd.flip_vertical = True
			atd.snick = True
			atd.center_letters = False
		case "3":
			atd.image_path = './fonts/smallfont.png'
			atd.character_layout = [
				["ð", "ñ", "ò", "ó", "õ", "õ", "ö", "÷", "ø", "ù", "ú", "û", "ü", "ý", "þ", "ÿ" ],
				["à", "á", "â", "ã", "ä", "å", "æ", "ç", "è", "é", "ê", "ë", "ì", "í", "î", "ï" ],
				["Ð", "Ñ", "Ò", "Ó", "Ô", "Õ", "Ö", "×", "Ø", "Ù", "Ú", "Û", "Ü", "Ý", "Þ", "ß" ],
				["À", "Á", "Â", "Ã", "Ä", "Å", "Æ", "Ç", "È", "É", "Ê", "Ë", "Ì", "Í", "Î", "Ï" ],
				["°", "±", "²", "³", "´", "µ", "¶", "·", "¸", "¹", "º", "»", "¼", "½", "¾", "¿" ],
				[" ", "¡", "¢", "£", "¤", "¥", "¦", "§", "̈", "©", "ᵃ", "«", "¬", "–", "®", "̄" 	], #Two dots diacritic, Combining Macron
				["|", "`", "´", "“", "”", "•", "–", "—", "‾", "™", "š", ">", "œ", "□", " ", "Ÿ" ],
				["€", "□", "‚", "ƒ", "„", "…", "†", "‡", "^", "‰", "Š", "<", "Œ", "□", "Ž", "□" ],
				["p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "□" ],
				["`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o" ],
				["P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_"],
				["@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O" ],
				["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?" ],
				[" ", "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/"],
				["╋", "⯇", "⬍",  "‼", "¶", "┻", "┳", "┫", "⬆", "┣", "⭢", "⭠", "" , "" , "" , ""	],
				["" , "" , "┓",  "┗", "┛", "┃", "━", "•", "◘", "" , "" , "♂", "▭", "" , "♫", "𝖃"] #This last one is a educated guess.
			]
			atd.crop_x = 16
			atd.crop_y = 32
			atd.space_size = 3
			atd.letter_spacing = 0
			atd.line_spacing = 2
			atd.force_crop_width = -2
			atd.force_crop_top = 0
			atd.flip_vertical = True
			atd.snick = False
			atd.center_letters = False
		case "4":
			atd.image_path = './fonts/mediumfont.png'
			atd.character_layout = [
				["ð", "ñ", "ò", "ó", "õ", "õ", "ö", "÷", "ø", "ù", "ú", "û", "ü", "ý", "þ", "ÿ" ],
				["à", "á", "â", "ã", "ä", "å", "æ", "ç", "è", "é", "ê", "ë", "ì", "í", "î", "ï" ],
				["Ð", "Ñ", "Ò", "Ó", "Ô", "Õ", "Ö", "×", "Ø", "Ù", "Ú", "Û", "Ü", "Ý", "Þ", "ß" ],
				["À", "Á", "Â", "Ã", "Ä", "Å", "Æ", "Ç", "È", "É", "Ê", "Ë", "Ì", "Í", "Î", "Ï" ],
				["°", "±", "²", "³", "´", "µ", "¶", "·", "¸", "¹", "º", "»", "¼", "½", "¾", "¿" ],
				[" ", "¡", "¢", "£", "¤", "¥", "¦", "§", "̈",  "©", "ᵃ", "«", "¬", "–", "®", "̄"	], #Two dots diacritic, Combining Macron
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
			atd.crop_x = 16
			atd.crop_y = 32
			atd.space_size = 4
			atd.letter_spacing = 0
			atd.line_spacing = 2
			atd.force_crop_width = 0
			atd.force_crop_top = 0
			atd.flip_vertical = True
			atd.snick = False
			atd.center_letters = False
		case _:
			print("Error: Invalid Answer! (" + answer + ")")
			print("Returning to menu...")
			mainMenu()
	return atd

def textToFont(textData):
	atd = textData #Active text data.

	image = Image.open(atd.image_path).convert('RGBA')
	if atd.snick:
		image = snick(image)
	if atd.flip_vertical:
		image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
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
			if image_list == []:
				os.system('cls' if os.name == 'nt' else 'clear')
				print("Returning to menu...")
				mainMenu()
			break
		#We need to pre-make the image with the appropriate width. If there is extra it doesn't matter because we crop it anyway.
		result_image = Image.new('RGBA', (len(user_input) * atd.crop_x + user_input.count(" ") * atd.crop_x, atd.crop_y))

		x_position = 0
		#Iterate through the input, cropping source image for character via referencing character_layout, concatinate them together.
		for char in user_input:
			found = False
			if char == " ":
				x_position += atd.space_size
			else:
				for y, row in enumerate(atd.character_layout):
					if char in row:
						x = row.index(char)
						segment = image.crop((x * atd.crop_x, y * atd.crop_y + atd.force_crop_top, x * atd.crop_x + atd.crop_x + atd.force_crop_width, y * atd.crop_y + atd.crop_y))

						bbox = segment.getbbox()
						if bbox is not None:
							left, upper, right, lower = bbox
							#width = right - left  #Calculate the width of the bounding box
							right = right + atd.letter_spacing
							segment = segment.crop((left, 0, right, atd.crop_y))
							result_image.paste(segment, (x_position, 0))
							x_position += segment.width
						found = True
						break

				if not found:
					print(f"Character '{char}' not found in atd.character_layout.")
					
		left, upper, right, lower = result_image.getbbox()
		result_image = result_image.crop((left, upper, right, lower))
		
		#Add to the list.
		image_list.append(result_image)
	
	if not image_list:
		os.system('cls' if os.name == 'nt' else 'clear')
		print("Returning to menu...")
		mainMenu()
	
	#Get the total height of all the images combined, and the widest image.
	total_height = sum(img.size[1] + atd.line_spacing for img in image_list) - atd.line_spacing
	max_width = max(img.size[0] for img in image_list)

	#Create a new image of this size.
	result_image = Image.new('RGBA', (max_width, total_height), (255, 255, 255, 0))

	#Append all the images together.
	current_height = 0
	for img in image_list:
		#This would center the text.
		#result_image.paste(img, ((max_width - img.size[0]) // 2, current_height))
		result_image.paste(img, (0, current_height))
		current_height += img.size[1] + atd.line_spacing

	#Save ^-^
	trySaveImage(result_image)
	
def trySaveImage(result_image):
	try:
		print("Input file name or blank to cancel")
		should_flip = input("Flip Image Upside-Down? (Y/N): ")
		if "Y" in should_flip:
			print("Flipped!")
			result_image = result_image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
		else:
			print("Not Flipping? Fine.")
		filename = input("Save as: ")
		if filename == "":
			os.system('cls' if os.name == 'nt' else 'clear')
			print("Save Aborted: Returning to menu...")
			mainMenu()
		else:
			result_image.save(filename + ".png")
		should_restart = input("Return to main menu? (Y/N): ")
		if "Y" in should_restart:
			os.system('cls' if os.name == 'nt' else 'clear')
			mainMenu()
		else:
			print("Quitting...")
			quit()
	except KeyboardInterrupt:
		print("Save Aborted: Quitting...")
		quit()
	
def fontToImage(answer):
	#Get textData.
	atd = answerReply(answer)
	cont = False
	while cont != True:
		try:
			print("TEMPLATE: " + atd.image_path)
			print("Place font files in script folder (Linux/Windows) or have them installed (Windows)")
			print("Enter nothing to cancel.")
			font_file = input("Font File Name & Extension:")
			if font_file == "":
				os.system('cls' if os.name == 'nt' else 'clear')
				print("Returning to menu...")
				mainMenu()
			font_size = input("Font Size (Number):")
			if font_size == "":
				os.system('cls' if os.name == 'nt' else 'clear')
				print("Returning to menu...")
				mainMenu()
			font_size = int(font_size)
			font = ImageFont.truetype(font_file, font_size)
		except OSError:
			os.system('cls' if os.name == 'nt' else 'clear')
			print("Error: " + font_file + " not found!")
		except ValueError:
			os.system('cls' if os.name == 'nt' else 'clear')
			print("Error: Font Size must be an integer.")
		except KeyboardInterrupt:
			os.system('cls' if os.name == 'nt' else 'clear')
			print("Returning to menu...")
			mainMenu()
		else:
			cont = True
		
	#For tracking errors:
	failed_char_list = []
		
	#Generate a new blank image sized to the reference.
	img = Image.open(atd.image_path)
	image_size = img.size
	img.close()
	img = Image.new('RGBA', image_size)
	
	#Prep for writing.
	draw = ImageDraw.Draw(img)
	font = font
	char_size = font_size
	#Iterate through the character_layout and draw text at appropriate spots.
	for y, row in enumerate(atd.character_layout):
		for x, char in enumerate(row):
			if char != "" and char != " ":
				try:
					left, top, right, bottom = font.getbbox(char)
					char_width = right - left
					char_height = bottom - top
					center_x = 0
					center_y = 0
					if atd.center_letters:			
						center_x = (atd.crop_x - char_width) // 2
						center_y = (atd.crop_y - char_height) // 2
					draw.text((x * atd.crop_x + center_x, y * atd.crop_y - center_y + atd.crop_y - bottom), char, fill="black", font=font)
				except UnicodeEncodeError:	#If the character isn't part of the font.
					failed_char_list.append(char)
	if failed_char_list != []:
		print("Unsupported Characters (SKIPPED):")
		failed_row_length = 16
		failed_iterator = 0
		for letter in failed_char_list:
			if failed_iterator >= 16:
				print()
				failed_iterator = 0
			print(letter + " ", end="")
			failed_iterator += 1
	trySaveImage(img)
		
#This is for turning a character_layout into a string, for testing.
'''
		with open("test_characters.txt", "w", encoding="utf-8") as file:
			for row in character_layout:
				for char in row:
					file.write(char)
'''

def snick(img):	#This is a fix for the no-alpha encoded fontbase24r.rfi file extraction.
	try:
		width, height = img.size
		#Info for the long-ish load.
		print("Swift Neutral Image Clarity Korrection | SNICK")
		print("Size:\t" + str(width) + "x" + str(height))
		print("Pixels:\t" + str(width*height))
		print("Please do not enter anything while snicking is in progress.")
		#Calculate transparency based on the RGB Values. This kills the black background too.
		print("Calculating Transparency...")
		for x in range(width):
			for y in range(height):
				r, g, b, _ = img.getpixel((x, y))
				avg = (r + g + b) // 3
				img.putpixel((x, y), (r, g, b, avg)) #I get the average although r==g==b on the image.
		#Since they are now properly transparent, set them all to pure white.
		print("Fixing Foreground...")
		for y in range(height):
			for x in range(width):
				r, g, b, a = img.getpixel((x, y))
				img.putpixel((x, y), (255, 255, 255, a))
		print("SNICKED!")
		os.system('cls' if os.name == 'nt' else 'clear')
		return img
	except KeyboardInterrupt:
		print("Cancelled snick: Returning to main menu...")
		mainMenu()

if __name__ == "__main__":
	mainMenu()
