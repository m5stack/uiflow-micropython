/*
 * SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */
#include "py_esp_dl.h"
#include <list>
#include <string.h>
#include <stdio.h>
#include <iostream>
#include <vector>
#include "py_image.h"
#include "imlib.h"

#include "human_face_detect.hpp"
#include "pedestrian_detect.hpp"
#include "human_face_recognition.hpp"



// =================================================================================================
// class dl.ObjectDetector
// =================================================================================================
extern const mp_obj_type_t py_object_detector_type;
extern const mp_obj_type_t py_detect_result_type;

static HumanFaceDetect *human_face_detector = nullptr;
static PedestrianDetect *pedestrian_detector = nullptr;


mp_obj_t py_object_detector_make_new(const mp_obj_type_t *type, mp_uint_t n_args, mp_uint_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 1, 1, false);

    py_object_detector_obj_t *obj = m_new_obj(py_object_detector_obj_t);
    obj->base.type = &py_object_detector_type;

    if (mp_obj_is_int(args[0])) { // 使用内置模型，输入模型ID
        obj->model_id = mp_obj_get_int(args[0]);
        obj->model_path = NULL;
        if (obj->model_id == HUMAN_FACE_DETECT) {
            if (human_face_detector == nullptr) {
                if (pedestrian_detector) {
                    delete pedestrian_detector;
                    pedestrian_detector = nullptr;
                }
                human_face_detector = new HumanFaceDetect();
            }
        } else if (obj->model_id == PEDESTRIAN_DETECT) {
            if (pedestrian_detector == nullptr) {
                if (human_face_detector) {
                    delete human_face_detector;
                    human_face_detector = nullptr;
                }
                pedestrian_detector = new PedestrianDetect();
            }
        }
    } else if (mp_obj_is_str(args[0])) { // 使用自定义模型，输入模型路径
        obj->model_path = mp_obj_str_get_str(args[0]);
        obj->model_id = -1;
        mp_raise_TypeError("Loading custom model is not support at this time!");
    } else {
        mp_raise_TypeError("Expected a string (custom model path) or integer (built-in model ID)");
    }

    return MP_OBJ_FROM_PTR(obj);
}

mp_obj_t py_object_detector_del(mp_obj_t self_in) {
    py_object_detector_obj_t *self = (py_object_detector_obj_t *)(self_in);

    if (self->model_id == HUMAN_FACE_DETECT) {
        delete human_face_detector;
        human_face_detector = nullptr;
    } else if (self->model_id == PEDESTRIAN_DETECT) {
        delete pedestrian_detector;
        pedestrian_detector = nullptr;
    }

    return mp_const_none;
}

mp_obj_t py_object_detector_infer(mp_obj_t self_in, mp_obj_t img_obj) {
    py_object_detector_obj_t *self = (py_object_detector_obj_t *)(self_in);
    image_t *img = (image_t *)py_image_cobj(img_obj);

    std::list < dl::detect::result_t > detect_results;
    if (self->model_id == HUMAN_FACE_DETECT) {
        detect_results = human_face_detector->run((uint16_t *)img->data, {img->h, img->w, 3});
    } else if (self->model_id == PEDESTRIAN_DETECT) {
        detect_results = pedestrian_detector->run((uint16_t *)img->data, {img->h, img->w, 3});
    } else {
        // TODO: 使用自定义模型，待实现
    }

    if (detect_results.size()) {
        mp_obj_t detection_list = mp_obj_new_list(0, NULL);
        mp_obj_t keypoint_tuple[10];
        for (const auto &res : detect_results) {
            py_detect_result_obj_t *o = m_new_obj(py_detect_result_obj_t);
            o->base.type = &py_detect_result_type;
            o->category = mp_obj_new_int(res.category);
            o->score = mp_obj_new_float(res.score);
            o->x = mp_obj_new_int(res.box[0]);
            o->y = mp_obj_new_int(res.box[1]);
            o->w = mp_obj_new_int(res.box[2] - res.box[0]);
            o->h = mp_obj_new_int(res.box[3] - res.box[1]);
            // keypoint for human face detect only
            if (self->model_id == HUMAN_FACE_DETECT) {
                for (int j = 0; j < 10; j++) {
                    keypoint_tuple[j] = mp_obj_new_int(res.keypoint[j]);
                }
                o->keypoint = mp_obj_new_tuple(10, keypoint_tuple);
            } else {
                for (int j = 0; j < 10; j++) {
                    keypoint_tuple[j] = mp_obj_new_int(0);
                }
                o->keypoint = mp_obj_new_tuple(10, keypoint_tuple);
            }
            mp_obj_list_append(detection_list, o);
        }
        return detection_list;
    } else {
        return mp_const_none;
    }
}


