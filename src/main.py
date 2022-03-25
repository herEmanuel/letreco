from typing import Tuple, List
import pygame, json, random

WIDTH, HEIGHT = 600, 700
BOX_WIDTH, BOX_HEIGHT = 90, 90

class Box:
    def __init__(self, image: pygame.Surface, pos: Tuple[int, int]) -> None:
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = pos

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
        self.chooseWord()

    def chooseWord(self) -> None:
        index = random.randint(0, len(self.wordList) - 1)
        self.answer = self.wordList[index]
        print(self.answer)

    def generateGrid(self) -> List[Box]:
        # laaazy
        xCords = [16, 135, 255, 374, 493]
        yCords = [38, 168, 298, 429, 559]

        grid = []
        for row in range(0, 5):
            for cell in range(0, 5):
                grid.append(Box(self.normalBox, (xCords[cell], yCords[row])))
        return grid 

    def mainLoop(self) -> None:
        allowedLetters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 
                            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", 
                            "u", "v", "w", "x", "y", "z", "ç", "á", "â", "ã",
                            "é", "ê", "í", "ó", "ô", "õ", "ú"]

        displayedLetters = []

        grid = self.generateGrid()
        for fuck in grid:
            print(fuck.rect.topleft)
            
        test = self.font.render("FALHA Ç ê", False, (0, 255, 0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

                if event.type == pygame.KEYDOWN:
                    if event.unicode in allowedLetters:
                        self.currentGuess += event.unicode
                        displayedLetters.append(self.font.render(event.unicode.upper(), False, (255, 255, 255)))
                        self.currentCell += 1
                        if self.currentCell >= 5:
                            self.currentLine += 1
                            self.currentCell = 0

                            if self.currentLine >= 5:
                                pass #TODO: end game

                    elif event.key == pygame.K_RETURN:
                        print(self.currentCell)
                        if self.currentCell != 4:
                            continue

                        for (i, char) in enumerate(self.currentGuess):
                            if char == self.answer[i]:
                                print("got one right!!!")

                            if self.answer.count(char) != 0:
                                print("its there, but not at that position")
                    
                    elif event.key == pygame.K_BACKSPACE:
                        if self.currentCell == 0:
                            continue
                        print("backspace")
                        self.currentGuess = self.currentGuess[:-1]
                        displayedLetters.pop()
                        self.currentCell -= 1


            self.screen.fill((55, 171, 200))
            # self.screen.blit(test, (10, 10))
            for cell in grid:
                self.screen.blit(cell.image, cell.rect)

            for (i, letter) in enumerate(displayedLetters):
                self.screen.blit(letter, grid[i].rect.center)

            pygame.display.flip()

def main() -> None:
    game = Game()
    game.mainLoop()

if __name__ == "__main__":
    main()