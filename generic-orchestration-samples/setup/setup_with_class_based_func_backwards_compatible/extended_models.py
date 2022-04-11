from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.workflow import Workflow
import inspect


def _is_bound_method(method):
    """
    check if the method or function is bound (will pass self as first arg)
    :param method:
    :return:
    """
    return hasattr(method, '__self__')


class CustomWorkflow(Workflow):
    def __init__(self, sandbox):
        super(CustomWorkflow, self).__init__(sandbox)

    def _validate_function(self, func):
        """
        changing validation from a requirement of two parameters, to restricting to max of 2 optional parameters
        bound class methods will receive an extra 'self' param
        :param function func: the user function that is passed to orchestration
        :return:
        """
        args = inspect.getargspec(func).args
        is_bound_method = _is_bound_method(func)

        if is_bound_method:
            if len(args) > 3:
                raise Exception("Orchestration methods can not have more than 2 parameters. (Sandbox, Components)")
        else:
            if len(args) > 2:
                raise Exception("Orchestration functions can not have more than 2 parameters. (Sandbox, Components)")


class CustomSandbox(Sandbox):
    def __init__(self):
        super(CustomSandbox, self).__init__()
        self.workflow = CustomWorkflow(self)

    def _execute_workflow_process(self, func, components):
        self.logger.info("Executing method: {0}. ".format(func.__name__))
        execution_failed = 0

        args = inspect.getargspec(func).args
        is_bound_method = _is_bound_method(func)

        try:
            if is_bound_method:
                if len(args) == 1:
                    self.logger.info("Executing workflow bound method with no additional parameters passed")
                    func()
                elif len(args) == 2:
                    self.logger.info("Executing workflow bound method with 1 parameter passed (Sandbox)")
                    func(self)
                else:
                    self.logger.info("Executing workflow bound method with 2 parameters passed (Sandbox, Components)")
                    func(self, components)
            else:
                if not len(args):
                    self.logger.info("Executing workflow function with no parameters passed")
                    func()
                elif len(args) == 1:
                    self.logger.info("Executing workflow function with 1 parameter passed (Sandbox)")
                    func(self)
                else:
                    self.logger.info("Executing workflow function with 2 parameters passed (Sandbox, Components)")
                    func(self, components)

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


