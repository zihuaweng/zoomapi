"""Zoom.us REST API Python Client -- Chat Messages component"""

from zoomapi import util
from zoomapi.components import base


class ChatMessagesComponentV2(base.BaseComponent):
    """Component dealing with all chat messages related matters"""

    def list(self, **kwargs):
        util.require_keys(kwargs, ["userId", "to_contact"])
        return self.get_request(
            "/chat/users/{}/messages".format(kwargs.get("userId")), params=kwargs
        )

    def send(self, **kwargs):
        util.require_keys(kwargs, ["message", "to_contact"])
        return self.post_request("/chat/users/me/messages", data=kwargs)

    def update(self, **kwargs):
        util.require_keys(kwargs, ["messageId", "message", "to_contact"])
        return self.put_request("/chat/users/me/messages/{}".format(kwargs.get("messageId")), data=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, ["messageId", "to_contact"])
        return self.delete_request("/chat/users/me/messages/{}".format(kwargs.get("messageId")), params=kwargs)
