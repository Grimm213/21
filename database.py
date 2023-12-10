from tkinter import *           #импортируется модуль графического интерфейса
from tkinter import ttk         #импортируется модуль дополненного графического интерфейса 
import sqlite3                  #импортируется модуль по работе с базой данных
       
class Database:                       #класс по работе с базой данных
    def __init__(self, table, field, field_type =()):  #конструктор класса, куда передаётся имя таблицы, кортеж с именами полей таблицы и кортеж с типами полей таблицы; типы можно не передавать, тогда по умолчанию используется пустой кортеж, который далее будет заполнен типом Text
        self.table = table            #имя таблицы делается свойством класса
        self.field = ('id',) + field  #в начало кортежа с полями добавляется дополнительное поле id, где будет храниться уникальный номер каждой записи, этот кортеж полей становится свойством класса
        self.field_type = ('INTEGER PRIMARY KEY AUTOINCREMENT',) + field_type #в начало кортежа добавляется дополнительный тип для поля id; это целочисленный тип, ключевое поле, которое автоматически заполняется при создании любой записи очередным натуральным числом; кортеж типов становится свойством класса
        self.connection = ''          #объявляется переменная, где будет храниться соединение с базой данных
        self.cursor = ''              #объявляется переменная, гда будет храниться объект-курсор, который будет пробегать по базе данных при выполнении соответствующих запросов или команд
        self.selected_id = ()         #объявляется кортеж, куда будут записываться ключевые коды записей, которые будут выбраны для удаления 
        self.indicator = []           #объявляется массив, куда будут записываться кортежи с параметрами запросов для расчёта обобщающих показателей, чтобы при удалении записей их можно было обновить
        self.indicator_label = []     #объявляется массив, куда будут записываться сообщения с рассчитанными значениями обобщающих показателей, чтобы при удалении записей можно было изменить текст сообщений, отразив в них новые обновлённые значения
        self.create_table()           #запускается метод класса создающий таблицу с переданным именем и полями; если таблица уже существует, то этот метод ничего дополнительно делать не будет

    def change(self, query, values = ()):      #метод класса, отвечающий за внесение изменений в базу данных в соответствии с передаваемым сюда запросом в виде строки и значениями к этому запросу в виде кортежа; если никакие значения не переданы, то по умолчанию используется пустой кортеж значений
        self.connection = sqlite3.connect('my_database.db')  #создаётся соединение с файлом базы данных
        self.cursor = self.connection.cursor() #создаётся объект - курсор, который будет пробегать по базе данных при выполнении соответствующих запросов
        try:                          #модуль обработки исключений на случай, если запрос на изменения базы данных будет некорректным
            self.cursor.execute(query, values)  #объекту - курсору даётся команда выполнить переданный запрос или команду с соответствующими значениями; если запрос с ошибками, то изменения выполнены не будут, а программа перейдёт в блок except
            self.connection.commit()  #выполненные изменения подтверждаются; если этого не сделать, то эти изменения не будут внесены в базу данных; программы переходит в блок finally
        except:                       #блок, куда переходит выполнение программы, если запрос с ошибкой
            print('Неверный ввод!')   #в консоли пишем сообщение о том, что была попытка неправильного запроса к базе данных, чтобы принять это к сведению и разобраться с этим, если надо
        finally:                      #блок, куда переходит выполнение программы в любом случае независимо от того, была ошибка или её не было
            self.connection.close()   #соединение с файлом базы данных закрывается

    def create_table(self):           #метод класса для создания таблицы с параметрами, переданными в конструктор класса и являющиеся свойствами класса
        query = 'CREATE TABLE IF NOT EXISTS ' + self.table           #начинается составление текста запроса: команда создания таблицы, если она не существует, и подстановка имени таблицы из свойств класса
        query += '(' + self.field[0] + ' ' + self.field_type[0]      #в текст запроса добавляется имя и тип нулевого поля (ключевого кода); это не делается в цикле ниже потому, что в случае пустого кортежа с типами полей здесь надо задать особый тип в отличие от других полей
        for i in range(1, len(self.field)):                          #в цикле перебираются все поля после нулевого из кортежа с полями
            if self.field_type == ():                                #если кортеж с типами полей пустой, то
                self.field_type.append('TEXT NOT NULL')              #для текущего поля в кортеж с типами полей добавляется тип поля TEXT
            query += ', ' + self.field[i] + ' ' + self.field_type[i] #в текст запроса добавляется запятая после предыдущего поля, а далее очередное поле и его тип
        query += ')'                  #текст запроса заканчивается скобкой
        self.change(query)            #запускается метод класса, выполняющий сформированный запрос по созданию таблицы

    def insert(self, values):         #метод класса для добавления новой записи, куда передаётся кортеж со значениями полей новой записи, кроме значения ключевого поля, которое будет заполнено автоматически
        query = 'INSERT INTO ' + self.table +' (' + self.field[1]    #начинается составление текста запроса: команда добавления записи, подстановка имени таблицы и имени первого поля; нулевое поле с ключевым кодом не указывается, так как оно будет заполнено автоматически
        for i in range(2,len(self.field)):                           #цикл перебирает имена полей, начиная со второго
            query += ', ' + self.field[i]                            #в текст запроса добавляется запятая после предыдущего поля и имя очередного поля
        query += ') VALUES(' + '?, ' * (len(values) - 1) + '?)'      #в текст запроса добавляются знаки вопроса, на место которых будут добавляться значения из полученного кортежа значений
        self.change(query, values)                                   #запускается метод класса, выполняющий сформированный запрос по добавлению полученных значений новой записи в таблицу
        
    def update(self, values):                                        #метод класса по обновлению уже существующей записи, куда передаются новые значения для этой записи, в том числе значение ключевого поля, которое не изменяется, но используется для идентификации записи, которую надо обновить
        query = 'UPDATE ' + self.table +' SET ' + self.field[1] + ' = ?'  #начинается составление текста запроса: команда по обновлению записи, подстановка имени таблицы, команда установить в первое поле значение, которое обозначается знаком вопроса, т.е. это значение будет браться из кортежа со значениями 
        for i in range(2,len(self.field)):           #цикл перебирает имена полей, начиная со второго              
            query += ', ' + self.field[i] + ' = ?'   #в текст запроса добавляется запятая после предыдущего поля, имя очередного поля и его значение, которое обозначается знаком вопроса, т.е. это значение будет браться из кортежа со значениями 
        query += ' WHERE id = ?'                     #в текст запроса добавляется условие отбора записей, т.е. выбирается только запись, у которой ключевое поле равно значению, подставляемое вместо знака вопроса из переданного кортежа значений
        values = values[1:] + (values[0],)           #в кортеже значений ключевое поле с нулевого места перемещается в конец кортежа, так как в запрос вместо знаков вопроса сначала подставляются все значения, начиная с первого, а значение ключевого поля подставляется в самом конце в условие отбора
        self.change(query, values)                   #запускается метод класса, выполняющий сформированный запрос по обновлению записи новыми значениями

    def delete(self, id):                            #метод класса по удалению уже существующей записи, куда передаётся ключевой код этой записи
        query = 'DELETE FROM ' + self.table +' WHERE id = ?'  #формируется запрос на удаление записи, куда подставляется имя таблицы и условие отбора этой записи по значению ключевого кода
        self.change(query, (id,))                    #запускается метод класса, выполняющий сформированный запрос по удалению записи, соответствующей передаваемому значению ключевого кода
        
    def find(self, query, values = ()):              #метод класса, отвечающий за поиск данных в базе в соответствии с передаваемым сюда запросом в виде строки и значениями к этому запросу в виде кортежа; если никакие значения не переданы, то по умолчанию используется пустой кортеж значений
        self.connection = sqlite3.connect('my_database.db')   #создаётся соединение с файлом базы данных
        self.cursor = self.connection.cursor()       #создаётся объект - курсор, который будет пробегать по базе данных при выполнении соответствующих запросов
        self.cursor.execute(query, values)           #объекту - курсору даётся команда выполнить переданный запрос или команду с соответствующими значениями
        result = self.cursor.fetchall()              #в переменную результата записывается массив всех найденных в соответствии с запросом записей
        self.connection.close()                      #соединение с файлом базы данных закрывается
        return result                                #результат, т.е. массив со всеми найденными записями, передаётся в то место программы, откуда этот метод был вызван

    def show_history(self, place, user_id, text_column):      #метод класса, показывающий на экране историю операций, т.е. все записи таблицы, которые отображаются в рамке или окне place и относятся только к пользователю с ключевым кодом user_id, кроме этих параметров передаются названия столбцов на русском языке, которые подставляются вместо названий полей для удобства чтения данных пользователем 
        history_frame = Frame(place)                 #создаётся рамка, где будет отображаться история операций, куда передаётся имя окна, где будет размещаться сама рамка
        history_frame.pack()                         #рамка отображается на экране
        history_frame.rowconfigure(index=0, weight=1)#в рамке будет использоваться метод grid; в строке с номером 0 устанавливается весовой коэффициент в 1, т.е. 100% свободного пространства будет отдано этой строке, остальные строки будут сжаты до минимума
        history_frame.columnconfigure(index=0, weight=1)      #в рамке будет использоваться метод grid; в колонке с номером 0 устанавливается весовой коэффициент в 1, т.е. 100% свободного пространства будет отдано этой колонке, остальные колонки будут сжаты до минимума
        tree = ttk.Treeview(history_frame, columns=self.field,displaycolumns = self.field[2:], show="headings", selectmode="extended", height = 10)  #создаётся виджет, который отображает данные в виде таблицы, колонки в которой будут соответствовать всем полям из таблицы данных, но на экране будут отображаться только значения полей, начиная со второго, так как значения ключевых полей пользователю неинтересны; таблица будет показываться с названиями колонок; в таблице можно будет выделять сразу несколько записей; высота таблицы будет равна 10 записям
        tree.grid(row=0, column=0, sticky="nsew")    #эта виджет-таблица будет размещена в нулевой строке и нулевой колонке и растянута во все стороны, т.е. всё свободное пространство будет заполнено

        for i in range(2,len(text_column)):          #цикл перебирает переданные названия колонок, начиная со второго, так как первые две колонки не будут отображаться на экране, хотя будут невидимо содержаться в этой таблице-виджете
            tree.heading(self.field[i], text=text_column[i], anchor='n')    #в названии колонки, соответствующей текущему полю, меняется текст на соответствующее переданное название на русском языке
            tree.column("#"+str(i-1), stretch=NO, width=120, anchor = 'n')  #задаются параметры текущей отображаемой колонки; сначала указывается номер колонки, начиная с 1; далее запрещается растягивать колонки при увеличении размера рамки; задаётся ширина колонки в 100 пикселей; содержимое колонок смещается к северу, т.к. к середине верхней границы

        result = self.find('SELECT * FROM ' + self.table + ' WHERE user_id = ?', (user_id,))  #в переменную сохраняется массив кортежей из базы данных, содержащих все значения строк, ключевое значение которых равно переданному значению ключевого кода пользователя
        for row in result:                           #цикл перебирает все записи, т.е. все кортежи, в  массиве
            tree.insert("", END, values = row)       #в таблицу - виджет добавляются значения текущей записи, кортежа, полученные из базы данных

        yscrollbar = ttk.Scrollbar(history_frame, orient=VERTICAL, command=tree.yview) #в рамке истории операций создаётся вертикальная полоса прокрутки, при использовании которой запускается встроенный метод прокрутки содержимого вдоль оси Oy
        tree.configure(yscroll=yscrollbar.set)        #задаётся вид полосы прокрутки с помощью встроенного набора элементов для полосы прокрутки
        yscrollbar.grid(row=0, column=1, sticky="ns") #полоса прокрутки размещается в нулевой строке и первой колонке и растягивается вверх и вниз, чтобы заполнить всё свободное пространство этой ячейки

        xscrollbar = ttk.Scrollbar(history_frame, orient=HORIZONTAL, command=tree.xview) #в рамке истории операций создаётся вертикальная полоса прокрутки, при использовании которой запускается встроенный метод прокрутки содержимого вдоль оси Oy
        tree.configure(xscroll=xscrollbar.set)        #задаётся вид полосы прокрутки с помощью встроенного набора элементов для полосы прокрутки
        xscrollbar.grid(row=1, column=0, sticky="we") #полоса прокрутки размещается в нулевой строке и первой колонке и растягивается вверх и вниз, чтобы заполнить всё свободное пространство этой ячейки

        tree.bind("<<TreeviewSelect>>", lambda event: self.item_selected(tree))       #добавляется обработчик событий, связанных с выделением записей таблицы щелчком мыши; при выделении какой-либо записи запускается метод класса, куда передаётся имя таблицы-виджета

        delete_button = Button(history_frame, text = 'Удалить записи', command = lambda: self.click_delete(tree,user_id))  #создаётся кнопка в рамке истории операций для удаления выделенных записей; при нажатии на кнопку запускается метод класса, куда передаётся имя таблицы-виджета и ключевой код пользователя
        delete_button.grid(row=2, column=0, pady = 10)#кнопка размещается в первую строку и нулевую колонку с отступом по вертикали в 10 пикселей
        
    def item_selected(self, tree):                    #метод класса, запускающийся при выделении записей в таблице-виджете; сюда передаётся имя таблицы-виджета, чтобы воспользоваться её встроенными методами
        self.selected_id = ()                         #кортеж с ключевыми значениями выделенных записей обнуляется, чтобы записать сюда ключевые значения последних выделенных записей
        for selected_item in tree.selection():        #цикл перебирает записи из списка выделенных записей, возвращаемых встроенным методом selection()
            item = tree.item(selected_item)           #в переменную item сохраняем содержимое записи из списка
            self.selected_id += (item["values"][0],)  #из содержимого записи выбираем только значения, среди них выбираем нулевое значение, т.е. ключевой код записи, и записываем его в кортеж с ключевыми значениями выделенных записей
         
    def click_delete(self, tree,user_id):             #метод класса для удаления выделенных записей, куда передаётся имя таблицы-виджета и ключевой код пользователя
        for id in self.selected_id:                   #цикл перебирает ключевые значения из кортежа этих значений для выделенных записей
            self.delete(id)                           #запускается метод класса, удаляющий запись с текущим ключевым значением из базы данных
        result = self.find('SELECT * FROM ' + self.table + ' WHERE user_id = ?', (user_id,))  #в переменную сохраняется массив кортежей из базы данных, содержащих все значения строк, ключевое значение которых равно переданному значению ключевого кода пользователя; этот запрос опять повторяется, чтобы получить обновлённую информацию, т.е. получить значения строк без удалённых строк
        tree.delete(*tree.get_children())             #в таблице-виджете удаляются значения всех полей для записей, вложенных в родительские таблицы, но у нас таблица одна, поэтому выбираются все записи
        for row in result:                            #цикл перебирает все записи, т.е. все кортежи, в  массиве
            tree.insert("", END, values = row)        #в таблицу - виджет добавляются значения текущей записи, кортежа, полученные из базы данных   
        if result != []:                              #если массив с кортежами не пустой, т.е. есть хотя бы одна запись, то
            for i in range(len(self.indicator)):      #цикл перебирает кортежи, в которых записаны параметры запросов для расчёта обобщающих показателей
                result = self.find('SELECT ' + self.indicator[i][1] + '(' + self.indicator[i][2] + ') FROM ' + self.table + ' WHERE user_id = ?', (self.indicator[i][3],)) #в переменную записывается результат выполнения запроса, куда подставляется имя показателя (значение 1: AVG, SUM, MAX, MIN, COUNT), имя поля, для значений которого считается показатель (значение 2), имя таблицы в базе данных, ключевой код пользователя (значение 3)
                self.indicator_label[i].config(text = self.indicator[i][0] + str(round(result[0][0],2))) #в массиве сообщений со значениями обобщающих показателей у текущего сообщения меняется текст: записывается пояснение (значение 0 из параметров) и к нему добавляется результат выполнения предыдущего запроса, т.е. значение обобщающего показателя; хотя показатель один он записан в нулевом кортеже массива на нулевом месте, поэтому для записи его значения без всяких скобок дважды пишем нулевой индекс; кортеж используется потому, что одновременно можно запросить несколько обобщающих показетелей, но нам лучше по отдельности
        else:                                         #иначе, т.е. если массив кортежей с записями пустой, 
            for i in range(len(self.indicator)):      #цикл перебирает все сообщения с показателями
                self.indicator_label[i].config(text = self.indicator[i][0])  #в текст текущего сообщения пишется только пояснение с названием показателя, а само значение показателя не пишется
            
    def show_indicator(self, place, text, indicator, field, user_id):        #метод класса для вычисления обобщающих показателей, куда передаётся место вывода на экран сообщения со значением обобщающего показателя, текст-пояснение с названием этого показателя, имя показателя, поле, для значений которого будет рассчитываться этот показатель, ключевой код пользователя, для которого надо рассчитать показатель
        self.indicator.append((text, indicator, field, user_id))             #в массив с параметрами запроса для расчёта обобщающего показателя записываются полученные параметры, чтобы при удалении записей можно было повторить этот запрос для обновления данных
        control = self.find('SELECT * FROM ' + self.table + ' WHERE user_id = ?', (user_id,)) #в базе данных ищутся записи для заданного пользователя
        if control != []:                             #если результатом поиска является не пустой массив, т.е. записи есть, то выполняем запрос, иначе ничего не делаем
            result = self.find('SELECT ' + indicator + '(' + field + ') FROM ' + self.table + ' WHERE user_id = ?', (user_id,))  #в переменную записывается результат выполнения запроса, куда подставляется имя показателя (AVG, SUM, MAX, MIN, COUNT), имя поля, для значений которого считается показатель, имя таблицы в базе данных, ключевой код пользователя
            self.indicator_label.append(Label(place, text = text + str(round(result[0][0],2)), font = ('Tahoma', 14)))           #в массив сообщений со значениями обобщающих показателей добавляется текущее сообщение,куда записывается пояснение - название показателя и к нему добавляется результат выполнения предыдущего запроса, т.е. значение обобщающего показателя; хотя показатель один он записан в нулевом кортеже массива на нулевом месте, поэтому для записи его значения без всяких скобок дважды пишем нулевой индекс; кортеж используется потому, что одновременно можно запросить несколько обобщающих показетелей, но нам лучше по отдельности
            self.indicator_label[-1].pack(pady = 5)   #последнее добавленное в массив сообщение, т.е. текущее на данный момент сообщение выводится на экран
        
