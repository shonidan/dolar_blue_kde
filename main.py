import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction, QPixmap, QPainter
from PyQt6.QtCore import Qt
import requests
from bs4 import BeautifulSoup
import re

def create_icon_with_emoji(emoji):
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setPen(Qt.GlobalColor.black)
    font = painter.font()
    font.setPointSize(32)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, emoji)
    painter.end()
    return QIcon(pixmap)

def obtener_valores_dolar_blue():
    url = "https://dolarhoy.com/i/cotizaciones/dolar-blue"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        compra_element = soup.select_one('div.iframe-cotizaciones__container > div.container__data > div > p:nth-child(1)')
        venta_element = soup.select_one('div.iframe-cotizaciones__container > div.container__data > div > p:nth-child(2)')

        if compra_element and venta_element:
            valor_compra = re.findall(r'\d+\.\d+', compra_element.text.strip())
            valor_venta = re.findall(r'\d+\.\d+', venta_element.text.strip())

            if valor_compra and valor_venta:
                return f"Compra: {valor_compra[0]}\nVenta: {valor_venta[0]}"

    return None

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Dolar Blue")

    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("El sistema no soporta íconos en la bandeja")
        sys.exit(1)

    QApplication.setQuitOnLastWindowClosed(False)
    tray_icon = QSystemTrayIcon()
    tray_icon.setIcon(create_icon_with_emoji("💲"))
    menu = QMenu()
    quit_action = QAction("Salir")
    quit_action.triggered.connect(QApplication.quit)
    menu.addAction(quit_action)
    tray_icon.setContextMenu(menu)
    tray_icon.show()
    def show_dollar_value():
        valor_dolar_blue = obtener_valores_dolar_blue()
        if valor_dolar_blue:
            tray_icon.showMessage("Valor del Dólar Blue", valor_dolar_blue)
        else:
            tray_icon.showMessage("Error", "No se pudo obtener el valor del dólar blue.")

    tray_icon.activated.connect(lambda reason: show_dollar_value() if reason == QSystemTrayIcon.ActivationReason.Trigger else None)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
