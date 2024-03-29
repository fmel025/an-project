# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer

from multiprocessing import Value
import os
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from pydoc import doc
import tkinter
from tkinter import messagebox, BooleanVar
from tkinter import filedialog
import sympy as sp
import numpy as np
import pandas as pd
from math import *
import pylatex as pl
from datetime import datetime


def open_romberg_gui(root):
    # Simbolos a ocupar más adelante
    x = sp.Symbol('x')
    y = sp.Symbol('y')
    l = sp.Symbol('l')
    z = sp.Symbol('z')

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./romberg_assets")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def trap(f, a, b, n, y, z):
        h = (b-a)/n
        x = a
        I = f(a, y, z)
        for i in range(1, n):  # El valor 'n' definirá la iteración a retornar
            x += h
            I += 2*f(x, y, z)
        return (I + f(b, y, z))*h*0.5  # Se retorna el valor

    def romberg(f, a, b, a2, b2, a3, b3, n, y):
        if(type(y) == str):
            y = sp.Symbol('y')
        # 'a2' y 'b2' solo serán necesarios si se está trabajando con integrales dobles, lo mismo para 'a3' y 'b3'
        # Se define un arreglo de 'n' filas y 'n' columnas, inicialmete conformado por ceros
        R = np.zeros((n, n), dtype='object_')
        k = sp.Symbol('k')
        for i in range(0, n):
            # Se llena la primera columna con las aproximaciones de la regla del trapecio
            R[i, 0] = trap(f, a, b, 2**i, y, z)
            for j in range(0, i):
                # Con la primera columna llena, se puede empezar a extrapolar para llenar las columnas restantes hasta llegar a 'n'
                R[i, j+1] = R[i, j]+((R[i, j]-R[i-1, j])/(4**(j+1)-1))
        if y == 0:
            # En caso de que la última celda siga siendo una función (integral triple)
            if type(R[n-1, n-1]) != float:
                # El valor de la última celda se convierte en una función usando lambdify
                p = sp.lambdify([x, z, l], R[n-1, n-1])
                # Se vuelve a ejecutar el método con los nuevos valores
                return romberg(p, a3, b3, 0.0, 0.0, 0.0, 0.0, n, 0)
            ''' Cuando ya no se tienen funciones, se puede construir la tabla  '''
            df = pd.DataFrame(R, columns=[
                "R"+str(x) for x in range(n)])  # Convertimos el arreglo en un DataFrame
            # Construción del documento en latex
            global doc
            doc = pl.Document()
            doc.preamble.append(pl.Command('title', 'Romberg'))
            doc.preamble.append(pl.Command('date', pl.NoEscape(r'\today')))
            doc.append(pl.NoEscape(r'\maketitle'))
            doc.append('La integral')
            int1Var = "\int_{"+str(aEntry.get())+"}^{"+str(bEntry.get())+"}" + \
                str(func.get().replace('**', '^')) + "dx"
            int2Var = "\int_{"+str(a2Entry.get())+"}^{"+str(b2Entry.get())+"}\int_{"+str(
                aEntry.get())+"}^{"+str(bEntry.get())+"}" + str(func.get().replace('**', '^')) + "dxdy"
            int3Var = "\int_{"+str(a3Entry.get())+"}^{"+str(b3Entry.get())+"}\int_{"+str(a2Entry.get())+"}^{"+str(
                b2Entry.get())+"}\int_{"+str(aEntry.get())+"}^{"+str(bEntry.get())+"}" + str(func.get().replace('**', '^')) + "dxdydz"
            with doc.create(pl.Alignat(numbering=False, escape=False)) as equation:
                if (float(a2Entry.get()) == 0 or float(a2Entry.get()) == '') and (float(b2Entry.get()) == 0 or float(b2Entry.get()) == ''):
                    equation.append(int1Var)
                elif (float(a3Entry.get()) == 0 or float(a3Entry.get()) == '') and (float(b3Entry.get()) == 0 or float(b3Entry.get()) == ''):
                    equation.append(int2Var)
                else:
                    equation.append(int3Var)
            doc.append('Genera la siguiente tabla\n\n')
            with doc.create(pl.Tabular('|'+'c|'*(n+1))) as table:
                table.add_hline()
                table.add_row([df.index.name] + list(df.columns))
                table.add_hline()
                for row in df.index:
                    table.add_row([row] + list(df.loc[row, :]))
                    table.add_hline()
            res = "\n\nEl resultado es: "+str(R[n-1, n-1])+""
            doc.append(res)
            # Se muestra el resultado en una etiqueta
            resultado["text"] = 'Resultado: '+str(R[n-1, n-1])
        # Si el argumento 'y' es diferente de 0 (posee 2 o 3 variables), se hará lo siguiente
        # El valor de la última celda se convierte en una función usando lambdify
        p = sp.lambdify([y, x, z], R[n-1, n-1])
        '''
            Se vuelve a ejecutar el método utilizando la nueva función,
            sustituyendo los nuevos límites y estableciento los anteriores a 0
        '''
        return romberg(p, a2, b2, 0.0, 0.0, a3, b3, n, 0)

    window = tkinter.Toplevel(root)
    window.title('Romberg')
    window.geometry("600x475")
    window.configure(bg="#3C97D8")
    window.grab_set()

    hasUserCalc = BooleanVar(window, value=False)

    canvas = tkinter.Canvas(
        window,
        bg="#3C97D8",
        height=475,
        width=600,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        190.0,
        29.99999999999997,
        anchor="nw",
        text="Método de Romberg",
        fill="#FFFFFF",
        font=("Poppins", 24 * -1, 'bold')
    )

    canvas.create_text(
        200.0,
        74.99999999999997,
        anchor="nw",
        text="Función",
        fill="#FFFFFF",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        78.0,
        105.99999999999997,
        anchor="nw",
        text="Límite inferior (1° integral)",
        fill="#FFFFFF",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        68.0,
        136.99999999999997,
        anchor="nw",
        text="Límite superior (1° integral)",
        fill="#FFFFFF",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        73.0,
        167.99999999999997,
        anchor="nw",
        text="Límite inferior (2° integral)",
        fill="#FFFFFF",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        64.0,
        198.99999999999997,
        anchor="nw",
        text="Límite superior (2° integral)",
        fill="#FFFFFF",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        73.0,
        229.99999999999997,
        anchor="nw",
        text="Límite inferior (3° integral)",
        fill="#FFFFFF",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        63.0,
        261.0,
        anchor="nw",
        text="Límite superior (3° integral)",
        fill="#FFFFFF",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        200.0,
        292.0,
        anchor="nw",
        text="Nodos",
        fill="#FFFFFF",
        font=("Poppins", 16 * -1)
    )

    entry_image_1 = tkinter.PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        424.0,
        85.99999999999997,
        image=entry_image_1
    )
    func = tkinter.Entry(
        window,
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    func.place(
        x=317.0,
        y=74.99999999999997,
        width=214.0,
        height=22.0
    )

    entry_image_2 = tkinter.PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        424.0,
        117.99999999999997,
        image=entry_image_2
    )
    aEntry = tkinter.Entry(
        window,
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    aEntry.place(
        x=317.0,
        y=105.99999999999997,
        width=214.0,
        height=22.0
    )

    entry_image_3 = tkinter.PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        424.0,
        148.99999999999997,
        image=entry_image_3
    )
    bEntry = tkinter.Entry(
        window,
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    bEntry.place(
        x=317.0,
        y=136.99999999999997,
        width=214.0,
        height=22.0
    )

    entry_image_4 = tkinter.PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
        424.0,
        179.99999999999997,
        image=entry_image_4
    )
    a2Entry = tkinter.Entry(
        window,
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    a2Entry.place(
        x=317.0,
        y=167.99999999999997,
        width=214.0,
        height=22.0
    )

    entry_image_5 = tkinter.PhotoImage(
        file=relative_to_assets("entry_5.png"))
    entry_bg_5 = canvas.create_image(
        424.0,
        210.99999999999997,
        image=entry_image_5
    )
    b2Entry = tkinter.Entry(
        window,
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    b2Entry.place(
        x=317.0,
        y=198.99999999999997,
        width=214.0,
        height=22.0
    )

    entry_image_6 = tkinter.PhotoImage(
        file=relative_to_assets("entry_6.png"))
    entry_bg_6 = canvas.create_image(
        424.0,
        241.99999999999997,
        image=entry_image_6
    )
    a3Entry = tkinter.Entry(
        window,
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    a3Entry.place(
        x=317.0,
        y=229.99999999999997,
        width=214.0,
        height=22.0
    )

    entry_image_7 = tkinter.PhotoImage(
        file=relative_to_assets("entry_7.png"))
    entry_bg_7 = canvas.create_image(
        424.0,
        273.0,
        image=entry_image_7
    )
    b3Entry = tkinter.Entry(
        window,
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    b3Entry.place(
        x=317.0,
        y=261.0,
        width=214.0,
        height=22.0
    )

    entry_image_8 = tkinter.PhotoImage(
        file=relative_to_assets("entry_8.png"))
    entry_bg_8 = canvas.create_image(
        424.0,
        304.0,
        image=entry_image_8
    )
    n = tkinter.Entry(
        window,
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    n.place(
        x=317.0,
        y=292.0,
        width=214.0,
        height=22.0
    )

    var1 = tkinter.Variable()
    var1.set(0)

    tkinter.Radiobutton(canvas, text="1 variable", variable=var1,
                        value=0, bg='#3C97D8').place(x="195", y="335")
    tkinter.Radiobutton(canvas, text="2 o 3 variables", variable=var1,
                        value=y, bg='#3C97D8').place(x="290", y="335")

    resultado = tkinter.Label(canvas)
    resultado.config(fg='black', bg='#3C97D8',
                     font=("Poppins", 24 * -1, 'bold'))
    resultado.place(x="60", y="360")

    def fLam(x, y, z): return eval(func.get())

    def checkErrors():
        if(not func.get() or not aEntry.get() or not bEntry.get() or not a2Entry.get()
                or not b2Entry.get() or not a3Entry.get() or not b3Entry.get() or not n.get()):
            messagebox.showerror('Error', 'Por favor llene todos los campos')
            return
        if(int(n.get()) < 1):
            messagebox.showerror(
                'Error', 'El método debe tener por lo menos un nodo')
            return
        if(var1.get() == 0 and (float(a2Entry.get()) != 0 or float(b2Entry.get()) != 0 or float(a3Entry.get()) != 0
                                or float(b3Entry.get()) != 0)):
            messagebox.showwarning(
                'Advertencia', 'Verifique que el número de variables de la función corresponda con la cantidad de límites introducidos')
            return
        if(float(aEntry.get()) > float(bEntry.get()) or float(a2Entry.get()) > float(b2Entry.get()) or
                float(a3Entry.get()) > float(b3Entry.get())):
            messagebox.showwarning(
                'Advertencia', 'Ha introducido límites inferiores mayores a los superiores')
            return
        hasUserCalc.set(True)
        romberg(fLam, float(aEntry.get()), float(bEntry.get()), float(a2Entry.get()), float(b2Entry.get()),
                float(a3Entry.get()), float(b3Entry.get()), int(n.get()), var1.get())
        return

    button_image_1 = tkinter.PhotoImage(
        file=relative_to_assets("button_1.png"))
    btn = tkinter.Button(
        window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:
        [checkErrors()],
        relief="flat"
    )
    btn.place(
        x=242.0,
        y=411.0,
        width=128.0,
        height=30.0
    )

    now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

    def get_path():
        dir_path = filedialog.askdirectory(
            title="Seleccione un directorio para almacenar el reporte")
        return dir_path

    def generate_pdf(doc):
        if(not func.get() or not aEntry.get() or not bEntry.get() or not a2Entry.get()
                or not b2Entry.get() or not a3Entry.get() or not b3Entry.get() or not n.get()):
            messagebox.showerror('Error', 'Por favor llene todos los campos')
            return
        if(int(n.get()) < 1):
            messagebox.showerror(
                'Error', 'El método debe tener por lo menos un nodo')
            return
        if(var1.get() == 0 and (float(a2Entry.get()) != 0 or float(b2Entry.get()) != 0 or float(a3Entry.get()) != 0
                                or float(b3Entry.get()) != 0)):
            messagebox.showwarning(
                'Advertencia', 'Verifique que el número de variables de la función corresponda con la cantidad de límites introducidos')
            return
        if(float(aEntry.get()) > float(bEntry.get()) or float(a2Entry.get()) > float(b2Entry.get()) or
                float(a3Entry.get()) > float(b3Entry.get())):
            messagebox.showwarning(
                'Advertencia', 'Ha introducido límites inferiores mayores a los superiores')
            return
        messagebox.showinfo("Generacion del reporte",
                            "Se comenzara la generacion del reporte, seleccione una carpeta a guardar")
        path_to_save = get_path()
        if path_to_save == "":
            return
        filename = os.path.join(path_to_save, 'Romberg_'+now+'')
        doc.generate_pdf(filename, clean_tex=False, compiler='pdflatex'),
        messagebox.showinfo('Información', 'El archivo ha sido generado!')

    button_image_4 = tkinter.PhotoImage(
        file=relative_to_assets("button_4.png"))
    btnPdf = tkinter.Button(
        window,
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: generate_pdf(doc),
        relief="flat"
    )
    btnPdf.place(
        x=549.0,
        y=2.842170943040401e-14,
        width=51.0,
        height=30.0
    )

    window.resizable(False, False)
    window.mainloop()
