#include "python.h" 
#include <vector>
#include <iostream>
#include <algorithm>

static PyObject* spam_predict_price(PyObject* self, PyObject* args) 
{

    float a = 0, b = 0;
    std::string str;
    PyArg_ParseTuple(args, "s", str);
    std::cout << str << std::endl;

    return Py_BuildValue("ff", a, b);
}



static PyMethodDef SpamMethods[] = {
    {"PredictPrice", spam_predict_price, METH_VARARGS,
    "Predict Price through rsi and bb"},
    {NULL, NULL, 0, NULL}    
};


static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam",            
    "It is Termp Module", 
    -1,SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void)
{
    return PyModule_Create(&spammodule);
}

int main() {

}