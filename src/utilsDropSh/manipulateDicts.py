class dictConverter:
    def __init__(self) -> None:
        pass
    def dict_to_string(self,dict):
        string=""
        for key,value in dict.items():
            string=f"{string}{key}:{value}\n"
        return string

dc=dictConverter()