if __name__ == '__main__':                            #если текущий файл является стартовым, то выполняются все команды ниже, иначе ничего не происходит
    root = Tk()                                       #создаётся главное окно
    data = Database('Game2', ('user_id', 'date', 'duration', 'attempts','size'), ('INTEGER','TEXT', 'INTEGER', 'INTEGER', 'INTEGER')) #создаётся экземпляр класса по работе с базой данных, куда передаётся имя создаваемой таблицы в базе данных, кортеж с полями таблицы и кортеж с типами этих полей
    data.insert((1,'14.11.23', 23, 21, 20))           #для созданного экземпляра запускается метод, добавляющий в созданную таблицу новую запись
    data.insert((1,'15.11.23', 27, 25, 24))           #для созданного экземпляра запускается метод, добавляющий в созданную таблицу ещё новую запись с другими значениями
#    data.update((2,2,'10.11.23', 30, 24, 20))        #пример вызова метода обновления записи
#    data.update((4,2,'10.11.23', 34, 22, 20))        #пример вызова метода обновления записи
#    data.delete(3)                                   #пример вызова метода удаления записи
#    print(data.find('SELECT * FROM Game2'))          #вывод в консоль всех записей созданной таблицы из базы данных
    data.show_indicator(root, 'Среднее время игры: ', 'Avg', 'duration', 1)      #пример вызова метода, который рассчитывает и отображает на экране среднее значение времени игры для пользователя с ключевым кодом равным 1
    data.show_indicator(root, 'Суммарное время игры: ', 'SUm', 'duration', 1)    #пример вызова метода, который рассчитывает и отображает на экране суммарное значение времени игры для пользователя с ключевым кодом равным 1
    data.show_indicator(root, 'Количество игр: ', 'count', 'duration', 1)        #пример вызова метода, который рассчитывает и отображает на экране количество сеансов игры для пользователя с ключевым кодом равным 1
    data.show_indicator(root, 'Максимальное время игры: ', 'MAX', 'duration', 1) #пример вызова метода, который рассчитывает и отображает на экране максимальное значение времени игры для пользователя с ключевым кодом равным 1
    data.show_indicator(root, 'Минимальное время игры: ', 'min', 'duration', 1)  #пример вызова метода, который рассчитывает и отображает на экране минимальное значение времени игры для пользователя с ключевым кодом равным 1
    data.show_history(root, 1, ("Номер", "ID игрока", "Дата", "Время игры", "Число ходов", "Число клеток")) #пример вызова метода, который отображает на экране историю операций, куда передаётся место размещения на экране, ключевой код пользователя и кортеж с названиями колонок в таблице - виджете, используемой для отображения данных
    root.mainloop()                                   #активируется цикл, который отслеживает любые изменения в главном окне 

