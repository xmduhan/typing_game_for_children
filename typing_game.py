from unicodedata import digit
import pygame as pg
import pygame_menu as pgm
from glob import glob
from random import sample, choices
import string

THEME = pgm.themes.Theme(
    background_color=(40, 41, 35),
    cursor_color=(255, 255, 255),
    cursor_selection_color=(80, 80, 80, 120),
    scrollbar_color=(39, 41, 42),
    scrollbar_slider_color=(65, 66, 67),
    scrollbar_slider_hover_color=(90, 89, 88),
    selection_color=(255, 255, 255),
    title_background_color=(47, 48, 51),
    title_font_color=(215, 215, 215),
    widget_font_color=(200, 200, 200),
    title_font='font/kaiti.ttf',
    widget_font='font/kaiti.ttf',
    widget_font_size=40,
)

def get_font_size(screen, text):
    """ """
    W, _ = screen.get_size()
    # print(f'{W=}')
    font_size = W 

    while True:
        font_size = int(font_size)
        font = pg.font.Font(None, font_size)
        size = font.size(text)

        if size[0] > W * .91:
            font_size *= .9
            continue

        if size[0] < W * .89:
            font_size *= 1.1
            continue
        
        break
    return font_size

def play(screen, text, title, error):
    """ """
    W, H = screen.get_size()
    typing_sound_list = glob('audio/key*.wav')

    fg0 = 250, 240, 230
    fg1 = 255, 0, 0  
    bg = 5, 5, 5

    font_size = get_font_size(screen, text)
    font = pg.font.Font(None, font_size)
    size = font.size(text)
    w, h = size

    title_font = pg.font.Font('font/kaiti.ttf', 50)

    cursor = 0
    while cursor <= len(text):
        screen.fill(bg)
        horizontal = (W - w) // 2 
        vertical = (H - h) // 2 
        for i, ch in enumerate(text):
            size = font.size(ch)
            fg = fg1 if cursor > i else fg0
            surface = font.render(ch, 0, fg, bg)
            screen.blit(surface, (horizontal, vertical))
            horizontal += size[0]

        hint = f'{title}   出错: {error}' 
        surface = title_font.render(hint, 0, fg0, bg)
        screen.blit(surface, (0, 0))
        
        if cursor == len(text):
            pg.display.flip()
            break

        for event in pg.event.get():

            if event.type == pg.QUIT:
                return False, error

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return False, error
                
                if event.dict['unicode'] == text[cursor]:
                    cursor += 1
                    audio_filename = sample(typing_sound_list, 1)[0]
                    pg.mixer.Sound(audio_filename).play()
                    break
                
                if event.dict['unicode'] != '':
                    audio_filename = 'audio/warning.wav'
                    pg.mixer.Sound(audio_filename).play()
                    error += 1
                    break
                    
        pg.display.flip()

    audio_filename = 'audio/success1.wav'
    pg.mixer.Sound(audio_filename).play()

    return True, error

menu2keys = {
    '左手初级': 'sdf',
    '右手初级': 'jkl',
    '双手初级': 'sdfjkl',
    '左手进阶': 'asdfg',
    '左手进阶': 'hjkl;',
    '双手进阶': 'asdfghjkl;',
    '左手高级': 'asdfgqwertzxcvb',
    '右手高级': 'hjkl;yuiopnm,./',
    '双手高级': 'asdfgqwertzxcvbhjkl;yuiopnm,./',
    '数字练习': string.digits,
    '大写字母': string.punctuation,
    '符号练习': string.ascii_uppercase,
    '综合练习': string.ascii_uppercase + \
        string.ascii_lowercase + \
        string.digits + \
        string.punctuation
}

def play_menu(screen, menu_text, length=10, times=5):
    """ """
    error = 0
    keys = menu2keys.get(menu_text)
    playing = True
    for i in range(1, times+1):
        text = ''.join(choices(keys, k=length))
        title = f'关卡: {menu_text}({i}/{times})'
        playing, error = play(screen, text, title, error)
        if not playing:
            return

    pct = (1 - error / (length * times)) * 100
    if pct >= 95:
        message = f'恭喜您闯关成功! 您的正确率为: {pct}%, 很棒哦! :-)'
    else:
        message = f'您出错多了点, 不过不要气馁清继续努力! 当前正确率: {pct}%'
    
    W, H = screen.get_size()
    menu = pgm.Menu(
        f'关卡: {menu_text}', int(W * .6), int(H * .3), theme=THEME, 
        onclose=pgm.events.CLOSE,
    )
    menu.add.label(message)
    menu.add.label('')
    menu.add.button('确定', pgm.events.CLOSE)
    menu.mainloop(screen)
    

def main(screen=None):
    """ """
    if screen is None:
        pg.init()
        pg.mixer.init(11025)  
        pg.display.set_caption("打字练习")
        screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        
    W, H = screen.get_size()

    menu = pgm.Menu(
        '打字练习', int(W * .6), int(H * .6), theme=THEME, 
        columns=3, rows=7, onclose=pgm.events.CLOSE,
    )
    menu.add.button('左手初级', lambda : play_menu(screen, '左手初级'))
    menu.add.button('右手初级', lambda : play_menu(screen, '右手初级'))
    menu.add.button('双手初级', lambda : play_menu(screen, '双手初级'))
    menu.add.button('左手进阶', lambda : play_menu(screen, '左手进阶'))
    menu.add.button('左手进阶', lambda : play_menu(screen, '左手进阶'))
    menu.add.button('双手进阶', lambda : play_menu(screen, '双手进阶'))
    # menu.add.button('小游戏', lambda : play_with(screen))
    menu.add.label('')

    menu.add.button('左手高级', lambda : play_menu(screen, '左手高级'))
    menu.add.button('右手高级', lambda : play_menu(screen, '右手高级'))
    menu.add.button('双手高级', lambda : play_menu(screen, '双手高级'))
    menu.add.button('数字练习', lambda : play_menu(screen, '数字练习'))
    menu.add.button('大写字母', lambda : play_menu(screen, '大写字母'))
    menu.add.button('符号练习', lambda : play_menu(screen, '符号练习'))
    menu.add.button('综合练习', lambda : play_menu(screen, '综合练习'))

    menu.add.label('')
    menu.add.label('')
    menu.add.label('')
    menu.add.label('')
    menu.add.label('')
    menu.add.label('')
    menu.add.button('退出', pgm.events.CLOSE)
    menu.mainloop(screen)


if __name__=="__main__":
    main()