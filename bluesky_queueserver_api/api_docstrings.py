_doc_BItem = """
    A helper class that generates dictionary with queue item parameters. The class
    performs validation of values to ensure that the dictionary is formatted correctly.
    A queue item can be represented as a plain Python dictionary. Using this class
    to represent is queue items is optional.

    The item can be instantiated from a dictionary that contains valid item parameters
    or by passing item type, item name, args and kwargs or from another ``BItem`` object.
    The class implements public properties that allow to access all important item
    parameters, such as ``item_type``, ``name``, ``args``, ``kwargs``, ``meta``
    and ``item_uid``.

    Parameters
    ----------
    *args: list
        The first two arguments are required and should represent item type (allowed
        values are ``'plan'``, ``'instruction'`` and ``'function'``) and item name
        (name of the plan, instruction or function represented as a string). The remaining
        arguments are optional and represent args of the plan or function. Alternatively,
        an item may be instantiated from a valid dictionary of item parameters or another
        item object. In this case the constructor should be passed a single argument that
        contains the dictionary or the object and no keyword arguments.
    **kwargs: dict
        Keyword arguments of the plan or function.

    Raises
    ------
    KeyError, ValueError, TypeError
        Missing parameter or invalid parameter types or values

    Examples
    --------

    .. code-block:: python

        plan1 = BItem("plan", "count", ["det1", "det2"], num=10, delay=1)
        plan2 = BItem(plan1)  # Creates a copy of a plan
        plan3 = BItem({
            "item_type": "plan",
            "name": "count",
            "args": [["det1", "det2]],
            "kwargs": {"num": 10, "delay": 1}
        })

        item_type = plan1.item_type  # Require, always set
        item_name = plan1.name  # Required, always set
        item_args = plan1.args  # Optional, [] if not set
        item_kwargs = plan1.kwargs  # Optional, {} if not set
        item_uid = plan1.item_uid  # Usually set by the server, None if not set
        item_meta = plan1.meta  # Optional, {} if not set

        # Convert 'plan1' into 'queue_stop' instruction (properties are writable)
        plan1.item_type = "instruction"
        plan1.name = "queue_stop"
        plan1.args = []
        plan1.kwargs = {}
        plan1.meta = {}

        plan1_dict = plan1.to_dict()  # Returns a copy of the internal dictionary
        plan2.from_dict(plan1_dict)  # Makes 'plan2' a copy of 'plan1'
        plan2.from_dict(plan1)  # Works exactly the same

        # Access to internal dictionary
        dict_ref = plan3.dict_ref
        dict_ref["args"] = [["det1"]]
"""

_doc_BPlan_BInst_BFunc_common = """
    The helper class for creating dictionary representing --ITEM--. The class functionality
    is similar to ``BItems``, but configured for operations with items that represent --ITEMS--.

    Parameters
    ----------
    *args: list
        The first argument is a name of --ITEM-- represented as a string.
        The remaining arguments are optional and represent args of --ITEM--.
        Alternatively, an item may be instantiated from a valid dictionary
        of item parameters or another object that represent an item of matching type.
        Then the constructor receives a single argument that contains the dictionary or
        the item object and no keyword arguments.
    **kwargs: dict
        Keyword arguments of --ITEM--.

    Raises
    ------
    KeyError, ValueError, TypeError
        Missing parameter or invalid parameter types or values

    Examples
    --------

    .. code-block:: python

        plan1 = BPlan("count", ["det1", "det2"], num=10, delay=1)
        inst1 = BInst("queue_stop")
        func1 = BFunc("custom_func", 10)

        plan2 = BPlan(plan1.to_dict())  # Copy of 'plan'
        plan2 = BPlan(plan1)  # Works exactly the same

        # Initialization from items of another type always fails
        BPlan(func1.to_dict())  # Fails
        BPlan(inst1)  # Fails
        plan1.from_dict(func1.to_dict())  # Fails
        plan1.from_dict(inst1)  # Fails

        # BItem can be initialized from specialized item objects
        item = BItem(inst1.to_dict)  # Works
        item = BItem(inst1)  # Works

        # The following sequence works, because item type is correct
        item1 = BItem(plan1)  # 'item1' is still a plan
        plan3 = BPlan(item1)  # Initialize a plan object with another plan object
"""

