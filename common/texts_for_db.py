import asyncio

from database.crud import MarathonsQuery, BannerQuery
from database.db_config import drop_db, create_db

basic_banners = {
    "main": {
        "image": "AgACAgQAAxkBAAMzZkkNGPjPlGWtuwXnxtCfaO8h3HEAAue_MRvHJlFSwmXA1LPKjuEBAAMCAAN4AAM1BA",
        "sub_data": {
            "header": f", добро пожаловать в нашего бота по пилатесу!",
            "text": "  Здесь вы найдете эксклюзивные видеокурсы для занятий пилатесом, "
                    "которые помогут Вам привести в порядок и укрепить Ваше тело."
                    "Выбирайте подходящий для вас курс и давайте начнем Ваш путь к здоровью и благополучию вместе!"
        }},
    "admin_panel": {
        "image": "AgACAgQAAxkBAAM1ZkkP6mi7X-xO5guts76fQfN6XPwAAui_MRvHJlFSZVGmQFFrg64BAAMCAAN4AAM1BA",
        "sub_data": {
            "header": f"Добро пожаловать в панель администратора!\n",
            "text": "  Здесь можно добавить новый марафон или изменить информацию о уже существующем"
        }},
    "marathons": {
        "image": "AgACAgQAAxkBAAM3ZkkRLVru9AitbqEqmGJL5mI16_IAAuq_MRvHJlFSBNEZnEblpI8BAAMCAAN4AAM1BA",
        "sub_data": {
            "header": f"МАРАФОНЫ вместе с Pilates_Mari\n",
            "text": "  Регулярные тренировки по пилатесу обеспечивают не только внешними, "
                    "но и внутренними изменениями. Вы получаете более свободные движения, "
                    "увеличение гибкости тела и силы. Занятия помогают добиваться разных целей: "
                    "похудение, реабилитация после травм или улучшение самочувствия. "
                    "При регулярном подходе и соблюдении техники выполнения упражнений "
                    "можно достигнуть хороших результатов. Пилатес полезен для всего тела."
                    "  Проходя марафоны вместе с Pilates_Mari, Вы сможете сделать коррекцию фигуры🧍🏻‍♀️, "
                    "избавитесь от болей в спине🕺🏻, стабилизируете нервную систему🧖🏻‍♀️ и улучшите обмен веществ🧘‍♀️."
        }},
    "payment": {
        "image": "AgACAgQAAxkBAAM5ZkkRXe8LtgTS7IoFhyXYhfZFt18AAuu_MRvHJlFS3tfeOzt0Rl4BAAMCAAN4AAM1BA",
        "sub_data": {
            "header": f"Доступные способы оплаты:\n",
            "text": "✅Monobank\n✅Bunq"
        }},
    "about": {
        "image": "AgACAgQAAxkBAAM7ZkkRmZB4oPF7vPmCgFgJ4ChavloAAuy_MRvHJlFSuf34Hp6mFB4BAAMCAAN4AAM1BA",
        "sub_data": {
            "header": f"Привет, ",
            "text": "  Меня зовут Маша🙋🏻‍♀️, Я - профессиональный тренер по пилатесу с многолетним опытом работы, "
                    "преданный принципам здорового образа жизни и гармонии тела и ума."
                    "Мое вдохновение лежит в способности помочь людям достичь своих фитнес-целей"
                    " и улучшить качество своей жизни через практику пилатеса."
                    "Я стремлюсь создать поддерживающую и вдохновляющую атмосферу во время занятий, "
                    "где каждый участник чувствует себя комфортно и мотивированно."
                    "С моими курсами Вы не только улучшите свою физическую форму, "
                    "но и обретете гармонию и баланс, необходимые для полноценной жизни."
                    "Я стараюсь делиться своими знаниями и опытом, "
                    "чтобы люди, учавствующие в моих марафонах, "
                    "могли получить максимальную пользу от занятий и стать лучшей версией себя.💃"
        }},
    "faq": {
        "image": "AgACAgQAAxkBAAM9ZkkR0JSVG_t1nj2hfNsyC9-uYm8AAu6_MRvHJlFSS_pX00LsNyMBAAMCAAN4AAM1BA",
        "sub_data": {
            "header": f"'Если у Вас есть дополнительные вопросы, Вы можете найти ответы на них здесь:'⬇️\n",
            "text": f"'1. Каким образом я могу получить доступ к курсу после покупки?'\n"
                    f"Все материалы здесь, в телеграме. "
                    f"Вы получаете доступ к видеоматериалам из закрытого приватного канала\n"
                    f"'2. Сколько времени требуется на прохождение каждого курса?'\n"
                    f"Каждый курс длиться 7 дней\n"
                    f"'3. Могу ли я заниматься пилатесом, если у меня есть медицинские противопоказания или ограничения??'\n"
                    f"Занятия подойдут для людей с ограничениями по здоровью. "
                    f"Тренировки будут эффективны для атлетов: возраст и уровень физической подготовки не имеет значения. "
                    f"Плавность выполнения, спокойное дыхание и простая техника упражнений будут полезны "
                    f"для пожилых (60+ лет) и людей с заболеваниями сердца и сосудистой системы. "
                    f"При беременности заниматься фитнесом разрешается, но не интенсивно."
                    f"'4. Какие уровни подготовки подразумевают ваши курсы? Есть ли курсы для начинающих, продвинутых и т. д.?'\n"
                    f"У Вас есть возможность узнать это здесь\n"
                    f"'5. Есть ли у вас пробные уроки или возможность попробовать курс перед покупкой?\n"
                    f"Не знаю))"
                    f"'6. Какие материалы или оборудование мне понадобятся для прохождения курса?'\n"
                    f"Не знаю))"
                    f"'7. Как я могу связаться с вами или получить поддержку во время прохождения курса?'\n"
                    f"Через мой инстаграм - https://www.instagram.com/masha.pro.pilates/ "
                    f"'8. Есть ли у вас акции или скидки на курсы?'\n"
                    f"Не знаю))"
                    f"'9. Как я могу оценить курс или оставить отзыв после его завершения?'\n"
                    f"Думаю над этим)"
                    f"'10. Что делать, если у меня возникли технические проблемы при доступе к курсу или просмотре видеоматериалов?'\n"
                    f"Свяжитесь со мной через инстаграм - https://www.instagram.com/masha.pro.pilates/"

        }},
    "buy_marathon": {
        "image": "AgACAgQAAxkBAAIE22ZTKIJrg6djl6JgHEssVetMIDbTAAK8wDEbTTyZUq9Te1FgoCx7AQADAgADeQADNQQ",
        "sub_data": {
            "header": f"Чтобы приобрести данный марафон перейдите по этой ссылке "
                      f"https://www.instagram.com/masha.pro.pilates/",
            "text": None
        }}
}

