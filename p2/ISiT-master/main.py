import matplotlib.pyplot as plt
import networkx as nx
import scipy as sp
from vk_api import VkApi, ApiError # для работы с ВК + для обработки ошибок с ВК (например юзер удален или в бане)
from vk_api.longpoll import VkLongPoll, Event
from vk_api.utils import get_random_id

my_group = [
    613133307, # issa
    750743366, # ibrahim
]

final_friends_list = []

# Авторизация в ВК
vk_session = VkApi(token="vk1.a.lZMPlFKfuJpgHOgby28XH6DVBM3Sr1ESA_rfGtdVUl68lMUg-W1TEGtq9MmTEXRO54Obu8c0hdLP1oaiQmlLd0gc3rR7d0B5xGrG2JmWjti6BpuGuwBpvEGlBN5nwXPC7MKwTW7evQj76xHsvJU5nCaf62PCyn7CcgYSJoQE8pOn4EGP1OSrQdwbLjPutotY-HP9K6db1pswTwOpi845rw") #токен не стали скидывать специально
vk = vk_session.get_api()

# Получение списка друзей пользователя
friends_list = vk.friends.get(user_id=613133307)["items"]
for friend_id in friends_list:
  if friend_id in my_group: # оставляем только нашу группу
    final_friends_list.append(friend_id)
final_friends_list.append(613133307) # добавляем пользователя, чьих друзей отбирали выше

################# Блок выше можно пропустить, оставить my_group, но этот блок нужен из-за задания (требовалось два уровня вложенности) #################

# Создание графа
graph = nx.Graph()
graph.add_nodes_from(final_friends_list) # создаем ноды

# Добавление ребер для друзей друзей
for friend_id in final_friends_list:
  try:
    final_friends_list = vk.friends.get(user_id=friend_id)["items"]
    graph.add_edges_from([(friend_id, friend2_id) for friend2_id in final_friends_list]) # создаем ребра
  except ApiError as e:
# Проверка кода ошибки на наличие кода 18, 30
    if e.code == 18: # код ошибки с https://clck.ru/3Durd6
      print(f"{friend_id} === User was deleted or banned.")
    elif e.code == 30: # код ошибки с https://clck.ru/3Dusje
      print(f"{friend_id} === This profile is private")
    else:
      print(f"{friend_id} === {e}")

# Визуализация
plt.figure(figsize=(200,200))
plt.title("Граф друзей и друзей друзей")
nx.draw(graph, with_labels=True, node_size=300, node_color="#f1f1f1", edge_color="#228b22")
plt.show()