_doc_BPlan = _doc_BPlan_BInst_BFunc_common.replace("--ITEM--", "a plan").replace("--ITEMS--", "plans")
_doc_BInst = _doc_BPlan_BInst_BFunc_common.replace("--ITEM--", "an instruction").replace(
    "--ITEMS--", "instructions"
)
_doc_BFunc = _doc_BPlan_BInst_BFunc_common.replace("--ITEM--", "a function").replace("--ITEMS--", "functions")


_doc_REManagerAPI_ZMQ = """
    API for communication with RE Manager using 0MQ protocol.

    Parameters
    ----------
    zmq_server_address: str or None
        Address of control 0MQ socket of RE Manager. If ``None``,
        then the default address ``"tcp://localhost:60615"`` is used.
    timeout_recv: float
        ``recv`` timeout for 0MQ socket. Default value is 2.0 seconds.
    timeout_send: float
        ``send`` timeout for 0MQ socket. Default value is 0.5 seconds.
    server_public_key: str or None
        Public key of RE Manager if the encryption is enabled. Set to ``None``
        if encryption is not enabled
    request_fail_exceptions: boolean
        If ``True`` (default) then API functions that communicate with
        RE Manager are raising the ``RequestFailError`` exception if
        the request is rejected (the response contains ``"success": False``,
        e.g. if a submitted plan is rejected). If ``False``, then API
        functions are always returning the response and user code is
        responsible for checking and processing the ``success`` flag.
    status_expiration_period: float
        Expiration period for cached RE Manager status,
        default value: 0.5 seconds
    status_polling_period: float
        Polling period for RE Manager status used by 'wait' operations,
        default value: 1 second
    loop: asyncio.Loop
        ``asyncio`` event loop (use only with Async version of the API).

    Examples
    --------

    Synchronous API:

    .. code-block:: python

        from bluesky_queueserver_api.zmq import REManagerAPI
        RM = REManagerAPI()
        # < some useful code >
        RE.close()

    Asynchronous API:

    .. code-block:: python

        from bluesky_queueserver_api.zmq.aio import REManagerAPI

        async def testing():
            RM = REManagerAPI()
            # < some useful code >
            await RE.close()

        asyncio.run(testing())
"""

_doc_REManagerAPI_HTTP = """
    API for communication with RE Manager using HTTP (RESTful API) protocol.

    Parameters
    ----------
    http_server_uri: str or None
        URI of Bluesky HTTP Server. If ``None``, then the default URI
        `"http://localhost:60610"`` is used.
    timeout: float
        Request timeout. Default value is 5.0 seconds.
    request_fail_exceptions: boolean
        If ``True`` (default) then API functions that communicate with
        RE Manager are raising the ``RequestFailError`` exception if
        the request is rejected (the response contains ``"success": False``,
        e.g. if a submitted plan is rejected). If ``False``, then API
        functions are always returning the response and user code is
        responsible for checking and processing the ``success`` flag.
    status_expiration_period: float
        Expiration period for cached RE Manager status,
        default value: 0.5 seconds
    status_polling_period: float
        Polling period for RE Manager status used by 'wait' operations,
        default value: 1 second
    loop: asyncio.Loop
        ``asyncio`` event loop (use only with Async version of the API).
        The parameter is included only for compatibility with 0MQ version
        of the API and is ignored in HTTP version.

    Examples
    --------

    Synchronous API:

    .. code-block:: python

        from bluesky_queueserver_api.http import REManagerAPI
        RM = REManagerAPI()
        # < some useful code >
        RE.close()

    Asynchronous API:

    .. code-block:: python

        from bluesky_queueserver_api.http.aio import REManagerAPI

        async def testing():
            RM = REManagerAPI()
            # < some useful code >
            await RE.close()

        asyncio.run(testing())
"""


