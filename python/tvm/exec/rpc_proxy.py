# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# pylint: disable=redefined-outer-name, invalid-name
"""RPC web proxy, allows redirect to websocket based RPC servers(browsers)"""
import logging
import argparse
import os
from tvm.rpc.proxy import Proxy


def find_example_resource():
    """Find resource examples."""
    curr_path = os.path.dirname(os.path.realpath(os.path.expanduser(__file__)))
    base_path = os.path.abspath(os.path.join(curr_path, "..", "..", ".."))
    print("find_example_resource ===>  base_path={}".format(base_path))
    index_page = os.path.join(base_path, "web", "apps", "browser", "rpc_server.html")

    resource_files = [
        os.path.join(base_path, "web", "dist", "tvmjs.bundle.js"),
        os.path.join(base_path, "web", "dist", "wasm", "tvmjs_runtime.wasi.js"),
        # os.path.join(base_path, "web", "dist", "wasm", "module.json"), # dyg adds
        # os.path.join(base_path, "web", "dist", "wasm", "module.params"), # dyg add
    ]
    
    tunning_wasm = os.path.join(base_path, "web", "dist", "wasm", "turning.wasm")
    if os.path.exists(tunning_wasm):
        resource_files.append(tunning_wasm);
    print("resource_files : {}".format(resource_files))
    resource_base = os.path.join(base_path, "web", "dist", "www")
    if os.path.isdir(resource_base):
        for fname in os.listdir(resource_base):
            full_name = os.path.join(resource_base, fname)
            if os.path.isfile(full_name):
                resource_files.append(full_name)
    for fname in [index_page] + resource_files:
        print(fname)
        if not os.path.exists(fname):
            raise RuntimeError("Cannot find %s" % fname)
    return index_page, resource_files


def main(args):
    """Main function"""
    if args.tracker:
        url, port = args.tracker.split(":")
        port = int(port)
        tracker_addr = (url, port)
    else:
        tracker_addr = None

    if args.example_rpc:
        index, js_files = find_example_resource()
        prox = Proxy(
            args.host,
            port=args.port,
            web_port=args.web_port,
            index_page=index,
            resource_files=js_files,
            tracker_addr=tracker_addr,
        )
    else:
        prox = Proxy(args.host, port=args.port, web_port=args.web_port, tracker_addr=tracker_addr)
    prox.proc.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="127.0.0.1", help="the hostname of the server")
    parser.add_argument("--port", type=int, default=9090, help="The port of the RPC")
    parser.add_argument(
        "--web-port", type=int, default=8888, help="The port of the http/websocket server"
    )
    parser.add_argument(
        "--example-rpc", type=bool, default=False, help="Whether to switch on example rpc mode"
    )
    parser.add_argument("--tracker", type=str, default="", help="Report to RPC tracker")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    main(args)
