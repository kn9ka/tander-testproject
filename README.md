Тестовое задание:  
Создать базу данных  в СУБД sqlite. Создать необходимые для выполнения задания таблицы и справочные данные (сделать это в виде sql скрипта). При запуске приложения проверять на наличие файла БД и при отсутствии файла создавать автоматически на основании sql скрипта.
Написать wsgi приложение заполнения формы обратной связи с сохранением результата в базу данных. Приложение должно реализовывать возможность просмотра и удаления добавленных записей.
Требования и ограничения: приложение должно запускаться на любом web сервере поддерживающем wsgi стандарт. Для реализации возможно использовать только стандартные  библиотеки и модули python версии 2.6 или более новой. Использование фреймворков и сторонних библиотек запрещено. Желательно при написании кода на javascript так же не применять дополнительные библиотеки.
Добавление комментариев. После запуска приложения при обращении по относительному пути /comment/ должна отображаться форма для заполнения. Форма состоит из следующих полей:
•	фамилия
•	имя
•	отчество
•	регион
•	город
•	контактный телефон
•	e-mail
•	комментарий.
Поля фамилия, имя и комментарий являются обязательными. Поле комментарий текстовое. Для полей телефон и email следует производить проверку ввода. Номер телефона в формате «(код города) номер». Поля с некорректным вводом и не заполненные обязательные поля должны визуально выделяться красным цветом. Поля регион и город являются выпадающими списками, при этом список выбора поля город зависит от выбранного поля регион. Данные для этих списков должны храниться в СУБД. Значение в поля город должно динамически подгружаться по технологии ajax в соответствии с выбранным полем регион.  Таблица соответствия для примера:
Регион	Город
Краснодарский край	Краснодар
	Кропоткин
	Славянск
Ростовская область	Ростов
	Шахты
	Батайск
Ставропольский край	Ставрополь
	Пятигорск
	Кисловодск
Просмотр/удаление комментариев. При обращении по относительному пути /view/ должна выводиться таблица со списком добавленных комментариев. В этом же представлении должна быть возможность удалить определенную запись.
Просмотр статистики.  При обращении по относительному пути /stat/ должна выводиться таблица со списком тех регионов у которых количество комментариев больше 5, выводить так же и количество комментариев по каждому региону. Каждая строчка должны быть ссылкой на список города этого региона в котором отображается количество комментариев по этому городу.
 