_doc_send_request = """
    Send request to RE Manager and receive the response. The function directly passes
    the request to low-level Queue Server API. The detailed description of available
    methods, including names, parameters and returned values, can be found in Queue
    Server API reference. The function may raise exceptions in case of request timeout
    or failure.

    Parameters
    ----------
    method: str
        Name of the API method
    params: dict or None, optional
        Dictionary of API parameters or ``None`` if no parameters are passed.

    Returns
    -------
    dict
        Dictionary with the returned results.

    Raises
    ------
    RequestTimeoutError
        Request timed out.
    RequestFailedError
        Request failed (``response["success"]==False``).
    RequestError, ClientError
        Error while processing the request or communicating with the server. Raised only
        for HTTP requests.

    Examples
    --------

    .. code-block:: python

        # Synchronous code (0MQ)
        from bluesky_queueserver_api.zmq import REManagerAPI
        RM = REManagerAPI()
        status = RM.send_request(method="status")
        RM.close()

        # Synchronous code (HTTP)
        from bluesky_queueserver_api.http import REManagerAPI
        RM = REManagerAPI()
        status = RM.send_request(method="status")
        RM.close()

        # Asynchronous code (0MQ)
        from bluesky_queueserver_api.zmq.aio import REManagerAPI
        RM = REManagerAPI()
        status = await RM.send_request(method="status")
        await RM.close()

        # Asynchronous code, (HTTP)
        from bluesky_queueserver_api.http.aio import REManagerAPI
        RM = REManagerAPI()
        status = await RM.send_request(method="status")
        await RM.close()
"""

_doc_close = """
    Close RE Manager client.

    Examples
    --------

    .. code-block:: python

        # Synchronous code (0MQ and HTTP)
        RM.close()

        # Asynchronous code (0MQ and HTTP)
        await RM.close()
"""

_doc_api_status = """
    Load status of RE Manager. The function returns status or raises exception if
    operation failed (e.g. timeout occurred).

    Parameters
    ----------
    reload: boolean
        Immediately reload status (``True``) or return cached status if it
        is not expired (``False``). Calling the API with ``reload=True`` always
        initiates communication with the server.

    Returns
    -------
    dict
        Copy of the dictionary with RE Manager status.

    Raises
    ------
        Reraises the exceptions raised by ``send_request`` API.

    Examples
    --------

    .. code-block:: python

        # Synchronous code (0MQ and HTTP)
        status = RM.status()
        assert status["manager_state"] == "idle"

        # Asynchronous code (0MQ and HTTP)
        status = await RM.status()
        assert status["manager_state"] == "idle"
"""

_doc_api_ping = """
    Current implementation of the API loads status of RE Manager, but this may change
    in future releases. The function returns status or raises exception if operation
    failed (e.g. timeout occurred). See documentation for ``status`` API.
"""

_doc_api_wait_for_idle = """
    Wait for RE Manager to return to ``idle`` state. The function performs
    periodic polling of RE Manager status and returns when ``manager_state``
    status flag is ``idle``. Polling period is determined by ``status_polling_period``
    parameter of ``REManagerAPI`` class. The function raises ``WaitTimeoutError``
    if timeout occurs or ``WaitCancelError`` if wait operation was cancelled by
    ``monitor.cancel()``. See instructions on ``WaitMonitor`` class, which allows
    cancelling wait operations (from a different thread or task), modify timeout
    and monitoring the progress.

    Synchronous version of ``wait_for_idle`` is threadsafe. Multiple instances
    may run simultanously in multiple threads (sync) or tasks (async). Results
    of polling RE Manager status are shared between multiple running instances.

    Parameters
    ----------
    timeout: float
        Timeout for the wait operation. Default timeout: 60 seconds.
    monitor: bluesky_queueserver_api.WaitMonitor or None
        Instance of ``WaitMonitor`` object. The object is created internally if
        the parameter is ``None``.

    Returns
    -------
    None

    Raises
    ------
    REManagerAPI.WaitTimeoutError, REManagerAPI.WaitCancelError

    Examples
    --------

    .. code-block:: python

        # Synchronous code (0MQ, HTTP)
        RM.queue_start()
        try:
            RM.wait_for_idle(timeout=120)  # Wait for 2 minutes
            # < queue is completed or stopped, RE Manager is idle >
        except RM.WaitTimeoutError:
            # < process timeout error, RE Manager is probably not idle >

        # Aynchronous code (0MQ, HTTP)
        await RM.queue_start()
        try:
            await RM.wait_for_idle(timeout=120)  # Wait for 2 minutes
            # < queue is completed or stopped, RE Manager is idle >
        except RM.WaitTimeoutError:
            # < process timeout error, RE Manager is probably not idle >
"""

