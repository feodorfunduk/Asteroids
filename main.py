import pygame
import sys
import random
from Asteroids import Ast
from Asteroids import och
from Bullets import Bullet
from Boosts import boost
from Bullets import sprite_list
from Buttons import ImageButton
from Bullets import razbito
import sqlite3
from ImputBox import InputBox

pygame.init()
font2 = pygame.font.SysFont("Times", 20)
razb = 0
ochki = 0
con = sqlite3.connect("records")
cur = con.cursor()
user_name = ''
font = pygame.font.SysFont("Times", 40)
font3 = pygame.font.SysFont('Times', 80)


def game():
    global ochki
    global razb
    screen = pygame.display.set_mode()
    W, H = screen.get_width(), screen.get_height()
    bg = pygame.image.load("space.jpg")
    bg = pygame.transform.scale(bg, (W, H))

    BLUE = (30, 10, 75)
    WHITE = (255, 255, 255)
    pygame.display.set_caption("Asteroids")
    rabota = True  # infinity cycle

    korabl = pygame.image.load("korabl2.jpg")
    korabl = pygame.transform.scale(korabl, (70, 70))
    k_rect = korabl.get_rect()
    k_rect.center = W // 2, H - 60

    zachita = pygame.image.load("Защитный круг.jpg")
    zachita = pygame.transform.scale(zachita, (90, 125))
    z_rect = zachita.get_rect()
    z_rect.center = W // 2, H - 45

    colorkey = zachita.get_at((0, 0))
    zachita.set_colorkey(colorkey)

    colorkey = korabl.get_at((0, 0))
    korabl.set_colorkey(colorkey)

    booststrength = pygame.image.load("Буст силы.jpg")
    colorkey = booststrength.get_at((0, 0))
    booststrength.set_colorkey(colorkey)

    boostarmor = pygame.image.load("Буст жизни.jpg")
    colorkey = boostarmor.get_at((0, 0))
    boostarmor.set_colorkey(colorkey)

    clock = pygame.time.Clock()

    konec = 1
    pause = True

    patrons = 10
    zarad = 100
    maxzarad = 100
    maxpatrons = 10

    bullet_list = pygame.sprite.Group()
    boost_list1 = pygame.sprite.Group()
    boost_list2 = pygame.sprite.Group()

    # Системные
    q = True  # Для исчезновения корабля
    w = True  # Для исчезновения защитного поля

    korleft = False
    korright = False

    while rabota:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ochki = och()
                    razb = razbito()
                    sprite_list.empty()
                    bullet_list.empty()
                    boost_list1.empty()
                    boost_list2.empty()
                    main_menu()
                    sys.exit()

                if not pause:
                    if event.key == pygame.K_TAB:
                        konec = 1
                        pause = True
                        sprite_list.empty()
                        bullet_list.empty()
                        boost_list1.empty()
                        boost_list2.empty()
                        patrons = 10
                        zarad = 100
                        ochki = och()
                        razb = razbito()
                        q = True
                        w = True
                        maxpatrons = 10
                        maxzarad = 100
                        k_rect.center = W // 2, H - 60
                        z_rect.center = W // 2, H - 45
                if event.key == pygame.K_q:
                    pause = False

                if event.key == pygame.K_w and konec:
                    pause = True
                if event.key == pygame.K_a:
                    korleft = True
                    korabl = pygame.transform.rotate(korabl, (90))
                elif event.key == pygame.K_d:
                    korright = True
                    korabl = pygame.transform.rotate(korabl, (-90))
            if patrons >= 1:
                if event.type == pygame.KEYDOWN:
                    if korleft == False and korright == False:
                        if event.key == pygame.K_SPACE:
                            newBullet = Bullet(k_rect.center)
                            bullet_list.add(newBullet)
                            patrons -= 1
            if patrons <= maxpatrons:
                patrons += 0.025
                if patrons > maxpatrons:
                    patrons = maxpatrons

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    korleft = False
                    korabl = pygame.transform.rotate(korabl, (-90))
                if event.key == pygame.K_d:
                    korright = False
                    korabl = pygame.transform.rotate(korabl, (90))
        if pause:
            if k_rect.left <= 0:
                korleft = False
            if W <= k_rect.right:
                korright = False
            if korleft:
                k_rect.x -= 7
                z_rect.x -= 7
            if korright:
                k_rect.x += 7
                z_rect.x += 7

            h = random.randint(0, W)
            posAste = (h, 0)
            speedy = random.randint(6, 12 + (och() - ochki) // 100)
            zaderjka = random.randint(0, 18 - ((och() - ochki) // 100) * 2)

            if zaderjka == 0:
                speedx = 0
                scale_ast = random.randrange(40, 100)
                newAst = Ast(posAste, scale_ast, speedx, speedy)
                sprite_list.add(newAst)
            boostzaderjka = random.randint(0, 300)
            if boostzaderjka == 5:
                boostspeedx = 0
                boostspeedy = random.randint(6, 12)
                boostPos = (random.randint(0, W), 0)
                boostImage = random.randint(1, 2)
                if boostImage == 1:
                    newBoost1 = boost(booststrength, boostPos, boostspeedx, boostspeedy)
                    boost_list1.add(newBoost1)
                if boostImage == 2:
                    newBoost2 = boost(boostarmor, boostPos, boostspeedx, boostspeedy)
                    boost_list2.add(newBoost2)

            for s in sprite_list:
                if z_rect.colliderect(s.rect):
                    sprite_list.remove(s)
                    zarad -= 50
            for s in boost_list1:
                if k_rect.colliderect(s.rect):
                    boost_list1.remove(s)
                    if patrons == 10:
                        maxpatrons += 3
                    patrons += 3
            for s in boost_list2:
                if k_rect.colliderect(s.rect):
                    boost_list2.remove(s)
                    if zarad == 100:
                        maxzarad += 25
                    zarad += 25

            if zarad < 50:
                w = False
                z_rect.y = H + 500
            if zarad >= 50:
                z_rect.centerx = k_rect.centerx - 2
                z_rect.centery = k_rect.centery + 16
                w = True
            for s in sprite_list:
                if k_rect.colliderect(s.rect):
                    sprite_list.remove(s)
                    q = False
                    konec = 0
            if zarad < maxzarad:
                zarad += 0.025

            sprite_list.update()
            bullet_list.update()
            boost_list1.update()
            boost_list2.update()
            screen.fill(BLUE)
            screen.blit(bg, (0, 0))

        if q:
            screen.blit(korabl, (k_rect.x, k_rect.y))
        if w:
            screen.blit(zachita, (z_rect.x, z_rect.y))

        sprite_list.draw(screen)
        bullet_list.draw(screen)
        boost_list1.draw(screen)
        boost_list2.draw(screen)
        draw_string1 = "Высота: " + str(och() - ochki)
        text = font2.render(draw_string1, True, WHITE)
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.y = H - (H - 100)
        text_rect.x = W - (W - 100)
        screen.blit(text, text_rect)
        draw_string2 = "Патроны: " + str(int(patrons))
        text = font2.render(draw_string2, True, WHITE)
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.y = H - (H - 100)
        text_rect.x = W - (W - 225)
        screen.blit(text, text_rect)
        draw_string3 = "Уничтоженно астероидов: " + str(razbito() - razb)
        text = font2.render(draw_string3, True, WHITE)
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.y = H - (H - 100)
        text_rect.x = W - (W - 375)
        screen.blit(text, text_rect)
        draw_string4 = "Заряд защитного поля: " + str(int(zarad)) + "%"
        text = font2.render(draw_string4, True, WHITE)
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.y = H - (H - 100)
        text_rect.x = W - (W - 650)
        screen.blit(text, text_rect)
        clock.tick(60)
        pygame.display.update()

        if pause:
            if konec == 0:
                draw_string = "Конец игры! Чтобы сыграть еще раз нажмите TAB"
                text = font.render(draw_string, True, WHITE)
                text_rect = text.get_rect()
                text_rect.centerx = screen.get_rect().centerx
                text_rect.y = H // 2
                screen.blit(text, text_rect)
                pygame.display.update()
                pause = False
                if och() - ochki > \
                        list(cur.execute('SELECT result from results WHERE users = ?', (user_name,)).fetchone())[0]:
                    cur.execute('DELETE from results where users=?', (user_name,))
                    con.commit()
                    cur.execute("INSERT INTO results(users, result) VALUES(?, ?)",
                                (user_name, och() - ochki))
                    con.commit()


def main_menu():
    pygame.display.set_mode()
    screen1 = pygame.display.set_mode()
    pygame.display.set_caption('Asteroids - Menu')
    W1, H1 = screen1.get_width(), screen1.get_height()
    sound = None
    if user_name:
        sound = 'click.mp3'
    green_button = ImageButton(W1 / 2 - (500 / 2), 250, 500, 150, "Старт", "green_button.png", "green_button2.png", sound)
    score_button = ImageButton(W1 / 2 - (500 / 2), 450, 500, 150, "Рекорды", "green_button.png", "green_button2.png")
    exit_button = ImageButton(W1 / 2 - (500 / 2), 650, 500, 150, "Выйти", "red_button.png", "red_button2.png")
    user_button = ImageButton(W1 - (W1 - 100), H1 - 100, 300, 75, "Сменить пользователя", "green_button.png",
                              "green_button2.png")
    acc = True
    text = font.render('', True, (255, 255, 255))
    text_rect = text.get_rect()

    bg1 = pygame.image.load('bg1.webp')
    bg1 = pygame.transform.scale(bg1, (screen1.get_width(), screen1.get_height()))
    running = True
    while running:
        screen1.blit(bg1, (0, 0))
        if not acc:
            draw_string1 = "Войдите в аккаунт"
            text = font3.render(draw_string1, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.centerx = screen1.get_rect().centerx
            text_rect.y = H1 // 2 + 10
            text_rect.x = W1 // 2 - 300

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT and event.button == green_button:
                if user_name:
                    game()
                    running = False
                else:
                    acc = False
            elif event.type == pygame.USEREVENT and event.button == exit_button:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT and event.button == score_button:
                scores()
            elif event.type == pygame.USEREVENT and event.button == user_button:
                users()

            green_button.handle_event(event)
            user_button.handle_event(event)
            exit_button.handle_event(event)
            score_button.handle_event(event)

        user_button.check_hover(pygame.mouse.get_pos())
        user_button.draw(screen1)

        score_button.check_hover(pygame.mouse.get_pos())
        score_button.draw(screen1)
        exit_button.check_hover(pygame.mouse.get_pos())
        exit_button.draw(screen1)
        green_button.check_hover(pygame.mouse.get_pos())
        green_button.draw(screen1)
        if not acc:
            screen1.blit(text, text_rect)
        pygame.display.flip()


def scores():
    pygame.display.set_mode()
    screen2 = pygame.display.set_mode()
    pygame.display.set_caption('Asteroids - Best Scores')
    W2, H2 = screen2.get_width(), screen2.get_height()
    bg2 = pygame.image.load('bg1.webp')
    bg2 = pygame.transform.scale(bg2, (screen2.get_width(), screen2.get_height()))
    exit_button = ImageButton(W2 / 2 - (500 / 2), H2 - 200, 500, 150, "Назад", "red_button.png", "red_button2.png")
    keep_going = True
    first = int(max(list(cur.execute('SELECT result from results')))[0])
    second = int(max(list(cur.execute(f'SELECT result from results WHERE result != {first}')))[0])
    third = int(max(list(cur.execute(f'SELECT result from results WHERE result != {second} and result != {first}')))[0])

    draw_string1 = f"1.     {cur.execute(f'SELECT users from results WHERE result = {first}').fetchone()[0]}     {first}"
    text = font3.render(draw_string1, True, (255, 255, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen2.get_rect().centerx
    text_rect.y = H2 // 2 - (H2 // 5)
    text_rect.x = W2 // 2 - (W2 // 10)

    draw_string2 = f"2.     {cur.execute(f'SELECT users from results WHERE result = {second}').fetchone()[0]}     {second}"
    text1 = font3.render(draw_string2, True, (192, 192, 192))
    text_rect1 = text1.get_rect()
    text_rect1.centerx = screen2.get_rect().centerx
    text_rect1.y = H2 // 2 - (H2 // 10)
    text_rect1.x = W2 // 2 - (W2 // 10)

    draw_string3 = f"3.     {cur.execute(f'SELECT users from results WHERE result = {third}').fetchone()[0]}     {third}"
    text2 = font3.render(draw_string3, True, (205, 127, 50))
    text_rect2 = text2.get_rect()
    text_rect2.centerx = screen2.get_rect().centerx
    text_rect2.y = H2 // 2
    text_rect2.x = W2 // 2 - (W2 // 10)

    if user_name:
        draw_string4 = f"{user_name}(You): {cur.execute('SELECT result from results WHERE users = ?', (user_name,)).fetchone()[0]}"
        text3 = font3.render(draw_string4, True, (255, 255, 255))
        text_rect3 = text3.get_rect()
        text_rect3.centerx = screen2.get_rect().centerx
        text_rect3.y = H2 // 2 - (H2 // 2)
        text_rect3.x = W2 // 2 - (W2 // 10)

    while keep_going:
        screen2.blit(bg2, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT and event.button == exit_button:
                main_menu()
                sys.exit()

            exit_button.handle_event(event)
        exit_button.check_hover(pygame.mouse.get_pos())
        exit_button.draw(screen2)
        screen2.blit(text, text_rect)
        screen2.blit(text1, text_rect1)
        screen2.blit(text2, text_rect2)
        if user_name:
            screen2.blit(text3, text_rect3)
        pygame.display.flip()


def users():
    global user_name
    pygame.display.set_mode()
    screen2 = pygame.display.set_mode()
    pygame.display.set_caption('Asteroids - Best Scores')
    W2, H2 = screen2.get_width(), screen2.get_height()
    bg2 = pygame.image.load('bg1.webp')
    bg2 = pygame.transform.scale(bg2, (screen2.get_width(), screen2.get_height()))
    exit_button = ImageButton(W2 / 2 - (1000 / 2), H2 - 200, 500, 150, "Назад", "red_button.png", "red_button2.png")
    save_burron = ImageButton(W2 / 2, H2 - 200, 500, 150, "Войти", "green_button.png", "green_button2.png")
    input_box = InputBox(W2 // 2 - 70, H2 // 2, 350, 50)
    keep_going = True
    draw_string1 = "Введите имя"
    text = font3.render(draw_string1, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.centerx = screen2.get_rect().centerx
    text_rect.y = H2 // 2 - 100
    text_rect.x = W2 // 2 - 200
    us = False

    while keep_going:
        screen2.blit(bg2, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT and event.button == exit_button:
                main_menu()
                sys.exit()
            elif event.type == pygame.USEREVENT and event.button == save_burron:
                if input_box.get_text():
                    user_name = input_box.get_text()
                    for i in cur.execute('SELECT users from results').fetchall():
                        if user_name == list(i)[0]:
                            us = True
                            main_menu()
                            sys.exit()

                    if not us:
                        cur.execute("INSERT INTO results(users, result) VALUES(?, ?)",
                                    (user_name, 0))
                        con.commit()
                        main_menu()
                        sys.exit()

            input_box.handle_event(event)
            exit_button.handle_event(event)
            save_burron.handle_event(event)
        exit_button.check_hover(pygame.mouse.get_pos())
        exit_button.draw(screen2)
        input_box.update()
        input_box.draw(screen2)
        save_burron.check_hover(pygame.mouse.get_pos())
        save_burron.draw(screen2)
        screen2.blit(text, text_rect)
        pygame.display.flip()


main_menu()
pygame.quit()