// =================================================================================================
// class dl.HumanFaceRecognizer
// =================================================================================================
extern const mp_obj_type_t py_human_face_recognizer_type;
extern const mp_obj_type_t py_recognize_result_type;

typedef struct {
    mp_obj_base_t base;
    FaceRecognizer *recognizer;
} py_human_face_recognizer_obj_t;


mp_obj_t py_human_face_recognizer_make_new(const mp_obj_type_t *type, mp_uint_t n_args, mp_uint_t n_kw, const mp_obj_t *args) {
    py_human_face_recognizer_obj_t *obj = m_new_obj(py_human_face_recognizer_obj_t);
    obj->base.type = &py_human_face_recognizer_type;
    obj->recognizer = new FaceRecognizer(static_cast < dl::recognition::db_type_t > (CONFIG_DB_FILE_SYSTEM),
        HumanFaceFeat::model_type_t::MODEL_MFN);

    return MP_OBJ_FROM_PTR(obj);
}

mp_obj_t py_human_face_recognizer_del(mp_obj_t self_in) {
    py_human_face_recognizer_obj_t *self = (py_human_face_recognizer_obj_t *)(self_in);
    delete self->recognizer;
    return mp_const_none;
}

mp_obj_t py_human_face_recognizer_enroll_id(size_t n_args, const mp_obj_t *args) {
    py_human_face_recognizer_obj_t *self = (py_human_face_recognizer_obj_t *)(args[0]);
    image_t *img = (image_t *)py_image_cobj(args[1]);

    size_t len;
    mp_obj_t *elem;
    mp_obj_get_array(args[2], &len, &elem);
    std::vector < int > landmarks;
    for (uint8_t i = 0; i < 10; i++) {
        landmarks.push_back(mp_obj_get_int(elem[i]));
    }

    int res = self->recognizer->enroll((uint16_t *)img->data, {(int)img->h, (int)img->w, 3}, landmarks);
    if (res == 0) {
        return mp_obj_new_bool(true);
    } else {
        return mp_obj_new_bool(false);
    }
}

mp_obj_t py_human_face_recognizer_delete_id(size_t n_args, const mp_obj_t *args) {
    py_human_face_recognizer_obj_t *self = (py_human_face_recognizer_obj_t *)(args[0]);
    int remained_id = 0;

    if (n_args == 1) {
        remained_id = self->recognizer->delete_last_feat();
    } else {
        remained_id = self->recognizer->delete_feat(mp_obj_get_int(args[1]));
    }

    return mp_obj_new_int(remained_id);
}

mp_obj_t py_human_face_recognizer_enrolled_id_num(mp_obj_t self_in) {
    py_human_face_recognizer_obj_t *self = (py_human_face_recognizer_obj_t *)(self_in);
    return mp_obj_new_int(self->recognizer->feat_num());
}

mp_obj_t py_human_face_recognizer_clear_id(mp_obj_t self_in) {
    py_human_face_recognizer_obj_t *self = (py_human_face_recognizer_obj_t *)(self_in);
    self->recognizer->clear_all_feats();

    return mp_const_none;
}

mp_obj_t py_human_face_recognizer_recognize(mp_obj_t self_in, mp_obj_t img_obj, mp_obj_t keypoint) {
    py_human_face_recognizer_obj_t *self = (py_human_face_recognizer_obj_t *)(self_in);
    image_t *img = (image_t *)py_image_cobj(img_obj);

    size_t len;
    mp_obj_t *elem;
    mp_obj_get_array(keypoint, &len, &elem);
    std::vector < std::vector < int >> landmarks;
    std::vector < int > temp;
    for (uint8_t i = 0; i < 10; i++) {
        temp.push_back(mp_obj_get_int(elem[i]));
    }
    landmarks.push_back(temp);

    std::vector < std::list < dl::recognition::query_info >> res;
    res = self->recognizer->recognize((uint16_t *)img->data, {(int)img->h, (int)img->w, 3}, landmarks);

    py_recognize_result_obj_t *o = m_new_obj(py_recognize_result_obj_t);
    o->base.type = &py_recognize_result_type;
    o->similarity = mp_obj_new_float(0);
    o->id = mp_obj_new_int(0);
    if (res.size() == 1) {
        for (const auto &top_k : res) {
            for (const auto &k : top_k) {
                o->similarity = mp_obj_new_float(k.similarity);
                o->id = mp_obj_new_int(k.id);
            }
        }
    } else {
        // return mp_const_none; // TODO: 待优化
    }

    return MP_OBJ_FROM_PTR(o);
}
