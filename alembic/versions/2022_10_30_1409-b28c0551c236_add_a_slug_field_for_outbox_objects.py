"""Add a slug field for outbox objects

Revision ID: b28c0551c236
Revises: 604d125ea2fb
Create Date: 2022-10-30 14:09:14.540461+00:00

"""
import sqlalchemy as sa
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from alembic import op

# revision identifiers, used by Alembic.
revision = 'b28c0551c236'
down_revision = '604d125ea2fb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('outbox', schema=None) as batch_op:
        batch_op.add_column(sa.Column('slug', sa.String(), nullable=True))
        batch_op.create_index(batch_op.f('ix_outbox_slug'), ['slug'], unique=False)

    # ### end Alembic commands ###

    # Backfill the slug for existing articles
    from app.models import OutboxObject
    from app.utils.text import slugify
    sess = Session(op.get_bind())
    articles = sess.execute(select(OutboxObject).where(
        OutboxObject.ap_type == "Article")
    ).scalars()
    for article in articles:
        title = article.ap_object["name"]
        article.slug = slugify(title)
    sess.commit()


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('outbox', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_outbox_slug'))
        batch_op.drop_column('slug')

    # ### end Alembic commands ###
