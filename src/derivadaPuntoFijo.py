from email import message
import os
from queue import Empty
import tkinter as tk
from tkinter import filedialog
from unicodedata import name
import pylatex as pl
from scipy.__config__ import show
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo


from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel

def open_single_derivative(root):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./derivadapuntofijo_assets")


    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)


    window = Toplevel(root)

    window.geometry("599x396")
    window.configure(bg="#FFFFFF")
    window.grab_set()
    window.title("Diferencia Centrales: Derivada comun")

    ########### Derivadas en un punto fijo ##############
    def central_diff(n, x, h, f):
        return f(x) if n == 0 else central_diff(n-1, x + h/2, h, f)-central_diff(n-1, x - h/2,  h, f)


    def order_Derivative(k, x, h, f):
        return central_diff(k, x, h, f)/h**k


    def derivate(symb, k, x, h, f):
        function = sp.lambdify(symb, f)
        return order_Derivative(k, x, h, function)


    def get_path():
        dir_path = filedialog.askdirectory(
            title="Seleccione un directorio para almacenar el reporte")
        return dir_path

    def generate_pdf(x,resultderiv):
        path_to_save = get_path()
        if path_to_save == "":
            return
        filename = os.path.join(path_to_save, "DiferenciaCentral_Simple")
        doc = pl.Document(filename)
        doc.preamble.append(pl.Command('title', 'Derivadas en un punto fijo'))
        doc.preamble.append(pl.Command(
            'author', 'Steffensen Methodverse of madness '))
        doc.append(pl.NoEscape(r'\maketitle'))
        with doc.create(pl.Section("Función")):
            funpdf = ""+f_function.get().replace("**", "^")+""
            doc.append("Esta es la función que ingreso y se va a derivar:  ")
            doc.append(funpdf)
            with doc.create(pl.Subsection("Valores dados en el ejercicio")):
                doc.append("La variable que se va a derivar es: ")
                doc.append(x+"\n")
                doc.append("El espaciamiento h es: ")
                doc.append(h_space.get()+"\n")
                doc.append("El valor de la variable es: ")
                doc.append(vvariable_str.get()+"\n")
                doc.append("El orden de la derivada es: ")
                doc.append(order_str.get()+"\n")
            with doc.create(pl.Subsection("Resultado")):
                doc.append("El resultado de la derivada es: ")
                doc.append(resultderiv)
        doc.generate_pdf(clean_tex=False, compiler='pdflatex')
        showinfo(title="Informacion", message="Reporte generado")

    def calculate():
        try:
            if f_function.get() == "":
                showerror("Error", "No ha ingresado la funcion")
                return
            else:
                f = sp.sympify(f_function.get())

            if variable_deriv.get() == "":
                showerror("Error", "No ha ingresado la variable")
                return
            else:
                x = variable_deriv.get()
            if h_space.get() == "":
                showerror("Error", "No ha ingresado el espaciamiento")
                return
            else:
                hspace = float(h_space.get())
            if vvariable_str.get() == "":
                showerror("Error", "No ha ingresado el valor de la variable")
                return
            else:
                value = float(vvariable_str.get())

            if order_str.get() == "":
                showerror("Error", "No ha ingresado el orden")
                return
            else:
                n = int(order_str.get())
            try:
                resultderiv = derivate(x, n, value, hspace, f)
                result_label.config(
                    text=f"El resultado de la derivada es: {resultderiv} ")
                showinfo(title="Informacion", message="Calculo finalizado, generando reporte")
                generate_pdf(x,resultderiv)
            except ValueError as error:
                showerror(title="Error", message=str(error))
        except ValueError as error:
            showerror(title="Error", message=str(error))
        
    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=396,
        width=599,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        0.0,
        0.0,
        599.0,
        68.0,
        fill="#399DD6",
        outline="")

    canvas.create_text(
        76.0,
        10.0,
        anchor="nw",
        text=" Derivadas en un punto fijo",
        fill="#FFFFFF",
        font=("Poppins Bold", 32 * -1)
    )

    canvas.create_text(
        116.0,
        80.0,
        anchor="nw",
        text="Ingrese la funcion",
        fill="#000000",
        font=("Poppins Light", 14 * -1)
    )

    canvas.create_text(
        116.0,
        130.0,
        anchor="nw",
        text="Variable a derivar",
        fill="#000000",
        font=("Poppins Light", 14 * -1)
    )

    canvas.create_text(
        114.0,
        177.0,
        anchor="nw",
        text="Espaciamiento h",
        fill="#000000",
        font=("Poppins Light", 14 * -1)
    )

    canvas.create_text(
        114.0,
        228.0,
        anchor="nw",
        text="Valor de la variable",
        fill="#000000",
        font=("Poppins Light", 14 * -1)
    )

    canvas.create_text(
        101.0,
        284.0,
        anchor="nw",
        text="Orden de la derivada",
        fill="#000000",
        font=("Poppins Light", 14 * -1)
    )

    canvas.create_text(
        101.0,
        284.0,
        anchor="nw",
        text="Orden de la derivada",
        fill="#000000",
        font=("Poppins Light", 14 * -1)
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        368.0,
        90.5,
        image=entry_image_1
    )
    f_function = tk.StringVar(window)
    entry_1 = Entry(  # para guardar la función
        window,
        bd=0,
        bg="#f5f5f5",
        highlightthickness=0,
        textvariable=f_function,

    )
    entry_1.place(
        x=263.0,
        y=75.0,
        width=210.0,
        height=29.0
    )
    variable_deriv = tk.StringVar(window)
    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        368.0,
        135.5,
        image=entry_image_2
    )

    entry_2 = Entry(  # variable a derivar
        window,
        bd=0,
        bg="#f5f5f5",
        highlightthickness=0,
        textvariable=variable_deriv

    )
    entry_2.place(
        x=263.0,
        y=120.0,
        width=210.0,
        height=29.0
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        368.0,
        193.5,
        image=entry_image_3
    )
    h_space = tk.StringVar(window)
    entry_3 = Entry(  # espaciamiento h
        window,
        bd=0,
        bg="#f5f5f5",
        highlightthickness=0,
        textvariable=h_space

    )
    entry_3.place(
        x=263.0,
        y=178.0,
        width=210.0,
        height=29.0
    )
    vvariable_str = tk.StringVar(window)
    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(  # valor de la variable
        368.0,
        243.5,
        image=entry_image_4
    )
    entry_4 = Entry(
        window,
        bd=0,
        bg="#f5f5f5",
        highlightthickness=0,
        textvariable=vvariable_str,
    )
    entry_4.place(
        x=263.0,
        y=228.0,
        width=210.0,
        height=29.0
    )


    entry_image_6 = PhotoImage(
        file=relative_to_assets("entry_6.png"))
    entry_bg_6 = canvas.create_image(
        368.0,
        291.5,
        image=entry_image_6
    )
    order_str = tk.StringVar(window)
    entry_6 = Entry(  # orden de la derivada
        window,
        bd=0,
        bg="#f5f5f5",
        highlightthickness=0,
        textvariable=order_str

    )
    entry_6.place(
        x=263.0,
        y=276.0,
        width=210.0,
        height=29.0
    )


    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=calculate,
        relief="flat"
    )
    button_1.place(
        x=119.0,
        y=320.0,
        width=111.0,
        height=39.0
    )

    result_label = ttk.Label(window, text="Resultado:", font=("Arial", 12))
    result_label.place(x=119.0, y=365.0)

    window.resizable(False, False)
    window.mainloop()
