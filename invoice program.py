import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox 
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import threading
import os

## You need to have selenium and ttkbootstrap libraries installed, in Spanish (Necesitas las librerias selenium y ttkbootstrap instaladas)
## Change "PASSWORD" for your own password, in Spanish (Cambia "PASSWORD" en el codigo por tu propia contraseña)
## Change "C:\" paths for your own .cer and .key paths, in Spanish (busca tus archivos .cer y .key en tu ruta crítica "C:\")
## It will work only for edge driver tested on version 136, in Spanish (Funciona solo para el driver de edge version 136)
## Install your edge webdriver in C:\ in your computer, in Spanish (instala el webdriver de edge en C:\ en tu ordenador)

## Change "COMPANY NAME", in Spanish (Razón Social)
## Change "POSTAL CODE", in Spanish (Codigo Postal)
## Change "REGIMEN", in Spanish ("Régimen")
## Change "VAT", in Spanish ("IVA")
## Change this line intentar_operacion(lambda: self.driver.find_element(By.XPATH, '//*[@id="135textboxautocomplete113"]').send_keys(Keys.ARROW_DOWN, Keys.ENTER)) for whatever product you need, in Spanish Puedes cambiar el producto por send_keys("NOMBRE DEL PRODUCTO", Keys.ENTER)
## Change cuantity of the product by default you are going to find "39" and "35-38" in a combobox widget, in Spanish Cambia la cantidad del producto las encontrararas en un widget combobox como "39" y "35-38"

## This version of the program has all the warings and custom messages in Spanish because the web page is from Mexico only 

