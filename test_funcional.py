"""Prueba FUNCIONAL PF-01 — casos CP-F01 (login) y CP-F02 (checkout/stock).
ACA Final Calidad de Software. Ejecucion: pytest -v
"""
import pytest
from minitienda import MiniTienda


def tienda_base() -> MiniTienda:
    t = MiniTienda()
    t.registrar_usuario("laura", "cun2026*")
    return t


# CP-F01: autenticacion
def test_cp_f01_login_valido():
    t = tienda_base()
    assert t.login("laura", "cun2026*") is True
    assert t.sesion is not None and t.sesion.username == "laura"


def test_cp_f01_login_invalido_rechazado():
    t = tienda_base()
    assert t.login("laura", "clave_mala") is False
    assert t.login("nadie", "cun2026*") is False


def test_cp_f01_clave_corta_rechazada():
    t = MiniTienda()
    with pytest.raises(ValueError, match="minimo 6"):
        t.registrar_usuario("pedro", "123")


# CP-F02: checkout y stock
def test_cp_f02_checkout_calcula_total_y_descuenta_stock():
    t = tienda_base()
    assert t.login("laura", "cun2026*")
    arroz = t.agregar_producto("Arroz 1kg", 5200, 20)
    cafe = t.agregar_producto("Cafe 500g", 18500, 10)
    t.agregar_al_carrito(arroz.id, 2)  # 10.400
    t.agregar_al_carrito(cafe.id, 1)   # 18.500
    assert t.total_carrito() == 28900.00
    venta = t.checkout()
    assert venta["total"] == 28900.00
    assert t.productos[arroz.id].stock == 18
    assert t.carrito == {}


def test_cp_f02_stock_insuficiente_bloquea():
    t = tienda_base()
    assert t.login("laura", "cun2026*")
    pan = t.agregar_producto("Pan x5", 8000, 3)
    with pytest.raises(ValueError, match="Stock insuficiente"):
        t.agregar_al_carrito(pan.id, 5)


def test_cp_f02_checkout_carrito_vacio_bloquea():
    t = tienda_base()
    assert t.login("laura", "cun2026*")
    with pytest.raises(ValueError, match="vacio"):
        t.checkout()


def test_cp_f02_precio_invalido_rechazado():
    t = tienda_base()
    assert t.login("laura", "cun2026*")
    with pytest.raises(ValueError, match="mayor a 0"):
        t.agregar_producto("Mal", -100, 5)
