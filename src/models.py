from pydantic import BaseModel, Field, conint, constr, conlist, conset, validator, PositiveInt, AnyUrl
from typing import Optional, List, Dict, Union, Any, Literal
from datetime import datetime

# ----- Core Models -----

class CoreStats(BaseModel):
    version: str
    started: bool
    logs_websocket: str


# ----- Token Model -----

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ----- Admin Models -----

class Admin(BaseModel):
    username: str
    is_sudo: bool
    telegram_id: Optional[int] = None
    discord_webhook: Optional[str] = None

class AdminCreate(Admin):
    password: str

class AdminModify(BaseModel):
    is_sudo: bool
    password: Optional[str] = None
    telegram_id: Optional[int] = None
    discord_webhook: Optional[str] = None


# ----- Node Models -----

NodeStatus = Literal["connected", "connecting", "error", "disabled"]

class NodeCreate(BaseModel):
    name: str
    address: str
    port: Optional[int] = 62050
    api_port: Optional[int] = 62051
    usage_coefficient: Optional[float] = 1.0
    add_as_new_host: Optional[bool] = True

class NodeModify(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    port: Optional[int] = None
    api_port: Optional[int] = None
    usage_coefficient: Optional[float] = None
    status: Optional[NodeStatus] = None

class NodeResponse(BaseModel):
    id: int
    name: str
    address: str
    port: int
    api_port: int
    usage_coefficient: float
    xray_version: Optional[str] = None
    status: NodeStatus
    message: Optional[str] = None


class NodeSettings(BaseModel):
    min_node_version: Optional[str] = "v0.2.0"
    certificate: str


class NodeUsageResponse(BaseModel):
    node_id: int
    node_name: str
    uplink: int
    downlink: int


class NodesUsageResponse(BaseModel):
    usages: List[NodeUsageResponse]


# ----- Proxy Models -----

ProxyHostSecurity = Literal["inbound_default", "none", "tls"]
ProxyHostALPN = Literal["http/1.1", "h3", "h2", "h3,h2,http/1.1", "h3,h2", "h2,http/1.1", ""]
ProxyHostFingerprint = Literal["chrome", "firefox", "safari", "ios", "android", "edge", "qq", "random", "randomized", ""]

class ProxyHost(BaseModel):
    remark: str
    address: str
    port: Optional[int] = None
    sni: Optional[str] = None
    host: Optional[str] = None
    path: Optional[str] = None
    security: ProxyHostSecurity = "inbound_default"
    alpn: Optional[ProxyHostALPN] = None
    fingerprint: Optional[ProxyHostFingerprint] = None
    allowinsecure: Optional[bool] = None
    is_disabled: bool
    mux_enable: bool
    fragment_setting: Optional[str] = None
    noise_setting: Optional[str] = None
    random_user_agent: bool


class ProxyInbound(BaseModel):
    tag: str
    protocol: str
    network: str
    tls: str
    port: Union[int, str]


# ----- User Models -----

UserStatus = Literal["active", "disabled", "limited", "expired", "on_hold"]
UserDataLimitResetStrategy = Literal["no_reset", "day", "week", "month", "year"]

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    proxies: Dict[str, Dict[str, Any]]
    expire: Optional[int] = None
    data_limit: Optional[int] = None
    data_limit_reset_strategy: UserDataLimitResetStrategy = "no_reset"
    inbounds: Dict[str, List[str]] = {}
    note: Optional[str] = None
    sub_updated_at: Optional[datetime] = None
    sub_last_user_agent: Optional[str] = None
    online_at: Optional[datetime] = None
    on_hold_expire_duration: Optional[int] = None
    on_hold_timeout: Optional[datetime] = None
    auto_delete_in_days: Optional[int] = None
    status: UserStatus = "active"


class UserModify(BaseModel):
    proxies: Optional[Dict[str, Dict[str, Any]]] = {}
    expire: Optional[int] = None
    data_limit: Optional[int] = None
    data_limit_reset_strategy: Optional[UserDataLimitResetStrategy] = None
    inbounds: Optional[Dict[str, List[str]]] = {}
    note: Optional[str] = None
    sub_updated_at: Optional[datetime] = None
    sub_last_user_agent: Optional[str] = None
    online_at: Optional[datetime] = None
    on_hold_expire_duration: Optional[int] = None
    on_hold_timeout: Optional[datetime] = None
    auto_delete_in_days: Optional[int] = None
    status: Optional[UserStatus] = None


class UserResponse(BaseModel):
    username: str
    proxies: Dict[str, Dict[str, Any]]
    expire: Optional[int] = None
    data_limit: Optional[int] = None
    data_limit_reset_strategy: UserDataLimitResetStrategy
    inbounds: Dict[str, List[str]] = {}
    note: Optional[str] = None
    sub_updated_at: Optional[datetime] = None
    sub_last_user_agent: Optional[str] = None
    online_at: Optional[datetime] = None
    on_hold_expire_duration: Optional[int] = None
    on_hold_timeout: Optional[datetime] = None
    auto_delete_in_days: Optional[int] = None
    status: UserStatus
    used_traffic: int
    lifetime_used_traffic: Optional[int] = 0
    created_at: datetime
    links: List[str] = []
    subscription_url: Optional[str] = None
    excluded_inbounds: Dict[str, List[str]] = {}
    admin: Optional[Admin] = None


# ----- Subscription Models -----

class SubscriptionUserResponse(BaseModel):
    username: str
    status: UserStatus
    used_traffic: int
    proxies: Dict[str, Dict[str, Any]]
    expire: Optional[int] = None
    data_limit: Optional[int] = None
    data_limit_reset_strategy: UserDataLimitResetStrategy
    inbounds: Dict[str, List[str]] = {}
    note: Optional[str] = None
    created_at: datetime
    links: List[str] = []
    subscription_url: Optional[str] = None
    excluded_inbounds: Dict[str, List[str]] = {}
    admin: Optional[Admin] = None


# ----- System Models -----

class SystemStats(BaseModel):
    version: str
    mem_total: int
    mem_used: int
    cpu_cores: int
    cpu_usage: float
    total_user: int
    users_active: int
    incoming_bandwidth: int
    outgoing_bandwidth: int
    incoming_bandwidth_speed: int
    outgoing_bandwidth_speed: int


# ----- HTTP Validation Error Model -----

class ValidationErrorDetail(BaseModel):
    loc: List[Union[str, int]]
    msg: str
    type: str

class HTTPValidationError(BaseModel):
    detail: List[ValidationErrorDetail]
