# THIS FILE WAS CHANGED FROM THE ORIGINAL

"""Zoom.us REST API Python Client"""

from zoomapi import util
from zoomapi.components import base

class MeetingComponent(base.BaseComponent):
    """Component dealing with all meeting related matters"""

    def list(self, **kwargs):
        util.require_keys(kwargs, "host_id")
        if kwargs.get("start_time"):
            kwargs["start_time"] = util.date_to_str(kwargs["start_time"])
        return self.post_request("/meeting/list", params=kwargs)

    def create(self, **kwargs):
        util.require_keys(kwargs, ["host_id", "topic", "type"])
        if kwargs.get("start_time"):
            kwargs["start_time"] = util.date_to_str(kwargs["start_time"])
        return self.post_request("/meeting/create", params=kwargs)

    def update(self, **kwargs):
        util.require_keys(kwargs, ["id", "host_id"])
        if kwargs.get("start_time"):
            kwargs["start_time"] = util.date_to_str(kwargs["start_time"])
        return self.post_request("/meeting/update", params=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, ["id", "host_id"])
        return self.post_request("/meeting/delete", params=kwargs)

    def end(self, **kwargs):
        util.require_keys(kwargs, ["id", "host_id"])
        return self.post_request("/meeting/end", params=kwargs)

    def get(self, **kwargs):
        util.require_keys(kwargs, ["id", "host_id"])
        return self.post_request("/meeting/get", params=kwargs)


class MeetingComponentV2(base.BaseComponent):
    @util.Throttled
    def list(self, **kwargs):
        util.require_keys(kwargs, "user_id")
        return self.get_request(
            "/users/{}/meetings".format(kwargs.get("user_id")), params=kwargs
        )

    @util.Throttled
    def create(self, **kwargs):
        util.require_keys(kwargs, "user_id")
        if kwargs.get("start_time"):
            kwargs["start_time"] = util.date_to_str(kwargs["start_time"])
        return self.post_request(
            "/users/{}/meetings".format(kwargs.get("user_id")), params=kwargs
        )

    @util.Throttled
    def get(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.get_request("/meetings/{}".format(kwargs.get("id")), params=kwargs)

    @util.Throttled
    def update(self, **kwargs):
        util.require_keys(kwargs, "id")
        if kwargs.get("start_time"):
            kwargs["start_time"] = util.date_to_str(kwargs["start_time"])
        return self.patch_request(
            "/meetings/{}".format(kwargs.get("id")), params=kwargs
        )

    @util.Throttled
    def delete(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.delete_request(
            "/meetings/{}".format(kwargs.get("id")), params=kwargs
        )
