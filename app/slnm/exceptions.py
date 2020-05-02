def exc(type):
    exceptions = {
        "warning": [
            'Превышено время ожидания'
        ],
        "critical": []
    }

    return exceptions[type]