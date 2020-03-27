"""Added VehicleYear table

Revision ID: c4463d847749
Revises: b158bad8f9ee
Create Date: 2020-03-27 14:42:11.387934

"""
from alembic import op
import sqlalchemy as sa
import tksqla.migration_types


# revision identifiers, used by Alembic.
revision = 'c4463d847749'
down_revision = 'b158bad8f9ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tksqla_vehicleyear',
    sa.Column('id', tksqla.migration_types.Integer(), nullable=False),
    sa.Column('vehicletrim_id', tksqla.migration_types.Integer(), nullable=False),
    sa.Column('year', tksqla.migration_types.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['vehicletrim_id'], ['tksqla_vehicletrim.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('year', 'vehicletrim_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tksqla_vehicleyear')
    # ### end Alembic commands ###