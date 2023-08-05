import logging
from typing import Any

from quart import render_template

log = logging.getLogger(__name__)


async def send_email(to: str, subject: str, template: str, ctx: [dict, Any]):
    content = await render_template(template, **ctx)
    log.info("Sending email %s to %s \n %s", template, to, content)
