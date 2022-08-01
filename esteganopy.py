"""
esteganopy.py - 2022/07/28

Resume: script que sobreescribe bits de una imagen en cada componente de color de segunda imagen,
        tecnica LSB sobre RGB,se genera tercer imagen final ocultando la segunda

Author: morinigo rodrigo (ing.remz@gmail.com)

"""
import os
import argparse
from PIL import Image

class Hiddenimg:

    ZERO = (0, 0, 0)

    def _match_color(self, color1, color2):
        #Une 2 componentes *rojo,verde,azul de imagenes
        #retorna entero de ambas imagenes rojo,verde,azul
        r1, v1, a1 = self._int_to_bin(color1)
        r2, v2, a2 = self._int_to_bin(color2)
        color = r1[:4] + r2[:4], v1[:4] + v2[:4], a1[:4] + a2[:4]
        return self._bin_to_int(color)

    def  _unmatch_color(self, color):
        #desune componentes rojo,verde,azul de imagen
        r, v, a = self._int_to_bin(color)
        # resta 4 bits (imagen no oculta)
        # se agrega 4bits hasta 8 bit
        new_color = r[4:] + '0000', v[4:] + '0000', a[4:] + '0000'
        return self._bin_to_int(new_color)

    def paste(self, imagen1, imagen2):
        #retorna imagen fusionadas o pegada.

        # chequear dimensiones[a:b]
        if imagen2.size[0] > imagen1.size[0] or imagen2.size[1] > imagen1.size[1]:
            raise ValueError('Segunda Imagen mas chica que Primer Imagen!!')

        # pixeles de imagen fusionada
        m1 = imagen1.load()
        m2 = imagen2.load()

        new_img = Image.new(imagen1.mode, imagen1.size)
        new_m = new_img.load()

        for i in range(imagen1.size[0]):
            for j in range(imagen1.size[1]):
                is_valid = lambda: i < imagen2.size[0] and j < imagen2.size[1]
                color1 = m1[i ,j]
                color2 = m2[i, j] if is_valid() else self.ZERO
                new_m[i, j] = self._match_color(color1, color2)

        return new_img

    def unpaste(self, imagen):
        #despega imagenes.
        #retorna imagen oculta de la primera.
        pixel_m = imagen.load()

        # Crear tercer imagen y mapa pixeles
        new_img = Image.new(imagen.mode, imagen.size)
        new_m = new_img.load()

        for i in range(imagen.size[0]):
            for j in range(imagen.size[1]):
                new_m[i, j] = self._unmatch_color(pixel_m[i, j])

        return new_img
    
    #Convierte entero a binario 3bits 
    def _int_to_bin(self, color):
        r, v,a= color
        return f'{r:08b}', f'{v:08b}', f'{a:08b}'

    #Convierte binario 3bits a entero
    def _bin_to_int(self, color):
        r, v, a = color
        return int(r, 2), int(v, 2), int(a, 2)


def main():
    parser = argparse.ArgumentParser(description='Ocultar Imagen')
    subparser = parser.add_subparsers(dest='command')

    merge = subparser.add_parser('unir')
    merge.add_argument('--imagen1', required=True, help='Imagen1')
    merge.add_argument('--imagen2', required=True, help='Imagen2')
    merge.add_argument('--output', required=True, help='Output')

    unmerge = subparser.add_parser('desunir')
    unmerge.add_argument('--imagen', required=True, help='Imagen')
    unmerge.add_argument('--output', required=True, help='Output')

    args = parser.parse_args()

    if args.command == 'unir':
        image1 = Image.open(args.imagen1)
        image2 = Image.open(args.imagen2)
        Hiddenimg().paste(image1, image2).save(args.output)
    elif args.command == 'desunir':
        image = Image.open(args.imagen)
        Hiddenimg().unpaste(image).save(args.output)



if __name__ == '__main__':
    main()

