# test_fleets.py

import pytest

from app import schemas

# @pytest.mark.parametrize(
#     "fleet_name, fleet_info, phone_number, expected",
#     [
#         ("Team F", "NYC", "113", 201),
#         ("Team ABC", "NYC", "113", 201),
#         ("Team bruh bruh", "BKK", "114", 201),
#         ("Team lmao", "London", "115", 201),
#     ],
# )
# def test_create_fleet(client, fleet_name, fleet_info, phone_number, expected):
#     ret = client.post(
#         "/api/fleets/",
#         json={
#             "fleet_name": f"{fleet_name}",
#             "fleet_info": f"{fleet_info}",
#             "phone_number": f"{phone_number}",
#         },
#     )
#     print(ret.json())
#     assert ret.status_code == expected
#     new_fleet = schemas.CreateFleet(**ret.json())
#     assert new_fleet.fleet_name == fleet_name
#     assert new_fleet.fleet_info == fleet_info
#     assert new_fleet.phone_number == phone_number


def test_create_error_fleet(client):
    ret1 = client.post(
        "/api/fleets/",
        json={
            "fleet_name": "a",
            "fleet_info": "b",
            "phone_number": "123",
        },
    )
    assert ret1.status_code == 201
    ret2 = client.post(
        "/api/fleets/",
        json={
            "fleet_name": "c",
            "fleet_info": "d",
            "phone_number": "123",
        },
    )
    assert ret2.status_code == 400
    assert ret2.json().get("detail") == "Error create fleet"


def test_get_fleets(client, test_fleets):
    ret = client.get("/api/fleets/")

    def validate(fleets):
        return schemas.Fleet(**fleets)

    fleets_map = map(validate, ret.json())
    fleets_list = list(fleets_map)

    assert len(fleets_list) == len(test_fleets)
    assert ret.status_code == 200
