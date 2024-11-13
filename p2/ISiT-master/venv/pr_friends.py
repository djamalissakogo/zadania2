import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import requests
import scipy as sp
from vk_api import VkApi, ApiError # для работы с ВК + для обработки ошибок с ВК (например юзер удален или в бане)
from vk_api.longpoll import VkLongPoll, Event
from vk_api.utils import get_random_id
from coalesce import coalesce
from io import BytesIO

classmates = [
    613133307,  # issa
    613133307,  # ibrahim
    172350665,
    229180632,
    193887357,
    386272361,
    162225997,
    860446539,
    472133870,
    195614586,
    825545292,
    750743366,
    637593527,
    299106540,
    164679738,
    101098087,
    239666833,
    205762499,
    270780454,
    155290829,
    151413977,
    62269831,
    253407490,
    192574298,
    144399122,
    419376445,
    508644412,
    396854328,
]

classmate_friends = []
classmate_friends2 = []
name_dict={}

# Авторизация в ВК
vk_session = VkApi(token="")
vk = vk_session.get_api()

# Создание графа
graph = nx.Graph()



# Добавление ребер для друзей нашей группы
for classmate in classmates:
  try:
    temp_classmate_friends = vk.friends.get(user_id=classmate)["items"][:100] # оставляем КАКОЕ-ТО КОЛ-ВО ДРУЗЕЙ
    for classmate_friend in temp_classmate_friends:
        classmate_friends.append(classmate_friend)
    graph.add_edges_from([(classmate, classmate_friend) for classmate_friend in classmate_friends]) # создаем ребра
    temp_classmate_friends = []
  except ApiError as e:
# Проверка кода ошибки на наличие кода 18, 30
    if e.code == 18: # код ошибки с https://clck.ru/3Durd6
      print(f"{classmate} === User was deleted or banned.")
    elif e.code == 30: # код ошибки с https://clck.ru/3Dusje
      print(f"{classmate} === This profile is private")
    else:
      print(f"{classmate} === {e}")

# Добавление ребер для друзей друзей группы
for classmate_friend in classmate_friends:
  try:
    temp_classmate_friends2 = vk.friends.get(user_id=classmate_friend)["items"][:100] # оставляем КАКОЕ-ТО КОЛ-ВО ДРУЗЕЙ
    for classmate_friend2 in temp_classmate_friends2:
        classmate_friends2.append(classmate_friend2)
    graph.add_edges_from([(classmate_friend, classmate_friend2) for classmate_friend2 in temp_classmate_friends2]) # создаем ребра
    temp_classmate_friends2 = []
  except ApiError as e:
# Проверка кода ошибки на наличие кода 18, 30
    if e.code == 18: # код ошибки с https://clck.ru/3Durd6
      print(f"{classmate_friend} === User was deleted or banned.")
    elif e.code == 30: # код ошибки с https://clck.ru/3Dusje
      print(f"{classmate_friend} === This profile is private")
    else:
      print(f"{classmate_friend} === {e}")

# Добавление ребер для друзей друзей ребят нашей группы и самих ребят из нашей группы
for classmate in classmates:
  try:
    classmate_friends = vk.friends.get(user_id=classmate)["items"]
    for classmate_friend2 in classmate_friends2:
        if classmate_friend2 in classmate_friends:
            graph.add_edges_from([(classmate, classmate_friend2)]) # создаем ребра
  except ApiError as e:
# Проверка кода ошибки на наличие кода 18, 30
    if e.code == 18: # код ошибки с https://clck.ru/3Durd6
      print(f"{classmate} === User was deleted or banned.")
    elif e.code == 30: # код ошибки с https://clck.ru/3Dusje
      print(f"{classmate} === This profile is private")
    else:
      print(f"{classmate} === {e}")



