"""Added tables for Asset, AssetVehicle

Revision ID: a11a0b560384
Revises: c4463d847749
Create Date: 2020-03-27 23:49:09.375735

"""
from alembic import op
import sqlalchemy as sa
import tksqla.migration_types


# revision identifiers, used by Alembic.
revision = 'a11a0b560384'
down_revision = 'c4463d847749'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tksqla_asset',
    sa.Column('id', tksqla.migration_types.Integer(), nullable=False),
    sa.Column('assettype', sa.Enum('vehicle', name='assettypeenum'), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tksqla_asset_vehicle',
    sa.Column('id', tksqla.migration_types.Integer(), nullable=False),
    sa.Column('vehicleyear_id', tksqla.migration_types.Integer(), nullable=False),
    sa.Column('vin', tksqla.migration_types.String(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['tksqla_asset.id'], ),
    sa.ForeignKeyConstraint(['vehicleyear_id'], ['tksqla_vehicleyear.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('vin')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tksqla_asset_vehicle')
    op.drop_table('tksqla_asset')
    # ### end Alembic commands ###