_doc_api_item_add = """
    Add item to the queue. The item may be a plan or an instruction represented
    as a dictionary or as an instance of ``BItem``, ``BPlan`` or ``BInst`` classes.
    By default the item is added to the back of the queue. Alternatively
    the item can be placed at the desired position in the queue or before
    or after one of the existing items. The parameters ``pos``, ``before_uid`` and
    ``after_uid`` are mutually exclusive, i.e. only one of the parameters may
    have a value different from ``None``.

    Parameters
    ----------
    item: dict, BItem, BPlan or BInst
        Dictionary or an instance of ``BItem``, ``BPlan`` or ``BInst`` representing
        a plan or an instruction.
    pos: str, int or None
        Position of the item in the queue. RE Manager will attempt to insert the
        item at the specified position. The position may be positive or negative
        (counted from the back of the queue) integer. If ``pos`` value is a string
        ``"front"`` or ``"back"``, then the item is inserted at the front or the back
        of the queue. If the value is ``None``, then the position is not specified.
    before_uid, after_uid: str or None
        Insert the item before or after the item with the given item UID. If ``None``
        (default), then the parameters are not specified.

    Returns
    -------
    dict
        Dictionary with item parameters. Dictionary keys: ``success`` (*boolean*),
        ``msg`` (*str*) - error message in case the request was rejected by RE Manager,
        ``qsize`` (*int* or *None*) - new size of the queue or *None* if operation
        failed, ``item`` (*dict* or *None*) - inserted item with assigned UID.
        If the request is rejected, ``item`` may contain the copy of the submitted
        item (with assigned UID), *None* or be missing depending on the failure.

    Raises
    ------
    Reraises the exceptions raised by ``send_request`` API.

    Examples
    --------

    .. code-block:: python

        # Synchronous code (0MQ, HTTP)
        # Add an item to the back of the queue
        RM.item_add({"item_type": "plan", "name": "count", "args": [["det1"]]})
        # Add an item to the front of the queue
        RM.item_add(BItem("plan", "count", ["det1"], num=10, delay=1), pos="front")
        RM.item_add(BItem("plan", "count", ["det1"], num=10, delay=1), pos=0)
        # Insert an item to the position #5 (numbers start from 0)
        RM.item_add(BPlan("count", ["det1"], num=10, delay=1), pos=5)
        # Insert an item before the last item
        RM.item_add(BPlan("count", ["det1"], num=10, delay=1), pos=-1)

        try:
            response = RM.item_add(BPlan("count", ["det1"], num=10, delay=1))
            # No exception was raised, so the request was successful
            assert response["success"] == True
            assert response["msg"] == ""
            # Print some parameters
            print(f"qsize = {response['qsize']}")
            print(f"item = {response['item']}")

            # Insert another plan before the plan that was just inserted
            item_uid = response["item"]["item_uid"]
            RM.item_add(BPlan("count", ["det1"], num=10, delay=1), before_uid=item_uid)
        except RM.RequestFailedError as ex:
            print(f"Request was rejected: {ex}")
            # < code that processes the error >

        # Asynchronous code (0MQ, HTTP)
        # Add an item to the back of the queue
        await RM.item_add({"item_type": "plan", "name": "count", "args": [["det1"]]})
        # Add an item to the front of the queue
        await RM.item_add(BItem("plan", "count", ["det1"], num=10, delay=1), pos="front")
        await RM.item_add(BItem("plan", "count", ["det1"], num=10, delay=1), pos=0)
        # Insert an item to the position #5 (numbers start from 0)
        await RM.item_add(BPlan("count", ["det1"], num=10, delay=1), pos=5)
        # Insert an item before the last item
        await RM.item_add(BPlan("count", ["det1"], num=10, delay=1), pos=-1)
"""

