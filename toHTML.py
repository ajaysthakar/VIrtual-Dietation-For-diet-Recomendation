def createHTML(diet):
    text_file = open("templates/showDiet.html", "w")
    text_file.write('{% extends "homeLayout.html"%}\n{% block content %}\n<div id="main-content" class="container">\n<label>\n</h1>BREAKFIRST</h1>')
    text_file.write(diet[0])
    text_file.write('\n</label>\n<label>\n</h1>BREAKFIRST SNACK</h1><br>\n')
    text_file.write(diet[1])
    text_file.write('\n</label>\n<label>\n</h1>LUNCH</h1><br>\n')
    text_file.write(diet[2])
    text_file.write('\n</label>\n<label>\n</h1>EVENING SNACK</h1><br>\n')
    text_file.write(diet[3])
    text_file.write('\n</label>\n<label>\n</h1>DINNER</h1><br>\n')
    text_file.write(diet[4])
    text_file.write('\n</label>\n{% endblock%}\n')
    text_file.close()

#'+diet[0]+diet[1]+diet[2]++diet[3]+'</label><label>dinner<br>'+diet[4]+'</label>{% endblock%}'
import shutil
import os

def copy_rename(new_file_name):
        src_dir= "templates/"
        dst_dir= "templates/dietDB/"
        src_file = os.path.join(src_dir, "showDiet.html")
        shutil.copy(src_file,dst_dir)
        dst_file = os.path.join(dst_dir, "showDiet.html")
        new_dst_file_name = os.path.join(dst_dir, new_file_name+".html")
        os.rename(dst_file, new_dst_file_name)
        return ("dietDB/"+new_file_name+".html")