# Тк мы берем не всех друзей, а только часть, то есть вероятность потерять ребра между вершинами члены нашей группы
# Добавим их вручную
for classmate1 in classmates:
    try:
        classmate1_friends = vk.friends.get(user_id=classmate1)["items"]
        for classmate2 in classmates:
            if classmate2 in classmate1_friends:
                graph.add_edges_from([(classmate1, classmate2)]) # создаем ребра между одногруппниками
    except ApiError as e:
        # Проверка кода ошибки на наличие кода 18, 30
        if e.code == 18:  # код ошибки с https://clck.ru/3Durd6
            print(f"{classmate} === User was deleted or banned.")
        elif e.code == 30:  # код ошибки с https://clck.ru/3Dusje
            print(f"{classmate} === This profile is private")
        else:
            print(f"{classmate} === {e}")

####################### Повышение читаемости графа #######################

# Красим ноды (уникальным цветом помечены члены нашей команды-группы)
color_dict = {
    165171730: 'red',
    145195585: 'green',
    204720239: 'blue',
    342040017: 'yellow',
    172350665: 'cyan',
    229180632: 'magenta',
    193887357: 'orange',
    386272361: 'purple',
    162225997: 'brown',
    860446539: 'pink',
    472133870: 'olive',
    195614586: 'maroon',
    825545292: 'navy',
    750743366: 'teal',
    637593527: 'lavender',
    299106540: 'coral',
    164679738: 'aquamarine',
    101098087: 'gold',
    239666833: 'silver',
    205762499: 'indigo',
    270780454: 'violet',
    155290829: 'salmon',
    151413977: 'tomato',
    62269831:  'khaki',
    253407490: 'paleGreen',
    192574298: 'chocolate',
    144399122: 'beige',
    419376445: 'peachPuff',
    508644412: 'fireBrick',
    396854328: 'slateBlue'
}
node_colors = []
for node in graph.nodes():
    color = color_dict.get(node) if color_dict.get(node) is not None else False
    if color:
        node_colors.append(color)
    else:
        node_colors.append('gray')

# Красим ребра (уникальным цветом помечены ребра с нодами каждого члена нашей команды-группы)
edge_colors = []
for node1, node2 in graph.edges():
    color = coalesce([color_dict.get(node1),color_dict.get(node2)], ignore=None, default='gray')
    if node1 in classmates and node2 in classmates:
        edge_colors.append('black') # ребра между членами команды-группы
    else:
        edge_colors.append(color)

name_updates = {}

for node in graph.nodes:
    try:
        # Получаем информацию о пользователях
        user = vk.users.get(user_ids=node, fields='first_name,last_name')[0]
        name_updates[node] = f"{user['first_name']} {user['last_name']}"

    except ApiError as e:
        print(f"Ошибка при обращении к API: {e}")

graph = nx.relabel_nodes(graph, name_updates)

# Определяем позиции вершин с помощью spring_layout
pos = nx.spring_layout(graph)

# Определяем функцию для увеличения расстояния между несвязанными вершинами
def increase_distance(pos, graph, factor):
    # Получаем список всех узлов
    nodes = list(graph.nodes)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if not graph.has_edge(nodes[i], nodes[j]):  # Если узлы несвязаны
                # Увеличиваем расстояние между ними, перемещая их вдоль направления
                vec = np.array(pos[nodes[j]]) - np.array(pos[nodes[i]])
                dist = np.linalg.norm(vec)
                if dist > 0:  # Избегаем деления на ноль
                    # Нормализуем вектор и увеличиваем расстояние
                    vec_normalized = vec / dist
                    pos[nodes[j]] += vec_normalized * factor

# Вызываем функцию - увеличиваем расстояние между НЕсвязанными вершинами
increase_distance(pos, graph, factor=2)

# Визуализация
plt.figure(figsize=(200,200))
plt.title("Граф друзей и друзей друзей")
# Добавляем текст на полотно
plt.annotate(text=f"Количество вершин: {graph.number_of_nodes()}\nКоличество рёбер: {graph.number_of_edges()}\n{max(graph.degree, key=lambda x: x[1])[0]} имеет больше всего друзей: {max(graph.degree, key=lambda x: x[1])[1]}",
             xy=(0, 0), xycoords='axes fraction', fontsize=12, ha='left', va='bottom')
nx.draw(graph, pos, with_labels=True, node_size=200, node_color=node_colors, edge_color=edge_colors)
plt.show()