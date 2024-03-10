import os
from tkinter import filedialog, messagebox
from pylatex import Document, Section, Subsection, Command, Alignat, Figure, Tabular
from pylatex.utils import italic, NoEscape

def get_path():
    dir_path = filedialog.askdirectory(title="Seleccione un directorio")
    return dir_path
"""
# Funcion para generar un reporte de una funcion
# El argumento function es la funcion a integrar, el argumento variables es un arreglo que contiene las variables por las cuales se integrara(simbolos), en el orden de integracion
# El argumento limits es un arreglo que contiene los limites inferior y superior de la integral, en el orden de integracion
# El argumento nodes es el numero de nodos a usar
# El argumento option es una opcion que indica si se quiere generar un reporte de una integral simple o de una integral doble o triple
"""
def generate_pdf(function: str, variables, limits, nodes, result, option, tableNodes):
    path_to_save = get_path()
    if path_to_save == "":
        return
    geometry_options = {"tmargin": "1.5in","lmargin":"1.5in"}
    filename = os.path.join(path_to_save, "gaussQuadReport")
    doc = Document(filename, geometry_options=geometry_options)
    doc.preamble.append(Command("title","Metodo: Cuadratura de Gauss"))
    doc.preamble.append(Command("author","Stephensen Methodverse of madness"))
    doc.append(NoEscape(r'\maketitle'))
    function =  function.replace("**", "^")
    function =  function.replace("*", "")
    with doc.create(Section("Reporte de la integral")):
        with doc.create(Subsection("Funcion a integrar")):
            if option == 1:
                f_exp = f"f({variables[0]}) = "
                doc.append(NoEscape(r'\[' + f_exp + function + '\]'))
            elif option == 2:
                f_exp = f"f({variables[0]},{variables[1]}) = "
                doc.append(NoEscape(r'\[' + f_exp + function + '\]'))
            elif option == 3:
                f_exp = f"f({variables[0]},{variables[1]},{variables[2]}) = "
                doc.append(NoEscape(r'\[' + f_exp + function + '\]'))
        with doc.create(Subsection("Integral de la funcion")):
            integral = ""
            if option == 1:
                integral = "\int_{"+str(limits[0][0])+"}^{"+str(limits[0][1])+"} " + f"{function} \ d{variables[0]}"
            elif option == 2:
                integral = "\int_{"+str(limits[1][0])+"}^{"+str(limits[1][1])+"} \int_{"+str(limits[0][0])+"}^{"+str(limits[0][1])+"} " + f"{function} \ d{variables[0]} d{variables[1]}"
            elif option == 3:
                integral = "\int_{"+str(limits[2][0])+"}^{"+str(limits[2][1])+"} \int_{"+str(limits[1][0])+"}^{"+str(limits[1][1])+"} \int_{"+str(limits[0][0])+"}^{"+str(limits[0][1])+"} " + f"{function} \ d{variables[0]} d{variables[1]} d{variables[2]}"
            doc.append(NoEscape(r'\[' + integral + '\]'))

        with doc.create(Subsection("Resultado de integracion")):
            doc.append(NoEscape(r'\[' + "I = " + str(result) + '\]'))

        with doc.create(Subsection("Nodos y Pesos de Gauss-Legendre")):
            with doc.create(Alignat(numbering=False, escape=False)) as table_space:
                table = Tabular("|c|c|")
                table.add_hline()
                table.add_row(["Nodos (x_i)", "Pesos (w)"])
                table.add_hline()
                node_list = tableNodes.get("Raices")
                weight_list = tableNodes.get("Pesos")
                for i in range(len(node_list)):
                    table.add_row([round(node_list[i], 6), round(weight_list[i], 6)])
                    table.add_hline()
                table_space.append(table)
    doc.generate_pdf(clean_tex=False,compiler="pdflatex")
    doc.generate_tex()
    messagebox.showinfo("Reporte generado", "El reporte se ha generado en el directorio seleccionado")
