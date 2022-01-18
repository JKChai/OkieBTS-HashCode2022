## #! usr/bin/python3

## create dict
ingredient_dict = dict()

## reading data
with open('./input/a_an_example.in.txt') as file:
    for idx, line in enumerate(file.readlines()):    
        data = line.strip() ## strip newline
        items_list = str(data).split() ## create list

        ## simple hash algo from Joonmo 
        if idx > 0: ## start with clients
            if idx % 2 == 1: ## like
                del items_list[0]
                for i in items_list:
                    if i not in ingredient_dict.keys():
                        ingredient_dict[i] = 1
                    else:
                        ingredient_dict[i] += 1

            elif idx == 0:
                pass

            else: # dislike
                del items_list[0]
                for i in items_list:
                    if i not in ingredient_dict.keys():
                        ingredient_dict[i] = 0
                    else:
                        ingredient_dict[i] -= 1

## create output
final_ingredient = set()

cnt = 0
for k, v in ingredient_dict.items():
    if v > 0:
        final_ingredient.add(k)
        cnt += 1

## create string
ingredients = ' '.join(list(final_ingredient))
output_string = str(cnt) + ' ' + ingredients

with open('./output/a_an_example.out.txt', 'w') as file:
    file.write(output_string)

# ## test
# print(ingredient_dict)
