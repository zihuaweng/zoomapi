"""Zoom.us REST API Python Client -- Chat Messages component"""

from zoomapi.util import Throttled, require_keys
from zoomapi.components import base


class ChatChannelsComponentV2(base.BaseComponent):
    """Component dealing with all chat channels related matters"""

    @Throttled
    def list(self, **kwargs):
        return self.get_request("/chat/users/me/channels", params=kwargs)

    def create(self, **kwargs):
        return self.post_request("/chat/users/me/channels", data=kwargs)

    def get(self, **kwargs):
        require_keys(kwargs, "channelId")
        return self.get_request("/chat/channels/{}".format(kwargs.get("channelId")), params=kwargs)

    def update(self, **kwargs):
        require_keys(kwargs, "channelId")
        return self.patch_request("/chat/channels/{}".format(kwargs.get("channelId")), data=kwargs)

    def delete(self, **kwargs):
        require_keys(kwargs, "channelId")
        return self.delete_request("/chat/channels/{}".format(kwargs.get("channelId")), params=kwargs)

    def list_members(self, **kwargs):
        require_keys(kwargs, "channelId")
        return self.get_request("/chat/channels/{}/members".format(kwargs.get("channelId")), params=kwargs)

    def invite_member(self, **kwargs):
        require_keys(kwargs, "channelId")
        return self.post_request("/chat/channels/{}/members".format(kwargs.get("channelId")), data=kwargs)

    def join(self, **kwargs):
        require_keys(kwargs, "channelId")
        return self.post_request("/chat/channels/{}/members/me".format(kwargs.get("channelId")), params=kwargs)

    def leave(self, **kwargs):
        require_keys(kwargs, "channelId")
        return self.delete_request("/chat/channels/{}/members/me".format(kwargs.get("channelId")), params=kwargs)

    def remove_member(self, **kwargs):
        require_keys(kwargs, ["channelId", "memberId"])
        return self.delete_request(
            "/chat/channels/{}/members/{}".format(kwargs.get("channelId"), kwargs.get("memberId")), params=kwargs)
