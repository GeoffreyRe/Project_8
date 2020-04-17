class ProductParser:
    
    @staticmethod
    def separate_brands(brands):
        if "," in brands:
            brands_list = brands.split(",")
            return brands_list[0].strip()
        return brands
    @staticmethod

    def check_if_empty_values(product):
        for key, value in product.items():
            try:
                value = value.strip()
            except AttributeError:
                value = str(value)
                value = value.strip()
            if value == "":
                return True
        return False