from cloudshell.api.cloudshell_api import CloudShellAPISession, Connector


def is_layer_2_connector(connector: Connector) -> bool:
    for attr in connector.Attributes:
        if attr.Name == "Selected Network":
            return True
    return False


def disconnect_all(api: CloudShellAPISession):
    all_sbs = api.GetCurrentReservations().Reservations
    for sb in all_sbs:
        details = api.GetReservationDetails(sb.Id, True).ReservationDescription
        l2_routes = [connector for connector in details.Connectors if is_layer_2_connector(connector)]
        for route in l2_routes:
            try:
                api.DisconnectRoutesInReservation(reservationId=sb.Id, endpoints=[route.Source, route.Target])
            except Exception as e:
                pass
            else:
                print(f"Disconnected {route.Source} -> {route.Target} in sandbox {sb.Id}")


if __name__ == "__main__":
    api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")
    disconnect_all(api)
