/*
 * SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */
#ifdef __cplusplus
extern "C" {
#endif

#include "py/runtime.h"


typedef struct {
    mp_obj_base_t base;
    void *detector;
    int model_id;           // 内置模型的模型ID
    const char *model_path; // 自定义模型的模型路径
} py_object_detector_obj_t;

typedef struct {
    mp_obj_base_t base;
    mp_obj_t category;
    mp_obj_t score;
    mp_obj_t x, y, w, h;
    mp_obj_t keypoint;
} py_detect_result_obj_t;

enum {
    HUMAN_FACE_DETECT,
    PEDESTRIAN_DETECT,
};

mp_obj_t py_object_detector_make_new(const mp_obj_type_t *type, mp_uint_t n_args, mp_uint_t n_kw, const mp_obj_t *args);
mp_obj_t py_object_detector_del(mp_obj_t self_in);
mp_obj_t py_object_detector_infer(mp_obj_t self_in, mp_obj_t img);



typedef struct {
    mp_obj_base_t base;
    mp_obj_t similarity;
    mp_obj_t id;
} py_recognize_result_obj_t;

mp_obj_t py_human_face_recognizer_make_new(const mp_obj_type_t *type, mp_uint_t n_args, mp_uint_t n_kw, const mp_obj_t *args);
mp_obj_t py_human_face_recognizer_del(mp_obj_t self_in);
mp_obj_t py_human_face_recognizer_enroll_id(size_t n_args, const mp_obj_t *args);
mp_obj_t py_human_face_recognizer_delete_id(size_t n_args, const mp_obj_t *args);
mp_obj_t py_human_face_recognizer_clear_id(mp_obj_t self_in);
mp_obj_t py_human_face_recognizer_enrolled_id_num(mp_obj_t self_in);
mp_obj_t py_human_face_recognizer_recognize(mp_obj_t self_in, mp_obj_t img, mp_obj_t keypoint);


#ifdef __cplusplus
}
#endif
