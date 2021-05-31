from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.setup.default_setup_logic import DefaultSetupLogic
from cloudshell.workflow.orchestration.workflow import Workflow


class CustomWorkflow(Workflow):
    def __init__(self, sandbox):
        super(CustomWorkflow, self).__init__(sandbox)

    def _validate_function(self, func):
        self.sandbox.logger.info('Custom Sandbox Object being used. No validation done on Workflow functions')
        pass


class CustomSandbox(Sandbox):
    def __init__(self):
        super(CustomSandbox, self).__init__()
        self.workflow = CustomWorkflow(self)

    def _execute_workflow_process(self, func, components):
        self.logger.info("Executing method: {0}. ".format(func.__name__))
        execution_failed = 0
        try:
            self.logger.info("Executing workflow function with no parameters passed")
            func()

        except Exception as exc:
            self.logger.info("except Exception as exc")
            execution_failed = 1
            if not hasattr(exc, 'message'):  # python 3
                error = str(exc)
                self.logger.info("type of exc is {}".format(str(type(exc))))
            else:
                error = exc.message
            self._exception = exc
            if not error or not isinstance(error, str):
                try:
                    error = str(exc)
                except Exception:
                    pass

            if self.suppress_exceptions:
                print (error)
            self.logger.exception("Error was thrown during orchestration execution: ")

        return execution_failed


class CustomSetupWorkflow(object):
    def __init__(self, sandbox):
        """
        :param Sandbox sandbox:
        """
        self.sandbox = sandbox
        self._deploy_result = None
        self._resource_details_cache = {}

    def register(self, enable_provisioning=True, enable_connectivity=True, enable_configuration=True):
        """
        :param bool enable_provisioning:
        :param bool enable_connectivity:
        :param bool enable_configuration:
        :return:
        """
        self.sandbox.logger.info("Adding default setup orchestration")
        if enable_provisioning:
            self.sandbox.logger.debug("Default provisioning is added to sandbox orchestration")
            self.sandbox.workflow.add_to_provisioning(self.default_provisioning, None)
        if enable_connectivity:
            self.sandbox.logger.debug("Default connectivity is added to sandbox orchestration")
            self.sandbox.workflow.add_to_connectivity(self.default_connectivity, None)
        if enable_configuration:
            self.sandbox.logger.debug("Default configuration is added to sandbox orchestration")
            self.sandbox.workflow.add_to_configuration(self.default_configuration, None)

    def default_provisioning(self):
        """
        :return:
        """
        api = self.sandbox.automation_api

        self.sandbox.logger.info("Executing default provisioning")

        reservation_details = api.GetReservationDetails(reservationId=self.sandbox.id, disableCache=True)
        self._deploy_result = DefaultSetupLogic.deploy_apps_in_reservation(api=api,
                                                                           reservation_details=reservation_details,
                                                                           reservation_id=self.sandbox.id,
                                                                           logger=self.sandbox.logger)

        DefaultSetupLogic.validate_all_apps_deployed(deploy_results=self._deploy_result,
                                                     logger=self.sandbox.logger)

        self.sandbox.components.refresh_components(sandbox=self.sandbox)

        DefaultSetupLogic.try_exeucte_autoload(api=api,
                                               deploy_result=self._deploy_result,
                                               resource_details_cache=self._resource_details_cache,
                                               reservation_id=self.sandbox.id,
                                               logger=self.sandbox.logger, components=self.sandbox.components)

    def default_connectivity(self):
        """
        :return:
        """
        api = self.sandbox.automation_api

        self.sandbox.logger.info("Executing default connectivity")

        reservation_details = api.GetReservationDetails(reservationId=self.sandbox.id, disableCache=True)

        connect_results = DefaultSetupLogic.connect_all_routes_in_reservation(api=api,
                                                                              reservation_details=reservation_details,
                                                                              reservation_id=self.sandbox.id,
                                                                              resource_details_cache=self._resource_details_cache,
                                                                              logger=self.sandbox.logger)

        DefaultSetupLogic.activate_routes(api=api,
                                          reservation_details=reservation_details,
                                          reservation_id=self.sandbox.id,
                                          logger=self.sandbox.logger)

        DefaultSetupLogic.run_async_power_on_refresh_ip(api=api,
                                                        reservation_details=reservation_details,
                                                        deploy_results=self._deploy_result,
                                                        resource_details_cache=self._resource_details_cache,
                                                        reservation_id=self.sandbox.id,
                                                        logger=self.sandbox.logger,
                                                        components=self.sandbox.components)

        DefaultSetupLogic.refresh_vm_details(api=api,
                                             reservation_details=reservation_details,
                                             connect_results=connect_results,
                                             resource_details_cache=self._resource_details_cache,
                                             logger=self.sandbox.logger,
                                             components=self.sandbox.components)

    def default_configuration(self):
        """
        :return:
        """
        self.sandbox.logger.info("Executing default configuration")
        DefaultSetupLogic.configure_apps(api=self.sandbox.automation_api,
                                         reservation_id=self.sandbox.id,
                                         logger=self.sandbox.logger)