_doc_api_item_add_batch = """
    Add a batch of items to the queue. The batch is represented as a list of items.
    Each item may be a plan or an instruction represented as a dictionary or as an
    instance of ``BItem``, ``BPlan`` or ``BInst`` classes. If one of plans in
    the batch can not be added to the queue (e.g. it does not pass validation),
    then the whole batch is rejected. See documentation for ``item_add`` API
    for more detailed information.

    Parameters
    ----------
    items: list(dict), list(BItem), list(BPlan) or list(BInst)
        A list of dictionary or instances of ``BItem``, ``BPlan`` or ``BInst``
        representing a plan or an instruction.
    pos: str, int or None
        Position of the first item of the batch in the queue. RE Manager will attempt
        to insert the batch so that the first item is at the specified position.
        The position may be positive or negative (counted from the back of the queue)
        integer. If ``pos`` value is a string ``"front"`` or ``"back"``, then the item
        is inserted at the front or the back of the queue. If the value is ``None``,
        then the position is not specified.
    before_uid, after_uid: str or None
        Insert the batch of items before or after the item with the given item UID.
        If ``None`` (default), then the parameters are not specified.

    Returns
    -------
    dict
        Dictionary with item parameters. Dictionary keys: ``success`` (*boolean*),
        ``msg`` (*str*) - error message in case the request was rejected by RE Manager,
        ``qsize`` (*int* or *None*) - new size of the queue or *None* if operation
        failed, ``items`` (*list(dict)* or *None*) - the list of inserted item with
        assigned UID. If the request is rejected, ``item`` may contain the copy of
        the list of submitted items (with assigned UID), *None* or be missing depending
        on the failure.

    Raises
    ------
    Reraises the exceptions raised by ``send_request`` API.

    Examples
    --------

    .. code-block:: python

        plan1 = BPlan("count", ["det1"], num=10, delay=1)
        plan2 = BPlan("count", ["det1"], num=15, delay=1)

        # Synchronous code (0MQ, HTTP)
        RM.item_add_batch([plan1, plan2])

        # Asynchronous code (0MQ, HTTP)
        await RM.item_add_batch([plan1, plan2])
"""

_doc_api_item_update = """
    Update the existing item in the queue. The method is intended for editing queue
    items, but may be used for replacing the existing items with completely different
    ones. The updated item may be a plan or an instruction. The item parameter
    ``item_uid`` must be set to a UID of an existing queue item that is expected
    to be replaced. The method fails if the item UID is not found. By default,
    the UID of the updated item is not changed and ``user`` and ``user_group``
    parameters are set to the values provided in the request. The ``user_group``
    is also used for validation of submitted item. If it is preferable to replace
    the item UID with a new random UID (e.g. if the item is replaced with completely
    different item), the method should be called with the optional parameter
    ``replace=True``.

    Parameters
    ----------
    item: dict, BItem, BPlan or BInst
        Dictionary or an instance of ``BItem``, ``BPlan`` or ``BInst`` representing
        a plan or an instruction.
    replace: boolean
        Replace the updated item UID with the new random UID (``True``) or keep
        the original UID (``False``). Default value is (``False``).

    Returns
    -------
    dict
        Dictionary with item parameters. Dictionary keys: ``success`` (*boolean*),
        ``msg`` (*str*) - error message in case the request was rejected by RE Manager,
        ``qsize`` (*int* or *None*) - the size of the queue or *None* if operation
        failed, ``item`` (*dict* or *None*) - inserted item with assigned UID.
        If the request is rejected, ``item`` may contain the copy of the submitted
        item (with assigned UID), *None* or be missing depending on the failure.

    Raises
    ------
    Reraises the exceptions raised by ``send_request`` API.

    Examples
    --------

    .. code-block:: python

        # Synchronous code (0MQ, HTTP)
        RM.item_add(BPlan("count", ["det1"], num=10, delay=1), pos="back")
        response = RM.item_get(pos="back")
        item = BItem(response["item"])
        item.kwargs["num"] = 50
        RM.item_update(item)

        # Asynchronous code (0MQ, HTTP)
        await RM.item_add(BPlan("count", ["det1"], num=10, delay=1), pos="back")
        response = await RM.item_get(pos="back")
        item = BItem(response["item"])
        item.kwargs["num"] = 50
        await RM.item_update(item)
"""

