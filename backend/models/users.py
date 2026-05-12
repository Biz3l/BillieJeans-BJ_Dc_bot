import sqlalchemy as sa
from db import metadata

users = sa.Table('users',
                 metadata,
                 sa.Column('id', sa.Integer, autoincrement=True, primary_key=True, unique=True, nullable=False),
                 sa.Column('discord_id', sa.BigInteger, unique=True, nullable=False),
                 sa.Column('coins', sa.Integer, nullable=False),
                 sa.Column('joined_at', sa.DateTime, nullable=True),
                 )