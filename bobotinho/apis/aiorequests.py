# -*- coding: utf-8 -*-
import asyncio
from typing import Union

import aiohttp

__all__ = ("request", "no_wait_request", "get", "post")


async def request(
    url: str,
    method: str = "get",
    res_method: str = "json",
    raise_for_status: bool = True,
    *args,
    **kwargs
) -> Union[str, dict]:
    async with aiohttp.ClientSession(raise_for_status=raise_for_status) as session:
        async with session.request(method, url, *args, **kwargs) as response:
            return await getattr(response, res_method)()


def no_wait_request(
    url: str,
    method: str = "get",
    res_method: str = "json",
    raise_for_status: bool = True,
    *args,
    **kwargs
) -> asyncio.Task:
    return asyncio.create_task(request(url, method, res_method, raise_for_status, *args, **kwargs))


async def get(
    url: str,
    res_method: str = "json",
    raise_for_status: bool = True,
    wait_response: bool = True,
    *args,
    **kwargs
) -> Union[str, dict, asyncio.Task]:
    if wait_response:
        return await request(url, "get", res_method, raise_for_status, *args, **kwargs)
    return no_wait_request(url, "get", res_method, raise_for_status, *args, **kwargs)


async def post(
    url: str,
    res_method: str = "json",
    raise_for_status: bool = True,
    wait_response: bool = True,
    *args,
    **kwargs
) -> Union[str, dict, asyncio.Task]:
    if wait_response:
        return await request(url, "post", res_method, raise_for_status, *args, **kwargs)
    return no_wait_request(url, "post", res_method, raise_for_status, *args, **kwargs)
