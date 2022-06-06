def calculate_star(sum_of_stars, number_of_stars):
    try:
        asd = sum_of_stars / number_of_stars
    except:
        asd = 0
    x = str(asd).split('.')
    if x[1] == "0":
        return int(x[0])
    else:
        x = f"{str(sum_of_stars / number_of_stars).split('.')[0]}.5"
        return float(x)
