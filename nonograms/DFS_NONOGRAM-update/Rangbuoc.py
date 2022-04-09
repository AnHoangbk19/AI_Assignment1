from typing import List, Dict, Tuple, Any, Type

class Constraints:
    def __init__(self, so_cot: int, so_hang: int, chi_so_hang: List[List[int]], chi_so_cot: List[List[int]]) -> None:
        self.so_cot = so_cot
        self.so_hang = so_hang
        self.chi_so_hang = chi_so_hang
        self.chi_so_cot = chi_so_cot

    @staticmethod
    def kiem_tra_dau_vao(dau_vao: Dict[str, Any]) -> Tuple[List[str], "Constraints"]:
        errors = []
        def kiem_tra_chi_so(key: str) -> bool:
            if key not in dau_vao:
                errors.append("Chi so '{}' khong hop le.".format(key))
                return False
            return True
        
        for prop in ["width", "height"]:
            if kiem_tra_chi_so(prop) and type(dau_vao[prop]) != int:
                errors.append("'{}' phai la so nguyen.".format(
                    prop, type(dau_vao[prop])
                ))

        if errors:
            return errors, None
        for prop in ["rows", "columns"]:
            if not kiem_tra_chi_so(prop):
                continue

            if type(dau_vao[prop]) != list:
                errors.append("'{}' phai la 1 mang.".format(
                    prop, type(dau_vao[prop])
                ))
                continue
        if errors:
            return errors, None
        if len(dau_vao["rows"]) != dau_vao["height"]:
            errors.append("So hang phai trung voi chieu cao cua bang")
        if len(dau_vao["columns"]) != dau_vao["width"]:
            errors.append("So cot phai trung voi chieu dai cua bang")
        if errors:
            return errors, None
        return [], Constraints(dau_vao['width'],
                               dau_vao['height'],
                               dau_vao['rows'],
                               dau_vao['columns'])
