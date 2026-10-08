import os
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen

from business_brief import dashboard


def test_server_binds_public_interface_and_env_port(monkeypatch):
    addresses = []

    class Server:
        def __init__(self, address, handler):
            addresses.append(address)

        def serve_forever(self):
            pass

    monkeypatch.setenv("PORT", "18765")
    monkeypatch.setattr(dashboard, "ThreadingHTTPServer", Server)
    dashboard.main()
    assert addresses == [("0.0.0.0", 18765)]


def test_real_module_startup_and_http():
    # Exercise real dependency imports and the same module entrypoint as Railway.
    import socket

    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    env = dict(os.environ, PORT=str(port), PYTHONPATH="src")
    process = subprocess.Popen(
        [sys.executable, "-m", "business_brief.dashboard"], env=env,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    try:
        for _ in range(100):
            assert process.poll() is None, process.communicate()[1].decode()
            try:
                with urlopen(f"http://127.0.0.1:{port}/", timeout=1) as response:
                    assert response.status == 200
                    assert b"Business Brief Control Tower" in response.read()
                break
            except URLError:
                time.sleep(0.05)
        else:
            raise AssertionError("Dashboard did not serve HTTP within 5 seconds")
    finally:
        process.terminate()
        process.communicate(timeout=5)
