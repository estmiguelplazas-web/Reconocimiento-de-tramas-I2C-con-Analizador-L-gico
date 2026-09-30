# Reconocimiento de Tramas I2C con Analizador Lógico

## Autores

* **Daniel Mateo Alegría Bernate**
* **Miguel Ángel Plazas Llanes**

**Ingeniería de Telecomunicaciones**  
**Universidad Militar Nueva Granada**  
**Docente:** José de Jesús Rúgeles Uribe

---

## Reconocimiento de Tramas I2C con Analizador Lógico y Raspberry Pi Pico 2W

Este repositorio contiene el desarrollo de la Práctica 3 de Comunicaciones Digitales de la carrera de Ingeniería de Telecomunicaciones en la Universidad Militar Nueva Granada.  
En esta práctica se analizó experimentalmente el proceso de comunicación serial mediante el protocolo **I2C**, utilizando el periférico I2C de la **Raspberry Pi Pico 2W** (programada en MicroPython), una pantalla **OLED SSD1306** (dirección `0x3C`) y un analizador lógico **Saleae Logic 2**.

Se estudió la estructura física y temporal de la trama I2C (condiciones de *Start* y *Stop*, dirección de 7 bits, bit de lectura/escritura R/W y el ciclo de respuesta ACK/NACK). Asimismo, se caracterizó experimentalmente la frecuencia del reloj (SCL), se validó el direccionamiento mediante escaneo automático por software (`i2c.scan()`) y se correlacionaron las instrucciones de software con los comandos hexadecimales enviados al controlador SSD1306.

---

## Objetivos

### Objetivo general
Analizar e identificar experimentalmente la estructura de las tramas de comunicación en el bus I2C mediante el uso de un analizador lógico, evaluando la temporización del reloj SCL, la respuesta de reconocimiento (ACK/NACK), el escaneo de direcciones y el intercambio de comandos/datos con un dispositivo esclavo (pantalla OLED SSD1306).

### Objetivos específicos
* Identificar visualmente los elementos de la trama I2C (*Start*, dirección de 7 bits, bit R/W, bit ACK/NACK y *Stop*) en capturas digitales del analizador lógico.
* Comprobar experimentalmente la diferencia entre las respuestas **ACK** y **NACK** al transmitir direcciones válidas (`0x3C`) e inválidas (`0x3D`).
* Caracterizar la señal de reloj SCL, midiendo su frecuencia experimental y calculando el error relativo respecto a la frecuencia nominal de 100 kHz.
* Confirmar la dirección física del periférico esclavo mediante un algoritmo de escaneo automático por software (`i2c.scan()`).
* Mapear las instrucciones enviadas desde MicroPython con los códigos hexadecimales transmitidos hacia la pantalla OLED para la gestión de comandos y datos en la memoria GDDRAM.

---

## Parámetros de la práctica

| Parámetro | Valor |
| :--- | :--- |
| **Microcontrolador** | Raspberry Pi Pico 2W (RP2350) |
| **Líneas del Bus I2C** | I2C0: SCL (GP15 / Pin 20), SDA (GP14 / Pin 19) |
| **Dispositivo Esclavo** | Pantalla OLED SSD1306 (`0x3C`) |
| **Frecuencia Nominal Bus (SCL)** | 100 kHz (`freq=100000`) |
| **Analizador Lógico** | Saleae Logic 2 |
| **Canales de Captura** | CH0 → SCL, CH1 → SDA |
| **Tasa de Muestreo (Logic 2)** | 1 MS/s ($10\times$ la frecuencia nominal) |
| **Lenguajes y Entorno** | MicroPython / Thonny IDE |

---

## Metodología

### 1. Configuración de Hardware y Monitoreo del Bus
Se conectó la pantalla OLED SSD1306 al bus I2C0 de la Raspberry Pi Pico 2W y se derivaron los canales CH0 y CH1 del analizador lógico en paralelo hacia las líneas SCL y SDA.
La conexión utilizada fue:
* **SCL:** GP15 (Pin 20) ↔ CH0 Analizador Lógico ↔ SCL OLED
* **SDA:** GP14 (Pin 19) ↔ CH1 Analizador Lógico ↔ SDA OLED
* **Alimentación:** 3.3V (Pin 36) y GND común (Pin 3 o Pin 38)

### 2. Prueba de Reconocimiento y Detección de ACK/NACK
Se ejecutó el script `OLED_ADDR_test.py` configurado a 100 kHz. Se inyectaron tramas con dos direcciones distintas para evaluar el noveno ciclo de reloj en la línea SDA:
* **Dirección `0x3C`:** Dispositivo presente, verificando la respuesta de nivel bajo (**ACK**).
* **Dirección `0x3D`:** Dirección inexistente, verificando el estado de nivel alto (**NACK**) provocado por los resistores de *pull-up*.

### 3. Caracterización del Reloj (SCL) y Medición de Frecuencia
Mediante el analizador lógico, se realizaron mediciones del periodo $T_{\text{SCL}}$ sobre los pulsos de reloj capturados en el bus para calcular la frecuencia real $f_{\text{SCL}}$ y determinar el error relativo respecto al valor nominal de 100 kHz:
$$Error\,\% = \left\vert{} \frac{f_{\text{nominal}} - f_{\text{medida}}}{f_{\text{nominal}}} \right\vert{} \times 100$$

### 4. Escaneo Automático de Direcciones (`i2c.scan()`)
Se ejecutó el script `scan_i2c_addr.py` para barrer las 112 direcciones posibles del bus comprende entre `0x08` y `0x77`, registrando las direcciones que respondieron con ACK para su validación por software.

### 5. Decodificación de Comandos del Controlador SSD1306
A través de `OLED_demo_menu.py`, se enviaron secuencias de control y datos hacia la pantalla OLED, identificando las tramas hexadecimales correspondientes a encendido/apagado, contraste, inversión de imagen y escritura en GDDRAM.

---

## Resultados y Análisis

### Análisis de la Respuesta del Bus y Caracterización de Señal

| Parámetro Evaluado | Valor Teórico / Esperado | Valor Experimental / Obtenido | Estado / Error |
| :--- | :--- | :--- | :--- |
| **Respuesta Dirección `0x3C`** | ACK (SDA en 0) | ACK (Octeto `0x78`) | Validado |
| **Respuesta Dirección `0x3D`** | NACK (SDA en 1) | NACK (Octeto `0x7A`) | Validado |
| **Frecuencia del Reloj SCL** | 100.0 kHz | 81.8 kHz | Error del 18.2 % |
| **Rango de Escaneo `i2c.scan()`**| 112 direcciones (`0x08`–`0x77`)| Dirección activa: `0x3C` | Validado |

### Comandos de Control Identificados (SSD1306)

| Función | Código Hexadecimal | Descripción en Trama I2C |
| :--- | :--- | :--- |
| **Apagar Pantalla** | `0xAE` | Byte de comando de apagado del panel. |
| **Encender Pantalla** | `0xAF` | Byte de comando de encendido del panel. |
| **Ajuste de Contraste** | `0x81` + valor | Comando de dos bytes para definir el nivel de corriente. |
| **Inversión / Modo Normal** | `0xA7` / `0xA6` | Alterna entre visualización invertida y normal. |
| **Envío de Datos (GDDRAM)**| `0x40` + datos | Byte de control indicando que los siguientes bytes son datos de vídeo. |

---

## Desarrollo

- [ ] Capturas Logic 2 
- [ ] Códigos
- [ ] Informe
- [ ] Capturas Analizador Lógico
- [ ] Códigos
- [ ] Informe
