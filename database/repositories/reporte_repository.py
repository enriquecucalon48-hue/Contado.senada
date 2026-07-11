from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime, date
from database.models.cliente import Cliente
from database.models.producto import Producto
from database.models.venta import Venta
from database.models.pago import Pago

class ReporteRepository:

    @staticmethod
    def total_clientes(
        db: Session,
    ):
        return (
            db.query(
                func.count(Cliente.id)
            )
            .scalar()
        )

    @staticmethod
    def total_productos(
        db: Session,
    ):
        return (
            db.query(
                func.count(Producto.id)
            )
            .scalar()
        )

    @staticmethod
    def total_ventas(
        db: Session,
    ):
        return (
            db.query(
                func.count(Venta.id)
            )
            .scalar()
        )

    @staticmethod
    def ventas_hoy(
        db: Session,
    ):
        return (
            db.query(
                func.coalesce(
                    func.sum(Venta.total),
                    0,
                )
            )
            .filter(
                func.date(Venta.fecha) == date.today()
            )
            .scalar()
        )

    @staticmethod
    def ventas_mes(
        db: Session,
    ):
        hoy = datetime.now()

        return (
            db.query(
                func.coalesce(
                    func.sum(Venta.total),
                    0,
                )
            )
            .filter(
                func.extract(
                    "year",
                    Venta.fecha,
                ) == hoy.year
            )
            .filter(
                func.extract(
                    "month",
                    Venta.fecha,
                ) == hoy.month
            )
            .scalar()
        )

    @staticmethod
    def productos_stock_bajo(
        db: Session,
    ):
        return (
            db.query(
                func.count(Producto.id)
            )
            .filter(
                Producto.stock <= 5
            )
            .scalar()
        )


    @staticmethod
    def saldo_pendiente(
        db: Session,
    ):
        total_ventas = (
            db.query(
                func.coalesce(
                    func.sum(Venta.total),
                    0,
                )
            )
            .scalar()
        )

        total_pagos = (
            db.query(
                func.coalesce(
                    func.sum(Pago.monto),
                    0,
                )
            )
            .scalar()
        )

        return float(total_ventas) - float(total_pagos)

    @staticmethod
    def clientes_con_deuda(
        db: Session,
    ):
        clientes = db.query(Cliente).all()

        resultado = []

        for cliente in clientes:

            total_vendido = (
                db.query(
                    func.coalesce(
                        func.sum(Venta.total),
                        0,
                    )
                )
                .filter(
                    Venta.cliente_id == cliente.id,
                )
                .scalar()
            )

            total_pagado = (
                db.query(
                    func.coalesce(
                        func.sum(Pago.monto),
                        0,
                    )
                )
                .join(
                    Venta,
                    Pago.venta_id == Venta.id,
                )
                .filter(
                    Venta.cliente_id == cliente.id,
                )
                .scalar()
            )

            deuda = float(total_vendido) - float(total_pagado)

            if deuda > 0:

                resultado.append(
                    {
                        "cliente": cliente,
                        "vendido": float(total_vendido),
                        "pagado": float(total_pagado),
                        "deuda": deuda,
                    }
                )

        return resultado
