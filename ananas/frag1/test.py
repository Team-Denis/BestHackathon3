def staline_sort(lst):
    if not lst:
        return []
    
    # Initialisation avec le premier élément de la liste
    sorted_list = [lst[0]]
    
    # Parcourir les éléments à partir du deuxième
    for number in lst[1:]:
        # Si le nombre est plus grand que le dernier élément de la liste triée, l'ajouter
        if number >= sorted_list[-1]:
            sorted_list.append(number)
    
    return sorted_list

# Exemple d'utilisation

i = input()
l = i.split(" ")
l = [int(i) for i in l]

sorted_list = staline_sort(l)
print("Liste triée :", sum(sorted_list))