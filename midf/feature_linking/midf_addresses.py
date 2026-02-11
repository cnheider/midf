import logging
from typing import Collection, Dict, List, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFAddress, IMDFFeature
from midf.model import MIDFAddress, MIDFVenue

__all__ = ["link_addresses"]

_logger = logging.getLogger(__name__)


def link_addresses(
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]],
    venue_mapping: dict[str, List[MIDFVenue]],
) -> Dict[str, MIDFAddress]:
    """

    :param imdf_dict:
    :type imdf_dict:
    :param venue_mapping:
    :type venue_mapping:
    :return:
    :rtype:
    """
    addresses = {}
    _logger.error(f"Linking addresses: {len(imdf_dict[IMDFFeatureType.address])}")

    found_venue_addresses = venue_mapping.keys()

    venue_mapping_copy = venue_mapping.copy()

    for address in imdf_dict[IMDFFeatureType.address]:
        address: IMDFAddress
        assert address.id not in addresses
        addresses[address.id] = MIDFAddress(
            id=address.id,
            address=address.address,
            locality=address.locality,
            country=address.country,
            province=address.province,
            unit=address.unit,
            postal_code=address.postal_code,
            postal_code_ext=address.postal_code_ext,
            postal_code_vanity=address.postal_code_vanity,
            venues=(
                venue_mapping_copy.pop(address.id)
                if address.id in found_venue_addresses
                else None
            ),
        )

    if len(addresses) == 0:
        _logger.error("No addresses were found in the data")
        if True:  # TODO: DISABLE WHEN DONE TESTING
            for address_id, v in venue_mapping_copy.items():
                dummy_address = MIDFAddress(
                    id=address_id,
                    address="dummy_address",
                    locality="dummy_address",
                    country="dummy_address",
                    province="dummy_address",
                    unit="dummy_address",
                    postal_code="dummy_address",
                    postal_code_ext="dummy_address",
                    postal_code_vanity="dummy_address",
                    venues=v,
                )

                addresses[address_id] = dummy_address

    return addresses
