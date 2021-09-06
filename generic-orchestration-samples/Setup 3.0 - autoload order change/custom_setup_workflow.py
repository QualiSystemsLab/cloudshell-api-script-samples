from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.setup.default_setup_logic import DefaultSetupLogic
from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow


class CustomSetupWorkflow(DefaultSetupWorkflow):
    def __init__(self):
        super(CustomSetupWorkflow, self).__init__()

    def register(self, sandbox, enable_provisioning=True, enable_connectivity=True, enable_configuration=True):
        """
        :param bool enable_provisioning:
        :param bool enable_connectivity:
        :param bool enable_configuration:
        :param Sandbox sandbox:
        :return:
        """
        sandbox.logger.info("Adding default setup orchestration")
        if enable_provisioning:
            sandbox.logger.debug("Default provisioning is added to sandbox orchestration")
            sandbox.workflow.add_to_provisioning(self.default_provisioning, None)
        if enable_connectivity:
            sandbox.logger.debug("Default connectivity is added to sandbox orchestration")
            sandbox.workflow.add_to_connectivity(self.default_connectivity, None)
        if enable_configuration:
            sandbox.logger.debug("Default configuration is added to sandbox orchestration")
            sandbox.workflow.add_to_configuration(self.default_configuration, None)

    def default_provisioning(self, sandbox, components):
        """
        :param Sandbox sandbox:
        :return:
        """
        api = sandbox.automation_api

        sandbox.logger.info("Executing default provisioning")

        reservation_details = api.GetReservationDetails(reservationId=sandbox.id, disableCache=True)
        self._deploy_result = DefaultSetupLogic.deploy_apps_in_reservation(api=api,
                                                                           reservation_details=reservation_details,
                                                                           reservation_id=sandbox.id,
                                                                           logger=sandbox.logger)

        DefaultSetupLogic.validate_all_apps_deployed(deploy_results=self._deploy_result,
                                                     logger=sandbox.logger)

        sandbox.components.refresh_components(sandbox=sandbox)



    def default_connectivity(self, sandbox, components):
        """
        :param Sandbox sandbox:
        :return:
        """
        api = sandbox.automation_api

        sandbox.logger.info("Executing default connectivity")

        reservation_details = api.GetReservationDetails(reservationId=sandbox.id, disableCache=True)

        connect_results = DefaultSetupLogic.connect_all_routes_in_reservation(api=api,
                                                            reservation_details=reservation_details,
                                                            reservation_id=sandbox.id,
                                                            resource_details_cache=self._resource_details_cache,
                                                            logger=sandbox.logger)

        DefaultSetupLogic.activate_routes(api=api,
                                        reservation_details=reservation_details,
                                        reservation_id=sandbox.id,
                                        logger=sandbox.logger)

        DefaultSetupLogic.run_async_power_on_refresh_ip(api=api,
                                                        reservation_details=reservation_details,
                                                        deploy_results=self._deploy_result,
                                                        resource_details_cache=self._resource_details_cache,
                                                        reservation_id=sandbox.id,
                                                        logger=sandbox.logger,
                                                        components=sandbox.components)

        DefaultSetupLogic.refresh_vm_details(api=api,
                                             reservation_details=reservation_details,
                                             connect_results=connect_results,
                                             resource_details_cache=self._resource_details_cache,
                                             logger=sandbox.logger,
                                             components=sandbox.components)

        DefaultSetupLogic.try_exeucte_autoload(api=api,
                                               deploy_result=self._deploy_result,
                                               resource_details_cache=self._resource_details_cache,
                                               reservation_id=sandbox.id,
                                               logger=sandbox.logger, components=sandbox.components)

    def default_configuration(self, sandbox, components):
        """
        :param Sandbox sandbox:
        :return:
        """
        sandbox.logger.info("Executing default configuration")
        DefaultSetupLogic.configure_apps(api=sandbox.automation_api,
                                         reservation_id=sandbox.id,
                                         logger=sandbox.logger)
