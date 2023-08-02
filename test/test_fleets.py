# test_fleets.py

from uuid import uuid4

import pytest

from app import schemas


@pytest.mark.parametrize(
    "fleet_name, fleet_info, phone_number, status_code",
    [
        ("Team F", "NYC", "117", 201),
        ("Team ABC", "NYC", "abc", 201),
        ("Team bruh bruh", "BKK", "090880", 201),
        ("Team lmao", "", "0zxfa221", 201),
    ],
)
def test_create_fleet(
    client, test_fleets, fleet_name, fleet_info, phone_number, status_code
):
    ret = client.post(
        "/api/fleets/",
        json={
            "fleet_name": f"{fleet_name}",
            "fleet_info": f"{fleet_info}",
            "phone_number": f"{phone_number}",
        },
    )
    print(ret.json())
    assert ret.status_code == status_code
    new_fleet = schemas.CreateFleet(**ret.json())
    assert new_fleet.fleet_name == fleet_name
    assert new_fleet.fleet_info == fleet_info
    assert new_fleet.phone_number == phone_number


@pytest.mark.parametrize(
    "fleet_name, fleet_info, phone_number, status_code",
    [
        ("Team F", "NYC", "113", 400),
        ("Team A", "NYC", "115", 400),
        ("Team bruh bruh", None, "114", 400),
        (None, "London", "115", 400),
    ],
)
def test_create_fleet_error(
    client, test_fleets, fleet_name, fleet_info, phone_number, status_code
):
    ret = client.post(
        "/api/fleets/",
        json={
            "fleet_name": f"{fleet_name}",
            "fleet_info": f"{fleet_info}",
            "phone_number": f"{phone_number}",
        },
    )
    print(ret.json())
    assert ret.status_code == status_code


def test_get_fleets(client, test_fleets):
    ret = client.get("/api/fleets/")

    def validate(fleets):
        return schemas.Fleet(**fleets)

    fleets_map = map(validate, ret.json())
    fleets_list = list(fleets_map)

    assert len(fleets_list) == len(test_fleets)
    assert ret.status_code == 200


def test_get_fleet(client, test_fleets):
    ret = client.get(f"/api/fleets/{test_fleets[0].id}")
    assert ret.status_code == 200


def test_get_unknown_fleet(client, test_fleets):
    random_uuid = uuid4()
    ret = client.get(f"/api/fleets/{random_uuid}")
    assert ret.status_code == 404
    assert ret.json().get("detail") == "Fleet does not exist"


def test_delete_fleet(client, test_fleets):
    fleet_uuid = test_fleets[0].id
    ret = client.delete(f"/api/fleets/{fleet_uuid}")
    assert ret.status_code == 204
    ret = client.get(f"/api/fleets/{fleet_uuid}")
    assert ret.status_code == 404
    assert ret.json().get("detail") == "Fleet does not exist"


@pytest.mark.parametrize(
    "fleet_name, fleet_info, phone_number, status_code",
    [
        ("Team 1", "NYC", "123456789", 200),
        ("Team 2", "SGN", "987654321", 200),
    ],
)
def test_update_fleet(
    client, test_fleets, fleet_name, fleet_info, phone_number, status_code
):
    fleet_uuid = test_fleets[1].id
    ret = client.put(
        f"/api/fleets/{fleet_uuid}",
        json={
            "fleet_name": f"{fleet_name}",
            "fleet_info": f"{fleet_info}",
            "phone_number": f"{phone_number}",
        },
    )
    updated_fleet = schemas.CreateFleet(**ret.json())
    assert ret.status_code == status_code
    assert updated_fleet.fleet_name == fleet_name
    assert updated_fleet.fleet_info == fleet_info
    assert updated_fleet.phone_number == phone_number


@pytest.mark.parametrize(
    "fleet_name, fleet_info, phone_number, status_code",
    [
        ("Team B", "NYC", "123456789", 400),  # existed name
        ("Black Pink", "SGN", "115", 400),  # existed phone
    ],
)
def test_update_fleet_error(
    client, test_fleets, fleet_name, fleet_info, phone_number, status_code
):
    fleet_uuid = test_fleets[0].id
    ret = client.put(
        f"/api/fleets/{fleet_uuid}",
        json={
            "fleet_name": f"{fleet_name}",
            "fleet_info": f"{fleet_info}",
            "phone_number": f"{phone_number}",
        },
    )
    assert ret.status_code == status_code
    assert ret.json().get("detail") == "Error update fleet"
