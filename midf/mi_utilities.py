__all__ = ["make_mi_building_admin_id_midf", "clean_admin_id"]


def make_mi_building_admin_id_midf(building_id: str, venue_key: str) -> str:
    """

    :param building_id:
    :type building_id:
    :param venue_key:
    :type venue_key:
    :return:
    :rtype:
    """
    return f"{building_id.lower().replace(' ', '_')}_{venue_key}"


def clean_admin_id(admin_id: str) -> str:
    """

    :param admin_id:
    :type admin_id:
    :return:
    :rtype:
    """
    return admin_id.lower().replace(" ", "_").replace("{", "").replace("}", "").strip()
