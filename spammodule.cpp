#include "python.h" 
#include <vector>
#include <iostream>
#include <numeric>
#include <algorithm>

void RSI(float& d, const std::vector<float>& v);
void Bollinger(float& a, float& b, float& c, const std::vector<float>& v);

static PyObject* spam_predict_price(PyObject* self, PyObject* args) 
{
    float a, b, c, d;

    PyObject* py_list;
    if (!PyArg_ParseTuple(args, "O", &py_list)) {
        return NULL; // 파싱 실패 시 NULL 반환
    }

    std::vector<float> v;
    Py_ssize_t size = PyList_Size(py_list);
    for (Py_ssize_t i = 0; i < size; ++i) {
        PyObject* item = PyList_GetItem(py_list, i);
        v.push_back(static_cast<float>(PyFloat_AsDouble(item)));
    }

    Bollinger(a, b, c, v);
    RSI(d, v);

    return Py_BuildValue("ffff", a, b, c, d);
}
void RSI(float& d, const std::vector<float>& v) {
    int period = 14;
    float gain = 0.0;
    float loss = 0.0;

    // 첫 번째 계산을 위한 초기 이익과 손실 계산
    for (int i = 1; i <= period; ++i) {
        float difference = v[i] - v[i - 1];
        if (difference > 0) gain += difference; // 이익
        else loss -= difference; // 손실
    }

    float average_gain = gain / period;
    float average_loss = loss / period;

    // 이후의 계산을 위한 평균 이익과 평균 손실 업데이트
    for (size_t i = period + 1; i < v.size(); ++i) {
        float difference = v[i] - v[i - 1];
        if (difference > 0) {
            average_gain = (average_gain * (period - 1) + difference) / period;
            average_loss = (average_loss * (period - 1)) / period;
        }
        else {
            average_gain = (average_gain * (period - 1)) / period;
            average_loss = (average_loss * (period - 1) - difference) / period;
        }
    }

    // 상대 강도 계산
    float RS = average_gain / average_loss;

    // RSI 계산
    d = 100.0 - (100.0 / (1.0 + RS));
}

void Bollinger(float& a, float& b, float& c, const std::vector<float>& v) {
    float sum = std::accumulate(v.begin(), v.end(), 0.0);
    float mean = sum / v.size();

    float squared_sum = std::inner_product(v.begin(), v.end(), v.begin(), 0.0);
    float variance = squared_sum / v.size() - mean * mean;
    float standard_deviation = std::sqrt(variance);

    float upper_band = mean + 2 * standard_deviation;
    float lower_band = mean - 2 * standard_deviation;

    a = lower_band;
    b = mean;
    c = upper_band;
}

static PyMethodDef SpamMethods[] = {
    {"PredictPrice", spam_predict_price, METH_VARARGS,
    "Predict Price through rsi and bb"},
    {NULL, NULL, 0, NULL}    
};


static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam",            
    NULL, 
    -1,
    SpamMethods
};

PyMODINIT_FUNC PyInit_spam(void)
{
    return PyModule_Create(&spammodule);
}

