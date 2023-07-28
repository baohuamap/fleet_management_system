# test_fleets.py

from test.database import client, session

import pytest

from app import schemas


@pytest.mark.parametrize(
    "fleet_name, fleet_info, phone_number, expected",
    [
        ("Team F", "NYC", "113", 201),
        ("Team ABC", "NYC", "113", 400),
        ("Team bruh bruh", "BKK", "114", 201),
        ("Team lmao", "London", "115", 201),
    ],
)
def test_create_fleet(client, fleet_name, fleet_info, phone_number, expected):
    ret = client.post(
        "/api/fleets/",
        json={
            "fleet_name": f"{fleet_name}",
            "fleet_info": f"{fleet_info}",
            "phone_number": f"{phone_number}",
        },
    )
    print(ret.json())
    assert ret.status_code == expected
    if expected == 201:
        new_fleet = schemas.CreateFleet(**ret.json())
        assert new_fleet.fleet_name == fleet_name
        assert new_fleet.fleet_info == fleet_info
        assert new_fleet.phone_number == phone_number
    if expected == 400:
        assert ret.json().get("detail") == "Error create fleet"


def test_get_fleets():
    pass
