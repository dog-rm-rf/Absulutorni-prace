# Co jsem se naučil

## Týden 1 - Python základy

### Filtrování dat
funkce pro filtrování
list comprehensions
porozumění funkcím(__init__)

Příklady mého kódu:
- filter_completed() - funguje
- filter_by_week() - funguje
- filter_high_rated() - funguje

### Kam to směřuje:
- Později to použiju pro kalendářový view
- Pro statistiky completion rate
- Pro weekly review

### Co ještě nerozumím:
- (sem si piš otázky)


# PYQT

## things i learnt

- app = QApplication(sys.argv)# this holds the event loop, can be only one instance of this object
- class MainWindow(QMainWindow): # qmainwindow is parent
- super().__init__()# we calling the init from the qmainwindow
- signals are notifications emitted by widgets when something happens
- slots are receivers of signals
- button.setCheckable(True) = This makes the button a toggle button that stays pressed/unpressed. It changes the button's visual state, allowing it to be "checked" (pressed down) or "unchecked" (normal state)