_doc_api_item_get = """
    Load an existing queue item. Items may be addressed by position or UID.
    Bu default, the API returns the item at the back of the queue.

    Parameters
    ----------
    pos: str, int or None
        Position of the item in the queue. The position may be positive or negative
        (counted from the back of the queue) integer. If ``pos`` value is a string
        ``"front"`` or ``"back"``, then the item at the front or the back of the queue
        is returned. If the value is ``None`` (default), then the position is not specified.
    uid: str or None
        UID of the item. If ``None`` (default), then the parameter are not specified.

    Returns
    -------
    dict
        Dictionary with item parameters. Dictionary keys: ``success`` (*boolean*),
        ``msg`` (*str*) - error message in case the request was rejected by RE Manager,
        ``item`` (*dict*) - the dictionary of item parameters, which is ``{}`` if
        the operation fails.

    Raises
    ------
    Reraises the exceptions raised by ``send_request`` API.

    Examples
    --------

    .. code-block:: python

        # Synchronous code (0MQ, HTTP)
        RM.item_get()
        RM.item_get(pos="front")
        RM.item_get(pos=-2)

        # Asynchronous code (0MQ, HTTP)
        await RM.item_get()
        await RM.item_get(pos="front")
        await RM.item_get(pos=-2)
"""

_doc_api_item_remove = """
    Remove item from the queue. By default the last item in the queue is removed.
    Alternatively the position or UID of the item can be specified.

    Parameters
    ----------
    pos: str, int or None
        Position of the item in the queue. The position may be positive or negative
        (counted from the back of the queue) integer. If ``pos`` value is a string
        ``"front"`` or ``"back"``, then the item at the front or the back of the queue
        is returned. If the value is ``None`` (default), then the position is not specified.
    uid: str or None
        UID of the item. If ``None`` (default), then the parameter are not specified.

    Returns
    -------
    dict
        Dictionary with item parameters. Dictionary keys: ``success`` (*boolean*),
        ``msg`` (*str*) - error message in case the request was rejected by RE Manager,
        ``item`` (*dict*) - the dictionary of item parameters, which is ``{}`` if
        the operation fails, ``qsize`` - the size of the queue.

    Raises
    ------
    Reraises the exceptions raised by ``send_request`` API.

    Examples
    --------

    .. code-block:: python

        # Synchronous code (0MQ, HTTP)
        RM.item_remove()
        RM.item_remove(pos="front")
        RM.item_remove(pos=-1)

        # Asynchronous code (0MQ, HTTP)
        await RM.item_remove()
        await RM.item_remove(pos="front")
        await RM.item_remove(pos=-1)
"""

_doc_api_item_remove_batch = """
    Remove a batch of items from the queue. The batch of items is represented
    as a list of item UIDs.

    Parameters
    ----------
    uids: list(str)
        List of UIDs of the items in the batch. The list may not contain repeated UIDs.
        All UIDs must be present in the queue. The list may be empty.
    ignore_missing: boolean (optional)
        If the value is ``False``, then the method fails if the batch contains repeating
        items or some of the batch items are not found in the queue. If ``True`` (default),
        then the method attempts to remove all items in the batch and ignores missing
        items. The method returns the list of items that were removed from the queue.

    Returns
    -------
    dict
        Dictionary with item parameters. Dictionary keys: ``success`` (*boolean*),
        ``msg`` (*str*) - error message in case the request was rejected by RE Manager,
        ``items`` (*list(dict)*) - the list of removed items, which is ``[]`` if
        the operation fails, ``qsize`` - the size of the queue.

    Raises
    ------
    Reraises the exceptions raised by ``send_request`` API.

    Examples
    --------

    .. code-block:: python

        # Synchronous code (0MQ, HTTP)
        RM.item_remove_batch(["item-uid1", "item-uid2"])

        # Asynchronous code (0MQ, HTTP)
        await RM.item_remove_batch(["item-uid1", "item-uid2"])
"""

_doc_api_item_move = """
    Move item to a different position in the queue. The parameters ``pos`` and
    ``uid`` are mutually exclusive. The parameters ``pos_dest``, ``before_uid``
    and ``after_uid`` are also mutually exclusive.

    Parameters
    ----------
    pos: str, int or None
        Position of the item in the queue. The position may be positive or negative
        (counted from the back of the queue) integer. If ``pos`` value is a string
        ``"front"`` or ``"back"``, then the item at the front or the back of the queue
        is returned. If the value is ``None`` (default), then the position is not specified.
    uid: str or None
        UID of the item to move. If ``None`` (default), then the parameter are not specified.
    pos_dest: str, int or None
        New position of the item. Integer number can be negative.
    before_uid, after_uid: str or None
        UID of an existing item in the queue. The selected item is moved before
        or after this item.

    Returns
    -------
    dict
        Dictionary with item parameters. Dictionary keys: ``success`` (*boolean*),
        ``msg`` (*str*) - error message in case the request was rejected by RE Manager,
        ``item`` (*dict*) - the dictionary of item parameters, which is ``{}`` if
        the operation fails, ``qsize`` - the size of the queue.

    Raises
    ------
    Reraises the exceptions raised by ``send_request`` API.

    Examples
    --------

    .. code-block:: python

        # Synchronous code (0MQ, HTTP)
        RM.item_move(pos="front", pos_dest="5")
        RM.item_move(uid="uid-source", before_uid="uid-dest")

        # Asynchronous code (0MQ, HTTP)
        await RM.item_move(pos="front", pos_dest="5")
        await RM.item_move(uid="uid-source", before_uid="uid-dest")
"""

