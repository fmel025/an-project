# Integrals and derivatives calculator

## Requirements

1. Python 3
2. [MikTex](https://miktex.org/howto/install-miktex) or any Tex distribution for pdflatex

## Installation

1. First you have to create a virtual enviroment, to do so, you can execute the following command:
```shell
python -m venv .venv
```
1. Activate the virtual enviroment running the script activate:
```shell
activate
```
1. Then we have to install the packages for the virtual enviroment:
```shell
pip install requirements.txt
```
1. Now we can run the app using the following command:
```shell
python src/main.py
```
1. To deactivate the virtualenv use the following command:
```shell
deactivate
```

## QA

1. How did we do that kind of GUI so easily?

   We just used a library that compiles a figma into a Tkinter GUI, if you want to make it this way you can watch this [video](https://www.youtube.com/watch?v=oLxFqpUbaAE)

2. How do you create an installer or an executable for the application?

    We used a library that compiles all the files and assets into an executable, the library name is [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/), pretty useful for creating the executable, if you need any guide i really recommend this [video](https://www.youtube.com/watch?v=dwXW2x7JPx8)

3. It seems I cannot generate a pdf report:

    You should probably install the MikTex or any other pdflatex Tex compiler, if you do not know how to install it, use the link from the requirements.

4. Why in some windows it makes the calculation and automatically generates a pdf?

    Because that was a requirement asked for the teacher back then my groupd made my project.

5. I don't understand the code, what can I do?

    If you don't know how windows are open, you should see the buttons code in the main.py and review the romberg file or the gauss_gui or gaussQuad.

    For any doubt you've got you can check those files or DM me to explain you.
