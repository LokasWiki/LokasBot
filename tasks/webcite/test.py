from tasks.webcite.data import list_of_template

list_of_all_template = []

for dic in list_of_template:
    for template in dic['list_of_template']:
        list_of_all_template.append(template)

print(list_of_all_template)