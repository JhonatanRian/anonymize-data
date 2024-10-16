COMPLEX_DICT = {
    "outer_key": {
        "inner_key1": [
            "SensitiveData1",
            {
                "outer_key2": {
                    "inner_key1x": "SensitiveData1",
                    "inner_key2": "SensitiveData2"
                }
            },
            {
                "outer_key3": "SensitiveData1"
            },
            {
                "outer_key2": {
                    "inner_key1x": "SensitiveData1",
                    "inner_key2": "SensitiveData2"
                }
            }
        ],
        "inner_key_data": ["inner_data1", "inner_data2", "inner_data3"],
        "inner_key_data2": ["inner1_data1", "inner2_data2", "inner3_data3"]
    },
    "outer_key2": {
        "inner_key1": "SensitiveData1",
    },
    "outer_key3": "SensitiveData3"
}
