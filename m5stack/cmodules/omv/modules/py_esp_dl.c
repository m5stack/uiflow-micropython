/*
 * SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */
 #include "py_esp_dl.h"


// =================================================================================================
// type detect_result
// =================================================================================================
mp_obj_t py_detect_result_x(mp_obj_t self_in) {
    return ((py_detect_result_obj_t *)self_in)->x;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_detect_result_x_obj, py_detect_result_x);

mp_obj_t py_detect_result_y(mp_obj_t self_in) {
    return ((py_detect_result_obj_t *)self_in)->y;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_detect_result_y_obj, py_detect_result_y);

mp_obj_t py_detect_result_w(mp_obj_t self_in) {
    return ((py_detect_result_obj_t *)self_in)->w;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_detect_result_w_obj, py_detect_result_w);

mp_obj_t py_detect_result_h(mp_obj_t self_in) {
    return ((py_detect_result_obj_t *)self_in)->h;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_detect_result_h_obj, py_detect_result_h);

mp_obj_t py_detect_result_category(mp_obj_t self_in) {
    return ((py_detect_result_obj_t *)self_in)->category;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_detect_result_category_obj, py_detect_result_category);

mp_obj_t py_detect_result_score(mp_obj_t self_in) {
    return ((py_detect_result_obj_t *)self_in)->score;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_detect_result_score_obj, py_detect_result_score);

mp_obj_t py_detect_result_bbox(mp_obj_t self_in) {
    mp_obj_t tuple[4] = {
        (((py_detect_result_obj_t *)self_in)->x),
        (((py_detect_result_obj_t *)self_in)->y),
        (((py_detect_result_obj_t *)self_in)->w),
        (((py_detect_result_obj_t *)self_in)->h),
    };

    return mp_obj_new_tuple(4, tuple);
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_detect_result_bbox_obj, py_detect_result_bbox);

mp_obj_t py_detect_result_keypoint(mp_obj_t self_in) {
    return ((py_detect_result_obj_t *)self_in)->keypoint;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_detect_result_keypoint_obj, py_detect_result_keypoint);

static const mp_rom_map_elem_t py_detect_result_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_category), MP_ROM_PTR(&py_detect_result_category_obj) },
    { MP_ROM_QSTR(MP_QSTR_score), MP_ROM_PTR(&py_detect_result_score_obj) },
    { MP_ROM_QSTR(MP_QSTR_x), MP_ROM_PTR(&py_detect_result_x_obj) },
    { MP_ROM_QSTR(MP_QSTR_y), MP_ROM_PTR(&py_detect_result_y_obj) },
    { MP_ROM_QSTR(MP_QSTR_w), MP_ROM_PTR(&py_detect_result_w_obj) },
    { MP_ROM_QSTR(MP_QSTR_h), MP_ROM_PTR(&py_detect_result_h_obj) },
    { MP_ROM_QSTR(MP_QSTR_bbox), MP_ROM_PTR(&py_detect_result_bbox_obj) },
    { MP_ROM_QSTR(MP_QSTR_keypoint), MP_ROM_PTR(&py_detect_result_keypoint_obj) },
};

static MP_DEFINE_CONST_DICT(py_detect_result_locals_dict, py_detect_result_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    py_detect_result_type,
    MP_QSTR_detect_result,
    MP_TYPE_FLAG_NONE,
    locals_dict, &py_detect_result_locals_dict);


// =================================================================================================
// class dl.ObjectDetector
// =================================================================================================
static MP_DEFINE_CONST_FUN_OBJ_1(py_object_detector_del_obj, py_object_detector_del);
static MP_DEFINE_CONST_FUN_OBJ_2(py_object_detector_infer_obj, py_object_detector_infer);

static const mp_rom_map_elem_t object_detector_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR___del__), MP_ROM_PTR(&py_object_detector_del_obj) },
    { MP_ROM_QSTR(MP_QSTR_infer), MP_ROM_PTR(&py_object_detector_infer_obj) },
};

static MP_DEFINE_CONST_DICT(object_detector_locals_dict, object_detector_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    py_object_detector_type,
    MP_QSTR_ObjectDetector,
    MP_TYPE_FLAG_NONE,
    make_new, py_object_detector_make_new,
    locals_dict, &object_detector_locals_dict);


// =================================================================================================
// type: recognize_result
// =================================================================================================
mp_obj_t py_recognitze_result_similarity(mp_obj_t self_in) {
    return ((py_recognize_result_obj_t *)self_in)->similarity;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_recognitze_result_similarityy_obj, py_recognitze_result_similarity);

