#  Copyright 2022 Terra Enabling Developers Limited
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import datetime
import typing as t

import requests

from terra import constants
from terra import models
from terra import utils
from terra.models import user as user_


class Terra:
    """
    #TODO docstring here - what is this class? + constructor args
    """

    def __init__(self, api_key: str, dev_id: str) -> None:
        self.api_key = api_key
        self.dev_id = dev_id

    @property
    def _auth_headers(self) -> t.Dict[str, str]:
        """
        Internal method used to fill in authentication headers for all requests to the API

        Returns:
            :obj:`dict`: Dictionary of required auth headers

        """
        return {"x-api-key": self.api_key, "dev-id": self.dev_id}

    def from_user_id(self, user_id: str) -> user_.User:
        """
        Creates a User instance out of a UUID corresponding to a registered User on the API

        Args:
            user_id (:obj:`str`): UUID corresponding to a user currently authenticated on the API

        Returns:
            :obj:`User`: Created User instance

        """
        return user_.User(user_id=user_id, client=self)

    def _get_arbitrary_data(
        self, user: user_.User, dtype: str, **kwargs: t.Any
    ) -> models.api_responses.TerraApiResponse:
        """
        Internal method used to retrieve data for a given User

        Args:
            user (:obj:`models.user.User`):
            dtype (:obj:`str`): datatype to be fetched
            **kwargs: optional additional parameters for the request

        Returns:
            :obj:`models.api_responses.TerraApiResponse`: API response object containing DataReturned parsed response object if no error has occured

        """
        params = {"user_id": user.user_id}
        params = utils.update_if_not_none(params, kwargs)
        data_resp = requests.get(
            f"{constants.BASE_URL}/{dtype}",
            params=params,
            headers=self._auth_headers,
        )

        return models.api_responses.TerraApiResponse(data_resp, user)

    def get_activity_for_user(
        self,
        user: user_.User,
        start_date: datetime.datetime,
        end_date: datetime.datetime = None,
        to_webhook: bool = True,
    ) -> models.api_responses.TerraApiResponse:
        """
        Retrieves workouts/activity data for a given User object. By default, data will be asynchronously sent to registered
        webhook URL.

        Args:
            user (:obj:`models.user.User`): User for whom to fetch data
            start_date (:obj:`datetime.datetime`): Datetime object for which to fetch data
            end_date:obj (:`datetime.datetime`): Optional end_date for which to fetch data - if not set, will default to start_date + 24h according to current API specifications
            to_webhook (:obj:`bool`): Whether to send data to registered webhook URL or return as a response body

        Returns:
            :obj:`models.api_responses.TerraApiResponse`: API response object containing DataReturned parsed response object if no error has occured

        """
        return self._get_arbitrary_data(
            user,
            "activity",
            start_date=int(start_date.timestamp()),
            end_date=int(end_date.timestamp()) if end_date is not None else None,
            to_webhook=to_webhook,
        )

    def get_body_for_user(
        self,
        user: user_.User,
        start_date: datetime.datetime,
        end_date: datetime.datetime = None,
        to_webhook: bool = True,
    ) -> models.api_responses.TerraApiResponse:
        """
        Retrieves body metrics data for a given User object. By default, data will be asynchronously sent to registered
        webhook URL.

        Args:
            user (:obj:`models.user.User`): User for whom to fetch data
            start_date (:obj:`datetime.datetime`): Datetime object for which to fetch data
            end_date:obj (:`datetime.datetime`): Optional end_date for which to fetch data - if not set, will default to start_date + 24h according to current API specifications
            to_webhook (:obj:`bool`): Whether to send data to registered webhook URL or return as a response body

        Returns:
            :obj:`models.api_responses.TerraApiResponse`: API response object containing DataReturned parsed response object if no error has occured

        """
        return self._get_arbitrary_data(
            user,
            "body",
            start_date=start_date,
            end_date=end_date,
            to_webhook=to_webhook,
        )

    def get_daily_for_user(
        self,
        user: user_.User,
        start_date: datetime.datetime,
        end_date: datetime.datetime = None,
        to_webhook: bool = True,
    ) -> models.api_responses.TerraApiResponse:
        """
        Retrieves daily summary data for a given User object. By default, data will be asynchronously sent to registered
        webhook URL.

        Args:
            user (:obj:`models.user.User`): User for whom to fetch data
            start_date (:obj:`datetime.datetime`): Datetime object for which to fetch data
            end_date:obj (:`datetime.datetime`): Optional end_date for which to fetch data - if not set, will default to start_date + 24h according to current API specifications
            to_webhook (:obj:`bool`): Whether to send data to registered webhook URL or return as a response body

        Returns:
            :obj:`models.api_responses.TerraApiResponse`: API response object containing DataReturned parsed response object if no error has occured

        """
        return self._get_arbitrary_data(
            user,
            "daily",
            start_date=start_date,
            end_date=end_date,
            to_webhook=to_webhook,
        )

    def get_sleep_for_user(
        self,
        user: user_.User,
        start_date: datetime.datetime,
        end_date: datetime.datetime = None,
        to_webhook: bool = True,
    ) -> models.api_responses.TerraApiResponse:
        """
        Retrieves sleep data for a given User object. By default, data will be asynchronously sent to registered
        webhook URL.

        Args:
            user (:obj:`models.user.User`): User for whom to fetch data
            start_date (:obj:`datetime.datetime`): Datetime object for which to fetch data
            end_date:obj (:`datetime.datetime`): Optional end_date for which to fetch data - if not set, will default to start_date + 24h according to current API specifications
            to_webhook (:obj:`bool`): Whether to send data to registered webhook URL or return as a response body

        Returns:
            :obj:`models.api_responses.TerraApiResponse`: API response object containing DataReturned parsed response object if no error has occured

        """
        return self._get_arbitrary_data(
            user,
            "sleep",
            start_date=start_date,
            end_date=end_date,
            to_webhook=to_webhook,
        )

    def get_athlete_for_user(
        self,
        user: user_.User,
        to_webhook: bool = True,
    ) -> models.api_responses.TerraApiResponse:
        """
        Retrieves profile info/athlete data for a given User object. By default, data will be asynchronously sent to
        registered webhook URL.

        Args:
            user (:obj:`models.user.User`): User for whom to fetch data
            to_webhook (:obj:`bool`): Whether to send data to registered webhook URL or return as a response body
        Returns:
            :obj:`models.api_responses.TerraApiResponse`: API response object containing DataReturned parsed response object if no error has occured

        """
        return self._get_arbitrary_data(user, "athlete", to_webhook=to_webhook)

    def get_menstruation_for_user(
        self,
        user: user_.User,
        start_date: datetime.datetime,
        end_date: datetime.datetime = None,
        to_webhook: bool = True,
    ) -> models.api_responses.TerraApiResponse:
        """
        Retrieves daily summary data for a given User object. By default, data will be asynchronously sent to registered
        webhook URL.

        Args:
            user (:obj:`models.user.User`): User for whom to fetch data
            start_date (:obj:`datetime.datetime`): Datetime object for which to fetch data
            end_date:obj (:`datetime.datetime`): Optional end_date for which to fetch data - if not set, will default to start_date + 24h according to current API specifications
            to_webhook (:obj:`bool`): Whether to send data to registered webhook URL or return as a response body

        Returns:
            :obj:`models.api_responses.TerraApiResponse`: API response object containing DataReturned parsed response object if no error has occured

        """
        return self._get_arbitrary_data(
            user,
            "menstruation",
            start_date=start_date,
            end_date=end_date,
            to_webhook=to_webhook,
        )

    def generate_widget_session(
        self,
        providers: t.Optional[t.List[str]] = None,
        auth_success_redirect_url: t.Optional[str] = None,
        auth_failure_redirect_url: t.Optional[str] = None,
        language: t.Optional[str] = None,
        reference_id: t.Optional[str] = None,
        **kwargs: t.Any,
    ) -> models.api_responses.TerraApiResponse:
        """
        Generates a widget session used to allow an end user to authenticate through the API. Users should be
        redirected to the given URL in order to complete authentication

        Args:
            providers (:obj:`t.List[str]`): Providers to display on widget wearable selection screen
            auth_success_redirect_url (:obj:`t.Optional[str]`): URL to redirect to upon successful authentication
            auth_failure_redirect_url (:obj:`t.Optional[str]`): URL to redirect to upon unsuccessful authentication
            language (:obj:`t.Optional[str]`): Language to display widget in
            reference_id (:obj:`t.Optional[str]`): ID of a user in your app, which will be returned at the end of a successful auth
            **kwargs: Optional additional arguments to be passed in to the body of the request

        Returns:
            :obj:`models.api_responses.TerraApiResponse`: API response object containing WidgetSession parsed response object if no error has occured
        """
        maybe_body_payload = {
            "providers": providers,
            "auth_success_redirect_url": auth_success_redirect_url,
            "auth_failure_redirect_url": auth_failure_redirect_url,
            "language": language,
            "reference_id": reference_id,
        }
        body_payload = utils.update_if_not_none({}, maybe_body_payload)
        body_payload.update(kwargs)

        widget_resp = requests.post(
            f"{constants.BASE_URL}/auth/generateWidgetSession",
            headers=self._auth_headers,
            json=body_payload,
        )
        return models.api_responses.TerraApiResponse(widget_resp, dtype="widget_sesion")

    def generate_authentication_url(
        self,
        resource: str,
        auth_success_redirect_url: t.Optional[str] = None,
        auth_failure_redirect_url: t.Optional[str] = None,
        reference_id: t.Optional[str] = None,
        **kwargs: t.Any,
    ) -> models.api_responses.TerraApiResponse:
        """
        Generates an authentication URL to allow an end user to authenticate through the API. Users should be
        redirected to the given URL in order to complete authentication. User ID will be provided in the response
        for convenience (note that at this stage, said user will have yet to complete the auth flow)

        Args:
            resource (:obj:`str`): Provider to authenticate user with
            auth_success_redirect_url (:obj:`t.Optional[str]`): URL to redirect to upon successful authentication
            auth_failure_redirect_url (:obj:`t.Optional[str]`): URL to redirect to upon unsuccessful authentication
            reference_id (:obj:`t.Optional[str]`): ID of a user in your app, which will be returned at the end of a successful auth
            **kwargs: Optional additional arguments to be passed in to the body of the request
        Returns:
            :obj:`models.api_responses.TerraApiResponse`: API response object containing UserAuthUrl parsed response object if no error has occured

        """

        body_payload = {
            "resource": resource,
            "auth_success_redirect_url": auth_success_redirect_url,
            "auth_failure_redirect_url": auth_failure_redirect_url,
            "reference_id": reference_id,
        }
        body_payload.update(kwargs)

        auth_resp = requests.post(
            f"{constants.BASE_URL}/auth/generateWidgetSession",
            headers=self._auth_headers,
            json=body_payload,
        )
        return models.api_responses.TerraApiResponse(auth_resp, dtype="auth_url")

    def get_user_info(self, user: user_.User) -> models.api_responses.TerraApiResponse:
        """
        Retrieve information on a given User, including is_authenticated status, indicating if the user has
        successfully completed auth flow, or has yet to do so
        Note: Also updates information on user object passed as an argument

        Args:
            user (:obj:`models.user.User`): User to retrieve information for

        Returns:
            :obj:`models.api_responses.TerraApiResponse`: API response object containing UserInfo parsed response object if no error has occured
        """
        user_resp = requests.get(
            f"{constants.BASE_URL}/userInfo",
            params={"user_id": user.user_id},
            headers=self._auth_headers,
        )
        return models.api_responses.TerraApiResponse(user_resp, dtype="user_info")

    def deauthenticate_user(
        self, user: user_.User
    ) -> models.api_responses.TerraApiResponse:
        """
        Deauthenticates given User from the Api
        Note: If successful, this triggers a User Deauthentication webhook event

        Args:
            user (:obj:`models.user.User`): User to Deauthenticate from the API

        Returns:
            :obj:`models.api_responses.TerraApiResponse`: API response object containing UserDeauthResp parsed response object if no error has occured
        """
        deauth_resp = requests.delete(
            f"{constants.BASE_URL}/deauthenticateUser",
            params={"user_id": user.user_id},
            headers=self._auth_headers,
        )
        deauth_resp.raise_for_status()
        return models.api_responses.TerraApiResponse(deauth_resp, dtype="user_deauth")

    def list_users(self) -> models.api_responses.TerraApiResponse:
        """
        Lists all users registered under Client's credentials on the API

        Returns:
            :obj:`models.api_responses.TerraApiResponse`: API response object containing SubscribedUsers parsed response object if no error has occured
        """
        users_resp = requests.get(
            f"{constants.BASE_URL}/subscriptions", headers=self._auth_headers
        )
        return models.api_responses.TerraApiResponse(users_resp, dtype="subscriptions")
