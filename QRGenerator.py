import reed_solomon as rs
import version_check as vc
import QRdrawer as qd
from PIL import Image

ECL = input("ERROR = ")
input_text = input("INPUT = ")
ver,size = vc.version_check(input_text,ECL)
msg = rs.final_codewords(input_text,ECL)
g = open("binary_file.out","w")

poza = qd.return_mat(ver,msg,ECL)

for linie in poza:
    for c in linie:
        g.write(str(c)+" ")
    g.write("\n")

# DE AICI ESTE DOAR AFISAREA MATRICEI IN POZA
color_map = {
    0: (255, 255, 255),  # White
    1: (0, 0, 0),  # Black
    8: (128, 128, 128)  # Gray
}
image = Image.new("RGB", (len(poza), len(poza)))
pixels = image.load()
for i in range(len(poza)):
    for j in range(len(poza)):
        pixels[j, i] = color_map[poza[i][j]]
scaling_factor = 10
new_size = (len(poza) * scaling_factor, len(poza) * scaling_factor)
upscaled_image = image.resize(new_size, Image.NEAREST)
upscaled_image.save("test.png")
upscaled_image.show()
