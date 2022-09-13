from tgi102_flask import sa, BASE, relationship


class Price(BASE):
    __tablename__ = 'price'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    # product_id = sa.Column(sa.Integer)
    date = sa.Column(sa.Date)
    price = sa.Column(sa.Integer)

    product_id = sa.Column(sa.Integer, sa.ForeignKey('product.id'))