mp_obj_t  py_recognitze_result_id(mp_obj_t self_in) {
    return ((py_recognize_result_obj_t *)self_in)->id;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_recognitze_result_id_obj, py_recognitze_result_id);

static const mp_rom_map_elem_t recognitze_result_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_similarity), MP_ROM_PTR(&py_recognitze_result_similarityy_obj) },
    { MP_ROM_QSTR(MP_QSTR_id), MP_ROM_PTR(&py_recognitze_result_id_obj) },
};

static MP_DEFINE_CONST_DICT(recognitze_result_locals_dict, recognitze_result_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    py_recognize_result_type,
    MP_QSTR_recognize_result,
    MP_TYPE_FLAG_NONE,
    locals_dict, &recognitze_result_locals_dict);


// =================================================================================================
// class dl.HumanFaceRecognizer
// =================================================================================================
static MP_DEFINE_CONST_FUN_OBJ_1(py_human_face_recognizer_del_obj, py_human_face_recognizer_del);
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(py_human_face_recognizer_enroll_id_obj, 3, 3, py_human_face_recognizer_enroll_id);
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(py_human_face_recognizer_delete_id_obj, 1, 2, py_human_face_recognizer_delete_id);
static MP_DEFINE_CONST_FUN_OBJ_1(py_human_face_recognizer_enrolled_id_num_obj, py_human_face_recognizer_enrolled_id_num);
static MP_DEFINE_CONST_FUN_OBJ_1(py_human_face_recognizer_clear_id_obj, py_human_face_recognizer_clear_id);
static MP_DEFINE_CONST_FUN_OBJ_3(py_human_face_recognizer_recognize_obj, py_human_face_recognizer_recognize);

static const mp_rom_map_elem_t py_human_face_recognizer_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR___del__), MP_ROM_PTR(&py_human_face_recognizer_del_obj) },
    { MP_ROM_QSTR(MP_QSTR_enroll_id), MP_ROM_PTR(&py_human_face_recognizer_enroll_id_obj) },
    { MP_ROM_QSTR(MP_QSTR_recognize), MP_ROM_PTR(&py_human_face_recognizer_recognize_obj) },
    { MP_ROM_QSTR(MP_QSTR_delete_id), MP_ROM_PTR(&py_human_face_recognizer_delete_id_obj) },
    { MP_ROM_QSTR(MP_QSTR_enrolled_id_num), MP_ROM_PTR(&py_human_face_recognizer_enrolled_id_num_obj) },
    { MP_ROM_QSTR(MP_QSTR_clear_id), MP_ROM_PTR(&py_human_face_recognizer_clear_id_obj) },
};

static MP_DEFINE_CONST_DICT(py_human_face_recognizer_locals_dict, py_human_face_recognizer_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    py_human_face_recognizer_type,
    MP_QSTR_HumanFaceRecognizer,
    MP_TYPE_FLAG_NONE,
    make_new, py_human_face_recognizer_make_new,
    locals_dict, &py_human_face_recognizer_locals_dict);


// =================================================================================================
// module dl.model
// =================================================================================================
static const mp_rom_map_elem_t dl_model_globals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_HUMAN_FACE_DETECT), MP_ROM_INT(HUMAN_FACE_DETECT) },
    { MP_ROM_QSTR(MP_QSTR_PEDESTRIAN_DETECT), MP_ROM_INT(PEDESTRIAN_DETECT) },
};

static MP_DEFINE_CONST_DICT(dl_model_globals_dict, dl_model_globals_dict_table);

// 定义 dl.model 模块
const mp_obj_module_t py_module_dl_model = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&dl_model_globals_dict,
};


// =================================================================================================
// module dl
// =================================================================================================
static const mp_rom_map_elem_t dl_globals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_dl) },
    { MP_ROM_QSTR(MP_QSTR_ObjectDetector), MP_ROM_PTR(&py_object_detector_type) },
    { MP_ROM_QSTR(MP_QSTR_HumanFaceRecognizer), MP_ROM_PTR(&py_human_face_recognizer_type) },
    { MP_ROM_QSTR(MP_QSTR_model), MP_ROM_PTR(&py_module_dl_model) },
};
static MP_DEFINE_CONST_DICT(dl_globals_dict, dl_globals_dict_table);

const mp_obj_module_t py_module_dl = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&dl_globals_dict,
};

MP_REGISTER_MODULE(MP_QSTR_dl, py_module_dl);


