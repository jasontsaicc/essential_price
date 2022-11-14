from tgi102_flask import sa, BASE, relationship


class Mart(BASE):
    __tablename__ = 'marts'
    id = sa.Column(sa.String(64), primary_key=True)
    mart_name = sa.Column(sa.String(64), unique=True)

    fk_product_mart = relationship('Product')

    def __repr__(self):
        return f"id={self.id}, mart_name={self.mart_name}"