class UnitTest(unittest.TestCase):  # Contiene inicialización del driver y la función de espera de elementos en la página web
    def __init__(self):
        self.driver = None

    def setUp(self):
        if self.driver is not None:
            self.driver.quit()
            self.driver = None
        self.driver = webdriver.Edge()
        self.driver.get("https://portal.facturaelectronica.sat.gob.mx/")
        self.driver.maximize_window()
        time.sleep(1)
        test_instance.inicio()

    def wait(self, xpath):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def inicio(self, intentos=3):
        """Intenta iniciar sesión en el portal. Reintenta en caso de error hasta un máximo de intentos."""
        if self.driver is None:
            # Mostrar advertencia en el hilo principal
            root.after(0, lambda: messagebox.showwarning("Advertencia", "El navegador no está abierto. Presiona 'Abrir web' primero."))
            return

        try:
            boton_fiel = self.driver.find_element(By.XPATH, '//*[@id="buttonFiel"]')
            UnitTest.wait(self, '//*[@id="buttonFiel"]')
            boton_fiel.click()
            time.sleep(0.5)

            clav_key = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            time.sleep(1)
            clav_key.send_keys(r"C:\Your\Own_cert.cer")
            time.sleep(0.5)

            clav_cer = self.driver.find_element(By.XPATH, "(//input[@type='file'])[2]")
            time.sleep(1)
            clav_cer.send_keys(r"C:\Your\Own_key.key")
            time.sleep(0.5)

            con_comprobante = self.driver.find_element(By.XPATH, '//*[@id="privateKeyPassword"]')
            UnitTest.wait(self, '//*[@id="privateKeyPassword"]')
            con_comprobante.send_keys("PASSWORD")
            con_comprobante.send_keys(Keys.ENTER)

            enviar = self.driver.find_element(By.XPATH, '//*[@id="submit"]')
            UnitTest.wait(self, '//*[@id="submit"]')
            enviar.click()

        except Exception as e:
            if intentos > 0 and not ventana.cerrando:  # Solo reintentar si quedan intentos y la aplicación no se está cerrando
                print(f"Error en el intento de inicio de sesión: {e}. Reintentando...")
                try:
                    # Redirigir al navegador a la página específica
                    self.driver.get("https://portal.facturaelectronica.sat.gob.mx/Factura/GeneraFactura")
                    time.sleep(0.5)  # Esperar un momento antes de reintentar
                    self.inicio(intentos - 1)  # Llamada recursiva con un intento menos
                except Exception as redir_error:
                    print(f"Error al redirigir: {redir_error}")
            else:
                # Mostrar mensaje de error si se alcanzan los intentos máximos
                root.after(0, lambda: messagebox.showerror("Error", f"No se pudo iniciar sesión después de varios intentos: {e}"))

    def auto(self, r=0):
        # Navegador debe estar abierto para ejecutar      
        if self.driver is None:
            root.after(0, lambda: messagebox.showwarning("Advertencia", "El navegador no está abierto. Presiona 'Abrir web' primero."))
            return 

        def intentar_operacion(operacion, intentos=5):
            """Reintenta una operación específica hasta `intentos` veces, esperando a que la página termine de cargar."""
            for intento in range(intentos):
                if ventana.cerrando:  # Verificar si la aplicación se está cerrando
                    return  # Salir si la aplicación se está cerrando
                try:
                    # Esperar a que la página esté completamente cargada
                    WebDriverWait(test_instance.driver, 10).until(
                        lambda driver: driver.execute_script("return document.readyState") == "complete"
                    )
                    operacion()  # Ejecutar la operación
                    return  # Salir si la operación tiene éxito
                except Exception as e:
                    print(f"Error en el intento {intento + 1}: {e}")
                    time.sleep(2)  # Esperar antes de reintentar
            raise Exception("No se pudo completar la operación después de varios intentos.")

        try:
            if ventana.cerrando:  # Verificar si la aplicación se está cerrando
                return  # Salir si la aplicación se está cerrando

            limpiar = Keys.CONTROL + "a" + Keys.DELETE
            # Reintentar cada operación de forma independiente
            intentar_operacion(lambda: UnitTest.wait(self, '//*[@id="135textboxautocomplete55"]'))
            intentar_operacion(lambda: self.driver.find_element(By.XPATH, '//*[@id="135textboxautocomplete55"]').send_keys("COMPANY NAME", Keys.ARROW_DOWN, Keys.ENTER))

            intentar_operacion(lambda: UnitTest.wait(self, '//*[@id="135textbox61"]'))
            intentar_operacion(lambda: self.driver.find_element(By.XPATH, '//*[@id="135textbox61"]').send_keys("POSTAL CODE", Keys.ENTER))

            intentar_operacion(lambda: UnitTest.wait(self, '//*[@id="135textboxautocomplete62"]'))
            intentar_operacion(lambda: self.driver.find_element(By.XPATH, '//*[@id="135textboxautocomplete62"]').send_keys("REGIME", Keys.ARROW_DOWN, Keys.ARROW_DOWN, Keys.ENTER))

            intentar_operacion(lambda: UnitTest.wait(self, '//*[@id="135gridformedit98"]/button[1]'))
            intentar_operacion(lambda: self.driver.find_element(By.XPATH, '//*[@id="135gridformedit98"]/button[1]').click())

            intentar_operacion(lambda: UnitTest.wait(self, '//*[@id="135textboxautocomplete113"]'))
            intentar_operacion(lambda: self.driver.find_element(By.XPATH, '//*[@id="135textboxautocomplete113"]').send_keys(Keys.ARROW_DOWN, Keys.ENTER))

            intentar_operacion(lambda: UnitTest.wait(self, '//*[@id="135textbox114"]'))
            intentar_operacion(lambda: self.driver.find_element(By.XPATH, '//*[@id="135textbox114"]').send_keys(limpiar)), self.driver.find_element(By.XPATH, '//*[@id="135textbox114"]').send_keys(str(r), Keys.ENTER)

            intentar_operacion(lambda: UnitTest.wait(self, '//*[@id="135select115"]'))
            intentar_operacion(lambda: self.driver.find_element(By.XPATH, '//*[@id="135select115"]').send_keys(Keys.ARROW_DOWN, Keys.ARROW_DOWN, Keys.ENTER))

            intentar_operacion(lambda: UnitTest.wait(self, '//*[@id="135checkbox154"]'))
            intentar_operacion(lambda: self.driver.find_element(By.XPATH, '//*[@id="135checkbox154"]').click())

            intentar_operacion(lambda: UnitTest.wait(self, '//*[@id="135textboxautocomplete158"]'))
            intentar_operacion(lambda: self.driver.find_element(By.XPATH, '//*[@id="135textboxautocomplete158"]').send_keys(limpiar)) , self.driver.find_element(By.XPATH, '//*[@id="135textboxautocomplete158"]').send_keys("VAT", Keys.ENTER)

            intentar_operacion(lambda: UnitTest.wait(self, '//*[@id="guardarEditar1350001"]'))
            intentar_operacion(lambda: self.driver.find_element(By.XPATH, '//*[@id="guardarEditar1350001"]').click())

            intentar_operacion(lambda: WebDriverWait(self.driver, 200).until(EC.presence_of_element_located((By.LINK_TEXT, 'Sellar'))))
            intentar_operacion(lambda: self.driver.find_element(By.LINK_TEXT, 'Sellar').click())

            intentar_operacion(lambda: UnitTest.wait(self, '//*[@id="privateKeyPassword"]'))
            intentar_operacion(lambda: self.driver.find_element(By.XPATH, '//*[@id="privateKeyPassword"]').send_keys("PASSWORD", Keys.ENTER))

            intentar_operacion(lambda: self.driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(r"C:\Your\Own_key.key"))
            intentar_operacion(lambda: self.driver.find_element(By.XPATH, "(//input[@type='file'])[2]").send_keys(r"C:\Your\Own_cert.cer"))

            intentar_operacion(lambda: UnitTest.wait(self, '//*[@id="btnValidaOSCP"]'))
            intentar_operacion(lambda: self.driver.find_element(By.XPATH, '//*[@id="btnValidaOSCP"]').click())

            intentar_operacion(lambda: UnitTest.wait(self, '//*[@id="btnFirmar"]'))
            intentar_operacion(lambda: self.driver.find_element(By.XPATH, '//*[@id="btnFirmar"]').click())

            intentar_operacion(lambda: UnitTest.wait(self, '//*[@id="btnBackComprobante"]'))
            intentar_operacion(lambda: self.driver.find_element(By.XPATH, '//*[@id="btnBackComprobante"]').click())

            # Incrementar el contador solo si todo se ejecuta correctamente
            ventana.actualizar_contador()

        except Exception as e:
            if not ventana.cerrando:  # Solo redirigir si la aplicación no se está cerrando
                # Redirigir al navegador a la página específica
                try:
                    self.driver.get("https://portal.facturaelectronica.sat.gob.mx/Factura/GeneraFactura")
                except Exception as redir_error:
                    print(f"Error al redirigir: {redir_error}")
                
                # Mostrar el mensaje de error en la GUI
                root.after(0, lambda e=e: messagebox.showerror("Error", f"Ocurrió un error en la ejecución automática: {e}"))


