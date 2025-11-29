# migrations/versions/001_initial.py
"""initial

Revision ID: 001_initial
Revises:
Create Date: 2025-11-29 13:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Категории: Id, имя
    op.create_table('categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    # Модель: Id, имя
    op.create_table('models',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    # Производства: Id, имя
    op.create_table('manufacturers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')

    )
    # Страна: Id, имя
    op.create_table('countries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    # Характеристики (чистые): Id, имя
    op.create_table('characteristic_keys_base',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    # Характеристики (из файла): Id, имя
    op.create_table('characteristic_keys',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    # Единицы измерения: Id, имя
    op.create_table('units',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('symbol')
    )
    # Значения характеристик: Id, имя
    op.create_table('characteristic_values',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('key_id', sa.Integer(), nullable=False),
        sa.Column('value_text', sa.Text(), nullable=False),
        sa.Column('unit_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['key_id'], ['characteristic_keys_base.id']),
        sa.ForeignKeyConstraint(['unit_id'], ['units.id']),
        sa.PrimaryKeyConstraint('id')
    )
    # Таблица с основными данными об СТЕ
    op.create_table('spu_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('spu_external_id', sa.Text(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('image_url', sa.Text(), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('model_id', sa.Integer(), nullable=True),
        sa.Column('manufacturer_id', sa.Integer(), nullable=True),
        sa.Column('country_id', sa.Integer(), nullable=True),
        sa.Column('normalized_name', sa.Text(), nullable=True),
        sa.Column('normalized_category', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id']),
        sa.ForeignKeyConstraint(['country_id'], ['countries.id']),
        sa.ForeignKeyConstraint(['manufacturer_id'], ['manufacturers.id']),
        sa.ForeignKeyConstraint(['model_id'], ['models.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('spu_external_id')
    )
    # Один ко многим. Связь между СТЕ и характеристиками
    op.create_table('spu_characteristics',
        sa.Column('spu_id', sa.Integer(), nullable=False),
        sa.Column('char_value_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['char_value_id'], ['characteristic_values.id']),
        sa.ForeignKeyConstraint(['spu_id'], ['spu_data.id']),
        sa.PrimaryKeyConstraint('spu_id', 'char_value_id')
    )

def downgrade():
    op.drop_table('spu_characteristics')
    op.drop_table('spu_data')
    op.drop_table('characteristic_values')
    op.drop_table('units')
    op.drop_table('characteristic_keys_base')
    op.drop_table('characteristic_keys')
    op.drop_table('countries')
    op.drop_table('manufacturers')
    op.drop_table('models')
    op.drop_table('categories')