_doc_api_item_move_batch = """
    Move a batch of item to a different position in the queue. The method accepts
    a list of UIDs of the items included in the batch. The UIDs in the list must
    be unique (not repeated) and items with listed UIDs must exist in the queue.
    If the list is empty, then operation succeeds and the queue remains unchanged.
    The destination must be specified using one of the mutually exclusive parameters
    ``pos_dest``, ``before_uid`` or ``after_uid``. The reference item with the UID
    of passed with the parameters ``before_uid`` or ``after_uid`` must not be
    in the batch. The parameter ``reorder`` controls the order of the items in
    the moved batch and indicates whether items in the batch should be reordered
    with respect to the order of UIDs in the list ``uids``. The batch may include
    any set of non-repeated items from the queue arranged in arbitrary order.
    By default (``reorder=False``) the batch is inserted in the specified position
    as a contiguous sequence of items ordered according to the UIDs in the list
    ``uids``. If ``reorder=True``, then the inserted items are ordered according
    to their original positions in the queue. It is assumed that the method will
    be mostly used with the default ordering option and user will be responsible
    for creating properly ordered lists of items. The other option is implemented
    for the cases when the user may want to submit randomly ordered lists of UIDs,
    but preserve the original order of the moved batch.

    Parameters
    ----------
    uids: list(str)
        List of UIDs of the items in the batch. The list may not contain repeated UIDs.
        All UIDs must be present in the queue. The list may be empty.
    pos_dest: str ("front" or "back")
        New position of the item. Only string values ``'front'`` and ``'back'``
        are accepted.
    before_uid, after_uid: str or None
        UID of an existing item in the queue. The selected item will be moved before
        or after this item. The item with the specified UID may not be included
        in the batch.
    reorder: boolean
        Arrange moved items in the order of UIDs in the ``uids`` list (False, default) or
        according to the original item positions in the queue (True).

    Returns
    -------
    dict
        Dictionary with item parameters. Dictionary keys: ``success`` (*boolean*),
        ``msg`` (*str*) - error message in case the request was rejected by RE Manager,
        ``items`` (*list(dict)*) - the list of moved items, which is ``[]`` if
        the operation fails, ``qsize`` - the size of the queue.

    Raises
    ------
    Reraises the exceptions raised by ``send_request`` API.

    Examples
    --------

    .. code-block:: python

        # Synchronous code (0MQ, HTTP)
        RM.item_move_batch(uids=["uid1", "uid2"], pos_dest="front")
        RM.item_move_batch(uids=["uid1", "uid2"], before_uid="uid-dest")

        # Asynchronous code (0MQ, HTTP)
        await RM.item_move_batch(uids=["uid1", "uid2"], pos_dest="front")
        await RM.item_move_batch(uids=["uid1", "uid2"], before_uid="uid-dest")
"""


_doc_api_item_execute = """
    Immediately start execution of the submitted item. The item may be a plan or
    an instruction. The request fails if item execution can not be started immediately
    (RE Manager is not in IDLE state, RE Worker environment does not exist, etc.).
    If the request succeeds, the item is executed once. The item is not added to
    the queue if it can not be immediately started and it is not pushed back into
    the queue in case its execution fails/stops. If the queue is in the LOOP mode,
    the executed item is not added to the back of the queue after completion.
    The API request does not alter the sequence of enqueued plans.

    Parameters
    ----------
    item: dict, BItem, BPlan or BInst
        Dictionary or an instance of ``BItem``, ``BPlan`` or ``BInst`` representing
        a plan or an instruction.

    Returns
    -------
    dict
        Dictionary with item parameters. Dictionary keys: ``success`` (*boolean*),
        ``msg`` (*str*) - error message in case the request was rejected by RE Manager,
        ``item`` (*dict*) - the dictionary of item parameters, ``None`` if the
        request contains no ``item`` parameter, ``qsize`` - the size of the queue.

    Raises
    ------
    Reraises the exceptions raised by ``send_request`` API.

    Examples
    --------

    .. code-block:: python

        # Synchronous code (0MQ, HTTP)
        RM.item_execute(BPlan("count", ["det1"], num=10, delay=1))

        # Asynchronous code (0MQ, HTTP)
        await RM.item_execute(BPlan("count", ["det1"], num=10, delay=1))
"""


