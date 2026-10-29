"""Authorization shared by changing and paid services."""

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import Unauthorized


async def require_admin(hass: HomeAssistant, call: ServiceCall) -> None:
    """Changing and paid services are for administrators, like the panel. Calls
    without a user (automations, scripts) are allowed."""
    if not (user_id := call.context.user_id):
        return
    user = await hass.auth.async_get_user(user_id)
    if user is None or not user.is_admin:
        raise Unauthorized(context=call.context)
