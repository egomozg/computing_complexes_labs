from xml.dom import minidom

def Ikz(elements,SC_place_out):
    # обработка файла xml по имени
    my_data = minidom.parse(elements)

    power_systems = my_data.getElementsByTagName('powersystem')
    def get_power_system_X(system, U_base):
        S_kz = float(system.getElementsByTagName('s_kz')[0].firstChild.data)
        U = float(system.getElementsByTagName('u_rated')[0].firstChild.data)
        X_GS = 1.1 * (S_base / S_kz) * (U**2 / U_base**2)
        return X_GS

    transformers = my_data.getElementsByTagName('transformer')
    def get_power_transformer_X(transformer, U_base):
        U_kz = float(transformer.getElementsByTagName('u_kz')[0].firstChild.data)
        P_kz = float(transformer.getElementsByTagName('p_kz')[0].firstChild.data)
        S_nom = float(transformer.getElementsByTagName('s_rated')[0].firstChild.data)
        U_nom = float(transformer.getElementsByTagName('u_rated')[0].firstChild.data)

        X_T = U_kz / 100 * (S_base / S_nom) * (U_nom**2 / U_base**2)
        return X_T

    transmission_lines = my_data.getElementsByTagName('transmission_line')
    def get_transmission_line_X(line, U_base):
        L = float(line.getElementsByTagName('l')[0].firstChild.data)
        x_per_km = float(line.getElementsByTagName('x_per_km')[0].firstChild.data)
        r_per_km = float(line.getElementsByTagName('r_per_km')[0].firstChild.data)

        X_L = x_per_km * L * S_base / (U_base**2)
        return X_L

    # Определяем порядок, в котором стоят элементы
    elements = [] 
    elements.append(power_systems[0])
    for i in range(len(transformers) + len(transmission_lines)):
        for j in range(len(transformers)):
            if elements[i].attributes['out'].value == transformers[j].attributes['name'].value:
                elements.append(transformers[j])

        for j in range (len(transmission_lines)):
            if elements[i].attributes['out'].value == transmission_lines[j].attributes['name'].value:
                elements.append(transmission_lines[j])

    #замыкание, соответственно, за одним из элементов:
    SC_place = str(SC_place_out)
    SC_place_i = 0
    for i in range(len(elements)):
        if SC_place == elements[i].attributes['name'].value:
            SC_place_i = i

    S_base = 100 #базовая мощность в МВА
    U_base = [] # напряжения ступеней в кВ
    U_base.append(int(power_systems[0].getElementsByTagName('u_rated')[0].firstChild.data)) 
    for elem in transformers:
        ratio = float(elem.getElementsByTagName('ratio')[0].firstChild.data)
        U_nom = float(elem.getElementsByTagName('u_rated')[0].firstChild.data)
        U_trans = int(U_nom / ratio)
        U_base.append(U_trans)
    
    #определяем, на какой ступени произошло замыкание:
    k = 0 # искомая ступень
    i = 0
    while i < SC_place_i + 1:
        if elements[i] in transformers:
            k += 1
        i += 1
        
    I_base = S_base/((3**0.5) * U_base[k]) # базовый ток в кА

    EMF_1 = 1 # ЭДС системы
    X = 0  # X системы
    for i in range(SC_place_i + 1):
        #определяем, на какой ступени проходит расчёт:
        k = 0 # искомая ступень
        if elements[i] in transformers:
            k += 1

        if elements[i] in power_systems:
            X += (get_power_system_X (elements[i], U_base[k]))
        elif elements[i] in transformers:
            X += (get_power_transformer_X (elements[i], U_base[k]))
        elif elements[i] in transmission_lines:
            X += (get_transmission_line_X (elements[i], U_base[k]))

    Ikz_3 = EMF_1 / X * I_base

    return Ikz_3