_doc_api_queue_start = """
    Start execution of the queue. If the request is accepted, the ``manager_state``
    status parameter is expected to change to ``starting_queue``, then ``executing_queue``
    and change back to ``idle`` when the queue is completed or stopped.

    Returns
    -------
    dict
        Dictionary keys: ``success`` (*boolean*), ``msg`` (*str*) - error message
        in case the request was rejected by RE Manager, ``item`` (*dict*) - the dictionary
        of item parameters, which is ``{}`` if the operation fails.

    Raises
    ------
    Reraises the exceptions raised by ``send_request`` API.

    Examples
    --------

    .. code-block:: python

        # Synchronous code (0MQ, HTTP)
        RM.queue_start()

        # Asynchronous code (0MQ, HTTP)
        await RM.queue_start()
"""

_doc_api_environment_open = """
    Open RE Worker environment. The API request only initiates the operation of
    opening an environment. If the request is accepted, the ``manager_state``
    status parameter is expected to change to ``creating_environment`` and then
    changed back to ``idle`` when the operation is completed. Check
    ``worker_environment_exists`` to see if the environment was opened successfully.

    Returns
    -------
    dict
        Dictionary keys: ``success`` (*boolean*), ``msg`` (*str*) - error message
        in case the request was rejected by RE Manager.

    Raises
    ------
    Reraises the exceptions raised by ``send_request`` API.

    Examples
    --------

    .. code-block:: python

        # Synchronous code (0MQ, HTTP)
        RM.environment_open()

        # Asynchronous code (0MQ, HTTP)
        await RM.environment_open()
"""

_doc_api_environment_close = """
    Close RE Worker environment. The API request only initiates the operation of
    opening an environment. The environment can not be closed if any plans or
    foreground tasks are running. If the request is accepted, the ``manager_state``
    status parameter is expected to change to ``closing_environment`` and then
    back to ``idle`` when the operation is completed. Check ``worker_environment_exists``
    status flag to see if the environment was closed.

    Returns
    -------
    dict
        Dictionary keys: ``success`` (*boolean*), ``msg`` (*str*) - error message
        in case the request was rejected by RE Manager.

    Raises
    ------
    Reraises the exceptions raised by ``send_request`` API.

    Examples
    --------

    .. code-block:: python

        # Synchronous code (0MQ, HTTP)
        RM.environment_close()

        # Asynchronous code (0MQ, HTTP)
        await RM.environment_close()
"""

_doc_api_environment_destroy = """
    Destroy RE Worker environment. This is the last-resort operation that allows to
    recover the Queue Server if RE Worker environment becomes unresponsive and needs
    to be shut down. The operation kills RE Worker process, therefore it can be executed
    with the environment in any state. The operation may be dangerous, since it kills any
    running plans or tasks. After the operation is completed, a new environment
    may be opened and operations countinued. The API request only initiates the operation
    of destroying an environment. If the request is accepted, the ``manager_state``
    status parameter is expected to change to ``destroying_environment`` and then
    back to ``idle`` when the operation is completed. Check ``worker_environment_exists``
    status flag to see if the environment was destroyed.

    Returns
    -------
    dict
        Dictionary keys: ``success`` (*boolean*), ``msg`` (*str*) - error message
        in case the request was rejected by RE Manager.

    Raises
    ------
    Reraises the exceptions raised by ``send_request`` API.

    Examples
    --------

    .. code-block:: python

        # Synchronous code (0MQ, HTTP)
        RM.environment_destroy()

        # Asynchronous code (0MQ, HTTP)
        await RM.environment_destroy()
"""
