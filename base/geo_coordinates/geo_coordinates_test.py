import sys
from dataclasses import dataclass

import pytest

from base.geo_coordinates.geo_coordinates import UTMInfo, find_utm_info


@dataclass
class LatLon:
    latitude: float
    longitude: float


@pytest.mark.parametrize(
    "lat_lon, expected_utm_info",
    [
        (  # Bonn
            LatLon(latitude=50.735851, longitude=7.10066),
            UTMInfo(easting=365974, northing=5622171, zone_number=32, zone_letter="U", epsg_code="EPSG:32632"),
        ),
        (  # Artery data north east of 0,0
            LatLon(latitude=0.1, longitude=0.1),
            UTMInfo(easting=177164, northing=11067, zone_number=31, zone_letter="N", epsg_code="EPSG:32631"),
        ),
        (  # Artery data south west of 0,0
            LatLon(latitude=-0.1, longitude=-0.1),
            UTMInfo(easting=822836, northing=9988933, zone_number=30, zone_letter="M", epsg_code="EPSG:32730"),
        ),
    ],
)
def test_find_utm_info_pass(lat_lon: LatLon, expected_utm_info: UTMInfo) -> None:
    actual_utm_info = find_utm_info(latitude=lat_lon.latitude, longitude=lat_lon.longitude)
    assert actual_utm_info == expected_utm_info


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