class Ventana:  # Contiene las funciones de los botones y la configuración de la ventana principal
    def __init__(self):
        self.driver = None  # Inicializa el atributo driver
        self.facturas_realizadas = 0  # Contador de facturas realizadas
        self.contador_label = None  # Etiqueta para mostrar el contador
        self.cerrando = False  # Indicador de cierre

    def actualizar_contador(self):
        """Actualiza la etiqueta del contador en la ventana."""
        self.facturas_realizadas += 1
        self.contador_label.config(text=f"Facturas realizadas: {self.facturas_realizadas}")

    def on_close(self):
        """Cierra el navegador y la ventana de forma forzosa, ignorando excepciones."""
        self.cerrando = True  # Indicar que la aplicación se está cerrando
        try:
            if test_instance.driver:  # Verifica si el navegador está abierto
                try:
                    root.destroy()  
                    test_instance.driver.quit()# Intenta cerrar el navegador                    
                except Exception:
                    pass  # Ignora cualquier excepción al cerrar el navegador
                finally:            
                    test_instance.driver = None  # Asegura que el driver se establezca en None
        except Exception:
            pass  # Ignora cualquier excepción inesperada
        finally:
            os._exit(0)  # Detiene el programa por completo

# Crear un área neutra para deseleccionar botones
def deseleccionar(event):
    # Verifica si el clic no ocurrió en entry1 ni en entry2
    if event.widget != entry1 and event.widget:
        root.after(1, lambda: root.focus())  ## Mueve el foco al widget principal (ventana)

# Configuración de la ventana principal
root = ttk.Window(themename="solar")  # Usa un tema moderno de ttkbootstrap
root.title("Facturas")
root.geometry("300x360")
root.resizable(False, False)

# Vincular el evento de clic en la ventana para deseleccionar botones
root.bind("<Button-1>", deseleccionar)

ventana = Ventana()  # Instancia de la clase Ventana

# Crear el Notebook (pestañas)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Estilo para los botones
style = ttk.Style()
style.configure("TButton", font=("Arial", 13, "bold"))  # Doble tamaño de letra y negritas

# Abrir web
test_instance = UnitTest()

# Pestaña de Ejecución
frame_ejecucion = ttk.Frame(notebook)  # Fondo azul claro
notebook.add(frame_ejecucion, text="Ejecución automática")

# Crear un hilo para ejecutar la función setUp
def ejecutar_setUp_en_hilo():
    threading.Thread(target=test_instance.setUp).start()

