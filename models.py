from sqlalchemy import ForeignKey, Integer, String, MetaData
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Model


class Address(Model):
    __tablename__ = 'addresses'
    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(64))
    city: Mapped[str] = mapped_column(String(64))
    street: Mapped[str] = mapped_column(String(64))
    building: Mapped[str] = mapped_column(String(64))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    user: Mapped['User'] = relationship(lazy='joined', innerjoin=True, back_populates='addresses')

    def __repr__(self):
        return f'Address({self.id}, "{self.country}", "{self.city}", "{self.street}", "{self.building}",)'


class UserRole(Model):
    __tablename__ = 'users_roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    role_type: Mapped[int] = mapped_column(Integer)  # 1-Free, 2-Paid
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), index=True)
    user: Mapped['User'] = relationship(lazy='joined', innerjoin=True, back_populates='users_roles')

    def __repr__(self):
        return f'UserRole({self.id}, "{self.role_type}",)'


class Order(Model):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[int] = mapped_column(Integer)  # 1-Created,2-Payd,3-Canceled
    total: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), index=True)
    user: Mapped['User'] = relationship(lazy='joined', innerjoin=True, back_populates='orders')

    def __repr__(self):
        return f'Order({self.id}, "{self.total}",)'


class User(Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64))

    addresses: Mapped[list['Address']] = relationship(lazy='selectin', cascade='all, delete-orphan', back_populates='user')
    users_roles: Mapped[list['UserRole']] = relationship(lazy='selectin', cascade='all, delete-orphan', back_populates='user')
    orders: Mapped[list['Order']] = relationship(lazy='selectin', cascade='all, delete-orphan', back_populates='user')

    def __repr__(self):
        return f'User({self.id}, "{self.first_name}", "{self.last_name}")'
