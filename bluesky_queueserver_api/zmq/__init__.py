from ..api_threads import API_Threads_Mixin
from ..comm_threads import ReManagerComm_ZMQ_Threads
from .._defaults import (
    default_allow_request_fail_exceptions,
    default_zmq_request_timeout_recv,
    default_zmq_request_timeout_send,
)


class REManagerAPI(ReManagerComm_ZMQ_Threads, API_Threads_Mixin):
    def __init__(
        self,
        *,
        zmq_server_address=None,
        timeout_recv=default_zmq_request_timeout_recv,
        timeout_send=default_zmq_request_timeout_send,
        server_public_key=None,
        request_fail_exceptions=default_allow_request_fail_exceptions,
    ):
        ReManagerComm_ZMQ_Threads.__init__(
            self,
            zmq_server_address=zmq_server_address,
            timeout_recv=timeout_recv,
            timeout_send=timeout_send,
            server_public_key=server_public_key,
            request_fail_exceptions=request_fail_exceptions,
        )
        API_Threads_Mixin.__init__(self)
