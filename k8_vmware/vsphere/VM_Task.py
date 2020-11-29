import pyVmomi


class VM_Task:
    def __init__(self, sdk, vm=None):
        self.sdk = sdk
        self.vm = vm


    def wait_for_task(self, task):
        self.wait_for_tasks([task])
        return task

    def wait_for_tasks(self, tasks):        # todo: refactor this out (the management of multiple tasks should be done by the caller not by this method)
        service_instance = self.sdk.service_instance()
        """Given the service instance si and tasks, it returns after all the
       tasks are complete
       """
        property_collector = service_instance.content.propertyCollector
        task_list = [str(task) for task in tasks]
        # Create filter
        obj_specs = [pyVmomi.vmodl.query.PropertyCollector.ObjectSpec(obj=task)
                     for task in tasks]

        property_spec = pyVmomi.vmodl.query.PropertyCollector.PropertySpec(type=pyVmomi.vim.Task,
                                                                           pathSet=[],
                                                                           all=True)
        filter_spec = pyVmomi.vmodl.query.PropertyCollector.FilterSpec()
        filter_spec.objectSet = obj_specs
        filter_spec.propSet = [property_spec]
        pcfilter = property_collector.CreateFilter(filter_spec, True)
        try:
            version, state = None, None
            # Loop looking for updates till the state moves to a completed state.
            while len(task_list):
                update = property_collector.WaitForUpdates(version)
                for filter_set in update.filterSet:
                    for obj_set in filter_set.objectSet:
                        task = obj_set.obj
                        for change in obj_set.changeSet:
                            if change.name == 'info':
                                state = change.val.state
                            elif change.name == 'info.state':
                                state = change.val
                            else:
                                continue

                            if not str(task) in task_list:
                                continue

                            if state == pyVmomi.vim.TaskInfo.State.success:
                                # Remove task from taskList
                                task_list.remove(str(task))
                            elif state == pyVmomi.vim.TaskInfo.State.error:
                                raise task.info.error
                # Move to next version
                version = update.version
        finally:
            if pcfilter:
                pcfilter.Destroy()

        return tasks