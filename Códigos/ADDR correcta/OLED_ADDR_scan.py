from machine import Pin, I2C
import time
import ssd1306

# 1. Configurar I2C(1) en GP14 (SDA) y GP15 (SCL)
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=100000)

# 2. Escanear bus para obtener la dirección real
dispositivos = i2c.scan()
print("Dispositivos I2C encontrados:", [hex(d) for d in dispositivos])

if not dispositivos:
    print("❌ No se detectó la pantalla en el bus I2C.")
else:
    addr = dispositivos[0]
    print(f"✅ Usando dirección: {hex(addr)}")
    
    # 3. Inicializar pantalla
    oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=addr)
    
    # 4. Configuración de prueba de fuerza (Máximo brillo e inversión)
    oled.contrast(255) # Contraste al 100%
    oled.invert(1)     # Invertir pantalla (fondo blanco para forzar luz)
    oled.fill(1)       # Llenar todo de píxeles activos
    
    # 5. Enviar a la pantalla
    oled.show()
    print("✅ Comando de pantalla en blanco/invertida enviado.")