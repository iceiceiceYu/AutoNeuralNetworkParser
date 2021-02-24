import JSON_loader
import Code_generator
if __name__ == '__main__':

    n_list = JSON_loader.loader('final_demo.json')
    code = Code_generator.Translator(n_list).translate()
    print(code)