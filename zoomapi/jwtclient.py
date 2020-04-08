"""Zoom.us REST API Python Client"""

from zoomapi import components, util
from zoomapi.client import ZoomClient

API_VERSION_1 = 1
API_VERSION_2 = 2

API_BASE_URIS = {
    API_VERSION_1: "https://api.zoom.us/v1",
    API_VERSION_2: "https://api.zoom.us/v2",
}

COMPONENT_CLASSES = {
    API_VERSION_1: {
        "user": components.user.UserComponent,
        "meeting": components.meeting.MeetingComponent,
        "report": components.report.ReportComponent,
        "webinar": components.webinar.WebinarComponent,
        "recording": components.recording.RecordingComponent,
    },
    API_VERSION_2: {
        "user": components.user.UserComponentV2,
        "meeting": components.meeting.MeetingComponentV2,
        "report": components.report.ReportComponentV2,
        "webinar": components.webinar.WebinarComponentV2,
        "recording": components.recording.RecordingComponentV2,
        "chat_channels": components.chat_channels.ChatChannelsComponentV2,
        "chat_messages": components.chat_messages.ChatMessagesComponentV2
    },
}


class JWTZoomClient(ZoomClient):
    """Zoom.us REST API Python Client"""

    """Base URL for Zoom API"""

    def __init__(
            self, api_key, api_secret, data_type="json", timeout=15, version=API_VERSION_2
    ):
        """Create a new Zoom client

        :param api_key: The Zooom.us API key
        :param api_secret: The Zoom.us API secret
        :param data_type: The expected return data type. Either 'json' or 'xml'
        :param timeout: The time out to use for API requests
        """
        try:
            BASE_URI = API_BASE_URIS[version]
            self.components = COMPONENT_CLASSES[version].copy()
        except KeyError:
            raise RuntimeError("API version not supported: %s" % version)

        super(JWTZoomClient, self).__init__(base_uri=BASE_URI, timeout=timeout)

        # Setup the config details
        self.config = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data_type": data_type,
            "version": version,
            "token": util.generate_jwt(api_key, api_secret),
        }

        # Instantiate the components
        for key in self.components.keys():
            self.components[key] = self.components[key](
                base_uri=BASE_URI, config=self.config
            )

    def refresh_token(self):
        self.config["token"] = (
            util.generate_jwt(self.config["api_key"], self.config["api_secret"]),
        )

    @property
    def api_key(self):
        """The Zoom.us api_key"""
        return self.config.get("api_key")

    @api_key.setter
    def api_key(self, value):
        """Set the api_key"""
        self.config["api_key"] = value
        self.refresh_token()

    @property
    def api_secret(self):
        """The Zoom.us api_secret"""
        return self.config.get("api_secret")

    @api_secret.setter
    def api_secret(self, value):
        """Set the api_secret"""
        self.config["api_secret"] = value
        self.refresh_token()

    @property
    def meeting(self):
        """Get the meeting component"""
        return self.components.get("meeting")

    @property
    def report(self):
        """Get the report component"""
        return self.components.get("report")

    @property
    def user(self):
        """Get the user component"""
        return self.components.get("user")

    @property
    def webinar(self):
        """Get the webinar component"""
        return self.components.get("webinar")

    @property
    def recording(self):
        """Get the recording component"""
        return self.components.get("recording")
