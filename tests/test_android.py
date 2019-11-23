# MIT licensed
# Copyright (c) 2017 Yen Chi Hsuan <yan12125 at gmail dot com>

import pytest
# Need https://github.com/Martiusweb/asynctest/issues/46 fixed for working correctly
# https://bugs.python.org/issue26467 targets the same functionality for the built-in unittests module
from asynctest import patch
pytestmark = [pytest.mark.asyncio, pytest.mark.needs_net]

async def test_android_addon(get_version):
    assert await get_version("android-google-play-apk-expansion", {"android_sdk": "extras;google;market_apk_expansion", "repo": "addon"}) == "1.r03"

async def test_android_package(get_version):
    assert await get_version("android-sdk-cmake", {"android_sdk": "cmake;", "repo": "package"}) == "3.6.4111459"

async def test_android_repo_manifest_cache(get_version):
    with patch('nvchecker.source.session.get') as patched_session_get, patch('nvchecker.source.android_sdk._repo_manifests_cache', new={}):
        await get_version("android-foo", {"android_sdk": "foo", "repo": "addon"})
        await get_version("android-bar", {"android_sdk": "bar", "repo": "addon"})
        patched_session_get.assert_called_once()
