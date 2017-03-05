from PIL import Image
import sys
import os

#Version 1.0
# Authors: Pau Pena & Brian Martinez

def encode():
	nombre = str(sys.argv[4])
	tmp = "0"

	for i in range(len(nombre)):
	  
	  tmp2 = (int(bin(ord(nombre[i]))[2:]))
	  tmp2 = str(tmp2)
	  if len(tmp2) == 6: 
	    tmp = tmp + "0"
	  tmp = tmp + tmp2
	  if i == len(nombre)-1:
	    tmp = tmp + "1"
	  else:
	    tmp = tmp + "0"
	    tmp = tmp + "0"
	#converts an image into a RGBA list of pixels ex: (255,255, 255, 255)
	image = Image.open(sys.argv[2])
	if image.mode == "RGB":
		rgba = 0
	else:
		rgba = 1
	width, height = image.size
	pixels = list(image.getdata())
	f = open('pixels.txt', 'w+')
	f.write(str(pixels))
	f.close()
	f = open('pixels.txt', 'r')
	f.seek(3)
	pix = ""
	resultado = "["
	cont_letra=0 # para avanzar en el mensaje oculto
	list_res = []
	while cont_letra < int(len(tmp)): #
		cont2 = 0# hacemos grupos de 9 componentes = 3 pixels
		while cont2 < 3: # pack de 3 pixeles
			cont = 0 # para movernos en las 3 componentes de 1 pixel
			pix = ""
			components=0
			while cont < 3: #dentro de un pixel
				v1 = f.read(1)
				if v1 == "," or v1 == ")":
					f.seek(-2,1)
					pix = pix + f.read(1)
				else:
					v2 = f.read(1)
					if v2 == "," or v2 == ")":
						f.seek(-3,1)
						pix = pix + f.read(2)
					else:
						v3 = f.read(1)
						if v3 == "," or v3 == ")":
							f.seek(-4,1)
							pix = pix + f.read(3)
				cont = cont +1
				pix2 = bin(int(pix))[2:].zfill(8) #valor de la componente del pixel en binario
				if pix2[7:] == str(0): #el ultimo digito es un 0?
					valor = int(pix) | int(tmp[cont_letra]) # hacemos la or bit a bit con 0000000X donde X = [0,1]
				else:
					if int(tmp[cont_letra]) == 0: # queremos meter un 0?
						valor = int(pix) & int(254) # and bit a bit entre el valor del pixel y 254
					else:
						valor = int(pix) & int(255) # and bit a bit entre el valor del pixel y 255
				if rgba == 0:
					if components == 0:
						resultado = resultado + "(" + str(valor) + ", "
						components = components + 1
					elif components == 1:
						resultado = resultado + str(valor) + ", "
						components = components + 1
					elif components == 2:
						if cont_letra + 1 == int(len(tmp)):
							resultado = resultado + str(valor) + ")"
						else:
							resultado = resultado + str(valor) + "), "
						components = components + 1
					elif components == 3:
						components = 1
				else:
					print str(components)
					if components == 0:
						resultado = resultado + "(" + str(valor) + ", "
						components = components + 1
					elif components == 1:
						resultado = resultado + str(valor) + ", "
						components = components + 1
					elif components == 2:
						resultado = resultado + str(valor) + ", "
						components = components + 1
					if components == 3:
						if cont_letra + 1 == int(len(tmp)):
							resultado = resultado + "0)"
						else:
							resultado = resultado + "0), "
						components = 0

				cont_letra = cont_letra + 1 # avanzamos una posicion del mensaje
				pix = ""
				f.seek(3,1)
			if(rgba == 0):
				f.seek(2,1)
			else:
				f.seek(5,1)
			cont2 = cont2 + 1
	f.seek(-4,1)
	res = resultado + f.read()
	f.close()
	g = open("final.txt", "w")
	g.write(res)
	g.close()
	string = ""
	with open("final.txt","r") as f:
		f.seek(1,0)
		while True:
			var = f.read(1)
			if not var:
				break
			else:
				if var != ")":
					string = string + var
				else:
					string = string + ")"
					f.seek(2,1)
					list_res.append(eval(string))
					string = ""
	list_res = tuple(list_res)
	im2 = Image.new(image.mode, image.size)
	im2.putdata(list_res)
	im2.save(sys.argv[3])
	os.system("rm final.txt pixels.txt")

def decode_imdata(imdata):
    imdata = iter(imdata)
    while True:
        pixels = list(imdata.next()[:3] + imdata.next()[:3] + imdata.next()[:3])
        byte = 0
        for c in xrange(7):
            byte |= pixels[c] & 1
            byte <<= 1
        byte |= pixels[7] & 1
        yield chr(byte)
        if pixels[-1] & 1:
            break
def decode():
	image = Image.open(sys.argv[2],"r")
	print ''.join(decode_imdata(image.getdata()))


#control de parametros de entrada
if len(sys.argv) >= 2:
	if sys.argv[1] == "--h":
		if len(sys.argv) == 2:
			print "Usage: Para codificar un mensaje: esteganografia.py --encode [imagen original] [nombre de la nueva imagen] [mensaje]"
			print "		Ejemplo: python esteganografia.py --encode imagen_original.png imagen_modificada.png 'Hola mundo'" + '\n'
			print "Usage: Para decodificar un mensaje: esteganografia.py --decode [imagen modificada]"
			print "		Ejemplo: python esteganografia.py --decode imagen_modificada.png"
		else:
			print "La entrada no es correcta. Usa la opcion --h para ver las opciones."
	elif sys.argv[1] == "--encode":
		if len(sys.argv) != 5:
			print "La entrada no es correcta. Usa la opcion --h para ver las opciones."
		else:
			encode()
			print "Enhorabuena, se ha creado la imagen " + str(sys.argv[3]) + " con tu mensaje oculto."
	elif sys.argv[1] == "--decode":
		if len(sys.argv) != 3:
			print "La entrada no es correcta. Usa la opcion --h para ver las opciones."
		else: 
			decode()
	else:
		print "La entrada no es correcta. Usa la opcion --h para ver las opciones."
else:
	print "La entrada no es correcta. Usa la opcion --h para ver las opciones."
