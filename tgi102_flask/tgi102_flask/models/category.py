from tgi102_flask import sa, BASE, relationship



class Category(BASE):
    __tablename__ = 'category'
    id = sa.Column(sa.String(64), primary_key=True)
    category_name = sa.Column(sa.String(64), unique=True, )

    fk_product_category = relationship('Product')

    def __repr__(self):
        return f"id={self.id}, category_name={self.category_name}"