marathons = {
    "back_hands": {
        "price": 10,
        "image": "AgACAgQAAxkBAAIDfWZO84TrKMb67r1GFcjzGdgaPrwhAAJNwjEb0TF4UsShICOQ7ghdAQADAgADeAADNQQ",
        "discount": 0,
        "sub_data": {
            "header": "СПИНА - РУКИ💪\n",
            "text": f"  Марафон включает в себя 7 нескучных тренировок для укрепления мышц спины, "
                    f"расслабления поясницы, улучшение осанки и раскрытия грудной клетки. "
                    f"Подходит для всех уровней тренировки. Каждая тренировка занимает не больше 20 минут в день.\n"
                    f"  Результат после прохождения марафона:\n"
                    f"1.  Уменьшиться или совсем пройдет боль в лопатках и пояснице.\n"
                    f"2. Улучшиться осанка, опустятся плечи.\n"
                    f"3. Расслабиться шейно-воротниковая зона.\n"
                    f"4. Мышцы спины и рук придут в тонус, что даст возможность почувствовать себя легко, как никогда!.\n"
                    f"5. Улучшиться мобильность и артикуляция позвоночника, "
                    f"что  благотворно влияет на вашу осанку и самочувствие в целом.\n"
                    f"6. Вы станете гибче и стабильнее в движениях.\n"
                    f"7. Общее состояние улучшиться, ибо вы будете чувствовать удовлетворение "
                    f"и гордость за то, что 7 дней посвятили себе и своему здоровью"
        }
    },
    "butt_legs": {
        "price": 10,
        "image": "AgACAgQAAxkBAAIDf2ZO86Xbp_jdo_SRCrRlCaipmq9GAAJOwjEb0TF4Umw6U0pKUc3UAQADAgADeAADNQQ",
        "discount": 0,
        "sub_data": {
            "header": "ПОПА - НОГИ🦵\n",
            "text": f"  Марафон включает в себя 7 нескучных тренировок, "
                    f"направленных на укрепление мышц ягодиц, внутренней, внешней и задней поверхности бедра. "
                    f"Подходит для всех уровней тренировки. Каждая тренировка занимает не больше 20 минут в день.\n"
                    f"  Результат после прохождения марафона:\n"
                    f"1. Ягодицы подтянуться и округляться\n"
                    f"2. Ноги станут стройнее\n"
                    f"3. Целлюлит и отеки визуально станут меньше\n"
                    f"4. Область галифе станет визуально меньше\n"
                    f"5. Повысится общая сила и выносливость вашего тела\n"
                    f"6. Мышцы спины так же укрепятся, боль в пояснице станет меньше\n"
                    f"7. Станет больше легкости и красоты движений в теле\n"
        }
    },
    "abdomen_back": {
        "price": 10,
        "image": "AgACAgQAAxkBAAIDgWZO879XuRA_-CAlvhHpaIgOutAkAAJPwjEb0TF4UtXlalOod0gTAQADAgADeAADNQQ",
        "discount": 0,
        "sub_data": {
            "header": "ПРЕСС - СПИНА👯‍♀️\n",
            "text": f"  Марафон включает в себя 7 нескучных тренировок "
                    f"для мышц кора (спина, прямая мышца живота, передняя поверхность бедра и ягодиц)"
                    f"Подходит для продвинутых уровней тренировки. "
                    f"Каждая тренировка занимает не больше 20 минут в день.\n"
                    f"  Результат после прохождения марафона:\n"
                    f"1. Пресс станет более рельефным\n"
                    f"2. Уйдет жир с боков и спины\n"
                    f"3. Целлюлит и отеки станут меньше"
                    f"4. Передняя поверхность бедра и ягодиц придут в больший тонус\n"
                    f"5. Мышцы рук и плеч станут рельефнее\n"
                    f"6.  Улучшиться осанка\n"
                    f"7. Станет больше легкости и красоты движений в теле\n"
        }
    },
    "abdomen_pelvis": {
        "price": 10,
        "image": "AgACAgQAAxkBAAIDg2ZO89nEdS59M4HmYFCG_8DIjEoeAAJQwjEb0TF4UrpapD3Jh5xsAQADAgADeAADNQQ",
        "discount": 0,
        "sub_data": {
            "header": "ПРЕСС - ТАЗ🧎‍♂️\n",
            "text": "Марафон находиться в процессе создания и скоро здесь появиться👩🏻‍💻"
        }
    }
}


async def fill_db():
    # await drop_db()
    # await create_db()
    for ban, ban_data in basic_banners.items():
        await BannerQuery.add_instance(new_instance={"name": ban,
                                                     "image": ban_data["image"]},
                                       sub_data=ban_data["sub_data"])
    for ban, ban_data in marathons.items():
        await MarathonsQuery.add_instance(new_instance={"name": ban,
                                                        "price": ban_data["price"],
                                                        "image": ban_data["image"],
                                                        "discount": ban_data["discount"]},
                                          sub_data=ban_data["sub_data"])



