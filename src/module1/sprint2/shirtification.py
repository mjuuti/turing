from fpdf import FPDF

def main():
    # Instantiation of inherited class

    name = input('Name for the t-shirt: ')

    pdf = FPDF(format='a4', orientation='portrait')
    pdf.add_page()
    pdf.set_font("Times", size=42, style='b')
    pdf.cell(text='CS50 Shirtificate', center=True, new_x="LMARGIN", new_y="NEXT")

    usable_width = 200 - pdf.l_margin

    pdf.image(name="shirtificate.png", y=50, x=pdf.l_margin, w=usable_width)
    pdf.set_font("Times", size=30, )
    pdf.set_text_color(255, 255, 255)
    pdf.cell(text=f'{name} took CS50', center=True, new_x="LMARGIN", new_y="NEXT", h=200)

    pdf.output("shirtificate.pdf")


if __name__ == '__main__':
    main()
