# Техническое задание проекта

Вы - бэкенд-разработчик API для обучающей платформы. Вам требуется создать полноценный сервис, который выполняет следующие функции:

- Создает пользователя (при этом проверяет существования почты и номера телефона)
- Возвращает данные по конкретному пользователю
- Генерирует простой математический пример. Пользователь может решить этот пример (за правильный ответ получает баллы)
- Создает вопрос (типы вопросов: с одним ответом, с вариантами ответов)
- Случайно выдает один существующий вопрос. На этот вопрос пользователь может дать ответ (за правильный ответ получает баллы)
- Возвращает историю решенных пользователем примеров и вопросов
- Возвращает список пользователей, отсортированный по рейтингу
- Возвращает график пользователей по рейтингу

Допущения:

- Объекты допустимо хранить в runtime (Т.е. только во время работы сервиса. При завершении работы сервиса данные можно не сохранять)
- Валидацию существования почты и номера телефона можно сделать через регулярные выражения, сторонние библиотеки

Необходимо:

- Код должен быть отформатирован (например, при помощи black)

# Запросы и ответы

- Создание пользователя `POST /users/create`

Request example:
```json
{
  "first_name": "string",
  "last_name": "string",
  "phone": "string",
  "email": "string"
}
```

Response example:
```json
{
  "id": "number",
  "first_name": "string",
  "last_name": "string",
  "phone": "string",
  "email": "string",
  "score": 0
}
```

- Получение данных по конкретному пользователю `GET /users/<user_id>`

Response example:
```json
{
  "id": "number",
  "first_name": "string",
  "last_name": "string",
  "phone": "string",
  "email": "string",
  "score": 0
}
```

- Генерация математического примера `GET /math/expression`

Request example:
```json
{
  "count_nums": "number",
  "operation": "string",
  "min": "number",
  "max": "number"
}
```

Response example:
```json
{
  "id": "number",
  "value1": "number",
  "value2": "number"
}
```

- Решение математического примера пользователем `POST /math/<expression_id>/solve`

Request example:
```json
{
  "user_id": "number",
  "user_answer": "number"
}
```

Response example:
```json
{
  "expression_id": "number",
  "result": "string",
  "reward": "number"
}
```

- Создание вопроса `POST /questions/create`

Request example (для вопроса с одним вариантом ответа):
```json
{
  "title": "string",
  "description": "string",
  "type": "ONE-ANSWER",
  "answer": "string"
}
```

Response example (для вопроса с одним вариантом ответа):
```json
{
  "id": "number",
  "title": "string",
  "description": "string",
  "type": "ONE-ANSWER",
  "answer": "string"
}
```

Request example (для вопроса с вариантами ответов):
```json
{
  "title": "string",
  "description": "string",
  "type": "MULTIPLE-CHOICE",
  "choices": [
    "string",
    "string",
    "..."
  ],
  "answer": "number"
}
```

Response example (для вопроса с вариантами ответов):
```json
{
  "id": "number",
  "title": "string",
  "description": "string",
  "type": "MULTIPLE-CHOICE",
  "choices": [
    "string",
    "string",
    "..."
  ],
  "answer": "number"
}
```

- Получение случайного вопроса `GET /questions/random`

Response example:
```json
{
  "question_id": "number",
  "reward": "number"
}
```

- Решение вопроса пользователем `POST /questions/<question_id>/solve`

Request example:
```json
{
  "user_id": "number",
  "user_answer": "number/string"
}
```

Response example:
```json
{
  "question_id": "number",
  "result": "string",
  "reward": "number"
}
```

- Получение истории решенных вопросов пользователем `GET /users/<user_id>/history`

Response example:
```json
{
  "history": [
    {
      "title": "string",
      "description": "string",
      "type": "ONE-ANSWER",
      "answer": "string",
      "user_answer": "string",
      "reward": "number"
    },
    {
      "...": "..."
    }
  ]
}
```

- Получение списка пользователей, отсортированных по рейтингу `GET /users/leaderboard`

Request example:
```json
{
  "type": "table"
}
```

Response example:
```json
{
  "leaderboard": [
    {
      "first_name": "string",
      "last_name": "string",
      "score": "number"
    },
    {
      "...": "..."
    }
  ]
}
```

- Получение графика пользователей по рейтингу `GET /users/leaderboard`

Request example:
```json
{
  "type": "graph"
}
```

Response example:
```html
<img src="path_to_graph">
```