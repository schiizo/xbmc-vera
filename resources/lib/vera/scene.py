# http://wiki.micasaverde.com/index.php/UI_Simple#Status_of_the_device_or_scene_and_control_buttons

# TODO: check that the scene status is 'active'
def run(scene, vera_controller):
    vera_controller.GET( \
'/data_request?id=lu_action'                                        + \
'&serviceId=urn:micasaverde-com:serviceId:HomeAutomationGateway1'   + \
'&action=RunScene&SceneNum=' + str(scene['id'])                     ) 

