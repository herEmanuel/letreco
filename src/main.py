from typing import Tuple
import pygame, json, random, pygame_gui

WIDTH, HEIGHT = 600, 700
BOX_WIDTH, BOX_HEIGHT = 90, 90

def telaInicial():
    pygame.init()
    pygame.font.init()
    
    tela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Letreco!")

    manager_menu = pygame_gui.UIManager((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
  
    fonte_default = pygame.font.get_default_font()
    titulo_txt = pygame.font.SysFont(fonte_default, 90)

    start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 360), (200, 50)), text="Jogar!",
                                                manager=manager_menu)

    texto = titulo_txt.render("Letreco!", True, (55, 171, 200))
    
    while True:
        relogio = clock.tick(60) / 1000
    
        for event in pygame.event.get():
            manager_menu.process_events(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    game = Game(tela)
                    game.mainLoop()

        tela.fill((255, 255, 255))
        tela.blit(texto, (178, 200))

        manager_menu.update(relogio)
        manager_menu.draw_ui(tela)
        pygame.display.update()
      
# returns True -> começar novo jogo; returns False -> tentar de novo
def menu(tela: pygame.Surface, errou: bool) -> bool:
    fonte_default = pygame.font.get_default_font()
    descricao_txt = pygame.font.SysFont(fonte_default, 50)

    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    newGame_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 360), (200, 50)), text="Próximo",
                                                manager=manager)
    if errou:
        newTry_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 420), (200, 50)), text="Tentar de novo",
                                                 manager=manager)

    errou_texto = descricao_txt.render("Você errou!", True, (55, 171, 200))
    acertou_texto = descricao_txt.render("Você acertou!", True, (55, 171, 200))
    
    while True:
        relogio = clock.tick(60) / 1000
        
        for event in pygame.event.get():
            manager.process_events(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == newGame_button:
                    return True
                if event.ui_element == newTry_button:
                    return False

        tela.fill((255, 255, 255))

        if errou:
            tela.blit(errou_texto, (205, 200))
        else:
            tela.blit(acertou_texto, (187, 200))

        manager.update(relogio)
        manager.draw_ui(tela)
        pygame.display.update()

class Box:
    def __init__(self, image: pygame.Surface, pos: Tuple[int, int]) -> None:
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = pos

class Game:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = pygame.font.Font(pygame.font.get_default_font(), 48)

        self.normalBox = pygame.image.load("../assets/box.png")
        self.greenBox = pygame.image.load("../assets/green-box.png")
        self.yellowBox = pygame.image.load("../assets/yellow-box.png")

        try:
            with open("../words.json") as wordsJson:
                self.wordList = json.loads(wordsJson.read())["words"]
        except:
            print("words.json is missing - exiting now")
            exit(1)

        self.currentLine = 0
        self.currentCell = 0
        self.currentGuess = ""
        self.displayedLetters = []
        self.chooseWord()

    def chooseWord(self) -> None:
        index = random.randint(0, len(self.wordList) - 1)
        self.answer = self.wordList[index]

    def generateGrid(self):
        # laaazy
        xCords = [16, 135, 255, 374, 493]
        yCords = [38, 168, 298, 429, 559]

        self.grid = []
        for row in range(0, 5):
            for cell in range(0, 5):
                self.grid.append(Box(self.normalBox, (xCords[cell], yCords[row])))

    def restart(self, newGame: bool) -> None:
        self.currentLine = 0
        self.currentCell = 0
        self.currentGuess = ""
        self.displayedLetters = []
        self.generateGrid()
        
        if newGame:
            self.chooseWord()

    def mainLoop(self) -> None:
        allowedLetters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 
                            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", 
                            "u", "v", "w", "x", "y", "z", "ç", "á", "â", "ã",
                            "é", "ê", "í", "ó", "ô", "õ", "ú"]

        self.generateGrid()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

                if event.type == pygame.KEYDOWN:
                    if event.unicode.lower() in allowedLetters:
                        if self.currentCell >= 5:
                            continue

                        self.currentGuess += event.unicode
                        self.displayedLetters.append(self.font.render(event.unicode.upper(), False, (255, 255, 255)))
                        self.currentCell += 1

                    elif event.key == pygame.K_RETURN:
                        if self.currentCell != 5:
                            continue

                        for (i, char) in enumerate(self.currentGuess):
                            if char == self.answer[i]:
                                self.grid[i + self.currentLine*5].image = self.greenBox
                                continue

                            if self.answer.count(char) != 0:
                                self.grid[i + self.currentLine*5].image = self.yellowBox
                    
                        if self.currentGuess == self.answer:
                            menu(self.screen, False)
                            self.restart(True)
                            continue

                        self.currentCell = 0
                        self.currentLine += 1
                        self.currentGuess = ""

                        if self.currentLine >= 5:
                            startNewGame = menu(self.screen, True)
                            if startNewGame:
                                self.restart(True)
                            else:
                                self.restart(False)
                            continue

                    elif event.key == pygame.K_BACKSPACE:
                        if self.currentCell == 0:
                            continue
                    
                        self.currentGuess = self.currentGuess[:-1]
                        self.displayedLetters.pop()
                        self.currentCell -= 1

            self.screen.fill((55, 171, 200))
            
            for cell in self.grid:
                self.screen.blit(cell.image, cell.rect)

            for (i, letter) in enumerate(self.displayedLetters):
                self.screen.blit(letter, letter.get_rect(center=self.grid[i].rect.center))
                
            pygame.display.flip()

def main() -> None:
    telaInicial()

if __name__ == "__main__":
    main()