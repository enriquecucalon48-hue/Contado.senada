from sqlalchemy.orm import Session

from database.models.gasto import Gasto


class GastoRepository:

    @staticmethod
    def crear(
        db: Session,
        concepto: str,
        categoria: str,
        monto: float,
    ):
        gasto = Gasto(
            concepto=concepto,
            categoria=categoria,
            monto=monto,
        )

        db.add(gasto)
        db.commit()
        db.refresh(gasto)

        return gasto

    @staticmethod
    def listar(
        db: Session,
    ):
        return (
            db.query(Gasto)
            .order_by(
                Gasto.fecha.desc(),
            )
            .all()
        )

    @staticmethod
    def obtener_por_id(
        db: Session,
        gasto_id: int,
    ):
        return db.get(
            Gasto,
            gasto_id,
        )

    @staticmethod
    def listar(
            db: Session,
    ):
        return (
            db.query(Gasto)
            .order_by(
                Gasto.fecha.desc(),
            )
            .all()
        )
    @staticmethod
    def eliminar(
        db: Session,
        gasto: Gasto,
    ):
        db.delete(gasto)
        db.commit()

    @staticmethod
    def obtener_por_id(
        db: Session,
        gasto_id: int,
    ):
        return (
            db.query(Gasto)
            .filter(Gasto.id == gasto_id)
            .first()
        )