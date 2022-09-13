from tgi102_flask.app.py import sa, BASE, relationship



class Category(BASE):
    __tablename__ = 'category'
    id = sa.Column(sa.String(64), primary_key=True)
    category_name = sa.Column(sa.String(64), unique=True, )

    fk_product_category = relationship('Product')