import requests
from typing import Optional, Dict, Any, Union, List
from pydantic import ValidationError as PydanticValidationError
import exceptions
from models import (
    Token, Admin, AdminCreate, AdminModify, NodeCreate, NodeModify, NodeResponse, NodeSettings,
    NodesUsageResponse, ProxyHost, CoreStats, SystemStats, UserCreate, UserModify, UserResponse,
    SubscriptionUserResponse, HTTPValidationError, ProxyInbound
)


class MarzbanAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.token = None

    def _send_request(self, method: str, url: str, **kwargs) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Internal method to send a request with retry logic and error handling."""
        attempts = 3
        for attempt in range(attempts):
            try:
                response = self.session.request(method, url, **kwargs)
                print(response.status_code)
                self._raise_for_status(response)
                return response.json()
            except exceptions.MarzbanAPIException as e:
                if attempt == attempts - 1:
                    raise e
                print(f"Attempt {attempt + 1} failed: {e}. Retrying...")

    def _raise_for_status(self, response: requests.Response):
        """Raise custom exceptions based on response status codes."""
        if response.status_code == 400:
            raise exceptions.BadRequestError("Bad request: " + response.json().get("detail", "Unknown error"))
        elif response.status_code == 403:
            raise exceptions.UnauthorizedError("Unauthorized access.")
        elif response.status_code == 404:
            raise exceptions.NotFoundError("Resource not found.")
        elif response.status_code == 409:
            raise exceptions.ConflictError("Conflict: " + response.json().get("detail", "Resource already exists"))
        elif response.status_code == 422:
            raise exceptions.ValidationError("Validation Error: " + str(response.json().get("detail", "Invalid input")))
        response.raise_for_status()

    def authenticate(self, username: str, password: str) -> Token:
        """
        Authenticate an admin and issue a token.

        Raises:
            - ValidationError: If the username or password is invalid (HTTP 422).
        """
        url = f"{self.base_url}/api/admin/token"
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
            # "client_id": self.client_id,
            # "client_secret": self.client_secret,
        }
        response = self._send_request("POST", url, data=data)
        try:
            token_data = Token(**response)
        except PydanticValidationError as e:
            raise exceptions.TokenError("Failed to obtain access token.")
        self.token = token_data.access_token
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        return token_data

    # ----- Admin Services -----

    def get_current_admin(self) -> Admin:
        """Retrieve the current authenticated admin."""
        url = f"{self.base_url}/api/admin"
        response = self._send_request("GET", url)
        return Admin(**response)

    def create_admin(self, username: str, is_sudo: bool, password: str) -> Admin:
        """Create a new admin with sudo privileges if the current admin is authorized."""
        url = f"{self.base_url}/api/admin"
        data = AdminCreate(username=username, is_sudo=is_sudo, password=password).model_dump()
        response = self._send_request("POST", url, json=data)
        return Admin(**response)

    def modify_admin(self, username: str, is_sudo: bool, password: Optional[str] = None) -> Admin:
        """Modify an existing admin's details."""
        url = f"{self.base_url}/api/admin/{username}"
        data = AdminModify(is_sudo=is_sudo, password=password).model_dump(exclude_unset=True)
        response = self._send_request("PUT", url, json=data)
        return Admin(**response)

    def remove_admin(self, username: str) -> None:
        """Remove an admin from the database."""
        url = f"{self.base_url}/api/admin/{username}"
        self._send_request("DELETE", url)

    def get_admins(self, offset: int = 0, limit: int = 10) -> List[Admin]:
        """Fetch a list of admins with pagination options."""
        url = f"{self.base_url}/api/admins"
        params = {"offset": offset, "limit": limit}
        response = self._send_request("GET", url, params=params)
        return [Admin(**admin) for admin in response]

    # ----- Core Services -----

    def get_core_stats(self) -> CoreStats:
        """Retrieve core statistics such as version and uptime."""
        url = f"{self.base_url}/api/core"
        response = self._send_request("GET", url)
        return CoreStats(**response)

    def restart_core(self) -> None:
        """Restart the core and all connected nodes."""
        url = f"{self.base_url}/api/core/restart"
        self._send_request("POST", url)

    def get_core_config(self) -> Dict[str, Any]:
        """Get the current core configuration."""
        url = f"{self.base_url}/api/core/config"
        response = self._send_request("GET", url)
        return response

    def modify_core_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Modify the core configuration and restart the core."""
        url = f"{self.base_url}/api/core/config"
        response = self._send_request("PUT", url, json=config)
        return response

    # ----- Node Services -----

    def add_node(self, node_data: NodeCreate) -> NodeResponse:
        """Add a new node to the database."""
        url = f"{self.base_url}/api/node"
        response = self._send_request("POST", url, json=node_data.model_dump())
        return NodeResponse(**response)

    def get_node(self, node_id: int) -> NodeResponse:
        """Retrieve details of a specific node by its ID."""
        url = f"{self.base_url}/api/node/{node_id}"
        response = self._send_request("GET", url)
        return NodeResponse(**response)

    def modify_node(self, node_id: int, node_data: NodeModify) -> NodeResponse:
        """Update a node's details."""
        url = f"{self.base_url}/api/node/{node_id}"
        response = self._send_request("PUT", url, json=node_data.model_dump(exclude_unset=True))
        return NodeResponse(**response)

    def remove_node(self, node_id: int) -> None:
        """Delete a node from the database."""
        url = f"{self.base_url}/api/node/{node_id}"
        self._send_request("DELETE", url)

    def get_nodes(self) -> List[NodeResponse]:
        """Retrieve a list of all nodes."""
        url = f"{self.base_url}/api/nodes"
        response = self._send_request("GET", url)
        return [NodeResponse(**node) for node in response]

    # ----- Subscription Services -----

    def get_user_subscription(self, token: str) -> SubscriptionUserResponse:
        """Provides a subscription link based on the user agent."""
        url = f"{self.base_url}/sub/{token}/"
        response = self._send_request("GET", url)
        return SubscriptionUserResponse(**response)

    def revoke_user_subscription(self, username: str) -> None:
        """Revoke the subscription link and proxies for a user."""
        url = f"{self.base_url}/api/user/{username}/revoke_sub"
        self._send_request("POST", url)

    # ----- System Services -----

    def get_system_stats(self) -> SystemStats:
        """Fetch system stats including memory, CPU, and user metrics."""
        url = f"{self.base_url}/api/system"
        response = self._send_request("GET", url)
        return SystemStats(**response)

    def get_inbounds(self) -> Dict[str, List[ProxyHost]]:
        """Retrieve inbound configurations grouped by protocol."""
        url = f"{self.base_url}/api/inbounds"
        response = self._send_request("GET", url)
        return {protocol: [ProxyInbound(**inbound) for inbound in inbounds] for protocol, inbounds in response.items()}

    def get_hosts(self) -> Dict[str, List[ProxyHost]]:
        """Get a list of proxy hosts grouped by inbound tag."""
        url = f"{self.base_url}/api/hosts"
        response = self._send_request("GET", url)
        print(response)
        return {tag: [ProxyHost(**host) for host in hosts] for tag, hosts in response.items()}

    # ----- User Services -----

    def add_user(self, user_data: UserCreate) -> UserResponse:
        """Add a new user."""
        url = f"{self.base_url}/api/user"
        response = self._send_request("POST", url, json=user_data.model_dump())
        return UserResponse(**response)

    def get_user(self, username: str) -> UserResponse:
        """Get user information."""
        url = f"{self.base_url}/api/user/{username}"
        response = self._send_request("GET", url)
        return UserResponse(**response)

    def modify_user(self, username: str, user_data: UserModify) -> UserResponse:
        """Modify an existing user's details."""
        url = f"{self.base_url}/api/user/{username}"
        response = self._send_request("PUT", url, json=user_data.model_dump(exclude_unset=True))
        return UserResponse(**response)

    def remove_user(self, username: str) -> None:
        """Remove a user."""
        url = f"{self.base_url}/api/user/{username}"
        self._send_request("DELETE", url)

    def get_users(self, offset: int = 0, limit: int = 10) -> List[UserResponse]:
        """Get all users with pagination options."""
        url = f"{self.base_url}/api/users"
        params = {"offset": offset, "limit": limit}
        response = self._send_request("GET", url, params=params)
        return [UserResponse(**user) for user in response.get('users')]
