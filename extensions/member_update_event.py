from interactions import Extension, listen
from interactions.api.events import MemberUpdate
from interactions.client.utils import get

from core.base import CustomClient
from models import Metarole


class MemberUpdateEvent(Extension):
    bot: CustomClient

    @listen()
    async def on_member_update(self, event: MemberUpdate):
        roles_before = set(event.before.roles) if event.before.roles else set()
        roles_after = set(event.after.roles) if event.after.roles else set()
        role_updated = list(roles_before.symmetric_difference(roles_after))[0]
        self.bot.logger.debug(f"Role updated : {role_updated}")
        metaroles = await Metarole.filter(
            guild=int(event.guild.id), enabled=True, conditions__id=role_updated
        )
        for metarole in metaroles:
            await self.bot.check_metarole(metarole, [event.after])


def setup(bot: CustomClient):
    """Let naff load the extension"""

    MemberUpdateEvent(bot)
