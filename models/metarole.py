from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.exceptions import NoValuesFetched
from tortoise.models import Model

if TYPE_CHECKING:
    from models import Condition


class Metarole(Model):
    id = fields.IntField(pk=True)
    guild = fields.IntField()
    enabled = fields.BooleanField()
    conditions: fields.ReverseRelation["Condition"]

    async def is_eligible(self, member_roles: list[int]):
        try:
            required = await self.conditions.filter(type=1).values_list("id", flat=True)
            forbidden = await self.conditions.filter(type=-1).values_list(
                "id", flat=True
            )
            if all([role in member_roles for role in required]) and not any(
                [role in member_roles for role in forbidden]
            ):
                return True
            return False
        except NoValuesFetched:
            return False