# Botón que llama a la función setUp en un hilo
button1 = ttk.Button(
    frame_ejecucion,
    text="Abrir web",
    command=ejecutar_setUp_en_hilo,
    bootstyle="PRIMARY"
)
button1.pack(pady=10, anchor="center")  # Centrado con padding

# Botón que llama a la función auto en un hilo
def ejecutar_auto_n_veces(valor, boton=None):
    """Ejecuta la función auto n veces, con un valor fijo o aleatorio."""
    try:
        n = int(valor)  # Convertir el valor ingresado a entero
        if n <= 0:
            root.after(0, lambda: messagebox.showwarning("Advertencia", "Por favor, ingresa un número mayor a 0."))
            return

        # Deshabilitar el botón mientras se ejecutan los bucles
        if boton:
            root.after(0, lambda: boton.config(state="disabled"))

        # Verificar si el navegador está abierto antes de ejecutar el bucle
        if test_instance.driver is None:
            root.after(0, lambda: messagebox.showwarning("Advertencia", "El navegador no está abierto. Presiona 'Abrir web' primero."))
            if boton:
                root.after(0, lambda: boton.config(state="normal"))  # Rehabilitar el botón si hay un error
            return

        # Ejecutar la función auto n veces
        for _ in range(n):
            if ventana.cerrando:  # Verificar si la aplicación se está cerrando
                break
            if combo.get() == "39":
                test_instance.auto(r=39)           
            else:
                test_instance.auto(r=random.randint(35, 38))  

    except ValueError:
        if not ventana.cerrando:  # Solo mostrar el error si la aplicación no se está cerrando
            root.after(0, lambda: messagebox.showerror("Error", "Por favor, ingresa un número válido."))
    finally:
        # Rehabilitar el botón después de completar la ejecución
        if boton:
            root.after(0, lambda: boton.config(state="normal"))

# Validación para que solo se acepten números en los Entry
def solo_numeros(texto):
    # Permitir que el campo esté vacío temporalmente
    return texto.isdigit() or texto == ""

# Crear validación para los Entry
validacion = root.register(solo_numeros)

# Etiqueta y Entry para el botón 2 (valor fijo)
label1 = ttk.Label(
    frame_ejecucion,
    text="Cantidad de productos",
    font=("Arial", 12),
    bootstyle="info"  # Aplica un estilo del tema
)
label1.pack(ipady=5)

# Crear el Combobox y vincular el evento
combo = ttk.Combobox(
    frame_ejecucion,
    width=5,
    state="readonly",
    values=["39", "35-38"],
    justify="center"
)
combo.set("39")  # Valor predeterminado
combo.pack(pady=(5, 30))  # Espacio adicional debajo del Combobox

# Segundo Label
label1 = ttk.Label(
    frame_ejecucion,
    text="Número de facturas",
    font=("Arial", 12),
    bootstyle="info"  # Aplica un estilo del tema
)
label1.pack(pady=5)  # Espacio estándar para el Label

# Función para reiniciar el Entry cuando cambie la selección del Combobox
def reiniciar_entry(event):
    entry1.delete(0, "end")  # Borra el contenido actual del Entry
    entry1.insert(0, "1")  # Inserta el valor "1"

# Vincular el evento <<ComboboxSelected>> al Combobox
combo.bind("<<ComboboxSelected>>", reiniciar_entry)

# Crear el Entry con texto centrado
entry1 = ttk.Entry(
    frame_ejecucion,
    validate="key",
    validatecommand=(validacion, "%P"),
    justify="center",  # Centrar el texto dentro del Entry
    width=15
)
entry1.pack(pady=10, anchor="center")

button_auto_fijo = ttk.Button(
    frame_ejecucion,
    text="Ejecutar",
        command=lambda: threading.Thread(target=ejecutar_auto_n_veces, args=(entry1.get(), button_auto_fijo)).start(), 
    bootstyle="SUCCESS"
)
button_auto_fijo.pack(pady=10)

# Etiqueta para mostrar el contador de facturas realizadas
ventana.contador_label = ttk.Label(
    root,
    text="Facturas realizadas: 0",
    font=("Arial", 12),
    bootstyle="success"  # Aplica un estilo del tema
)
ventana.contador_label.pack(pady=10)

# Configurar el cierre de la ventana
root.protocol("WM_DELETE_WINDOW", ventana.on_close)

# Ejecutar la aplicación
root.attributes("-topmost", True)
root.mainloop()
