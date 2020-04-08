# THIS FILE WAS CHANGED FROM THE ORIGINAL

"""Zoom.us REST API Python Client"""

from zoomapi import util


class BaseComponent(util.ApiClient):
    """A base component"""

    def __init__(self, base_uri=None, config=None, timeout=15, **kwargs):
        """Setup a base component

        :param base_uri: The base URI to the API
        :param config: The config details
        :param timeout: The timeout to use for requests
        :param kwargs: Any other attributes. These will be added as
                           attributes to the ApiClient object.
        """
        super(BaseComponent, self).__init__(
            base_uri=base_uri, timeout=timeout, config=config, **kwargs
        )

    def post_request(
            self, endpoint, params=None, data=None, headers=None, cookies=None
    ):
        """Helper function for POST requests

        Since the Zoom.us API only uses POST requests and each post request
        must include all of the config data, this method ensures that all
        of that data is there

        :param endpoint: The endpoint
        :param params: The URL parameters
        :param data: The data (either as a dict or dumped JSON string) to
                     include with the POST
        :param headers: request headers
        :param cookies: request cookies
        :return: The :class:``requests.Response`` object for this request
        """
        params = params or {}
        if headers is None:
            headers = {"Authorization": "Bearer {}".format(self.config.get("token"))}
        return super(BaseComponent, self).post_request(
            endpoint, params=params, data=data, headers=headers, cookies=cookies
        )
