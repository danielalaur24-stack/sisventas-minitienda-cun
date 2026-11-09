"""
SISVENTAS MiniTienda CUN — Sistema de Gestion de Ventas simple.
Modulo academico para ACA Final Calidad de Software (CUN).
Autor: Laura Daniela Losada Ibata.
Sin dependencias externas (solo stdlib).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Producto:
    id: int
    nombre: str
    precio: float
    stock: int


@dataclass
class Usuario:
    username: str
    password: str  # NOTA academica: en produccion usar hash + salt (ver riesgos)
    rol: str = "vendedor"


class MiniTienda:
    """Nucleo del sistema: auth + inventario + carrito + checkout."""

    def __init__(self) -> None:
        self.usuarios: dict[str, Usuario] = {}
        self.productos: dict[int, Producto] = {}
        self.carrito: dict[int, int] = {}  # producto_id -> cantidad
        self.sesion: Usuario | None = None
        self._next_id = 1
        self.ventas: list[dict] = []

    # --- Auth ---
    def registrar_usuario(self, username: str, password: str, rol: str = "vendedor") -> Usuario:
        if not username or not username.strip():
            raise ValueError("El nombre de usuario es obligatorio.")
        if len(password) < 6:
            raise ValueError("La clave debe tener minimo 6 caracteres.")
        if username in self.usuarios:
            raise ValueError(f"El usuario '{username}' ya existe.")
        u = Usuario(username=username.strip(), password=password, rol=rol)
        self.usuarios[username.strip()] = u
        return u

    def login(self, username: str, password: str) -> bool:
        u = self.usuarios.get((username or "").strip())
        if u and u.password == password:
            self.sesion = u
            return True
        return False

    def logout(self) -> None:
        self.sesion = None
        self.carrito.clear()

    def _exigir_sesion(self) -> None:
        if not self.sesion:
            raise PermissionError("Debe iniciar sesion para operar.")

    # --- Inventario ---
    def agregar_producto(self, nombre: str, precio: float, stock: int) -> Producto:
        self._exigir_sesion()
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto es obligatorio.")
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        p = Producto(id=self._next_id, nombre=nombre.strip(), precio=float(precio), stock=int(stock))
        self.productos[p.id] = p
        self._next_id += 1
        return p

    def buscar_producto(self, texto: str) -> list[Producto]:
        t = (texto or "").lower()
        return [p for p in self.productos.values() if t in p.nombre.lower()]

    # --- Carrito / ventas ---
    def agregar_al_carrito(self, producto_id: int, cantidad: int) -> None:
        self._exigir_sesion()
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        p = self.productos.get(producto_id)
        if not p:
            raise KeyError(f"Producto id={producto_id} no existe.")
        actual = self.carrito.get(producto_id, 0)
        if actual + cantidad > p.stock:
            raise ValueError(
                f"Stock insuficiente para '{p.nombre}': "
                f"solicitado {actual + cantidad}, disponible {p.stock}."
            )
        self.carrito[producto_id] = actual + cantidad

    def total_carrito(self) -> float:
        return round(sum(self.productos[pid].precio * cant for pid, cant in self.carrito.items()), 2)

    def checkout(self) -> dict:
        self._exigir_sesion()
        if not self.carrito:
            raise ValueError("El carrito esta vacio.")
        # Revalidar stock antes de confirmar (control de concurrencia basico)
        for pid, cant in self.carrito.items():
            if cant > self.productos[pid].stock:
                raise ValueError(f"Stock insuficiente para '{self.productos[pid].nombre}'.")
        assert self.sesion is not None
        vendedor = self.sesion.username
        total = self.total_carrito()
        detalle = []
        for pid, cant in self.carrito.items():
            p = self.productos[pid]
            p.stock -= cant
            detalle.append({"producto": p.nombre, "cantidad": cant, "subtotal": round(p.precio * cant, 2)})
        venta = {"vendedor": vendedor, "total": total, "detalle": detalle}
        self.ventas.append(venta)
        self.carrito.clear()
        return venta


def demo() -> None:
    t = MiniTienda()
    t.registrar_usuario("laura", "cun2026*")
    assert t.login("laura", "cun2026*")
    arroz = t.agregar_producto("Arroz 1kg", 5200, 20)
    cafe = t.agregar_producto("Cafe 500g", 18500, 10)
    t.agregar_al_carrito(arroz.id, 2)
    t.agregar_al_carrito(cafe.id, 1)
    print(f"Total carrito: ${t.total_carrito():,.2f}")
    venta = t.checkout()
    print(f"Venta registrada: total=${venta['total']:,.2f} vendedor={venta['vendedor']}")
    print(f"Stock restante Arroz: {t.productos[arroz.id].stock}")


if __name__ == "__main__":
    demo()
