
from server.worker import celery
from server.main.models import VirtualMachineModel

@celery.task()
def task_vmspawning(id):
    vmachine = VirtualMachineModel.get(id)
    vmachine.spawn(
        dhcp=False,
        on_running=running_vmcreate_callback,
        on_success=success_vmcreate_callback,
        on_error=error_vmcreate_callback
    )

    return vmachine.name

@celery.task()
def task_vmdestroying(id):
    vmachine = VirtualMachineModel.get(id)
    vmachine.destroy(
        on_success=success_vmdestroy_callback,
        on_running=running_vmdestroy_callback,
        on_error=error_vmdestroy_callback
    )

# # # # # #
def running_vmcreate_callback(task, *args, **kwargs):
    progress = task.info.progress
    if task.info.progress is None:
        progress = 100
    print(f"VM <{kwargs.get('vmname')}> Creation Progress: {progress}")
    
def success_vmcreate_callback(task, *args, **kwargs):
    print(f"VM <{kwargs.get('vmname')}> Creation Success: {task.info.result}")
    
    vm = task.info.result
    vmachine = VirtualMachineModel.query.filter_by(name=vm.name).first()
    vmachine.uuid = vm.summary.config.uuid
    vmachine.state = vm.summary.runtime.powerState

    for each in vm.summary.vm.guest.disk:
        vmachine.capacity = each.capacity/1024/1024/1024
    
    vmachine.save()

def error_vmcreate_callback(task, *args, **kwargs):
    print(f"VM <{kwargs.get('vmname')}>  Error Cause: {task.info.result}")

# # # # # #
def running_vmdestroy_callback(task, *args, **kwargs):
    progress = task.info.progress
    if task.info.progress is None:
        progress = 100
    print(f"VM <{kwargs.get('vmname')}> Deletion Progress: {progress}")
    
def success_vmdestroy_callback(task, *args, **kwargs):
    print(f"Success Callback (VM Deletion): {kwargs.get('vmname')}")

    vmachine = VirtualMachineModel.query.filter_by(name=kwargs.get("vmname")).first()    
    vmachine.delete()

def error_vmdestroy_callback(task, *args, **kwargs):
    print(f"Error Callback (VM Deletion): {task.info.error}")
# # # # # #




def make_task(action, vmid):
    assert action.lower() in ["create", "delete"], f"Action not accepted ({action.upper()})"
    
    if action.lower() == "create":
        task = task_vmspawning.delay(id=vmid)
    elif action.lower() == "delete":
        task = task_vmdestroying.delay(id=vmid)
    return task

def get_task(action, task_id):
    assert action.lower() in ["create", "delete"], f"Action not accepted ({action.upper()})"
    
    if action.lower() == "create":
        task = task_vmspawning.AsyncResult(task_id)
    elif action.lower() == "delete":
        task = task_vmdestroying.AsyncResult(task_id)
    return task