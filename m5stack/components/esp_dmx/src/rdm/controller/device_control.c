#include "include/device_control.h"

#include "../../dmx/include/driver.h"
#include "../../dmx/include/service.h"
#include "./include/utils.h"
#include "../include/driver.h"
#include "../include/uid.h"

size_t rdm_send_get_identify_device(dmx_port_t dmx_num, const rdm_uid_t *dest_uid, rdm_sub_device_t sub_device,
    bool *identify, rdm_ack_t *ack) {
    DMX_CHECK(dmx_num < DMX_NUM_MAX, 0, "dmx_num error");
    DMX_CHECK(dest_uid != NULL, 0, "dest_uid is null");
    DMX_CHECK(!rdm_uid_is_broadcast(dest_uid), 0, "dest_uid error");
    DMX_CHECK(sub_device < RDM_SUB_DEVICE_MAX, 0, "sub_device error");
    DMX_CHECK(identify != NULL, 0, "identify is null");
    DMX_CHECK(dmx_driver_is_installed(dmx_num), 0, "driver is not installed");

    const rdm_request_t request = {
        .dest_uid = dest_uid, .sub_device = sub_device, .cc = RDM_CC_GET_COMMAND, .pid = RDM_PID_IDENTIFY_DEVICE
    };

    const char *format = "b$";
    return rdm_send_request(dmx_num, &request, format, identify, sizeof(*identify), ack);
}

bool rdm_send_set_identify_device(dmx_port_t dmx_num, const rdm_uid_t *dest_uid, rdm_sub_device_t sub_device,
    const uint8_t identify, rdm_ack_t *ack) {
    DMX_CHECK(dmx_num < DMX_NUM_MAX, 0, "dmx_num error");
    DMX_CHECK(dest_uid != NULL, 0, "dest_uid is null");
    DMX_CHECK(sub_device < RDM_SUB_DEVICE_MAX || sub_device == RDM_SUB_DEVICE_ALL, 0, "sub_device error");
    DMX_CHECK(identify == 0 || identify == 1, 0, "identify is invalid");
    DMX_CHECK(dmx_driver_is_installed(dmx_num), 0, "driver is not installed");

    const rdm_request_t request = {.dest_uid = dest_uid,
                                   .sub_device = sub_device,
                                   .cc = RDM_CC_SET_COMMAND,
                                   .pid = RDM_PID_IDENTIFY_DEVICE,
                                   .pd = &identify,
                                   .pdl = sizeof(identify),
                                   .format = "b$"};

    return rdm_send_request(dmx_num, &request, NULL, NULL, 0, ack);
}
