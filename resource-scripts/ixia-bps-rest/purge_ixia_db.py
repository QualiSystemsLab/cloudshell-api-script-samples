from bps_restpy.bps import BPS
from bps_restpy.bps_restpy_v1.bpsAdminRest import BPS_Storrage


class IxiaCleanupException(Exception):
    pass


def validate_result(result: bool, action=""):
    if not result:
        msg = "Issue during Ixia action"
        if action:
            msg += f": '{action}'"
        raise IxiaCleanupException(msg)


def purge_ixia_db_flow(ip, user, password):
    """
    instantiate api session, purge and compact reports in ixia
    :param str ip:
    :param str user:
    :param str password:
    :return:
    """
    # Login to BPS box
    bps = BPS(ip, user, password)

    # get storage controller
    bps_storage = BPS_Storrage(bps)

    # login
    bps_storage.login()

    # purge reports
    purge_result = bps_storage.purgeReports(versionId=None)
    validate_result(purge_result, action="PURGE DB")

    # compact storage
    compact_result = bps_storage.compactStorage(versionId=None)
    validate_result(compact_result, action="COMPACT DB")


if __name__ == "__main__":
    # bps system info
    bps_system = '<BPS_BOX_IP/HOSTNAME>'
    bpsuser = 'bps user'
    bpspass = 'bps pass'

    purge_ixia_db_flow(bps_system, bpsuser, bpspass)
