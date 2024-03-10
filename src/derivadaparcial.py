
import tkinter as tk
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import pylatex as pl
from tkinter import StringVar, ttk
from tkinter.messagebox import showerror
from pathlib import Path
import os as os


from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, messagebox, Toplevel

def open_partial_derivative_window(root):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./derivadaparcial")


    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)


    window = Toplevel(root)
    window.title("Diferrencia Central: Derivadas parciales de una función")
    window.geometry("599x396")
    window.configure(bg="#FFFFFF")
    window.grab_set()

    ########## Derivadas parciales ##############


    def central_diff_mult(n, var):
        f = sp.Function("f")
        h = sp.Symbol("h")
        return f(var) if n == 0 else central_diff_mult(n-1, var + h/2)-central_diff_mult(n-1, var - h/2)


    def order_derivative_mult(n, var):
        h = sp.Symbol("h")
        return central_diff_mult(n, var)/h**n


    def partial_derivation(varsToDerivate, varsToEval, values, hspace, function):
        h = sp.Symbol("h")
        f = sp.Function("f")

        auxDif = 0

        auxFunc = function

        for var in varsToDerivate:

            auxDif = sp.lambdify([h, f], order_derivative_mult(1, var))
            auxFunc = sp.lambdify(var, auxFunc, modules=["sympy"])

            auxDif = auxDif(hspace, auxFunc)

            auxFunc = auxDif

        print(*varsToEval)
        derivatedFunction = sp.lambdify([*varsToEval], auxFunc, modules=["sympy"])
        return derivatedFunction(*values)


    ############# Derivadas Parciales Funciones ##############

    def get_path():
        dir_path = filedialog.askdirectory(title="Seleccione un directorio para almacenar el reporte")
        return dir_path

    def generate_pdf(result):
        messagebox.showinfo("Generacion del reporte", "Se comenzara la generacion del reporte, seleccione una carpeta a guardar")
        path_to_save = get_path()
        if path_to_save == "":
            return
        filename = os.path.join(path_to_save, "DiferenciaCentral_Parcial")
        doc = pl.Document(filename)
        doc.preamble.append(pl.Command("title", "Derivadas Parciales"))
        doc.preamble.append(pl.Command(
            "author", "Steffensen Methodverse of madness"))
        doc.append(pl.NoEscape(r"\maketitle"))
        with doc.create(pl.Section("Función")):
            funpdf = ""+f_str.get().replace("**", "^")+""
            funaux = ""+funpdf.replace("*", "")+""
            doc.append("Esta es la función a derivar: ")
            doc.append(funaux)
            with doc.create(pl.Subsection("Espaciamiento h")):
                doc.append("El espaciamiento en h es: ")
                doc.append(h_str.get())
            with doc.create(pl.Subsection("Variables y sus valores")):
                doc.append("Esta es la variable 1 a evaluar: ")
                doc.append(var1_str.get()+"\n")
                doc.append("Este es el valor asignado a la variable 1: ")
                doc.append(val1_str.get()+"\n")
                doc.append("Esta es la variable 2 a evaluar: ")
                doc.append(var2_str.get()+"\n")
                doc.append("Este es el valor asignado a la variable 2: ")
                doc.append(val2_str.get()+"\n")
                doc.append("Esta es la variable 3 a evaluar: ")
                doc.append(var3_str.get()+"\n")
                doc.append("Este es el valor asignado a la variable 3: ")
                doc.append(val3_str.get()+"\n")
            with doc.create(pl.Subsection("Orden de las variables a derivar")):
                doc.append("Esta es la variable 1 a derivar: ")
                doc.append(order1_str.get()+"\n")
                doc.append("Esta es la variable 2 a derivar: ")
                doc.append(order2_str.get()+"\n")
                doc.append("Esta es la variable 3 a derivar: ")
                doc.append(order3_str.get()+"\n")
            with doc.create(pl.Subsection("Resultado")):
                doc.append("El resultado de la derivada es: ")
                doc.append(result)
        doc.generate_pdf(clean_tex=False, compiler='pdflatex')
        messagebox.showinfo("Generado", "El reporte se ha generado correctamente")

    def calculate():
        try:
            varsToDerivate = [sp.Symbol(order1_str.get()), sp.Symbol(
                order2_str.get()), sp.Symbol(order3_str.get())]

            # Revisaremos si el ultimo valor de la entry de varsToDerivate esta en blanco para asi no añadirlo
            # Por si se quiere derivar dos variables
            if len(order3_str.get()) == 0:
                varsToDerivate.pop()
            if var1_str.get() == "":
                showerror("Error", "No ha ingresado un valor para la variable 1")
            elif var2_str.get() == "":
                showerror("Error", "No ha ingresado un valor para la variable 2 ")
            else:
                varsToEval = [sp.Symbol(var1_str.get()), sp.Symbol(var2_str.get())]

            values = [float(val1_str.get()), float(
                val2_str.get())]

            # Se revisa si el ultimo valor de la entry de values no esta en blanco para asi añadirlo
            if len(var3_str.get()) != 0:
                varsToEval.append(sp.Symbol(var3_str.get()))
                values.append(float(val3_str.get()))
            if f_str.get() == "":
                showerror("Error", "No ha ingresado un valor para la función")
                return
            else:
                function = sp.sympify(f_str.get())

            if h_str.get() == "":
                showerror("Error", "No ha ingresado un valor para el espaciamiento")
            else:
                hspace = float(h_str.get())
            try:
                if len(varsToDerivate) > len(varsToEval):
                    raise Exception(
                        "No puedes derivar mas variables de las que quieres evaluar")
                result = partial_derivation(
                    varsToDerivate, varsToEval, values, hspace, function)
                result_label.config(
                    text=f"El resultado de la derivada es: {result}")
                generate_pdf(result)
            except ValueError as error:
                showerror(title="Error", message="Por favor ingrese valores validos")
            except Exception as error:
                showerror(title="Error", message=str(error))
        except ValueError as error:
            showerror(title="Error", message="Por favor ingrese valores validos")


    #####Lo visualizamos en la pantalla#####
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
        48.0,
        fill="#399DD6",
        outline="")

    canvas.create_text(
        134.0,
        0.0,
        anchor="nw",
        text="Derivadas parciales",
        fill="#FFFFFF",
        font=("Poppins Bold", 32 * -1)
    )

    canvas.create_text(
        121.0,
        61.0,
        anchor="nw",
        text="Ingrese la funcion",
        fill="#000000",
        font=("Poppins Light", 14 * -1)
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        373.0,
        71.5,
        image=entry_image_1
    )
    f_str = StringVar(window)
    entry_1 = Entry(  # para la función
        window,
        bd=0,
        bg="#F5F5F5",
        highlightthickness=0,
        textvariable=f_str,
    )
    entry_1.place(
        x=268.0,
        y=56.0,
        width=210.0,
        height=29.0
    )

    canvas.create_text(
        120.0,
        100.0,
        anchor="nw",
        text="Espaciamiento h",
        fill="#000000",
        font=("Poppins Light", 14 * -1)
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        374.0,
        116.5,
        image=entry_image_2
    )
    h_str = StringVar()
    entry_2 = Entry(  # para el espaciamiento h
        window,
        bd=0,
        bg="#F5F5F5",
        highlightthickness=0,
        textvariable=h_str,
    )
    entry_2.place(
        x=269.0,
        y=101.0,
        width=210.0,
        height=29.0
    )

    canvas.create_text(
        59.0,
        162.0,
        anchor="nw",
        text="Variable 1",
        fill="#000000",
        font=("Poppins Light", 14 * -1)
    )

    canvas.create_text(
        57.0,
        201.0,
        anchor="nw",
        text="Variable 2",
        fill="#000000",
        font=("Poppins Light", 14 * -1)
    )

    canvas.create_text(
        57.0,
        246.0,
        anchor="nw",
        text="Variable 3",
        fill="#000000",
        font=("Poppins Light", 14 * -1)
    )

    canvas.create_text(
        14.0,
        313.0,
        anchor="nw",
        text="Orden de las variables a derivar",
        fill="#000000",
        font=("Poppins Light", 14 * -1)
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        195.0,
        172.5,
        image=entry_image_3
    )
    var1_str = StringVar(window)
    entry_3 = Entry(  # variable 1 a derivar
        window,
        bd=0,
        bg="#F5F5F5",
        highlightthickness=0,
        textvariable=var1_str,
    )
    entry_3.place(
        x=139.0,
        y=157.0,
        width=112.0,
        height=29.0
    )

    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
        289.0,
        318.5,
        image=entry_image_4
    )
    order1_str = StringVar(window)
    entry_4 = Entry(  # posición de la variable 1 a derivar
        window,
        bd=0,
        bg="#F5F5F5",
        highlightthickness=0,
        textvariable=order1_str,
    )
    entry_4.place(
        x=268.0,
        y=303.0,
        width=42.0,
        height=29.0
    )

    entry_image_5 = PhotoImage(
        file=relative_to_assets("entry_5.png"))
    entry_bg_5 = canvas.create_image(
        376.0,
        318.5,
        image=entry_image_5
    )
    order2_str = StringVar(window)
    entry_5 = Entry(  # posición de la variable 2 a derivar
        window,
        bd=0,
        bg="#F5F5F5",
        highlightthickness=0,
        textvariable=order2_str,
    )
    entry_5.place(
        x=355.0,
        y=303.0,
        width=42.0,
        height=29.0
    )

    entry_image_6 = PhotoImage(
        file=relative_to_assets("entry_6.png"))
    entry_bg_6 = canvas.create_image(
        457.0,
        318.5,
        image=entry_image_6
    )
    order3_str = StringVar(window)
    entry_6 = Entry(  # posición de la tercera variable a derivar
        window,
        bd=0,
        bg="#F5F5F5",
        highlightthickness=0,
        textvariable=order3_str,
    )
    entry_6.place(
        x=436.0,
        y=303.0,
        width=42.0,
        height=29.0
    )

    entry_image_7 = PhotoImage(
        file=relative_to_assets("entry_7.png"))
    entry_bg_7 = canvas.create_image(
        195.0,
        211.5,
        image=entry_image_7
    )
    var2_str = StringVar(window)
    entry_7 = Entry(  # variable dos a derivar
        window,
        bd=0,
        bg="#F5F5F5",
        highlightthickness=0,
        textvariable=var2_str,
    )
    entry_7.place(
        x=139.0,
        y=196.0,
        width=112.0,
        height=29.0
    )

    entry_image_8 = PhotoImage(
        file=relative_to_assets("entry_8.png"))
    entry_bg_8 = canvas.create_image(
        195.0,
        256.5,
        image=entry_image_8
    )
    var3_str = StringVar(window)
    entry_8 = Entry(
        window,
        bd=0,
        bg="#F5F5F5",
        highlightthickness=0,
        textvariable=var3_str,
    )
    entry_8.place(
        x=139.0,
        y=241.0,
        width=112.0,
        height=29.0
    )

    canvas.create_text(
        275.0,
        162.0,
        anchor="nw",
        text="Valor de la variable",
        fill="#000000",
        font=("Poppins Light", 14 * -1)
    )

    canvas.create_text(
        275.0,
        201.0,
        anchor="nw",
        text="Valor de la variable",
        fill="#000000",
        font=("Poppins Light", 14 * -1)
    )

    canvas.create_text(
        275.0,
        246.0,
        anchor="nw",
        text="Valor de la variable",
        fill="#000000",
        font=("Poppins Light", 14 * -1)
    )

    entry_image_9 = PhotoImage(
        file=relative_to_assets("entry_9.png"))
    entry_bg_9 = canvas.create_image(
        483.0,
        172.5,
        image=entry_image_9
    )
    val1_str = StringVar(window)
    entry_9 = Entry(  # valor de la variable 1
        window,
        bd=0,
        bg="#F5F5F5",
        highlightthickness=0,
        textvariable=val1_str,
    )
    entry_9.place(
        x=423.0,
        y=157.0,
        width=120.0,
        height=29.0
    )

    entry_image_10 = PhotoImage(
        file=relative_to_assets("entry_10.png"))
    entry_bg_10 = canvas.create_image(
        483.0,
        211.5,
        image=entry_image_10
    )
    val2_str = StringVar(window)
    entry_10 = Entry(  # valor de la variable 2
        window,
        bd=0,
        bg="#F5F5F5",
        highlightthickness=0,
        textvariable=val2_str,
    )
    entry_10.place(
        x=423.0,
        y=196.0,
        width=120.0,
        height=29.0
    )

    entry_image_11 = PhotoImage(
        file=relative_to_assets("entry_11.png"))
    entry_bg_11 = canvas.create_image(
        483.0,
        256.5,
        image=entry_image_11
    )
    val3_str = StringVar(window)
    entry_11 = Entry(  # valor de la variable 3
        window,
        bd=0,
        bg="#F5F5F5",  # color de fondo
        highlightthickness=0,
        textvariable=val3_str,
    )
    entry_11.place(
        x=423.0,
        y=241.0,
        width=120.0,
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
        x=10.0,
        y=342.0,
        width=100.0,
        height=39.0
    )
    result_label = ttk.Label(window, text="Resultado:", font=("Arial", 12))
    result_label.place(x=120.0, y=350.0)
    window.resizable(False, False)
    window.mainloop()
